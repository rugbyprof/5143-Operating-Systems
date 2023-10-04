## Filesystem - Implementation of a virtual file system.
#### Due: 10-09-2023 (Monday @ 2:30 p.m.)


## Files 

|   #   | Name                             | Description                        |
| :---: | :------------------------------- | :--------------------------------- |
|   1   | [data_types.md](data_types.md)   | Sqlite - Data Types                |
|   2   | [fileSystem.py](fileSystem.py)   | Filesystem Starter Class           |
|   3   | [files](files)                   | Python Scripts to Build Fake Files |
|   4   | [my_database.db](my_database.db) |                                    |
|   5   | [permissions.md](permissions.md) | Linux Permissions String Convert   |
|   6   | [sqliteCRUD.py](sqliteCRUD.py)   | Crud Class for Sqlite              |
|   7   | [timestamps.md](timestamps.md)   | Sqlite - Timestamp functions       |

## Overview

This project will implement a virtual database that uses Sqlite as its storage. We will not be storing files that huge, or storing thousands of them, so we should be fine. If there ever is an issue, it's not hard to change to PostGres or similar. This virtual file system will store all content in a single table like you see below. Our table will contain columns that represent the properties commonly found in a Linux long listing (e.g., `ls -l`). Here's an example table structure:

```sql
CREATE TABLE FileSystem (
    id INTEGER PRIMARY KEY,
    pid INTEGER NOT NULL,
    filename TEXT NOT NULL,
    file_type TEXT NOT NULL,
    file_size INTEGER,
    owner TEXT NOT NULL,
    group TEXT NOT NULL,
    permissions TEXT NOT NULL,
    modification_time DATETIME,
    content BLOB
    hidden NUMBER 
);
```

For detailed info about Sqlite data types:
- [datatypes.md](data_types.md)
- [timestamps.md](timestamps.md)

Let's break down each column:

| Column Name         | Description                                                                                               |
| ------------------- | --------------------------------------------------------------------------------------------------------- |
| `id`                | An auto-incrementing unique identifier for each file system entry.                                        |
| `pid`               | The id of the parent folder.                                                                              |
| `filename`          | The name of the file or directory.                                                                        |
| `file_type`         | A text field representing the type of the file (e.g., "file" or "directory").                             |
| `file_size`         | The size of the file in bytes. This can be `NULL` for directories.                                        |
| `owner`             | The owner of the file.                                                                                    |
| `group`             | The group associated with the file.                                                                       |
| `permissions`       | A text field representing the file permissions in the format "rwxr-xr-x" (example).                       |
| `modification_time` | The date and time when the file was last modified.                                                        |
| `content`           | A BLOB column where you can store the file's contents directly. This is suitable for small file contents. |
| `hidden`            | (Optional) Doesn't need to be a column as you could look for the dot in front of the filename. Up to you. |


### Example Data

| id  | pid | filename      | file_type | file_size | owner | group | permissions | modification_time       | content                 | hidden |
| --- | --- | ------------- | --------- | --------- | ----- | ----- | ----------- | ----------------------- | ----------------------- | ------ |
| 1   | 0   | /             | directory | NULL      | root  | root  | rwxr-xr-x   | 2023-09-13 14:00:00 UTC | NULL                    | false  |
| 2   | 1   | /home         | directory | NULL      | root  | root  | rwxr-xr-x   | 2023-09-13 14:05:00 UTC | NULL                    | false  |
| 3   | 2   | /home/user1   | directory | NULL      | user1 | users | rwxr-x---   | 2023-09-13 14:10:00 UTC | NULL                    | false  |
| 4   | 2   | /home/user2   | directory | NULL      | user2 | users | rwxr-x---   | 2023-09-13 14:15:00 UTC | NULL                    | false  |
| 5   | 2   | /home/user3   | directory | NULL      | user3 | users | rwxr-x---   | 2023-09-13 14:20:00 UTC | NULL                    | false  |
| 6   | 3   | file1.txt     | file      | 1024      | user1 | users | rw-r-----   | 2023-09-13 14:30:00 UTC | [Binary data for file1] | false  |
| 7   | 3   | file2.txt     | file      | 2048      | user1 | users | rw-r-----   | 2023-09-13 14:35:00 UTC | [Binary data for file2] | false  |
| 8   | 4   | file3.txt     | file      | 1536      | user2 | users | rw-r-----   | 2023-09-13 14:40:00 UTC | [Binary data for file3] | false  |
| 9   | 4   | file4.txt     | file      | 3072      | user2 | users | rw-r-----   | 2023-09-13 14:45:00 UTC | [Binary data for file4] | false  |
| 10  | 5   | file5.txt     | file      | 2560      | user3 | users | rw-r-----   | 2023-09-13 14:50:00 UTC | [Binary data for file5] | false  |
| 11  | 0   | /tmp          | directory | NULL      | root  | root  | rwxr-xr-x   | 2023-09-13 15:00:00 UTC | NULL                    | false  |
| 12  | 11  | temp_file.txt | file      | 512       | root  | root  | rw-r--r--   | 2023-09-13 15:05:00 UTC | [Binary data for temp]  | false  |

## Requirements

