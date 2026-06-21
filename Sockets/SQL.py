import sqlite3
class QueryBuilder:
    def __init__(self, dataframe):
        self.table_name = dataframe.get_table_name()
        # self.columns = list(data.keys())
        # self.column_name = ",".join(f"{column}" for column in self.columns)

        self.dispatch = {
            "CREATE": self.create_table,
            "SELECT": self.build_select,
            "INSERT": self.build_insert,
            "UPDATE": self.build_update,
            "DELETE": self.build_delete,
            "DROP"  : self.drop_table
        }

    def dispatcher(self, query_type, **kwargs):
        if query_type in self.dispatch:
            return query_type, self.dispatch[query_type](**kwargs)
        return None

    def build_select(self):
        print("Inside the BUILD SELECT SQL STATEMENT....")

        sql_select = f"SELECT * FROM {self.table_name}"
        return sql_select


    def build_insert(self, **kwargs):
        table_name = kwargs.get("table_name")
        columns = kwargs.get('columns', [])
        placeholders = ",".join("?" * len(columns))
        sql_insert = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"
        return sql_insert

    def build_update(self, **kwargs):
        table_name = kwargs.get("table_name")
        value = kwargs.get("values")
        columns = kwargs.get("columns")
        where = kwargs.get("where")

        result = dict(zip(columns, value))
        print(result)

        set_col_val = ", ".join(f"{col} = '{val}'" for col, val in result.items())

        where_condition = " AND ".join(f"{k} = '{v}'" for k, v in where.items())

        sql_update = f"""UPDATE {table_name} SET {set_col_val} WHERE {where_condition}"""

        return sql_update

    def build_delete(self, **kwargs):
        print("Inside the DELETE SELECT SQL STATEMENT....")

        table_name = kwargs.get("table_name")
        where = kwargs.get("where")
        placeholder = "".join(f"{k} =" for k in where.keys())
        value = tuple(where.values())
        # print(value)

        sql_delete = f"""DELETE FROM {table_name} WHERE {placeholder} ?
        """
        return sql_delete, value

    def drop_table(self, **kwargs):
        table_name = kwargs.get("table_name")
        print("Inside the DROP SQL STATEMENT....")
        sql_drop = f"""DROP Table {self.table_name}"""
        return sql_drop

    # CREATE TABLE
    def create_table(self, **kwargs):
        print("Creating a table...")
        table_name = kwargs.get("table_name", "default")
        columns = kwargs.get('columns', [])


        column_header = columns
        cols_unique = f"{columns[0]} TEXT UNIQUE,"
        print(cols_unique)
        column_name = ",".join(f"{column} TEXT" for column in columns[1:])
        cols_header = cols_unique + column_name

        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name}({cols_header})"
        return create_table_query

    def get_dispatch_keys(self):
        return self.dispatch.keys()

# HELPER FUNCTIONS
import re
def parse_table_name(filename):
    # remove .csv extension and use the file name for table name
    match = re.search(r"^(.+)\.csv$", filename)
    if match:
        name_only = match.group(1)
        return name_only
    return None


class CommandExecutor:
    def __init__(self):
        # self._database_file = dataframe.get_db_filename()
        # self._table_name = dataframe.get_table_name()
        # self._qb = QueryBuilder()
        self.conn = None


        self.exec_dispatch = {
            "CREATE": self._execute_create,
            "SELECT": self._execute_select,
            "UPDATE": self._execute_update,
            "INSERT": self._execute_insert,
            "DELETE": self._execute_delete,
            "DROP"  : self._execute_drop,
        }

    def cursor(self):
        return self.conn.cursor()

    def execute(self, sql_query, **kwargs):

        if sql_query.upper() in self.exec_dispatch:
            return self.exec_dispatch[sql_query.upper()](**kwargs)
        return f"{sql_query} not part of the list."


    def _execute_create(self):
        return f"Table Created in DB"
        # try:
        #     # self.conn = sqlite3.connect(self._database_file)
        #     # print("Database connected..")
        #     cols_list = list(row)
        #     # cursor = self.conn.cursor()
        #     sql_create_table, cols_header = self._qb.create_table(table_name, cols_list)
        #     # cursor.execute(sql_create_table)
        #     self.conn.commit()
        # except ConnectionError as e:
        #     return f"{e}."
        # finally:
        #     if self.conn:
        #         self.conn.close()
        #         print("Database connection closed.")
        return sql_create_table, cols_header


    def _execute_select(self):
        # print("Performing a SELECT query...")

        # try:
        #     # self.conn = sqlite3.connect(self._database_file)
        #     # print("Database connected..")
        #     # cursor = self.conn.cursor()
        #     sql_select = self._qb.build_select(table_name)
        #     # cursor.execute(sql_select)
        #     # rows = cursor.fetchall()
        #     self.conn.commit()
        # except ConnectionError as e:
        #     return f"{e}."
        # finally:
        #     if self.conn:
        #         self.conn.close()
        #         print("Database connection closed.")
        return "SELECT from DB"



    def _execute_insert(self):
        # # print("Performing an Insert Query...")
        # try:
        #     self.conn = sqlite3.connect(self._database_file)
        #     cursor = self.conn.cursor()
        #     sql_insert, values = self._qb.build_insert(table_name, row)
        #     cursor.execute(sql_insert, values)
        #     self.conn.commit()
        # except ConnectionError as e:
        #     return f"{e}."
        # finally:
        #     if self.conn:
        #         self.conn.close()
        #         # print("Database connection closed.")
        return f"INSERT TO DB"



    def _execute_update(self):
        # print(f"Updating {table_name} table.")
        #
        # try:
        #     self.conn = sqlite3.connect(self._database_file)
        #     cursor = self.conn.cursor()
        #     sql_update = self._qb.build_update(table_name, cols, where)
        #     print(sql_update)
        #     cursor.execute(sql_update)
        #     self.conn.commit()
        # except ConnectionError as e:
        #     print(f"{e}.")
        # finally:
        #     if self.conn:
        #         self.conn.close()
        #         print("Database connection closed.")
        return f"UPDATED DB"



    def _execute_delete(self, ):
        return f"Deleting from DB"
        # try:
        #     self.conn = sqlite3.connect(self._database_file)
        #     cursor = self.conn.cursor()
        #     sql_delete, delete_item = self._qb.build_delete(table_name, where)
        #     cursor.execute(sql_delete, delete_item)
        #     self.conn.commit()
        # except ConnectionError as e:
        #     print(f"{e}.")
        # finally:
        #     if self.conn:
        #         self.conn.close()
        #         print("Database connection closed.")


    def _execute_drop(self):
        return f"DROP from Database..."

        # try:
        #     self.conn = sqlite3.connect(self._database_file)
        #     cursor = self.conn.cursor()
        #     sql_drop = self._qb.drop_table(table_name)
        #     cursor.execute(sql_drop)
        #     self.conn.commit()
        # except ConnectionError as e:
        #     print(f"{e}.")
        # finally:
        #     if self.conn:
        #         self.conn.close()
        #         print("Database connection closed.")


        # print("Closing the db connection.")
        # self.conn.close()

    def get_table_name(self):
        return self._table_name

    def get_qb(self):
        return self._qb






