# create the SQLite DB connections

import sqlite3


class QueryBuilder:
    def __init__(self, table_name, columns):
        """
            CREATE TABLE IF NOT EXITS table (
                Presidency TEXT, 
                President TEXT, 
                Wikipedia Entry TEXT, 
                Took office TEXT, 
                Left office TEXT, 
                Party TEXT,
            )
        """
        sql_columns = ", ".join(f"{col} TEXT" for col in columns)
        print(sql_columns)

        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name}({sql_columns})
        """

        print("Tables created successfully.")

class CommandExecutor:
    def __init__(self, db_file):
        self.db = db_file
        self.conn = sqlite3.connect(self.db)
        print(f"Successfully connected to {self.db}.")
        print(f"Creating cursor object...")
        self.cursor = self.conn.cursor()


    def execute(self):
        return self.cursor

    def close_connection(self):
        print(f"Closing {self.db}....")
        return self.conn.close()




