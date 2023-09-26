# Crud Class for Sqlite

import sqlite3
from prettytable import PrettyTable
   
class SQLiteCRUD:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def __raw_results(self,results):
        table = []
        for row in results:
            table.append(row[0])
        return table     

    def __formatted_results(self,results):
        table = PrettyTable()
        table.field_names = [desc[0] for desc in self.cursor.description]
        table.add_rows(results)
        return table

    def create_table(self, table_name, columns):
        """
        Params:
            table_name (str) - name of table
            columns (list) - ["id INTEGER PRIMARY KEY", "name TEXT", "created TEXT", "modified TEXT", "size REAL","type TEXT","owner TEXT","owner_group TEXT","permissions TEXT"]
        """
        try:
            # Create a table with the given columns
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print(f"Table '{table_name}' created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
            
    def drop_table(self, table_name):
        """
        Params:
            table_name (str) - name of table
            columns (list) - ["id INTEGER PRIMARY KEY", "name TEXT", "created TEXT", "modified TEXT", "size REAL","type TEXT","owner TEXT","owner_group TEXT","permissions TEXT"]
        """
        try:
            # Create a table with the given columns
            create_table_query = f"DROP TABLE IF EXISTS {table_name});"
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print(f"Dropped '{table_name} successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
            

    def show_tables(self,raw=True):

        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        results = self.cursor.fetchall()

        if not raw: 
            return self.__formatted_results(results)
        else:
            return self.__raw_results(results)


    def describe_table(self,table_name,raw=False):
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        results = self.cursor.fetchall()
        table = None
        
        if not raw:
            table = self.__formatted_results(results)
           
        else:
        
            table= []

            for column_info in results:
                column_name = column_info[1]
                data_type = column_info[2]
                is_nullable = "NULL" if column_info[3] == 0 else "NOT NULL"
                table.append({"column_name":column_name,"data_type":data_type,"isnull":is_nullable})
                #print(f"Column Name: {column_name}, Data Type: {data_type}, Nullable: {is_nullable}")
                
        return table
        
            
    def insert_data(self, table_name, data):
        try:
            # Insert data into the table
            placeholders = ', '.join(['?'] * len(data))
            insert_query = f"INSERT INTO {table_name} VALUES ({placeholders});"
            self.cursor.execute(insert_query, data)
            self.conn.commit()
            print("Data inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")

    def read_data(self, table_name):
        try:
            # Retrieve all data from the table
            select_query = f"SELECT * FROM {table_name};"
            self.cursor.execute(select_query)
            result = self.cursor.fetchall()
            if result:
                for row in result:
                    print(row)
            else:
                print("No data found in the table.")
        except sqlite3.Error as e:
            print(f"Error reading data: {e}")

    def update_data(self, table_name, column, new_value, condition_column, condition_value):
        try:
            # Update data in the table based on a condition
            update_query = f"UPDATE {table_name} SET {column} = ? WHERE {condition_column} = ?;"
            self.cursor.execute(update_query, (new_value, condition_value))
            self.conn.commit()
            print("Data updated successfully.")
        except sqlite3.Error as e:
            print(f"Error updating data: {e}")

    def delete_data(self, table_name, condition_column, condition_value):
        try:
            # Delete data from the table based on a condition
            delete_query = f"DELETE FROM {table_name} WHERE {condition_column} = ?;"
            self.cursor.execute(delete_query, (condition_value,))
            self.conn.commit()
            print("Data deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")

    def close_connection(self):
        self.conn.close()
        print("Database connection closed.")
        
        
    def formatted_print(self,table_name):
        self.cursor.execute(f"SELECT * FROM {table_name};")
        table_info = self.cursor.fetchall()
        
        table_info_list = []

        table = PrettyTable()
        table.field_names = [desc[0] for desc in self.cursor.description]
        table.add_rows(table_info)

        return table

    def table_exists(self, table_name,db_path=None):
        different_conn = False
        if not db_path:
            db_path = self.db_path
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
        else:
            different_conn = True
            conn = self.conn
            cursor = self.conn.cursor()
            
        try:

            # Query the sqlite_master table to check if the table exists
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
            result = cursor.fetchone()

            # If result is not None, the table exists
            return result is not None

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False

        finally:
            if different_conn:
                conn.close()



    def drop_table(self,table_name):
        try:

            # Drop the table if it exists
            self.cursor.execute(f"DROP TABLE IF EXISTS {table_name};")

            # Commit the changes
            self.conn.commit()
            return True

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False


# Example usage:
if __name__ == "__main__":

    conn = SQLiteCRUD("database.sqlite")
    
    print(conn.table_exists("FileSystem2"))  
    print(conn.show_tables(raw=False))


    table_name = "files"
    columns = ["id INTEGER PRIMARY KEY", "name TEXT", "created TEXT", "modified TEXT", "size REAL","type TEXT","owner TEXT","owner_group TEXT","permissions TEXT"]
    # Create table
    conn.create_table(table_name, columns)

    print(conn.show_tables(raw=False))


    # crud = SQLiteCRUD("filesystem.sqlite")
    
    # tables = crud.show_tables(True)
    # print(tables)
    
    # table = crud.describe_table("FileSystem2",True)
    # print(table)




    # db_name = "my_database.sqlite"
    # crud = SQLiteCRUD(db_name)
    
    # # Define table schema
    # table_name = "students2"   
    # columns = ["id TEXT", "name TEXT", "age INTEGER"]

    # # # Create table
    # crud.create_table(table_name, columns)

    # # Insert data
    # data = (generate_uuid(), "Alice", 25)
    # crud.insert_data(table_name, data)
    
    # data = (generate_uuid(),"Bob", 23)
    # crud.insert_data(table_name, data)
    
    # data = (generate_uuid(),"Charlie", 11)
    # crud.insert_data(table_name, data)

    # # Read data
    # crud.read_data(table_name)

    # # Update data
    # crud.update_data(table_name, "age", 26, "name", "Alice")

    # # Delete data
    # crud.delete_data(table_name, "name", "Alice")

    # Close the database connection
    # crud.close_connection()

    # need the id parent folder 

    # SELECT SUM(file_size) FROM filesystem
    # WHERE pid = id