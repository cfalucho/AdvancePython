# create the SQLite DB connections

import sqlite3
import re
import numpy as np




class QueryBuilder:
    def __init__(self, file_name, **data):
        self.table_name = file_name
        self.columns = list(data.keys())

        self.column_name = ",".join(f"{column}" for column in self.columns)
        # print(self.column_name)

        col_len = len(self.columns)
        self.placeholders = ",".join("?" * col_len)

        self.dispatch = {
            "SELECT": self.build_select,
            "INSERT": self.build_insert,
            "UPDATE": self.build_update,
            "DELETE": self.build_delete,
            "DROP"  : self.drop_table


        }

    def dispatcher(self, query_type, **kwargs):
        if query_type in self.dispatch:
            result = self.dispatch[query_type](**kwargs)
            # print(result)
            return self.dispatch[query_type](**kwargs)
        return None

    def build_select(self):
        return f"""
            SELECT * FROM {self.table_name}
        """

    def build_insert(self, data):
        cols_name = ", ".join(f"{cols_n}" for cols_n in data.keys())
        values = tuple(data.values())

        sql_insert = f"""
            INSERT INTO {self.table_name}({cols_name})
            VALUES ({self.placeholders})
        """
        return sql_insert, values

    def build_update(self, data, where):
        set_column_value = ",".join(f"{col_n} = '{value}'" for col_n, value in data.items())
        # print(set_column_value)

        # print(len(data.items()))
        # print(len(where.items()))

        where_condition = ",".join(f"{k} = '{v}'" for k, v in where.items())
        # print(where_condition)

        sql_update = f"""
            UPDATE {self.table_name} 
            SET {set_column_value}
            WHERE {where_condition}
        """

        return sql_update

    def build_delete(self, where):
        placeholder = "".join(f"{k} =" for k in where.keys())
        value = tuple(where.values())
        sql_delete = f"""
            DELETE FROM {self.table_name} WHERE {placeholder} ?
        """
        return sql_delete, value

    def drop_table(self):
        sql_drop = f"""DROP Table {self.table_name}"""
        print("Dropping Table Successful...")
        return sql_drop

    # CREATE TABLE
    def create_table(self):
        table_name = self.table_name
        # Used to create table
        column_name = ",".join(f"{column} TEXT" for column in self.columns)
        create_table_query = f"""CREATE TABLE IF NOT EXISTS {table_name}({column_name})"""
        print("Table created successfully.")
        return create_table_query


class CommandExecutor:
    def __init__(self, db_file):
        self.db = db_file
        self.conn = None
        self.cursor = None



    # Create connection to Database
    def create_connection(self):
        self.conn = sqlite3.connect(self.db)
        print(f"Successfully connected to {self.db}...")

    # Create Cursor Object to interact with the Database
    def create_cursor(self):
        self.cursor = self.conn.cursor()
        print("Creating a Cursor object..")
        return self.cursor

    # def execute(self, query):
    #     return self.cursor.execute(query)

    def commit(self):
        return self.conn.commit()

    def close_connection(self):
        print(f"Closing {self.db}....")
        return self.conn.close()





