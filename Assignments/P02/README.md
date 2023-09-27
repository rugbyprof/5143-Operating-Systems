## Filesystem - Implementation of a virtual file system.
#### Due: 10-09-2023 (Monday @ 2:30 p.m.)


## Files 

|   #   | Name                                                 | Description                                        |
| :---: | :--------------------------------------------------- | :------------------------------------------------- |
|   1   | [data_formatting.md](data_formatting.md)             | [Data Formatting](data_formatting.md)              |
|   2   | [data_types.md](data_types.md)                       | [Sqlite - Data Types](data_types.md)               |
|   3   | [file-sys-primer-data.csv](file-sys-primer-data.csv) | [None](file-sys-primer-data.csv)                   |
|   4   | [fileSystem.py](fileSystem.py)                       | [Filesystem Starter Class](fileSystem.py)          |
|   5   | [filesystem.sqlite](filesystem.sqlite)               | [binary file](filesystem.sqlite)                   |
|   6   | [my_database.sqlite](my_database.sqlite)             | [binary file](my_database.sqlite)                  |
|   7   | [permissions.md](permissions.md)                     | [Linux Permissions String Convert](permissions.md) |
|   8   | [requirements.txt](requirements.txt)                 | [None](requirements.txt)                           |
|   9   | [sqliteCRUD.py](sqliteCRUD.py)                       | [conn Class for Sqlite](sqliteCRUD.py)             |
|  10   | [students.sqlite](students.sqlite)                   | [binary file](students.sqlite)                     |
|  11   | [testfilesystem.sqlite](testfilesystem.sqlite)       | [binary file](testfilesystem.sqlite)               |
|  12   | [timestamps.md](timestamps.md)                       | [Sqlite - Timestamp functions](timestamps.md)      |

## Overview

This project will implement a virtual database that uses Sqlite as its storage. We will not be storing large files, or storing thousands of them, so a sqlite db should be fine. If there ever is an issue, it's not hard to change to PostGres or similar. This virtual file system will store all content in a single database table, the structure of which is explained below. But what is a "virtual" file system? It can mean many things, but for this project it simply means that instead of writing data organized in a file to disk, we will write that data to a column in a database table. It is possible to store real files like word docs, powerpoints, images, etc. in a table, but for this project you will store some randomly generated assembly instructions which I will provide. These files are to simulate instructions in an executable file. See example tiny file below:

#### Example Executable
```asm
LOAD R1, 5           ; Load the value 5 into register R1
LOAD R2, 10          ; Load the value 10 into register R2
ADD R3, R1, R2       ; Add the values in R1 and R2, and store the result in R3
SUB R4, R2, R1       ; Subtract the value in R1 from the value in R2, and store the result in R4
MULT R5, R1, R2      ; Multiply the values in R1 and R2, and store the result in R5
DIV R6, R2, R1       ; Divide the value in R2 by the value in R1, and store the result in R6
MOD R7, R2, R1       ; Calculate the modulus of the value in R2 divided by the value in R1, and store the result in R7
```

Of course, a file system stores many more things beyond file content and we will need to address many of them. Look at the example data below. Where you see `[Binary data for _______]` replace it with pretend file content from the example above. Notice the data in the table below looks extremely similar to a long listing `ls -l` 

#### Example Data

>NOTE: `groop` is misspelled since it is a reserved word and causes problems with sql.

This data is organized into `rows` and `columns`, where a column is vertical and rows are horizontal. A "row" is a collection of data that is stored together, meaning it is associated with a single entry. If you stored data for a single person, all of there information would be in the same row. Columns are just data values that are alike. Like all the ages of a person would be in the same column. I don't want to get into database theory, but we need to be able to find a single row of data without ambiguity, and that is when we use a `key`, more specifially a `primary key`. In this example data the primary key is the `id` column. And a very abstracted query to obtain data from a database table could be: `Give me the row of data that has the id 7`. But using primary keys allows us to know that we are receiving the correct and unique data for that `id`.

