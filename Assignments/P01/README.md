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
  - groups
  - permissions

### 1. **Files Table**

This table stores metadata about each file (e.g., name, type, size, timestamps).

```sql
CREATE TABLE files (
    file_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    parent_id INTEGER,
    is_directory BOOLEAN NOT NULL,
    size INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES directories(dir_id)
);
```

### 2. **Directories Table**

This table represents directories, with each directory able to contain other directories or files.

```sql
CREATE TABLE directories (
    dir_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    parent_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES directories(dir_id) -- Self-referencing for subdirectories
);
```

### 3. **File Contents Table**

This table stores the actual content of each file, which allows larger files to be managed in chunks.

```sql
CREATE TABLE file_contents (
    content_id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER NOT NULL,
    chunk BLOB, -- Each file's content is split into chunks for efficient storage
    chunk_index INTEGER,
    FOREIGN KEY (file_id) REFERENCES files(file_id)
);
```

### 4. **Permissions Table**

This table manages file and directory permissions (e.g., read, write, execute) for different users or groups.

```sql
CREATE TABLE permissions (
    perm_id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER,
    dir_id INTEGER,
    user_id INTEGER,
    read_permission BOOLEAN DEFAULT 0,
    write_permission BOOLEAN DEFAULT 0,
    execute_permission BOOLEAN DEFAULT 0,
    FOREIGN KEY (file_id) REFERENCES files(file_id),
    FOREIGN KEY (dir_id) REFERENCES directories(dir_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

### 5. **Users Table**

This table manages user information, which helps in implementing multi-user systems with permission handling.

```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Key Takeaways:

1. **Separation of Concerns**: Dividing files and directories into separate tables makes it easier to manage metadata and relationships (e.g., parent-child relationships between directories).

2. **Efficient Content Management**: Splitting file content into chunks in the `file_contents` table ensures that large files can be handled in parts rather than being loaded all at once which could "feel" like your system froze.

3. **Self-Referencing for Directories**: Directories can reference themselves through the `parent_id`, allowing for hierarchical structures like a real filesystem.

4. **Permissions**: Implementing permissions helps mimic a true multi-user filesystem, where users may have different levels of access to files and directories.

- This is a tiny bit more robust than the awesome single table schema discussed in last class.
- It improves scalability and functionality, giving us a better chance of getting good file system behavior, in fact we may find that we get pretty damn close to an actual operating system's file system.
- It looks a lot more daunting, but overall, it should make running many query's easier. Not all queries, but most.

### 1. **Directories Table** (Root and Subdirectories)

```sql
INSERT INTO directories (name, parent_id) VALUES
    ('root', NULL),
    ('home', 1), -- Subdirectory under root
    ('usr', 1),
    ('documents', 2), -- Subdirectory under home
    ('photos', 2); -- Subdirectory under home
```

### 2. **Files Table** (Files within the Directories)

```sql
INSERT INTO files (name, parent_id, is_directory, size, created_at, modified_at) VALUES
    ('file1.txt', 2, 0, 1024, '2024-09-24 10:00:00', '2024-09-24 10:00:00'), -- File in home
    ('file2.txt', 4, 0, 2048, '2024-09-24 11:00:00', '2024-09-24 11:00:00'), -- File in documents
    ('file3.txt', 5, 0, 4096, '2024-09-24 12:00:00', '2024-09-24 12:00:00'), -- File in photos
    ('script.sh', 3, 0, 512, '2024-09-24 09:00:00', '2024-09-24 09:00:00');  -- File in usr
```

### 3. **File Contents Table** (Content Chunks for Large Files)

```sql
INSERT INTO file_contents (file_id, chunk, chunk_index) VALUES
    (1, 'This is the first chunk of file1.txt.', 1),
    (1, 'This is the second chunk of file1.txt.', 2),
    (2, 'This is the content of file2.txt.', 1),
    (3, 'This is the first part of file3.txt.', 1),
    (3, 'This is the second part of file3.txt.', 2);
```

### 4. **Users Table** (User Information)

```sql
INSERT INTO users (username, password) VALUES
    ('user1', 'password123'),
    ('user2', 'securepassword'),
    ('admin', 'adminpass');
```

