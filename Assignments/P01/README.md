# Filesystem Project - Implementation of a Virtual Filesystem

### Due Date: TBD (Will be discussed in class)

## Overview

In this project, you will implement a virtual filesystem using **SQLite** as the storage backend. While we won't be working with massive files or thousands of entries, the design should be flexible enough to handle typical filesystem operations. If the need arises, the project could be adapted to a more robust database system like PostgreSQL.

### Goal

The goal is to mimic a simple Unix-like filesystem. You will design a database that represents directories and files, supports basic operations such as reading, writing, and navigating the filesystem, and enforces permissions.

## Schema Discussion

- When implementing a filesystem using **SQLite**, using only one table like we started out with last class may limit the design's flexibility and efficiency.
- To improve the old schema (one table 😂), we could create multiple tables with the goal of trying to spread out the responsibility?
- Think about a file systems main purposes:
  - **directories** (to give that hierarchical structure)
  - **files** (the item that is really what were interested in)
  - **security** (stay away from my files)
- Security would include:
  - users
  - permissions

### 1. **Files Table**

```sql
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
);
```

This table stores file data. Everything about the file, even the contents. Notice the contents column is a BLOB
data type. I decided to `base64` encode the files so I don't have to deal with escaping characters.

```python


# Read file and base 64 encode it.
with open(file_path, "rb") as binary_file:
    binary_file_data = binary_file.read()
    base64_encoded_data = base64.b64encode(binary_file_data)


# Later on you can use the following to turn it back into something readable (depending on the filetype).
base64_output = base64_encoded_data.decode('utf-8')
```

### 2. **Directories Table**

This table represents directories, with each directory able to contain other directories or files.

```sql
CREATE TABLE IF NOT EXISTS directories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,   -- directory id
    pid INTEGER,                            -- parent directory id
    oid INTEGER,                            -- owner id
    name TEXT NOT NULL,                     -- directory name
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_permission INTEGER DEFAULT 1,
    write_permission INTEGER DEFAULT 0,
    execute_permission INTEGER DEFAULT 1,
    world_read INTEGER DEFAULT 1,
    world_write INTEGER DEFAULT 0,
    world_execute INTEGER DEFAULT 1;
```

### 3. **Users Table**

This table manages user information, which helps in implementing multi-user systems with permission handling.

```sql
CREATE TABLE  IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Key Takeaways:

1. **Separation of Concerns**: Dividing files and directories into separate tables makes it easier to manage metadata and relationships (e.g., parent-child relationships between directories).

2. **Efficient Content Management**: ~~Splitting file content into chunks in the `file_contents` table ensures that large files can be handled in parts rather than being loaded all at once which could "feel" like your system froze~~. Is a better overall solution, but we are simulating a small file system in which we are guaranteed to have files no larger than 1GB (and even that is way to large).

3. **Self-Referencing for Directories**: Directories can reference themselves through the `pid`, allowing for hierarchical structures like a real filesystem.

4. **Permissions**: ~~Implementing permissions helps mimic a true multi-user filesystem, where users may have different levels of access to files and directories~~. Permissions are stored directly in each table for files and directories. And then only the owners and the worlds permissions are stored (no groups).

## Getting Started

I wrote a new database creation and loading script: [`create_and_load_db.py`](./create_and_load_db.py). This script does:

1. creates all the tables as described above.
2. traverses a given directory and processes the files and directories inserting the info into `sqlite`.

Don't run it on a root folder, as it will process all files from a given directory recursively and you could end up with thousands of entries. Usage is printed below. You should provide the path to the folder you want processed, and the name of your db file.

```python
    print("Usage: python create_and_load_db.py <root_dir> <db_name>")
    print("Example: python create_and_load_db.py /home/user1/files/ files.db")
```

## Basics Of Your Filesystem

In the [`create_and_load_db.py`](./create_and_load_db.py) there are examples if inserting files and directories. But lets focus on what your filesystem should do in regards to the shell you will be running.

### Dealing with Directories

1. Starting your shell will take you to your home directory, whatever that may be. That entry will obviously exist in your database, but it is important to note that you must always know the directory ID of your current location. Many actions will based on "where you currently are".
2. Directory listings are simply selecting all the files of a directory. Right?
   1. So `ls -l` is simple enough. `SELECT * FROM files WHERE pid = currentDirID`
   2. However, what about `ls -l /home/yolanda/programs/data/`? How does that change things? You cannot just select all the files from the table that have the data's directory id. Which data? You will have to split that path and progressively find data's id by starting with /home's id, then progressing into each directory and getting its id.
3. The change directory would be easy as well, unless you provide a path like above. So:
   1. `cd ..` or `cd folderName` would be pretty easy as they are one level away. `cd ..` would be change to my parent directory. And the `cd folderName` would be getting the id for folderName, then making that my location.
   2. But: `cd /home/yolanda/programs/data/` is the same problem as above.
   3. OR: `cd ../../someDir/anotherDir/` ?
   4. AND: `cd programs/data/otherSubData/`?

Any path that starts with a "/" starts at the "root" folder. That id will be 1 or 0, whateveer you make your root folder id be. All the other path types are based on where you are. Number 3 backs up two directories from my current location. And number 4 is looking for a directory id : `SELECT id FROM files WHERE name = 'program' AND pid = currDirId;`

### 1. **Touch** command:

The `touch` command does these 2 things (for our project). For example the command: `touch someFile.txt` would do one of the following:

1. create a new file with 0 bytes with the name someFile.txt
2. update a files modified_at date time to now if someFile.txt already exists

Create a new file in the filesystem, specifying the parent directory and metadata (e.g., name, owner, permissions).

# MORE TO COME ... ITS LATE AND I'M DONE TILL LATER TONIGHT

I will add sql queries to basic shell commands, but the hardest is processing paths and determining where you are and where the path is trying to take you. So work on the new filesystem schema and I'll post more help tonight.

Also I will move the due date ...

<!-- ## Additional Features (Optional)

Consider implementing these additional features if time permits:

- **Search for files**: Search based on name, owner, or permissions.
- **Move or Copy files**: Transfer files between directories.
- **Version control**: Implement basic versioning for files.
- **File metadata management**: Allow users to add descriptions or tags to files.

---

## Submission Guidelines

1. **Repository**:

   - Create a private GitHub repository.
   - Ensure your team members have access and invite `rugbyprof` as a collaborator.

2. **Required Files**:

   - `filesystem.py`: Your Python code implementing the filesystem.
   - `README.md`: Instructions on how to set up and run your filesystem, including a list of commands implemented.
   - `filesystem.sqlite`: The SQLite database with the filesystem structure.

3. **Deliverables**:
   - A functioning virtual filesystem with the ability to create, read, delete, and manage files and directories.
   - Proper documentation in the README.

---

By organizing the project with multiple tables (files, directories, users, permissions), you’ll get a better structure for your filesystem, allowing it to more closely resemble a real-world implementation. Let me know if you need further refinements or additional help! -->
