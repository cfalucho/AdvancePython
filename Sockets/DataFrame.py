import pandas as pd
import re


#------------- HELPER FUNCTIONS -------------
def database_filename(filename):
    db_file = re.sub(r'.csv', '.db',  filename)
    return db_file

def table_name(filename):
    # remove .csv extension and use the file name for table name
    match = re.search(r"^(.+)\.csv$", filename)
    if match:
        name_only = match.group(1)
        return name_only
    return None

class DataFrame:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file, dtype=str)
        self.db_filename = database_filename(csv_file)
        self.table_name = table_name(csv_file)
        self.df.columns = self.df.columns.str.strip()
        self.df.columns = [re.sub(r' ', '_', key)
                                  for key in self.df.columns]


    def get_db_filename(self):
        return self.db_filename

    def get_table_name(self):
        return self.table_name

    def get_df(self):
        return self.df

    def get_list(self):
        return self.df.to_dict(orient='records')

    def iter_rows(self):
        for index, row in self.df.iterrows():
            yield row.to_dict()

    def get_cols(self):
        return tuple(self.df.columns)