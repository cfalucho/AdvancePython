import numpy as np
import pandas as pd


class Strand:
    def __init__(self, raw_strand):

        # Read a line of strand
        # split it into raw chunks
        # AUGGUCUGCUAUUGUCGUCGAGUCCUUCGCUAA
        # AUG GUC UGC UAU UGU CGU CGA GUC CUU CGC UAA
        self.strand_reshape = None


        self.np_char_array = np.array(list(raw_strand.upper().replace(" ","")))
        remainder = len(self.np_char_array ) % 3

        if remainder == 0:
            self.strand_reshape = np.reshape(self.np_char_array , (-1, 3))

        if remainder != 0:
            pads_needed = 3 - remainder
            self.np_char_array = np.pad(self.np_char_array , (0, pads_needed),
                                        constant_values=" ")
            self.np_reshape  = np.reshape(self.np_char_array , (-1, 3))

        self.chunks_arr = [''.join(base) for base in self.np_reshape]

        # print(self.chunks_arr)
        self.pd_Series = pd.Series(self.chunks_arr)
        result = self.pd_Series.apply(StrandFactory.segment_decision)






        # clean data
        # self.clean_strand = raw_strand.upper()
        # print(self.clean_strand)
        #
        # # convert to np array
        # self.strand_np_arr = np.array(list(self.clean_strand))
        #
        # # reshape the strand
        # # if strand is unable to be reshaped because incorrect length,
        # # add empty strings based on how many missing values it has.
        # remainder = len(self.strand_np_arr) % 3
        # if remainder == 0:
        #     self.strand_reshape = np.reshape(self.strand_np_arr, (-1, 3))
        #
        # if remainder != 0:
        #     pads_needed = 3 - remainder
        #     self.strand_np_arr = np.pad(self.strand_np_arr, (0, pads_needed),
        #                                 constant_values=" ")
        #     self.strand_reshape = np.reshape(self.strand_np_arr, (-1, 3))
        #
        # # print(self.strand_reshape)
        #
        # self.start_codon = self.strand_reshape[0]
        # self.protein_region_codon = self.strand_reshape[1:-1]
        # self.stop_codon = self.strand_reshape[-1]
        #
        # strand = StrandFactory()
        # strand_type, arr = strand.segment_decision(raw_strand)
        # # print(strand_type)
        # # print(arr)


        # Render itself
        # simply joins the string output of each segment


class StrandFactory:
    @staticmethod
    def segment_decision(raw_string):
        # print(raw_string)

        # Try DNA
        dna_check = DNA(raw_string)
        if dna_check.is_valid():
            print("This is a DNA.")
            segment_type = "DNA"

        # print("Proceed to check if it is RNA...")

        # rna_check = RNA(raw_strand)
        # if bool(rna_check):
        #     print("This is a RNA.")
        #     segment_type = "RNA"
        #
        # # print("Proceed to check if it is a Mutation...")
        #
        # mutation_check = Mutation(raw_strand)
        # if bool(mutation_check):
        #     print(
        #         "Mutation (uses biological characters but fails structural codon validation.")
        #     segment_type = "Mutation"
        # # print("Proceed to check if it is Noise...")
        #
        #
        # if bool(Noise(raw_strand)):
        #     print("This is Noise.")
        #     segment_type = "Noise"
        #
        # return segment_type, strand_arr





class Segment:
    biological_char_bases = ['A', 'T', 'C', 'G', 'U']

    def __init__(self, raw_string):
        self.raw_string = raw_string.strip()
        self.np_arr = np.array(list(raw_string))
        print(self.np_arr)
        self.valid_base = np.isin(self.np_arr, self.biological_char_bases)


        if np.any(self.valid_base == False):
            print("Not valid biological char bases.")
        else:
            print("All Characters are valid.")


    def is_valid(self):
        pass

    def to_str(self):
        pass




class DNA(Segment):
    def is_valid(self):

        # check start codon
        valid_start_codon = ['A','T','G']
        if not np.array_equal(valid_start_codon, self.raw_string):
            print("Start codon not ATG")
            return False

        valid_stop_codon = np.array([["T", "A", "A"],
                                     ["T", "A", "G"],
                                     ["T", "G", "A"]
                                            ])
        if not np.any(np.all(valid_stop_codon == self.stop_codon, axis=1)):
            print("Stop codon not TAA, TAG, TGA.")
            return False

        print("Valid DNA.")
        return True

