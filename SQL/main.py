import pandas as pd
import re
from SQL import QueryBuilder, CommandExecutor
from GUI import GUI

def table_name(filename):
    # remove .csv extension and use the file name for table name
    match = re.search(r"^(.+)\.csv$", filename)
    if match:
        name_only = match.group(1)
        return name_only
    return None

def db_name(filename):
    db_file = re.sub(r'.csv', '.db',  filename)
    return db_file

class DataFrame:
    def __init__(self, csv_file):
        self.database_filename = db_name(csv_file)
        self.table_name = table_name(csv_file)

        self.dataframe = pd.read_csv(csv_file, dtype=str)
        print(self.dataframe)

        self.dataframe.columns = self.dataframe.columns.str.strip()
        self.dataframe.columns = [re.sub(r' ', '_', key)
                                  for key in self.dataframe.columns]


    def get_dataframe(self):
        return self.dataframe

    def to_dict(self):
        df_dict = self.dataframe.to_dict(orient='records')
        return df_dict

    def get_db_filename(self):
        return self.database_filename

    def get_table_name(self):
        return self.table_name

    def get_df_cols(self):
        return self.dataframe.columns


def main():
    # csv file
    csv_file = "Presidents.csv"

    # DataFrame
    df = DataFrame(csv_file)

    # QueryBuilder
    qb = QueryBuilder()

    # CommandExecutor
    ce = CommandExecutor(df, qb)

    # GUI
    GUI(ce, df)



if __name__ == "__main__":
    main()
