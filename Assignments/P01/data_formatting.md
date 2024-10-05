## Data Formatting

- This formatting is "how it prints to the terminal (screen). Basically how people see it.
- Here are some common methods to display database information using some known libraries.

1. **Pretty-Printed Tabular Output**: You can use libraries like `prettytable` or `tabulate` to format query results into a visually appealing tabular format. These libraries make it easy to display rows and columns in a structured way.

Example with `prettytable`:

```python
from prettytable import PrettyTable
import sqlite3

conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM your_table")
rows = cursor.fetchall()

table = PrettyTable()
table.field_names = [desc[0] for desc in cursor.description]
table.add_rows(rows)

print(table)
```

2. **Custom Formatting**: You can manually format the query results using Python's string formatting capabilities. This allows you to have full control over the display format.

Example:

```python
conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM your_table")
rows = cursor.fetchall()

for row in rows:
      print(f"ID: {row[0]}, Name: {row[1]}, ...")
```

3. **JSON or CSV Export**: If you want to export data for further analysis or reporting, you can query the data and export it as JSON or CSV. Python has built-in support for both formats.

Example for CSV:

```python
import csv
import sqlite3

conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM your_table")
rows = cursor.fetchall()

with open('output.csv', 'w', newline='') as csvfile:
      csvwriter = csv.writer(csvfile)
      csvwriter.writerow([desc[0] for desc in cursor.description])
      csvwriter.writerows(rows)
```

4. **Interactive Displays**: If you're working in a Jupyter Notebook or an environment that supports rich interactive displays, you can use libraries like `pandas` to display dataframes interactively.

Example with `pandas`:

```python
import pandas as pd
import sqlite3

conn = sqlite3.connect('your_database.db')

df = pd.read_sql_query("SELECT * FROM your_table", conn)
df
```

The best method for displaying database information in SQLite using Python depends on your specific use case, whether you need interactive displays, further data processing, or simply a visually appealing tabular format. You can choose the method that best suits your needs and the environment in which you're working.

In SQLite, you can achieve similar functionality to `SHOW TABLES` and `DESCRIBE` commands, but they are not standard SQL commands like in some other database systems. SQLite provides alternative commands and queries to retrieve information about tables and their structure.

1. **List Tables**: To list all the tables in the current database, you can query the `sqlite_master` table, which contains metadata about database objects. Here's an example:

```python
import sqlite3

conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table in tables:
      print(table[0])
```

This query retrieves the names of all tables in the database.

2. **Describe Table**: To describe the structure of a specific table, you can query the `PRAGMA table_info(table_name)` statement. Here's an example:

```python
import sqlite3

conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(your_table_name);")
table_info = cursor.fetchall()

for column_info in table_info:
      column_name = column_info[1]
      data_type = column_info[2]
      is_nullable = "NULL" if column_info[3] == 0 else "NOT NULL"
      print(f"Column Name: {column_name}, Data Type: {data_type}, Nullable: {is_nullable}")
```

This query retrieves information about columns in the specified table, including their names, data types, and nullability.

These are the SQLite-specific commands you can use to achieve functionality similar to `SHOW TABLES` and `DESCRIBE` in other databases. They allow you to list tables and describe the structure of a specific table in an SQLite database.