#
#
# class RNA(Segment):
#     def __init__(self,strand):
#         super().__init__(strand)
#
#     def is_valid(self):
#         valid_base_list = ['A', 'U', 'C', 'G']
#         bool_arr = np.isin(self.strand_np_arr, valid_base_list)
#
#         if np.any(bool_arr == False):
#             print("One or more value(s) exist to be False.")
#             return False
#
#         # check start codon
#         valid_start_codon = ['A', 'U', 'G']
#         if not np.array_equal(valid_start_codon, self.start_codon):
#             print("Start codon not AUG")
#             return False
#
#         valid_stop_codon = np.array([["U", "A", "A"],
#                                      ["U", "A", "G"],
#                                      ["U", "G", "A"]
#                                      ])
#         if not np.any(np.all(valid_stop_codon == self.stop_codon, axis=1)):
#             print("Stop codon not TAA, TAG, TGA.")
#             return False
#
#         print("Valid RNA.")
#         return True
#
#     def __bool__(self):
#         if not self.is_valid():
#             print("Not a RNA.")
#             return False
#         return True
#
#
#
# class Mutation(Segment):
#     """
#     Strand has A, T, C, G , U as its base characters but the structural codon validation is not vali
#     for example...
#
#     this is a mutation because it doesn't follow a RNA codon structure even though
#     it uses biological characters
#     ['A' 'A' 'G']
#     ['C' 'U' 'A']
#     ['A' 'C' 'U']
#     ['U' 'C' 'U']
#     ['A' 'U' 'A']
#     ['C' 'U' 'A']
#     ['G' 'U' 'A']
#
#     similarly, with DNA. Invalid Start Codon but valid Stop Codon
#     ['A' 'T' 'T']
#     ['G' 'G' 'A']
#     ['C' 'G' 'C']
#     ['G' 'T' 'G']
#     ['G' 'C' 'A']
#     ['T' 'C' 'T']
#     ['A' 'A' 'T']
#     ['T' 'G' 'A']
#
#     """
#
#     def __init__(self,strand):
#         super().__init__(strand)
#
#
#     def is_valid(self):
#         bool_arr = np.isin(self.strand_np_arr, self.valid_base_list)
#
#         if np.any(bool_arr == False):
#             print("One or more of the base object is not a valid biological character.")
#             return True
#
#         print("Valid base objects. "
#             "Proceeding to check if the start codon structures is valid...")
#
#         valid_start_codon = [['A', 'U', 'G'],
#                              ['A', 'T', 'G']
#                              ]
#         if not np.any(np.all(valid_start_codon == self.start_codon, axis=1)):
#             print("Start codon not valid. Does not match ATG or AUG.")
#             return False
#
#         print("Valid start codon. "
#             "Proceeding to check if the stop codon structures is valid...")
#
#         valid_stop_codon = np.array([["T", "A", "A"],
#                                      ["T", "A", "G"],
#                                      ["T", "G", "A"],
#                                      ["U", "A", "A"],
#                                      ["U", "A", "G"],
#                                      ["U", "G", "A"]
#                                                     ])
#         if not np.any(np.all(valid_stop_codon == self.stop_codon, axis=1)):
#             print("Stop codon not a valid TAA, TAG, TGA, UAA, UAG, UGA.")
#             return False
#
#         print("Valid stop codon.\n")
#
#         print("Valid base objects, valid start codon and stop codon. Not a Mutation.")
#         return True
#
#     def __bool__(self):
#         if not self.is_valid():
#             return True
#         return False
#
#
# class Noise(Segment):
#     def __init__(self,strand):
#         super().__init__(strand)
#
#
#     def is_valid(self):
#         bool_arr = np.isin(self.strand_np_arr, self.valid_base_list)
#
#         if np.any(bool_arr == False):
#             print("Contains characters outside A, T, C, G and U.")
#             return False
#
#         return True
#
#     def __bool__(self):
#         if not self.is_valid():
#             return True
#         print("Not noise.")
#         return False
