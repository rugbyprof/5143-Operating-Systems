querys = [
    """
CREATE TABLE files (
    file_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    parent_id INTEGER,
    is_directory BOOLEAN NOT NULL,
    size INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES directories(dir_id)
);""",
    """CREATE TABLE directories (
    dir_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    parent_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES directories(dir_id) -- Self-referencing for subdirectories
);""",
    """CREATE TABLE file_contents (
    content_id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER NOT NULL,
    chunk BLOB, -- Each file's content is split into chunks for efficient storage
    chunk_index INTEGER,
    FOREIGN KEY (file_id) REFERENCES files(file_id)
);""",
    """CREATE TABLE permissions (
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
);""",
    """CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);""",
    """INSERT INTO users (username, password) VALUES
    ('bob', 'password1'),
    ('mia', 'password2'),
    ('raj', 'password3');
""",
    """INSERT INTO directories (name, parent_id, created_at, modified_at) VALUES
    ('linux', NULL, '2018-06-23 19:15:35', '2018-08-18 09:05:02'),
    ('drivers', 1, '2017-06-27 01:02:44', '2017-10-05 06:02:11'),
    ('perfctr', 2, '2021-10-19 15:58:04', '2021-11-13 10:21:53'),
    ('win2k', NULL, '2016-08-30 04:50:39', '2017-04-19 10:10:58'),
    ('shell', 4, '2020-08-13 21:18:45', '2021-07-04 22:32:53'),
    ('substrate', 4, '2020-11-18 16:16:19', '2021-03-16 15:28:57'),
    ('winpmc', NULL, '2015-10-11 05:21:17', '2017-01-30 15:14:55'),
    ('tools', 4, '2020-06-05 21:51:50', '2021-02-04 08:24:36'),
    ('papiex', 8, '2017-08-28 01:25:12', '2018-08-16 21:59:00'),
    ('src', 9, '2019-04-26 20:57:26', '2020-06-23 04:33:27'),
    ('tests', 8, '2022-11-16 14:46:10', '2023-10-07 20:57:47'),
    ('trapper', 8, '2015-02-14 20:25:29', '2016-02-06 19:51:11');
""",
    """INSERT INTO files (name, parent_id, is_directory, size, created_at, modified_at) VALUES
    ('global.c', 3, 0, 1024, '2020-02-20 10:42:37', '2021-05-26 23:26:11'),
    ('init.c', 3, 0, 2048, '2016-07-26 12:23:02', '2017-08-24 07:09:18'),
    ('virtual_stub.c', 3, 0, 4096, '2018-10-10 23:47:55', '2019-04-10 14:48:45'),
    ('x86.c', 3, 0, 512, '2018-01-15 16:15:14', '2018-11-03 06:47:49'),
    ('x86_setup.c', 3, 0, 1024, '2018-10-27 00:39:55', '2019-09-07 06:40:58'),
    ('PAPI_Errors.c', 5, 0, 2048, '2019-05-13 04:13:56', '2020-02-06 15:38:45'),
    ('StdAfx.c', 5, 0, 4096, '2016-10-24 15:45:12', '2017-01-31 02:44:03'),
    ('test_get_cycles.c', 5, 0, 8192, '2015-04-24 06:19:12', '2015-10-05 06:32:17'),
    ('winpapi_console.c', 5, 0, 1024, '2018-01-18 20:54:10', '2019-04-23 06:14:16'),
    ('WinPAPIShell.c', 5, 0, 2048, '2017-01-06 11:26:27', '2017-05-30 03:03:00'),
    ('cpuinfo.c', 6, 0, 1024, '2019-12-23 23:43:26', '2020-09-28 00:04:11'),
    ('win32.c', 6, 0, 2048, '2016-03-20 22:36:50', '2017-07-13 05:11:46'),
    ('pmclib.c', 7, 0, 1024, '2020-04-09 16:57:35', '2020-08-09 10:52:07'),
    ('pmc_x86.c', 7, 0, 2048, '2023-03-25 17:19:41', '2024-05-17 04:13:35'),
    ('WinPMC.c', 7, 0, 4096, '2016-10-28 07:42:59', '2017-11-03 16:28:42');
""",
    """INSERT INTO permissions (file_id, dir_id, user_id, read_permission, write_permission, execute_permission) VALUES
    (NULL, 1, 1, 1, 1, 1),  -- Full access to 'linux' directory
    (NULL, 2, 1, 1, 1, 1),  -- Full access to 'drivers' directory
    (4, NULL, 1, 1, 1, 0),  -- Read/write access to 'global.c'
    (5, NULL, 1, 1, 1, 0);  -- Read/write access to 'init.c'
""",
    """
INSERT INTO permissions (file_id, dir_id, user_id, read_permission, write_permission, execute_permission) VALUES
    (NULL, 4, 2, 1, 1, 1),  -- Full access to 'win2k' directory
    (NULL, 5, 2, 1, 1, 1),  -- Full access to 'shell' directory
    (12, NULL, 2, 1, 1, 0);  -- Read/write access to 'PAPI_Errors.c'
""",
    """
INSERT INTO permissions (file_id, dir_id, user_id, read_permission, write_permission, execute_permission) VALUES
    (NULL, 7, 3, 1, 1, 1),  -- Full access to 'winpmc' directory
    (44, NULL, 3, 1, 1, 0); -- Read/write access to 'pmclib.c'
""",
]
if __name__ == "__main__":
    import sqlite3

    # Connect to the SQLite database
    conn = sqlite3.connect("filesystem.db")

    # Create a cursor object
    cursor = conn.cursor()

    for query in querys:
        cursor.execute(query)

    # # Example table creation
    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS users (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         username TEXT NOT NULL,
    #         password TEXT NOT NULL
    #     )
    # ''')

    # # Prepare multiple rows of data for insertion
    # user_data = [
    #     ('bob', 'password1'),
    #     ('mia', 'password2'),
    #     ('raj', 'password3')
    # ]

    # # Use executemany to insert multiple rows in one call
    # cursor.executemany('INSERT INTO users (username, password) VALUES (?, ?)', user_data)

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()