```
| id  | pid | filename      | file_type | file_size | owner | groop | permissions | modification_time       | content                 | hidden |
| --- | --- | ------------- | --------- | --------- | ----- | ----- | ----------- | ----------------------- | ----------------------- | ------ |
| 1   | 0   |               | directory | NULL      | root  | root  | rwxr-xr-x   | 2023-09-13 14:00:00 UTC | NULL                    | false  |
| 2   | 1   | home          | directory | NULL      | root  | root  | rwxr-xr-x   | 2023-09-13 14:05:00 UTC | NULL                    | false  |
| 3   | 2   | user1         | directory | NULL      | user1 | users | rwxr-x---   | 2023-09-13 14:10:00 UTC | NULL                    | false  |
| 4   | 2   | user2         | directory | NULL      | user2 | users | rwxr-x---   | 2023-09-13 14:15:00 UTC | NULL                    | false  |
| 5   | 2   | user3         | directory | NULL      | user3 | users | rwxr-x---   | 2023-09-13 14:20:00 UTC | NULL                    | false  |
| 6   | 3   | file1.txt     | file      | 1024      | user1 | users | rw-r-----   | 2023-09-13 14:30:00 UTC | [Binary data for file1] | false  |
| 7   | 3   | file2.txt     | file      | 2048      | user1 | users | rw-r-----   | 2023-09-13 14:35:00 UTC | [Binary data for file2] | false  |
| 8   | 4   | file3.txt     | file      | 1536      | user2 | users | rw-r-----   | 2023-09-13 14:40:00 UTC | [Binary data for file3] | false  |
| 9   | 13  | file4.txt     | file      | 3072      | user2 | users | rw-r-----   | 2023-09-13 14:45:00 UTC | [Binary data for file4] | false  |
| 10  | 5   | file5.txt     | file      | 2560      | user3 | users | rw-r-----   | 2023-09-13 14:50:00 UTC | [Binary data for file5] | false  |
| 11  | 0   | tmp           | directory | NULL      | root  | root  | rwxr-xr-x   | 2023-09-13 15:00:00 UTC | NULL                    | false  |
| 12  | 11  | temp_file.txt | file      | 512       | root  | root  | rw-r--r--   | 2023-09-13 15:05:00 UTC | [Binary data for temp]  | false  |
| 13  | 5   | homework      | directory | NULL      | user3 | users | rwxr-x---   | 2023-09-13 14:20:00 UTC | NULL                    | false  |
```

Next I will discuss sqlite, and some of its benefits. But as I discuss storing files in a database table, I want you to think about implementing shell commands. What? Yes, I will be giving examples of how to `insert`, `find`, `update`, and `delete` data dealing with files. So as Im going over examples, think about ways to implement 

- `ls`
- `rm` 
- `mv` 
- `mkdir`
- `chmod`

## File System Purpose

The purpose of a file system is to provide the following basic functionality: 

  - Create files and directories
  - Copy and Move files and directories to different locations
  - Edit a file and a directories metadata (some of this overlaps with other purposes)
    - permissions
    - ownership
    - name
    - location
  - Delete files and directories
  - Get a file or directories contents 

All of the queries below are directly or indirectly supporting the above abilities with respect to our files and directories. With python we could use the `os` or `sys` libraries (amongst others) to apply these actions to our file system. Our goal now is to forgo these built in libraries, and implement these actions using sql queries and the Sqlite DB.

### Sqlite

Sqlite is a small local db that resides in a file. To interact with sqlite we will use a python library to run "queries". The query below creates a SQL table that matches the example data you see above. This is not a db class, so most (not all) of the sql you need will be provided by me. 

```sql
CREATE TABLE FileSystem (
    id INTEGER PRIMARY KEY,
    pid INTEGER NOT NULL,
    filename TEXT NOT NULL,
    file_type TEXT NOT NULL,
    file_size INTEGER,
    owner TEXT NOT NULL,
    groop TEXT NOT NULL,
    permissions TEXT NOT NULL,
    modification_time DATETIME,
    content BLOB
    hidden NUMBER 
);
```

#### Column Descriptions