### 5. **Permissions Table** (Permissions for Files and Directories)

```sql
INSERT INTO permissions (file_id, dir_id, user_id, read_permission, write_permission, execute_permission) VALUES
    (NULL, 1, 3, 1, 1, 1),  -- Admin has full access to root
    (NULL, 2, 1, 1, 1, 0),  -- User1 has read/write access to home directory
    (1, NULL, 1, 1, 1, 0),  -- User1 has read/write access to file1.txt
    (2, NULL, 2, 1, 0, 0),  -- User2 has read access to file2.txt
    (NULL, 4, 2, 1, 0, 0),  -- User2 has read access to documents directory
    (4, NULL, 3, 1, 1, 1);  -- Admin has full access to script.sh
```

### Data Explanation:

1. **Directories**:
   - Created a root directory with subdirectories for `/home`, `/usr`, `/documents`, and `/photos`.
2. **Files**:

   - Placed files within various directories (`home`, `documents`, `photos`, and `usr`). Each file has a size and timestamp for when it was created and last modified.

3. **File Contents**:

   - Files are split into chunks, mimicking how large files are often managed in blocks.

4. **Users**:

   - Created three users: `user1`, `user2`, and `admin`.

5. **Permissions**:
   - Set up various permissions to control access to files and directories. For example, `admin` has full access to the `root` directory and the script file, while `user1` has access to their `home` directory and a file within it.

### Additional Notes:

- You can further adjust the `size` of the files or `chunk` contents based on actual data needs.
- User permissions can be expanded to more complex scenarios (e.g., group-based permissions).


Explanation of Data Insertion:

- Users: Inserting users `bob`, `mia`, and `raj`.
- Directories: Each directory is inserted with a reference to its `parent_id` (null if its a root directory).
- Files: Files are linked to their corresponding directories through `parent_id` and have specific timestamps and sizes.
- Permissions: Each permission entry determines the access level for users on specific files and directories, following the `rwx` pattern.



## Required Operations

Here are some essential operations you will implement in Python, interfacing with your SQLite database.

### 1. **Create File**

Create a new file in the filesystem, specifying the parent directory and metadata (e.g., name, owner, permissions).

```python
def create_file(pid, filename, owner, group, size, permissions):
    cursor.execute("""
        INSERT INTO files (parent_id, name, is_directory, size, owner, group, permissions, created_at, modified_at)
        VALUES (?, ?, 0, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """, (pid, filename, size, owner, group, permissions))
```

### 2. **Create Directory**

Similar to creating a file, but for directories.

```python
def create_directory(pid, dirname, owner, group, permissions):
    cursor.execute("""
        INSERT INTO directories (parent_id, name, owner, group, permissions, created_at, modified_at)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """, (pid, dirname, owner, group, permissions))
```

### 3. **Delete File**

Delete a file by its unique ID.

```python
def delete_file(file_id):
    cursor.execute("DELETE FROM files WHERE file_id = ?", (file_id,))
```

### 4. **Delete Directory**

Delete a directory and recursively delete its contents.

```python
def delete_directory(dir_id):
    cursor.execute("SELECT file_id FROM files WHERE parent_id = ?", (dir_id,))
    for file_id in cursor.fetchall():
        delete_file(file_id)
    cursor.execute("DELETE FROM directories WHERE dir_id = ?", (dir_id,))
```

### 5. **List Directory Contents**

List all files and subdirectories within a specific directory.

```python
def list_directory(dir_id):
    cursor.execute("SELECT * FROM files WHERE parent_id = ?", (dir_id,))
    return cursor.fetchall()
```

### 6. **Change Permissions**

Update the permissions for a file or directory.

```python
def change_permissions(file_id, new_permissions):
    cursor.execute("UPDATE files SET permissions = ? WHERE file_id = ?", (new_permissions, file_id))
```

---

## Additional Features (Optional)

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

By organizing the project with multiple tables (files, directories, users, permissions), you’ll get a better structure for your filesystem, allowing it to more closely resemble a real-world implementation. Let me know if you need further refinements or additional help!
