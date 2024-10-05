"""
This script creates a SQLite database and populates it with file system data. You provide
the root directory and the script will recursively traverse the directory and gather file
information. The file information is then inserted into the SQLite database.
"""

from rich import print  # For pretty printing
from sqliteCRUD import SqliteCRUD  # Custom SQLite CRUD class
import base64  # For encoding binary data
import os  # For file system operations
import stat  # For file permissions
import sys  # For command line arguments
import time  # For file creation and modification times

tables = [
    """
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pid INTEGER,
    oid INTEGER,
    name TEXT,
    size INTEGER DEFAULT 0,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    contents BLOB,
    read_permission INTEGER DEFAULT 1,
    write_permission INTEGER DEFAULT 0,
    execute_permission INTEGER DEFAULT 1,
    world_read INTEGER DEFAULT 1,
    world_write INTEGER DEFAULT 0,
    world_execute INTEGER DEFAULT 1
)
""",
    """CREATE TABLE IF NOT EXISTS directories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,   -- parent directory
    pid INTEGER,                            -- parent directory
    oid INTEGER,                            -- owner
    name TEXT NOT NULL,                     -- directory name
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_permission INTEGER DEFAULT 1,
    write_permission INTEGER DEFAULT 0,
    execute_permission INTEGER DEFAULT 1,
    world_read INTEGER DEFAULT 1,
    world_write INTEGER DEFAULT 0,
    world_execute INTEGER DEFAULT 1
);""",
    """CREATE TABLE  IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);""",
    """INSERT INTO users (username, password) VALUES
    ('root', 'password0'),
    ('bob', 'password1'),
    ('mia', 'password2'),
    ('raj', 'password3')
""",
]


def printResults(res):
    """
    Description:
        Function to print the results of a query with key value pairs
    """
    for k, v in res.items():
        if k == "contents":
            print(f"{k}: {len(v)}")
        else:
            print(f"{k}: {v}")


def getDirId(dir_name):
    """
    Description:
        Function to get the directory id from the SQLite database
    Args:
        dir_name: (str) directory name
    Returns:
        (int) directory id or None
    """
    global conn
    query = f'SELECT * FROM directories WHERE name = "{dir_name}";'
    res = conn.runQuery(query)

    if res["affected"] == 0:
        return None

    return res["data"][0][0]


# Function to insert file info into SQLite
def insertFileData(
    pid: int,
    oid: int,
    name: str,
    size: int,
    creation_date: str,
    modified_date: str,
    contents: bytes,
    read_permission: int,
    write_permission: int,
    execute_permission: int,
    world_read: int,
    world_write: int,
    world_execute: int,
):
    """
    Description:
        Function to insert file info into SQLite
    Args:
        pid: (int) parent directory id
        oid: (int) owner id
        name: (str) file name
        size: (int) file size
        creation_date: (str) file creation date
        modified_date: (str) file modified date
        contents: (bytes) file contents
        read_permission: (int) read permission
        write_permission: (int) write permission
        execute_permission: (int) execute permission
        world_read: (int) world read permission
        world_write: (int) world write permission
        world_execute: (int) world execute permission
    Returns:
        res: (dict) result of the query
    """
    global conn
    query = f"""
            INSERT INTO files (
            pid, oid, name, size, creation_date, modified_date, contents,
            read_permission, write_permission, execute_permission,
            world_read, world_write, world_execute) 
            VALUES ("{pid}", "{oid}", "{name}", "{size}", "{creation_date}", "{modified_date}", "{contents}",
            "{read_permission}", "{write_permission}", "{execute_permission}",
            "{world_read}", "{world_write}", "{world_execute}")
            """
    res = conn.runQuery(query)
    return res


def load_directory(directory_path, oid=1):
    """
    Description:
        Function to recursively traverse a directory and insert file info into a sqlite database
    Args:
        directory_path: (str) directory path
        oid: (int) owner id
    Returns:
        dir_lookup: (dict) directory lookup
    """
    global conn
    pid = 0
    fcount = -1

    root_dir = os.path.basename(directory_path)
    curr_dir = None
    dir_lookup = {root_dir: 1}

    for root, dirs, files in os.walk(directory_path):
        path = root.split("/")
        path = path[5:]
        curr_dir = path[-1]
        if len(path) > 1:
            parent_dir = path[-2]

        if curr_dir == root_dir:
            query = f'INSERT INTO directories (pid,oid,name) VALUES ("{0}","{1}","{curr_dir}");'
            res = conn.runQuery(query)
            did = 1
        else:
            did = getDirId(curr_dir)
            pid = dir_lookup[parent_dir]

            if did is None:
                query = f'INSERT INTO directories (pid,oid,name) VALUES ("{pid}","{oid}","{curr_dir}");'
                res = conn.runQuery(query)
                did = getDirId(curr_dir)

        if curr_dir not in dir_lookup:
            dir_lookup[curr_dir] = did

        for file in files:
            fcount = fcount + 1
            # print(f"{fcount} {pid} {file} ")
            file_path = os.path.join(root, file)

            # Get file stats
            stats = os.stat(file_path)

            # File metadata
            name = file
            size = stats.st_size
            creation_date = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(stats.st_ctime)
            )
            modified_date = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(stats.st_mtime)
            )

            # File permissions
            permissions = stats.st_mode
            # print(f"Permissions: {permissions}")
            read_permission = int(bool(permissions & stat.S_IRUSR))
            write_permission = int(bool(permissions & stat.S_IWUSR))
            execute_permission = int(bool(permissions & stat.S_IXUSR))
            world_read = int(bool(permissions & stat.S_IROTH))
            world_write = int(bool(permissions & stat.S_IWOTH))
            world_execute = int(bool(permissions & stat.S_IXOTH))

            # Use the following line to read the file contents of a base64 encoded file
            # base64_output = base64_encoded_data.decode('utf-8')

            # Read file contents (if it's a small text file, for example)
            with open(file_path, "rb") as binary_file:
                binary_file_data = binary_file.read()
                base64_encoded_data = base64.b64encode(binary_file_data)

            # Insert data into SQLite
            res = insertFileData(
                did,
                oid,
                name,
                size,
                creation_date,
                modified_date,
                base64_encoded_data,
                read_permission,
                write_permission,
                execute_permission,
                world_read,
                world_write,
                world_execute,
            )
            print(res)


def usage():
    print("Usage: python create_and_load_db.py <root_dir> <db_name>")
    print("Example: python create_and_load_db.py /home/user1/files/ files.db")
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        root_dir = sys.argv[1]
        db = sys.argv[2]
    else:
        usage()

    # Remove the database if it exists
    delete = input("Delete existing database? (y/N): ")
    if delete.lower() == "y" and os.path.exists(db):
        os.remove(db)

    conn = SqliteCRUD(db)

    # Create tables
    for table in tables:
        res = conn.runQuery(table)
        printResults(res)

    # Traverse the directory
    load_directory(root_dir)

    # Close the connection
    conn.closeConnection()
