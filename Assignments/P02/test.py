import sqlite3
from sqliteCRUD import SQLiteCRUD


# # sql = SQLiteCRUD()

# import sqlite3




# # Connect to the SQLite database (assuming the database file is named 'filesystem.db')
# conn = sqlite3.connect('filesystem.sqlite')
# cursor = conn.cursor()


# cursor.execute("""
# CREATE TABLE FileSystem2 (
#     id INTEGER PRIMARY KEY,
#     pid INTEGER NOT NULL,
#     filename TEXT NOT NULL,
#     file_type TEXT NOT NULL,
#     file_size INTEGER,
#     owner TEXT NOT NULL,
#     group_name TEXT NOT NULL,
#     permissions TEXT NOT NULL,
#     modification_time DATETIME,
#     content BLOB,
#     hidden NUMBER 
# );
# """)

# # Inserting data into the FileSystem2 table
# cursor.execute("""
#     INSERT INTO FileSystem2 (pid, filename, file_type, file_size, owner, group_name, permissions, modification_time, content, hidden)
#     VALUES (0, 'root', 'directory', NULL, 'root', 'admin', 'rwxr-xr-x', '2023-09-22 12:00:00', NULL, 0)
# """)

# cursor.execute("""
#     INSERT INTO FileSystem2 (pid, filename, file_type, file_size, owner, group_name, permissions, modification_time, content, hidden)
#     VALUES (1, 'home', 'directory', NULL, 'root', 'admin', 'rwxr-xr-x', '2023-09-22 12:00:00', NULL, 0)
# """)

# cursor.execute("""
#     INSERT INTO FileSystem2 (pid, filename, file_type, file_size, owner, group_name, permissions, modification_time, content, hidden)
#     VALUES (2, 'user1', 'directory', NULL, 'user1', 'users', 'rwxr-xr-x', '2023-09-22 12:00:00', NULL, 0)
# """)

# cursor.execute("""
#     INSERT INTO FileSystem2 (pid, filename, file_type, file_size, owner, group_name, permissions, modification_time, content, hidden)
#     VALUES (2, 'user2', 'directory', NULL, 'user2', 'users', 'rwxr-xr-x', '2023-09-22 12:00:00', NULL, 0)
# """)

# cursor.execute("""
#     INSERT INTO FileSystem2 (pid, filename, file_type, file_size, owner, group_name, permissions, modification_time, content, hidden)
#     VALUES (1, 'docs', 'directory', NULL, 'user1', 'users', 'rwxr-xr-x', '2023-09-22 12:00:00', NULL, 0)
# """)

# cursor.execute("""
#     INSERT INTO FileSystem2 (pid, filename, file_type, file_size, owner, group_name, permissions, modification_time, content, hidden)
#     VALUES (1, 'pictures', 'directory', NULL, 'user2', 'users', 'rwxr-xr-x', '2023-09-22 12:00:00', NULL, 0)
# """)

# # Commit the changes and close the connection
# conn.commit()
# conn.close()


if __name__ == "__main__":
    crud = SQLiteCRUD("filesystem.sqlite")
    
    tables = crud.show_tables(True)
    print(tables)
    
    table = crud.describe_table("FileSystem2",True)
    print(table)