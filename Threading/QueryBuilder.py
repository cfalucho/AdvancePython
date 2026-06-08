class QueryBuilder:
    def __init__(self):
        # self.table_name = ""
        # self.columns = list(data.keys())
        # self.column_name = ",".join(f"{column}" for column in self.columns)

        self.dispatch = {
            "SELECT": self.build_select,
            "INSERT": self.build_insert,
            "UPDATE": self.build_update,
            "DELETE": self.build_delete,
            "DROP"  : self.drop_table
        }

    def dispatcher(self, query_type, **kwargs):
        if query_type in self.dispatch:
            return self.dispatch[query_type](**kwargs)
        return None

    def build_select(self, table_name):
        print("Inside the BUILD SELECT SQL STATEMENT....")

        sql_select = f"""
                SELECT * FROM {table_name}
        """
        return sql_select


    def build_insert(self, table_name, row):
        print(row)
        cols_name = ", ".join(f"{cols_n}" for cols_n in row.keys())
        cols_len = len(row.keys())
        values = tuple(row.values())
        print(values)

        placeholders = ",".join("?" * cols_len)
        sql_insert = f"""
            INSERT INTO {table_name}({cols_name})
            VALUES ({placeholders})
        """

        return sql_insert, values

    def build_update(self, table_name, cols, where):

        set_col_val = ", ".join(f"{column} = '{value}'"for column, value in cols.items())
        where_condition = ",".join(f"{k} = '{v}'" for k, v in where.items())
        # print(where_condition)

        sql_update = f"""
            UPDATE {table_name}
            SET {set_col_val}
            WHERE {where_condition}
        """

        return sql_update

    def build_delete(self, table_name, where):
        print("Inside the DELETE SELECT SQL STATEMENT....")

        placeholder = "".join(f"{k} =" for k in where.keys())
        value = tuple(where.values())
        print(value)

        sql_delete = f"""
            DELETE FROM {table_name} WHERE {placeholder} ?
        """
        return sql_delete, value

    def drop_table(self, table_name):
        print("Inside the DROP SQL STATEMENT....")
        sql_drop = f"""DROP Table {table_name}"""
        return sql_drop

    # CREATE TABLE
    def create_table(self, table_name, columns):
        print("Creating a table...")

        column_header = columns
        cols_unique = f"{columns[0]} TEXT UNIQUE,"
        print(cols_unique)
        column_name = ",".join(f"{column} TEXT" for column in columns[1:])
        cols_header = cols_unique + column_name

        create_table_query = f"""CREATE TABLE IF NOT EXISTS {table_name}({cols_header})"""
        print("Table created successfully.")
        print(create_table_query )
        return create_table_query, column_header