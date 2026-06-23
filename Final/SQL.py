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
    def __init__(self, table_name=None, qb=None):
        self._table_name = table_name
        self._qb = qb
        self.conn = None

        self.exec_dispatch = {
            "CREATE": self._execute_create,
            "SELECT": self._execute_select,
            "UPDATE": self._execute_update,
            "INSERT": self._execute_insert,
            "DELETE": self._execute_delete,
            "DROP"  : self._execute_drop,
        }



    def connect(self, name=None):
        db_to_open = name
        if not db_to_open:
            raise ValueError("No database file specified.")
        self.conn = sqlite3.connect(db_to_open)

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def execute(self, command_type, **kwargs):
        cmd_upper = command_type.upper()
        if cmd_upper in self.exec_dispatch:
            return self.exec_dispatch[cmd_upper](**kwargs)
        return f"Command '{command_type}' is not a recognized or supported operation."

    def _execute_create(self, **kwargs):
        table_name = kwargs.get("table_name", self._table_name)
        row = kwargs.get("row", [])

        if not self.conn:
            self.connect()

        try:
            cursor = self.conn.cursor()
            cols_list = list(row)
            sql_create_table, cols_header = self._qb.create_table(table_name, cols_list)

            cursor.execute(sql_create_table)
            self.conn.commit()
            return f"Table '{table_name}' created successfully."
        except sqlite3.Error as e:
            return f"Database error: {e}"

    def _execute_select(self, **kwargs):
        table_name = kwargs.get("table_name", self._table_name)

        if not self.conn:
            self.connect()

        try:
            cursor = self.conn.cursor()
            sql_select = self._qb.build_select(table_name)
            cursor.execute(sql_select)
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            return f"Database error: {e}"

    def _execute_insert(self, **kwargs):
        table_name = kwargs.get("table_name", self._table_name)
        row = kwargs.get("row")

        if not self.conn:
            self.connect()

        try:
            cursor = self.conn.cursor()
            sql_insert, values = self._qb.build_insert(table_name, row)
            cursor.execute(sql_insert, values)
            self.conn.commit()
            return "Insert successful."
        except sqlite3.Error as e:
            return f"Database error: {e}"

    def _execute_update(self, **kwargs):
        table_name = kwargs.get("table_name", self._table_name)
        cols = kwargs.get("cols")
        where = kwargs.get("where")

        if not self.conn:
            self.connect()

        try:
            cursor = self.conn.cursor()
            sql_update = self._qb.build_update(table_name, cols, where)
            cursor.execute(sql_update)
            self.conn.commit()
            return f"Table '{table_name}' updated."
        except sqlite3.Error as e:
            return f"Database error: {e}"

    def _execute_delete(self, **kwargs):
        table_name = kwargs.get("table_name", self._table_name)
        where = kwargs.get("where")

        if not self.conn:
            self.connect()

        try:
            cursor = self.conn.cursor()
            sql_delete, delete_item = self._qb.build_delete(table_name, where)
            cursor.execute(sql_delete, delete_item)
            self.conn.commit()
            return "Deletion successful."
        except sqlite3.Error as e:
            return f"Database error: {e}"

    def _execute_drop(self, **kwargs):
        table_name = kwargs.get("table_name", self._table_name)

        if not self.conn:
            self.connect()

        try:
            cursor = self.conn.cursor()
            sql_drop = self._qb.drop_table(table_name)
            cursor.execute(sql_drop)
            self.conn.commit()
            return f"Table '{table_name}' dropped successfully."
        except sqlite3.Error as e:
            return f"Database error: {e}"

    # Getters
    def get_table_name(self):
        return self._table_name

    def get_qb(self):
        return self._qb