The requirements to implement a filesystem could get extremely detailed and would involve several methods or functions to manage the various operations. Below is a list of **possible** methods. No we do not need to implement all of them, but I wanted to give you a taste of what a serious implementation might include. This is really a `File System API` or `class` that interacts with the underlying database to perform these operations.

### Example Query 

Below is an example query. It inserts a new row into some database. Notice the syntax with the ? marks as place holders for values.

```python
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('your_database.db')
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


1. **Create File**: Create a new file in a specified directory with the given name, owner, group, and permissions.
    ```python
    # Define the values for the new file
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
        INSERT INTO files (pid, filename, file_type, file_size, owner, group, permissions, modification_time, content, hidden)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (pid, filename, file_type, file_size, owner, group, permissions, modification_time, content, hidden))

    ```
2. **Create Directory**: Create a new directory in a specified parent directory with the given name, owner, group, and permissions.

    ```python
    # Same as above
    ```

3. **Delete File**: Delete an existing file from the file system.

    ```python
    # Find the ID of the file you want to delete
    file_id = 3  

    # Construct the DELETE query
    delete_query = "DELETE FROM files WHERE id = ?"

    # Execute the DELETE query with the file ID as a parameter
    cursor.execute(delete_query, (file_id,))
    ```

4. **Delete Directory**: Delete an existing directory and its contents from the file system.

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

5. **List Directory Contents**: List the contents (files and subdirectories) of a specified directory.
   
    ```python
    cursor.execute("SELECT * FROM files WHERE id = ?", (directory_id,))
    ```

6. **Read File**: Read the contents of an existing file.

    ```python
    cursor.execute("SELECT content FROM files WHERE id = ?", (directory_id,))
    ```

7. **Write File**: Write data to an existing file, potentially appending to the existing content.

8. **Move File or Directory**: Move a file or directory from one location to another within the file system.

9.  **Copy File or Directory**: Copy a file or directory to a new location within the file system.

10. **Change Ownership**: Change the owner of a file or directory.

11. **Change Group**: Change the group associated with a file or directory.

12. **Change Permissions**: Modify the permissions (e.g., read, write, execute) of a file or directory.

13. **Get File or Directory Information**: Retrieve metadata (e.g., size, modification time) about a file or directory.

14. **Search for Files**: Search for files or directories based on criteria like name, type, owner, or permissions.

15. **Access Control**: Implement access control checks to determine whether a user has permission to perform specific operations on files or directories.

16. **File Upload**: Upload a file from an external source (e.g., a client application) and store it in the file system.

17. **File Download**: Retrieve a file from the file system and provide it for download to an external client.

18. **File Versioning**: Implement version control for files to track changes and revisions.

19. **File Metadata Management**: Allow users to add and manage metadata (e.g., tags, descriptions) for files and directories.

20. **File and Directory Renaming**: Rename files and directories.

21. **Hidden Files and Directories Handling**: Implement functionality to hide or unhide files and directories based on naming conventions or attributes.

22. **File and Directory Permissions Enforcement**: Enforce access permissions to ensure that users can only perform actions allowed by their permissions.

23. **Error Handling and Logging**: Implement error handling to manage and log any exceptions or issues that arise during file system operations.

24. **File and Directory Locking**: Provide mechanisms to lock and unlock files and directories to prevent concurrent access conflicts.

25. **File and Directory Monitoring**: Implement mechanisms to monitor changes to files and directories (e.g., using inotify or similar technologies).

26. **File and Directory Permissions Inheritance**: Implement inheritance of permissions from parent directories to child directories and files.

27. **Trash or Recycle Bin**: Implement a feature to move deleted files and directories to a trash or recycle bin for potential recovery.



## Requirements 

### Those That Have Not Presented 

- If you haven't presented your shell yet and have opted to wait, then the [checklist](../P01/command_checklist.md) in `P02` applies to this assignment. 
- Meaning you will present just as all the others did, but using sqlite as a backend.

### Those That Have Presented 

- Here is a smaller checklist.
- You will not have to present per se. You will have to show a walkthrough

|    #    | Item                                             |  Value  | Earned |
| :-----: | ------------------------------------------------ | :-----: | :----: |
| ***1*** | ***Commands***                                   | **200** |        |
|    1    | *ls -lah*                                        |    ▢    |        |
|    2    | *mkdir bananas*                                  |    ▢    |        |
|    3    | *cd bananas*                                     |    ▢    |        |
|    4    | *cd ..*                                          |    ▢    |        |
|    5    | *pwd*                                            |    ▢    |        |
|    6    | *mv somefile.txt bananas*                        |    ▢    |        |
|    7    | *cp bananas/somefile.txt somefile/otherfile.txt* |    ▢    |        |
|    8    | *rm -rf bananas*                                 |    ▢    |        |
|    9    | *history*                                        |    ▢    |        |
|   10    | *chmod 777 somefile.txt*                         |    ▢    |        |

- You can simply run a file that shows an example `usage` of your file system.
- Example:

<img src="https://images2.imgbox.com/18/4e/iZzcjQcb_o.png">

- This should have a delay between commands so it can be seen running.
- Using python rich, you can have fun with it and format the output however you want, as long as you stay within the spirit of the command. 
- I've provided a mocked up example walkthrough [here](./walkthrough.py).



