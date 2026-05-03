import pandas as pd


class PandasDashboard:
    def __init__(self, strands_name_arr, dna_seq_arr):
        self.series_from_lists = pd.Series(dna_seq_arr, index=strands_name_arr)
        print(self.series_from_lists)


