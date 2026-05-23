import pandas as pd
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
    csv_file = "Temperature.csv"

    # Table name will be the csv file without .csv
    table_name = parse_table_name(csv_file)
    print(table_name)


    # 1. Read CSV using pandas
    df = pd.read_csv(csv_file)
    # print(df)
    # 2. store columns into a variable
    columns = df.columns

    # 3. Make a connection to a database
    # replace .csv file extension to .db
    db_file = db_name(csv_file)
    new_db = CommandExecutor(db_file)


    # conn = ce.create_connection
    print(new_db)

    cursor.execute(create_table_query)
    conn.commit()


    # QueryBuilder(table_name, columns)




    # 3. Then into SQLite Table

if __name__ == "__main__":
    main()