| Column Name         | Description                                                                                               |
| ------------------- | --------------------------------------------------------------------------------------------------------- |
| `id`                | A unique identifier for each file system entry (primary key).                                             |
| `pid`               | The id of the parent folder.                                                                              |
| `filename`          | The name of the file or directory.                                                                        |
| `file_type`         | A text field representing the type of the file (e.g., "file" or "directory").                             |
| `file_size`         | The size of the file in bytes. This can be `NULL` for directories.                                        |
| `owner`             | The owner of the file.                                                                                    |
| `groop`             | The group associated with the file.                                                                       |
| `permissions`       | A text field representing the file permissions in the format "rwxr-xr-x" (example).                       |
| `modification_time` | The date and time when the file was last modified.                                                        |
| `content`           | A BLOB column where you can store the file's contents directly. This is suitable for small file contents. |
| `hidden`            | (Optional) Doesn't need to be a column as you could look for the dot in front of the filename. Up to you. |



Each column in a sql table must have a data type and not all databases provide the same data types. The two docs below discuss sqlite data types, and how to deal with date and time types. 
- [Sqlite datatypes overview](data_types.md)
- [How to represent timestamps in sqlite](timestamps.md)

Thats a little background on representing file data, and how we might store it in a sql table. But it doesn't exactly explain how you might use this as a file system. To explain the relationship to how it can be used as a file system, I will go through some example querys next.



## Some Example Queries

####  Example Simple Query 

- This first example is a small "start" to "finish" example showing how to connect, excute a query, and close a connection.
- Mostly we will be using classes designed by us to abstract some of these details, but ultimately still connects and queries Sqlite like [the Sqlite Crud Class](./sqliteCRUD.py).
- This example inserts a new row into the `theDatabase` database. 
- Notice the syntax with the `?` marks as place holders for values.

```python
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('theDatabase.sqlite')
cursor = conn.cursor()

# Define the values you want to insert
name = 'John'
age = 30

# Construct the SQL query with placeholders
sql_query = "INSERT INTO users (name, age) VALUES (?, ?)"

# Execute the query with the values
cursor.execute(sql_query, (name, age))

# Commit the changes and close the database connection
conn.commit()
conn.close()

```

#### Create File Query

- Creates a new file in a specified directory with the given name, owner, group, and permissions.
- You would turn this into a function that gets the values as parameters
- Commands:
  - `touch` could create a new row of file data, but if a file exists, it would update modification time.
  - `cp` could create a new row of data as well, copying each column but would need to update `id` `pid` (possibly) `modification_time`
  
```python
# Define the values for the new file
id = 23                                     # file id
pid = 1                                     # Parent directory ID 
filename = 'new_file.txt'
file_type = 'file'
file_size = 1024                            # Actual file size in bytes
owner = 'user1'                             # Owner's username
group = 'users'                             # Group name
permissions = 'rw-r-----'                   # Desired permissions
modification_time = '2023-09-13 14:30:00 UTC'  # Modification time
content = b'Binary data for new file'       # Actual binary content
hidden = False                              # True or False

# Insert the new file into the database
cursor.execute("""
    INSERT INTO files (id, pid, filename, file_type, file_size, owner, group, permissions, modification_time, content, hidden)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (id, pid, filename, file_type, file_size, owner, group, permissions, modification_time, content, hidden))

```

#### Create Directory

- Creating  a new directory is the same as creating a file
- Commands: 
  - `mkdir` creates a new row of data

```python
# Same as above
```

#### Delete File

- Deletes an existing file from the file system.
- You would need to find its file id (discuss later) first.
- Commands:
  - `rm` removes a row from the table

```python
# Find the ID of the file you want to delete
file_id = 3  

# Construct the DELETE query
delete_query = "DELETE FROM files WHERE id = ?"

# Execute the DELETE query with the file ID as a parameter
cursor.execute(delete_query, (file_id,))
```

#### Delete Directory 

- Deletes an existing directory and its contents from the file system.
- This is a recursive function that handles child directories and files
- Just as deleting a file, you would need to get the directories id
- Commands:
  - `rm -r` removes a directory and all of its contents recursively

```python
def delete_directory(directory_id):
    # Check if the directory exists
    cursor.execute("SELECT id FROM files WHERE id = ? AND file_type = 'directory'", (directory_id,))
    dir_exists = cursor.fetchone()

    if dir_exists:
        # List contents of the directory 
        cursor.execute("SELECT id, file_type FROM files WHERE pid = ?", (directory_id,))
        contents = cursor.fetchall()

        for content_id, content_type in contents:
            if content_type == 'file':
                # Delete file
                cursor.execute("DELETE FROM files WHERE id = ?", (content_id,))
            elif content_type == 'directory':
                # Recursively delete subdirectory
                delete_directory(content_id)

        # Delete the directory itself
        cursor.execute("DELETE FROM files WHERE id = ?", (directory_id,))
    else:
        print("Directory not found.")

# Define the ID of the directory you want to delete
directory_id = 2  

# Call the delete_directory function to delete the directory and its contents
delete_directory(directory_id)
```

