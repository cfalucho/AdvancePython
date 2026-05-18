import pandas as pd
from DNAStrand import DNAStrand

"""
Could use some improvements can be made here to check for strand's without a value

Would need to research more panda library method when I have time. 
Could perform a try-catch block to check both the strand names and values

Such that is there a value for each strand?
"""
class DNATableModel:
    def __init__(self, strands_name_arr, dna_seq_arr):
        self.series_from_lists = pd.Series(dna_seq_arr, index=strands_name_arr)
        # print(self.series_from_lists)
        self.dna_objects_series = self.series_from_lists.apply(DNAStrand)



    # ========================================
    #               Getters
    # ========================================
    def get_objects(self):
        return self.dna_objects_series

    def get_list(self):
        return self.series_from_lists.index.tolist()

""" References used
https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html

https://pandas.pydata.org/docs/reference/api/pandas.Series.html#pandas.Series
"""
