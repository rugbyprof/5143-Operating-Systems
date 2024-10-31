import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect("filesystem.db")

# Set the row factory to sqlite3.Row
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Execute your query
cursor.execute(
    "SELECT 'id', 'pid', 'oid', 'name', 'size', 'creation_date', 'modified_date' FROM files"
)

# Fetch all rows
rows = cursor.fetchall()

# Convert each row to a dictionary
results = [dict(row) for row in rows]

# Print the formatted results
for result in results:
    print(result)
