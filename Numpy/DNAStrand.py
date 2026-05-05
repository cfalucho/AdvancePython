import numpy as np

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
def has_valid_stop(stop_codon):
    stop_codon_arr = np.array([["T", "A", "A"],
                               ["T", "A", "G"],
                               ["T", "G", "A"]
                              ])
    # result = np.any(np.all(stop_codon_arr == stop_codon, axis=1))
    return np.any(np.all(stop_codon_arr == stop_codon, axis=1))

# checks protein region
def has_valid_protein(protein_strand):
    codon = ['A', 'T', 'C', 'G']
    codon_indices = np.isin(protein_strand, codon)
    return np.any(codon_indices == False)

# checks start codon
def has_valid_start(start_codon):
    start_codon_arr = np.array(['A', 'T', 'G'])
    codon_indices = np.array_equal(start_codon_arr, start_codon)
    return np.any(codon_indices == False)

# reshape the list to a 2d array
def reshape(strand_list):
    try:
        return np.reshape(strand_list, (-1, 3))
    # fails if the array cannot reshape to 3 columns
    except ValueError as e:
        print(f"{e}. Please check the codon sequence.")
        exit()

# colors representing codon sequences in a dna strand
# example strand "ATGTGCCTACTGTAG"
# green = start codon = ATG
# cyan = protein region = TGCCTACTG
# red = stop codon = TAG
class DNAStrand:
    def __init__ (self, raw_strand):
        self.raw_sequence = raw_strand
        self.clean_dna_strand = np.array(list(clean_strand(raw_strand.upper())))
        self.colors_list = ["green", "cyan",  "red"]

        # store the codon seq ->
        # [("ATG", "green"), ("TGC CTA CTG", "cyan"), ("TAG", "red")]
        self.strand_list = []

        # codon flags for the strand
        self.start_codon_flag = False
        self.protein_region_flag = False
        self.stop_codon_flag = False

        # final check if strand is mutated
        self.is_strand_mutated = False

        # reshape the dna strand
        self.dna_array_shape = reshape(self.clean_dna_strand)

        # need to validate for 3 letter seq - MUST DO

        # break the full strand into smaller strands for validation
        self.start_codon = self.dna_array_shape[0]
        self.protein_region_codon = self.dna_array_shape[1:-1]
        """
        [
            ['T' 'G' 'C']
            ['C' 'T' 'A']
            ['C' 'T' 'G']
        ]
        """
        self.stop_codon = self.dna_array_shape[-1]

        # concat the letters into a codon sequence
        self.concat_seq(self.start_codon)
        self.concat_seq(self.protein_region_codon)
        self.concat_seq(self.stop_codon)
        self.zip_lists()

        # Function to validate strand
        if self.validate_strand():
            self.strand_list.insert(0, "Not Mutated")
            # print(self.strand_list)
            return

        self.strand_list.insert(0, "Mutated")
        # print(self.strand_list)
        return

    def concat_seq(self, codon):
        concat_codon = "".join(codon.flatten())
        self.strand_list.append(concat_codon)

    def zip_lists(self):
        self.strand_list = list(zip(self.strand_list, self.colors_list))

    def validate_strand(self):
        """
        This function will check each codon - Start, Protein, Stop
        If any invalid return False,

        """
        # check start codon
        if not has_valid_start(self.start_codon):
            self.start_codon_flag = True

        # check protein region
        if not has_valid_protein(self.protein_region_codon):
            self.protein_region_flag = True

        # check stop codon
        if has_valid_stop(self.stop_codon):
            self.stop_codon_flag = True

        # if this returns True, strand is mutated
        # if it returns False, it is not mutated
        self.is_strand_mutated = is_mutated(self.start_codon_flag,
                                 self.protein_region_flag,
                                 self.stop_codon_flag)
        return self.is_strand_mutated

    # ========================================
    #               Getters
    # ========================================
    def get_strand(self):
        return self.strand_list





"""References used

Didn't use numpy.char.join because it didn't join whitespaces for me
https://numpy.org/doc/2.1/reference/generated/numpy.char.join.html

https://stackoverflow.com/questions/66872545/how-to-get-np-char-add-to-put-a-space-between-the-concatenated-strings

To understand how to use numpy.any()
https://www.geeksforgeeks.org/python/numpy-any-in-python/
"""









