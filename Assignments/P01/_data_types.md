## Sqlite - Data Types
#### None

SQLite supports a variety of column types that you can use to define the structure of your database tables. Here's a list of the most commonly used column types in SQLite:

### Available
1. **INTEGER**: Used for whole numbers (integers). You can specify the number of bytes, but SQLite will adjust storage as needed.
2. **REAL**: Used for floating-point numbers. It can store both integers and decimal numbers.
3. **TEXT**: Used for storing text, strings, or character data.
4. **BLOB**: Binary Large Object. This column type is used for storing binary data, such as images, documents, or other binary files.
5. **NULL**: Represents a column that can contain a NULL value, which means it has no value or is unknown.
6. **NUMERIC**: This is a general-purpose numeric data type that can store various types of numbers, including integers and decimals. It is not recommended for most use cases because it can lead to unexpected behavior.

### Not Available

These are typical data types found in other DB systems. Although these aren't available you can use one the above types and some functions to replicate what you need.

7. **~~BOOLEAN~~**: SQLite does not have a native boolean data type, but you can use `INTEGER` or `NUMERIC` columns to represent boolean values. Typically, 0 is used to represent false, and 1 is used to represent true.
8. **~~DATE~~**: SQLite does not have a native date type, but you can use `TEXT` or `INTEGER` columns to store dates and times in a specific format or as Unix timestamps.
9.  **~~DATETIME~~**: Similar to the date, you can use `TEXT` or `INTEGER` columns to store date and time information. You'll need to manage the formatting and parsing yourself.
10. **~~TIMESTAMP~~**: Often used to store Unix timestamps (the number of seconds since January 1, 1970). See [THIS](timestamps.md) for more info. 

Remember that SQLite is a dynamically typed database system, which means it is quite flexible with data types. You can often store different types of data in the same column. However, it's good practice to use the appropriate data type for each column to ensure data integrity and facilitate queries.