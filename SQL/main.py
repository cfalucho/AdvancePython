import pandas as pd
import numpy as np
import re
from SQL import QueryBuilder, CommandExecutor


# from SQL import CommandExecutor


def parse_table_name(filename):
    # remove .csv extension and use the file name for table name
    match = re.search(r"^(.+)\.csv$", filename)
    if match:
        name_only = match.group(1)
        return name_only
    return None



def db_name(filename):
    db_file = re.sub(r'.csv', '.db',  filename)
    return db_file



def main():

    # csv file
    csv_file = "Presidents.csv"

    # Table name will be the csv file without .csv
    table_name = parse_table_name(csv_file)
    print(f"Table name: {table_name}")


    # 1. Read CSV using pandas
    df = pd.read_csv(csv_file)

    # clean empty spaces in columns
    df.columns = df.columns.str.strip()
    for column in df.columns[1:]:
        df[column] = df[column].str.strip()

    df.columns = [re.sub(r' ','_', key) for key in df.columns]
    # print(df.columns)

    df_dict = df.to_dict(orient='records')


    # 3. replace .csv file extension to .db
    db_filename = db_name(csv_file)

    # 4. Initialize the Database
    ce = CommandExecutor(db_filename)

    # 5. Make a connection to the database
    print(f"Making a connection to the {db_filename}...")
    ce.create_connection()

    # 6. Create a Cursor Object to execute SQL queries
    cursor = ce.create_cursor()

    # 7. Initialize the Table
    qb = QueryBuilder(table_name, **df)

    # ========= CREATE TABLE QUERY  =========
    cursor.execute(qb.create_table())

    """
    data={"Presidency": 45, "President": "Donald Trump",
                                     "Wikipedia_Entry": "https://en.wikipedia.org/wiki/Donald_Trump",
                                     "Took_office": "01/05/2016", "Left_office": "11/11/2020", "Party": "Republican", "Portrait": "trump.gif","thumbnail":"trump.gif", "Home_state":"New York"}"""

    data = {"Presidency": 45, "President": "Donald Trump",
            "Wikipedia_Entry": "https://en.wikipedia.org/wiki/Donald_Trump",
            "Took_office": "01/05/2016", "Left_office": "11/11/2020",
            "Party": "Republican", "Portrait": "trump.gif",
            "thumbnail": "trump.gif", "Home_state": "New York"}


    # ========= Single INSERT QUERY  =========
    sql_insert, values = qb.dispatcher("INSERT", data=data)
    cursor.execute(sql_insert, values)

    # ========= Multiple INSERT QUERY  =========
    # for row in df_dict:
    #     sql_insert, values = qb.dispatcher("INSERT", data=row)
    #     cursor.execute(sql_insert, values)

    # ========= UPDATE QUERY  =========
    sql_update = qb.dispatcher("UPDATE",
                  data={"Party":"whig"},
                  where={"Party":"Whig"})


    cursor.execute(sql_update)

    # ========= DELETE QUERY  =========
    # sql_delete, value = qb.dispatcher("DELETE", where={"Presidency":1})
    # cursor.execute(sql_delete, value)

    # ========= SELECT QUERY  =========
    # build the select
    # sql_select = qb.build_select()
    # cursor.execute(sql_select)
    # rows = cursor.fetchone()
    # for row in rows:
    #     print(row)


    # ========= DROP TABLE QUERY  =========
    # print("Performing to drop table...")
    # cursor.execute(qb.dispatcher("DROP"))
    # cursor.execute(sql_insert, values)

    ce.commit()



if __name__ == "__main__":
    main()
