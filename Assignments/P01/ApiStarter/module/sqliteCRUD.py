"""
SQLite CRUD Operations
======================
Last Updated: 5 October 2024
"""

import sqlite3
from prettytable import PrettyTable
from concurrent.futures import ThreadPoolExecutor, as_completed


class SqliteCRUD:
    """
    Comment
    """

    def __init__(self, db_path):
        """
        Initialize database connection and cursor.
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def __buildResponse(
        self, query: str, success: bool, message: str, affected: int, data: list
    ) -> dict:
        """
        Description:
            Build a response object.
        Args:
            query (str): SQL query.
            success (bool): Success status.
            message (str): Message to return.
            data (list): Query results.
        Returns:
            dict: Response object containing query, success status, message, and data.
        """
        return {
            "query": query,
            "success": success,
            "message": message,
            "affected": affected,
            "data": data,
        }

    def __runQuery(self, query, qtype="all"):
        """
        Description:
            Run a query and return the results.
        Args:
            query (str): SQL query to execute.
            qtype (str): Type of query to run (one, many, all). Defaults to 'all'.
        Returns:
            SqlResponse: Response object containing query, success status, message, and results.
        """
        affected_keys = ["UPDATE", "INSERT", "DELETE"]
        affected_rows = None
        try:
            self.cursor.execute(query)
            self.conn.commit()
            if qtype == "one":
                rows = self.cursor.fetchone()
            elif qtype == "many":
                rows = self.cursor.fetchmany()
            else:
                rows = self.cursor.fetchall()

            for key in affected_keys:
                if key in query:
                    affected_rows = self.conn.total_changes
            if not affected_rows:
                affected_rows = len(rows)

            return self.__buildResponse(query, True, f"None", int(affected_rows), rows)
        except sqlite3.Error as e:
            return self.__buildResponse(
                query, False, f"Error executing query: {e}", None, []
            )

    def run_query_in_thread(self, queries, qtype="all"):
        results = []
        # Using ThreadPoolExecutor to execute the queries in parallel
        with ThreadPoolExecutor() as executor:
            # Submit each query to be run in a separate thread
            future_to_query = {
                executor.submit(self.__runQuery, query): query for query in queries
            }

            # As each thread completes, retrieve the result
            for future in as_completed(future_to_query):
                query = future_to_query[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as exc:
                    print(f"Query {query} generated an exception: {exc}")

        return results

    def __rawResults(self, results):
        """
        Description:
            Convert raw results to a list of table names.
        Args:
            results (list): List of tuples containing query results.
        Returns:
            list: List of table names
        """
        table = []
        for row in results:
            table.append(row[0])
        return table

    def __formattedResults(self, results):
        """
        Description:
            Format results as a PrettyTable.
        Args:
            results (list): List of tuples containing query results.
        Returns:
            PrettyTable: Table object containing the formatted data.
        """
        table = PrettyTable()
        table.field_names = [desc[0] for desc in self.cursor.description]
        table.add_rows(results)
        return table

    def closeConnection(self):
        """Close the database connection."""
        self.conn.close()

    def createTable(self, table_name, columns):
        """
        Description:
            Create a new table with specified columns.
        Args:
            table_name (str): Name of the table.
            columns (list): List of column definitions.
        Returns:
            SqlResponse: Response object containing query, success status, message, and results.
        """

        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
        return self.__runQuery(query)

    def dropTable(self, table_name):
        """
        Description:
            Drop a table by name.
        Args:
            table_name (str): Name of the table to drop.
        Returns:
            SqlResponse: Response object containing query, success status, message, and results.
        """

        query = f"DROP TABLE IF EXISTS {table_name});"
        return self.__runQuery(query)

    def showTables(self, raw=True):
        """
        Description:
            Show all tables in the database.

        Args:
            raw (bool): Whether to return raw results or formatted table.
        Returns:
            list: List of table names
        """
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        results = self.cursor.fetchall()

        if not raw:
            return self.__formatted_results(results)
        else:
            return self.__raw_results(results)

    def describeTable(self, table_name, raw=False):
        """
        Description:
            Describe the structure of a table.
        Args:
            table_name (str): Name of the table.
            raw (bool): Whether to return raw data or a PrettyTable.
        Returns:
            list: List of dictionaries containing column information.
        """
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        results = self.cursor.fetchall()
        table = None

        if not raw:
            table = self.__formatted_results(results)

        else:

            table = []

            for column_info in results:
                column_name = column_info[1]
                data_type = column_info[2]
                is_nullable = "NULL" if column_info[3] == 0 else "NOT NULL"
                table.append(
                    {
                        "column_name": column_name,
                        "data_type": data_type,
                        "isnull": is_nullable,
                    }
                )
                # print(f"Column Name: {column_name}, Data Type: {data_type}, Nullable: {is_nullable}")

        return table

    def insertData(self, table_name, data):
        """
        Description:
            Insert data into a table.
        Args:
            table_name (str): Name of the table.
            data (tuple): Data to insert.
        Returns:
            SqlResponse: Response object containing query, success status, message, and results.
        """
        # Insert data into the table
        placeholders = ", ".join(["?"] * len(data))
        query = f"INSERT INTO {table_name} VALUES ({placeholders});"
        return self.__runQuery(query)

    def readData(self, table_name):
        """
        Description:
            Read data from a table.
        Args:
            table_name (str): Name of the table.
        Returns:
            SqlResponse: Response object containing query, success status, message, and results.
        """
        # Retrieve all data from the table
        query = f'SELECT * FROM "{table_name}";'
        return self.__runQuery(query)

    def updateData(self, table_name, target, new_value, where_column, where_value):
        """
        Description:
            Update data in a table based on a condition.
        Args:
            table_name (str): Name of the table.
            column (str): Column to update.
            new_value (str): New value to set.
            condition_column (str): Column to use in the WHERE clause.
            condition_value (str): Value to use in the WHERE clause.
        Returns:
            SqlResponse: Response object containing query, success status, message, and results.
        """
        query = f'UPDATE "{table_name}" SET {target} = "{new_value}" WHERE "{where_column}" = "{where_value}";'
        return self.__runQuery(query)

    def deleteData(self, table_name, condition_column, condition_value):
        """
        Description:
            Delete data from a table based on a single condition.
        Args:
            table_name (str): Name of the table.
            condition_column (str): Column to use in the WHERE clause.
            condition_value (str): Value to use in the WHERE clause.
        Returns:
            SqlResponse: Response object containing query, success status, message, and results.
        """
        query = f'DELETE FROM "{table_name}" WHERE "{condition_column}" = "{condition_value}";'
        return self.__runQuery(query)

    def formattedPrint(self, table_name):
        """
        Description:
            Print the contents of a table in a formatted manner.
        Args:
            table_name (str): Name of the table.
        Returns:
            PrettyTable: Table object containing the formatted data.
        """
        self.cursor.execute(f"SELECT * FROM {table_name};")
        table_info = self.cursor.fetchall()

        table_info_list = []

        table = PrettyTable()
        table.field_names = [desc[0] for desc in self.cursor.description]
        table.add_rows(table_info)

        return table

    def readFileData(self, table_name, file_id):
        """
        Description:
            Read file contents from a file contents table.
        Args:
            table_name (str): Name of the table.
            file_id (str): ID of the file.
        Returns:
            SqlResponse: Response object containing query, success status, message, and results.
        """
        query = f"SELECT chunk FROM {table_name} WHERE file_id = '{file_id}' ORDER BY 'chunk_index';"
        return self.__runQuery(query)

    def tableExists(self, table_name):
        """
        Description:
            Check if a table exists.
        Args:
            table_name (str): Name of the table.
        Returns:

        """
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        return self.__runQuery(query, "one")

    def dropTable(self, table_name):
        """
        Description:
            Drop a table by its name.
        Args:
            table_name (str): Name of the table to drop.
        Returns:
            SqlResponse: Response object containing query, success status, message, and results.
        """

        # Drop the table if it exists
        query = f"DROP TABLE IF EXISTS {table_name};"
        return self.__runQuery(query)

    def runQuery(self, query):
        """
        Description:
            Test a query.
        Args:
            query (str): SQL query to test.
        Returns:
            SqlResponse: Response object containing query, success status, message, and results.
        """
        return self.__runQuery(query)


# Example usage:
if __name__ == "__main__":

    db_name = "../data/filesystem.db"
    conn = SqliteCRUD(db_name)

    # res = conn.readFileData("file_contents", "13")

    # data = res["data"]
    # del res["data"]

    # print(res)

    # res = conn.readData("files")
    # print(res)

    # res = conn.updateData("files", "modified_at", CURRENT_TIMESTAMP, "file_id", "13")
    # print(res)

    res = conn.runQuery(
        'UPDATE "files" SET "created_at" = CURRENT_TIMESTAMP WHERE "file_id" = "16";'
    )
    print(res)

    # # Define table schema
    # table_name = "students"
    # columns = ["id TEXT", "name TEXT", "age INTEGER"]

    # # # Create table
    # conn.create_table(table_name, columns)

    # # Insert data
    # data = ("1", "Alice", 25)
    # conn.insert_data(table_name, data)

    # data = ("2", "Bob", 23)
    # conn.insert_data(table_name, data)

    # data = ("3", "Charlie", 11)
    # conn.insert_data(table_name, data)

    # # Read data
    # conn.read_data(table_name)

    # # Update data
    # conn.update_data(table_name, "age", 26, "name", "Alice")

    # # Delete data
    # conn.delete_data(table_name, "name", "Alice")

    # Close the database connection
    conn.closeConnection()
