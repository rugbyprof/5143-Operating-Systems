# Filesystem Starter Class

from crud import SQLiteCRUD

class FileSystem:
    def __init__(self):
        db_name = "filesystem.db"
        crud = SQLiteCRUD(db_name)
        current_location = "0"


    def __buildDB(self):
        # Define table schema
        table_name = "files"
        columns = ["id INTEGER PRIMARY KEY", "name TEXT", "created TEXT", "modified TEXT", "size REAL","type TEXT","owner TEXT","group TEXT","permissions TEXT"]
        # Create table
        crud.create_table(table_name, columns)

    def __getFileId(self,**kwargs):
        """ Find a file id using current location + name
        """
        pass

    def list(self,**kwargs):
        """ List the files and folders in current directory
        """
        pass



    def chmod(self,**kwargs):
        """ Change the permissions of a file
        """
        pass
    

# Example usage:
if __name__ == "__main__":
    db_name = "my_database.db"
    crud = SQLiteCRUD(db_name)
    
    # Define table schema
    table_name = "students"
    columns = ["id INTEGER PRIMARY KEY", "name TEXT", "age INTEGER"]

    # Create table
    crud.create_table(table_name, columns)

    # Insert data
    data = (1, "Alice", 25)
    crud.insert_data(table_name, data)

    # Read data
    crud.read_data(table_name)

    # Update data
    crud.update_data(table_name, "age", 26, "name", "Alice")

    # Delete data
    crud.delete_data(table_name, "name", "Alice")

    # Close the database connection
    crud.close_connection()