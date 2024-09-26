files = """
CREATE TABLE files (
    file_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    parent_id INTEGER,
    is_directory BOOLEAN NOT NULL,
    size INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES directories(dir_id)
);"""

CREATE TABLE directories (
    dir_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    parent_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES directories(dir_id) -- Self-referencing for subdirectories
);

CREATE TABLE file_contents (
    content_id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER NOT NULL,
    chunk BLOB, -- Each file's content is split into chunks for efficient storage
    chunk_index INTEGER,
    FOREIGN KEY (file_id) REFERENCES files(file_id)
);

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

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
