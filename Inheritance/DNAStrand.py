import numpy as np
from collections import defaultdict # Library to import default dict

"""
ATG CbT\nGCA XTT TGA -> invalid dna because "b" is not a DNA codon -> False

ATG CTT CTG GTA CGC TGA -> valid dna because all letters are DNA codon. Need to remove whitespaces -> True

ATG CTT CTG GTA CGC GTG -> valid dna codon but invalid stop codon -> False

AAT CTA ATT GGC ACT TGA -> remove white spaces, valid DNA codon, but invalid start codon -> False

if start, protein OR stop codon are invalid -> False


"""
# ========================================
#               Helper Functions
# ========================================

# remove whitespaces
def clean_strand(strand):
    return strand.replace(" ", "")

# check if any codon sequence is False
def is_mutated(start_codon, protein_region, stop_codon):
    # print(start_codon, protein_region, stop_codon)
    return np.all(np.array([start_codon, protein_region, stop_codon]))

# checks stop codon
def valid_stop(stop_codon):
    stop_codon_arr = np.array([["T", "A", "A"],
                               ["T", "A", "G"],
                               ["T", "G", "A"]
                              ])
    # result = np.any(np.all(stop_codon_arr == stop_codon, axis=1))
    # print(stop_codon)
    result = np.all(stop_codon_arr == stop_codon, axis=1)
    # print(result)
    is_equal = np.any(np.all(stop_codon_arr == stop_codon, axis=1))
    # print(is_equal)
    return np.any(np.all(stop_codon_arr == stop_codon, axis=1))

# checks protein region
def valid_protein_region(protein_strand):
    codon = ['A', 'T', 'C', 'G']
    is_equal = np.isin(protein_strand, codon)
    return np.any(is_equal != False)

# checks start codon
def valid_start(codon):
    start_codon = np.array(['A', 'T', 'G'])
    not_equal = np.array_equal(start_codon, codon)
    return not_equal



# reshape the list to a 2d array
def reshape(strand_list):
    try:
        return np.reshape(strand_list, (-1, 3))
    # fails if the array cannot reshape to 3 columns
    except ValueError as e:
        print(f"{e}. Please check the codon sequence.")

def invalid_base(base):
    valid_bases = ['A', 'T', 'C', 'G']
    indices = np.isin(base, valid_bases)
    result = np.any(indices == False)
    return result


# colors representing codon sequences in a dna strand
# example strand "ATGTGCCTACTGTAG"
# green = start codon = ATG
# cyan = protein region = TGCCTACTG
# red = stop codon = TAG
class DNAStrand:
    def __init__ (self, raw_strand):
        self.raw_sequence = clean_strand(raw_strand.upper())
        # check if every character is in A, T, U, C, G
        self.strand_arr = np.array(list(self.raw_sequence))
        # print(self.strand_arr)

        # final strand list
        self.final_strand_list = np.array([])

        # if all 3 true, not mutated
        self.start_codon_flag       = True
        self.protein_region_flag    = True
        self.stop_codon_flag        = True
        self.has_invalid_base       = False
        self.is_mutated             = False

        if invalid_base(self.strand_arr):
            self.has_invalid_base = True
            return

        array_2d = np.reshape(self.strand_arr, (-1, 3))
        self.start_codon          = array_2d[0]
        self.protein_region_codon = array_2d[1:-1]
        self.stop_codon           = array_2d[-1]

        if not valid_start(self.start_codon):
            self.start_codon_flag = False


        if not valid_stop(self.stop_codon):
            self.stop_codon_flag = False

        # if all 3 flags are true, it returns true
        # else, if there is at least 1 false, it returns false
        self.true_flags = np.array([self.start_codon_flag,
                                self.protein_region_flag,
                                self.stop_codon_flag])

        # if true, strand is not mutated
        if np.all(self.true_flags):
            self.is_mutated = False

        # if not true, strand is mutated
        if np.any(self.true_flags == False):
            self.is_mutated = True

        # print(self.is_valid)


        # dict of colors
        self.CODON_COLOR_MAPPING = {
            "ATG": "green",
            "TAG": "red",
            "TAA": "red",
            "TGA": "red"
            }
        default_color = "black"
        protein_default_color = "cyan"

        codon_arr = []
        start_codon_str = "".join(self.start_codon)
        # print(start_codon_str)
        codon_arr.append(start_codon_str)


        for x in self.protein_region_codon:
            protein_reg_codon_str = "".join(x)
            codon_arr.append(protein_reg_codon_str)
        # print(protein_arr)


        stop_codon_str = "".join(self.stop_codon)
        codon_arr.append(stop_codon_str)

        # for every codon in the strand arr
        # if a codon matches the keys in CODON COLOR MAPPING, assign it the value of the key
        # for example if codon is ATG -> ('ATG','green')

        # codon list of tuple
        self.codon_list = []

        if codon_arr[0] in self.CODON_COLOR_MAPPING:
            start_color_tuple = (codon_arr[0],
                                 self.CODON_COLOR_MAPPING[codon_arr[0]])
            self.codon_list.append(start_color_tuple)

        if not codon_arr[0] in self.CODON_COLOR_MAPPING:
            start_color_tuple = (codon_arr[0], default_color)
            self.codon_list.append(start_color_tuple)

        for codon in codon_arr[1:-1]:
            protein_color_tuple = (codon, protein_default_color)
            self.codon_list.append(protein_color_tuple)


        if codon_arr[-1] in self.CODON_COLOR_MAPPING:
            stop_color_tuple = (codon_arr[-1],
                                self.CODON_COLOR_MAPPING[codon_arr[-1]])
            self.codon_list.append(stop_color_tuple)


        if not codon_arr[-1] in self.CODON_COLOR_MAPPING:
            stop_color_tuple = (codon_arr[-1], default_color)
            self.codon_list.append(stop_color_tuple)

        # print(self.codon_list)


    # ========================================
    #               Getters
    # ========================================
    def get_codon_list(self):
        print(self.codon_list)
        return self.codon_list

    def get_mutation_status(self):
        return self.is_mutated

# class Segment(DNAStrand):
#     def __init__(self, raw_strand):
#         super().__init__(raw_strand)



"""References used

Didn't use numpy.char.join because it didn't join whitespaces for me
https://numpy.org/doc/2.1/reference/generated/numpy.char.join.html

https://stackoverflow.com/questions/66872545/how-to-get-np-char-add-to-put-a-space-between-the-concatenated-strings

To understand how to use numpy.any()
https://www.geeksforgeeks.org/python/numpy-any-in-python/
"""









