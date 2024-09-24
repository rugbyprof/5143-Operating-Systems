## Sqlite - Timestamp functions
#### None


SQLite does not have a dedicated `TIMESTAMP` data type like some other database systems. Instead, it allows you to work with dates and times using other data types, such as `TEXT` or `INTEGER`, and provides several date and time functions to manipulate and query these values.

Here are some of the commonly used SQLite date and time functions:

1. **CURRENT_TIMESTAMP**: This function returns the current date and time in the default format (`YYYY-MM-DD HH:MM:SS`).

   Example:
   ```sql
   SELECT CURRENT_TIMESTAMP;
   ```

2. **DATE**: This function extracts the date portion from a `DATETIME` or `TEXT` value.

   Example:
   ```sql
   SELECT DATE('2023-09-13 15:30:00');
   ```

3. **TIME**: This function extracts the time portion from a `DATETIME` or `TEXT` value.

   Example:
   ```sql
   SELECT TIME('2023-09-13 15:30:00');
   ```

4. **strftime**: This function is a powerful tool for formatting date and time values. It allows you to format dates and times in various ways.

   Example:
   ```sql
   SELECT strftime('%Y-%m-%d %H:%M:%S', 'now');
   ```

5. **julianday**: This function returns the Julian day number for a given date or time.

   Example:
   ```sql
   SELECT julianday('2023-09-13');
   ```

6. **datetime**: This function can be used to create a `DATETIME` value from separate date and time components.

   Example:
   ```sql
   SELECT datetime('2023-09-13', '15:30:00');
   ```

7. **unixepoch**: This function can be used to convert Unix timestamps (seconds since January 1, 1970) to a `DATETIME` value.

   Example:
   ```sql
   SELECT datetime(1631527800, 'unixepoch');
   ```

These functions can be quite handy for working with date and time values in SQLite, even though there isn't a dedicated `TIMESTAMP` data type. You can use them to format, extract, and manipulate date and time information as needed in your queries.