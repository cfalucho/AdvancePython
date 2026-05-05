import pandas as pd
import tkinter as tk
from DNAStrand import DNAStrand


class DNATableModel:
    def __init__(self, strands_name_arr, dna_seq_arr):
        self.series_from_lists = pd.Series(dna_seq_arr, index=strands_name_arr)
        self.dna_objects_series = self.series_from_lists.apply(DNAStrand)


    def get_objects(self):
        return self.dna_objects_series

    def get_list(self):
        return self.series_from_lists.index.tolist()