#### Directory Listing
- List the contents (files and subdirectories) of a specified directory.
- Won't recurse into other directories
- Commands:
  - `ls`
   
```python
cursor.execute("SELECT * FROM files WHERE id = ?", (directory_id,))
```

#### Get File Contents

- Reads the contents of an existing file.
- Commands:
  - `more`
  - `cat`
  - `less`
  - `head` , `tail`

```python
cursor.execute("SELECT content FROM files WHERE id = ?", (directory_id,))
```

#### Move File or Directory

- Move a file or directory from one location to another within the file system.
- Commands:
  - `mv`

```python
# find id of file or directory and target_id of where to be moved
cursor.execute("UPDATE files SET pid = ? WHERE id = ?", (id,target_id,))
```

#### Copy File or Directory

- Copys a file or directory to a new location within the file system.
- Steps:
  - Select all info of file or directory to be copied
  - Create a new row with same info but create a new id and ensure its not in the same place (has same pid)
- Commands:
  - `cp`

```python
cursor.execute("SELECT * FROM files WHERE id = ?", (id,))
# Then call the insert command from above with all the data, but with a new id and possibly parent id.

```

### Other Possible Queries

We can discuss these in class later. 

1. **Write File**: Write data to an existing file, potentially appending to the existing content.
4.  **Change Ownership**: Change the owner of a file or directory.
5.  **Change Group**: Change the group associated with a file or directory.
6.  **Change Permissions**: Modify the permissions (e.g., read, write, execute) of a file or directory.
7.  **Get File or Directory Information**: Retrieve metadata (e.g., size, modification time) about a file or directory.
8.  **Search for Files**: Search for files or directories based on criteria like name, type, owner, or permissions.
9.  **Access Control**: Implement access control checks to determine whether a user has permission to perform specific operations on files or directories.
10. **File Upload**: Upload a file from an external source (e.g., a client application) and store it in the file system.
11. **File Download**: Retrieve a file from the file system and provide it for download to an external client.
12. **File Versioning**: Implement version control for files to track changes and revisions.
13. **File Metadata Management**: Allow users to add and manage metadata (e.g., tags, descriptions) for files and directories.
14. **File and Directory Renaming**: Rename files and directories.
15. **Hidden Files and Directories Handling**: Implement functionality to hide or unhide files and directories based on naming conventions or attributes.
16. **File and Directory Permissions Enforcement**: Enforce access permissions to ensure that users can only perform actions allowed by their permissions.
17. **Error Handling and Logging**: Implement error handling to manage and log any exceptions or issues that arise during file system operations.
18. **File and Directory Locking**: Provide mechanisms to lock and unlock files and directories to prevent concurrent access conflicts.
19. **File and Directory Monitoring**: Implement mechanisms to monitor changes to files and directories (e.g., using inotify or similar technologies).
20. **File and Directory Permissions Inheritance**: Implement inheritance of permissions from parent directories to child directories and files.
21. **Trash or Recycle Bin**: Implement a feature to move deleted files and directories to a trash or recycle bin for potential recovery.


## Requirements

- Create a sqlite database to store the appropriate file system files, directories, and metadata for each. 
- You can change the provided `schema` (table structure) if you feel it will improve your own version, but you must be able to support the file systems basic purposes (listed way above).
- Your implementation should be written in a class that extends through composition or inheritance another more generic class that interfaces with Sqlite performing basic queries. For example, a `Sqlite Class` which provides basic inserts, updates, selects, and deletes (with some other helper methods of course) would be used by a `Filesystem Class` that supports everything listed in the **File System Purpose** section.
- I created a logical (yet fake) file system such that each id is correct. Meaning, each parent id for files and directories matches as it should. I did not create the "assembly code" for each of those files however and therefore there is no filesize. [HERE](./file-sys-primer-data.csv) is the results of the generator code.