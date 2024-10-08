# Libraries for FastAPI
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime

# Builtin libraries
import os

from random import shuffle
from random import choice

# Classes from my module
# from module import SqliteCRUD
from module import *

CURRENT_TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# """
#            _____ _____   _____ _   _ ______ ____
#      /\   |  __ \_   _| |_   _| \ | |  ____/ __ \\
#     /  \  | |__) || |     | | |  \| | |__ | |  | |
#    / /\ \ |  ___/ | |     | | | . ` |  __|| |  | |
#   / ____ \| |    _| |_   _| |_| |\  | |   | |__| |
#  /_/    \_\_|   |_____| |_____|_| \_|_|    \____/

# The `description` is the information that gets displayed when the api is accessed from a browser and loads the base route.
# Also the instance of `app` below description has info that gets displayed as well when the base route is accessed.
# /

description = """🚀
## File System Api
"""


# This is the `app` instance which passes in a series of keyword arguments
# configuring this instance of the api. The URL's are obviously fake.
app = FastAPI(
    title="File System",
    description=description,
    version="0.0.1",
    terms_of_service="https://profgriffin.com/terms/",
    contact={
        "name": "FileSystemAPI",
        "url": "https://profgriffin.com/contact/",
        "email": "chacha@profgriffin.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# """
#   _      ____   _____          _         _____ _                _____ _____ ______  _____
#  | |    / __ \ / ____|   /\   | |       / ____| |        /\    / ____/ ____|  ____|/ ____|
#  | |   | |  | | |       /  \  | |      | |    | |       /  \  | (___| (___ | |__  | (___
#  | |   | |  | | |      / /\ \ | |      | |    | |      / /\ \  \___ \\___ \|  __|  \___ \\
#  | |___| |__| | |____ / ____ \| |____  | |____| |____ / ____ \ ____) |___) | |____ ____) |
#  |______\____/ \_____/_/    \_\______|  \_____|______/_/    \_\_____/_____/|______|_____/

# This is where you will add code to load all the countries and not just countries. Below is a single
# instance of the class `CountryReader` that loads countries. There are 6 other continents to load or
# maybe you create your own country file, which would be great. But try to implement a class that
# organizes your ability to access a countries polygon data.
# """


dataPath = "./data/"
dbName = "filesystem.db"
if os.path.exists(os.path.join(dataPath, dbName)):
    fsDB = SqliteCRUD(os.path.join(dataPath, dbName))
else:
    print("Database file not found.")
    fsDB = None


# """
#   _      ____   _____          _        __  __ ______ _______ _    _  ____  _____   _____
#  | |    / __ \ / ____|   /\   | |      |  \/  |  ____|__   __| |  | |/ __ \|  __ \ / ____|
#  | |   | |  | | |       /  \  | |      | \  / | |__     | |  | |__| | |  | | |  | | (___
#  | |   | |  | | |      / /\ \ | |      | |\/| |  __|    | |  |  __  | |  | | |  | |\___ \\
#  | |___| |__| | |____ / ____ \| |____  | |  | | |____   | |  | |  | | |__| | |__| |____) |
#  |______\____/ \_____/_/    \_\______| |_|  |_|______|  |_|  |_|  |_|\____/|_____/|_____/

# I place local methods either here, or in the module we created. I'm leaving it here to help
# with the lecture we had in class, but it can easily be moved then imported. In fact you should
# move it if you have other "spatial" methods that it can be packaged with in the module folder.
# """


def split_binary_file_to_chunks(file_path, chunk_size=1024):
    chunks = []

    with open(file_path, "rb") as file:
        while True:
            # Read a chunk of size `chunk_size`
            chunk = file.read(chunk_size)
            if not chunk:
                break  # End of file
            chunks.append(chunk)

    return chunks


def split_file_to_chunks(file_path, chunk_size=1024, encoding="utf-8"):
    chunks = []

    with open(file_path, "r", encoding=encoding) as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break  # End of file
            chunks.append(chunk)

    return chunks


# """
#   _____   ____  _    _ _______ ______  _____
#  |  __ \ / __ \| |  | |__   __|  ____|/ ____|
#  | |__) | |  | | |  | |  | |  | |__  | (___
#  |  _  /| |  | | |  | |  | |  |  __|  \___ \\
#  | | \ \| |__| | |__| |  | |  | |____ ____) |
#  |_|  \_\\____/ \____/   |_|  |______|_____/

#  This is where your routes will be defined. Remember they are really just python functions
#  that will talk to whatever class you write above. Fast Api simply takes your python results
#  and packagres them so they can be sent back to your programs request.
# """


@app.get("/")
async def docs_redirect():
    """Api's base route that displays the information created above in the ApiInfo section."""
    return RedirectResponse(url="/docs")


@app.get("/files/")
async def getFiles(did=None):
    """
    ### Description:
        Get a list of files in the current directory.
    ### Params:
        did (int) : directory id to list files from
    ### Returns:
        list : of files in the directory
    ## Examples:
    [http://127.0.0.1:8080/files/](http://127.0.0.1:8080/files/)
    ### Results:
    json
    [
        "file1.txt",
        "file2.txt",
        "file3.txt",
        "file4.txt"
        ...
    ]
    """
    files = fsDB.read_data("files")
    if files:
        if did:
            filtered = []
            for row in files:
                print(row)
                if str(row[2]) == str(did):
                    filtered.append(row)
            files = filtered
        return files
    else:
        return {"Error": "Files list was empty or None."}


@app.post("/touch")
def create_file(name: str):
    """
    Creates a new file in the filesystem and records the action in the database.
    :param filepath: The path where the file is to be created.
    - need to know current location id
    - need to know the name of the file
    - use current time to set created_at and modified_at
    - size will be 0
    """
    # TODO: Check if file already exists, then create the file.
    # db.insert_file(filepath, "created")

    parent = choice([3, 4, 5, 6, 7])
    """INSERT INTO files (name, parent_id, is_directory, size, created_at, modified_at) VALUES
    ('global.c', 3, 0, 1024, '2020-02-20 10:42:37', '2021-05-26 23:26:11')"""
    fsDB.insert_data(
        "files", (None, name, parent, 0, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    )
    print(("files", (None, name, parent, 0, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)))


@app.get("/dirId")
def getDirId(dir: str, pid: int = 1):
    """
    Get the directory id by name
    @args:
        dir: str - the name of the directory
        pid: int - the parent id of the directory
    @returns:
        int - the id of the directory or response with error
    """
    dirs = dir.strip().rstrip("/").split("/")

    query = f"SELECT id FROM directories WHERE name = '{dirs[0]}' and pid = '{pid}'"

    res = fsDB.run_query_in_thread([query])[0]

    if res["success"]:
        if len(res["data"]) > 0:
            pid = res["data"][0][0]
        else:
            res["message"] = f"Directory {dirs[0]} not found."
            return res
    else:
        return res
    if len(dirs) > 1:
        for dir in dirs[1:]:
            print(f"dir: {dir}")
            query = f"SELECT id FROM directories WHERE name = '{dir}' and pid = '{pid}'"
            res = fsDB.run_query_in_thread([query])[0]
            if res["success"]:
                if len(res["data"]) > 0:
                    pid = res["data"][0][0]
                else:
                    res["message"] = f"Directory {dir} not found."
                    return res
            else:
                return res
    return pid


### 2. **File Deletion**
@app.delete("/rm")
def delete_file(filepath):
    """
    Deletes a file from the filesystem and records the deletion in the database.
    :param filepath: The path of the file to be deleted.
    """
    # TODO: Check if the file exists, delete the file, and update the DB.
    # db.update_file(filepath, "deleted")
    pass


### 3. **File Read**
@app.get("/file")
def read_file(filepath):
    """
    Reads the contents of a file and tracks the access in the database.
    :param filepath: The path of the file to read.
    """
    # TODO: Open the file, read its content, and log the read action in the DB.
    # db.insert_action(filepath, "read")
    pass


### 4. **File Write**


@app.post("/filePath")
def write_file(filepath, content):
    """
    Writes data to a file and logs the write operation in the database.
    :param filepath: The path of the file to write to.
    :param content: The content to write to the file.
    """
    # TODO: Open the file in write mode, save content, and update the DB.
    # db.insert_action(filepath, "written")
    pass


### 5. **File Rename**
@app.put("/mv")
def rename_file(old_filepath, new_filepath):
    """
    Renames a file in the filesystem and updates the database with the new name.
    :param old_filepath: The current file path.
    :param new_filepath: The new file path.
    """
    # TODO: Rename the file and update the DB with the new path.
    # db.update_filename(old_filepath, new_filepath)
    pass


### 6. **Directory Creation**
@app.post("/dir")
def create_directory(directory_path):
    """
    Creates a new directory in the filesystem and records the action in the database.
    :param directory_path: The path of the directory to be created.
    """
    # TODO: Create a directory and log the action in the DB.
    # db.insert_directory(directory_path, "created")
    pass


### 7. **Directory Deletion**


@app.delete("/dir")
def delete_directory(directory_path):
    """
    Deletes a directory and its contents from the filesystem and records it in the database.
    :param directory_path: The path of the directory to be deleted.
    """
    # TODO: Delete the directory (and its contents) and log the action.
    # db.update_directory(directory_path, "deleted")
    pass


### 8. **Directory Listing**


@app.get("/dir")
def list_directory(directory_path):
    """
    Lists the contents of a directory and logs the access in the database.
    :param directory_path: The path of the directory to be listed.
    """
    # TODO: Retrieve all files/directories and log the action in the DB.
    # db.insert_action(directory_path, "listed")
    pass


### 9. **File Copy**


@app.get("/cp")
def copy_file(src_path, dest_path):
    """
    Copies a file from one location to another and logs it in the database.
    :param src_path: The source file path.
    :param dest_path: The destination file path.
    """
    # TODO: Copy the file and log the action in the database.
    # db.insert_action(src_path, "copied to", dest_path)
    pass


### 10. **File Move**


@app.get("/mv")
def move_file(src_path, dest_path):
    """
    Moves a file from one location to another and updates the database.
    :param src_path: The current file path.
    :param dest_path: The new file path.
    """
    # TODO: Move the file and update the DB with the new location.
    # db.insert_action(src_path, "moved to", dest_path)
    pass


### 11. **File Permissions**


@app.get("/perm")
def get_file_permissions(filepath):
    """
    Retrieves the permissions of a file and logs the action in the database.
    :param filepath: The path of the file.
    """
    pass


@app.put("/chmod")
def set_file_permissions(filepath, permissions):
    """
    Sets the permissions of a file and logs the action in the database.
    :param filepath: The path of the file.
    :param permissions: The new permissions to set.
    """
    pass


"""
This main block gets run when you invoke this file. How do you invoke this file?

        python api.py 

After it is running, copy paste this into a browser: http://127.0.0.1:8080 

You should see your api's base route!

Note:
    Notice the first param below: api:app 
    The left side (api) is the name of this file (api.py without the extension)
    The right side (app) is the bearingiable name of the FastApi instance declared at the top of the file.
"""
if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8080, log_level="debug", reload=True)
