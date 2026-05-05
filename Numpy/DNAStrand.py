import numpy as np

"""
ATG CbT\nGCA XTT TGA -> invalid dna because "b" is not a DNA codon -> False

ATG CTT CTG GTA CGC TGA -> valid dna because all letters are DNA codon. Need to remove whitespaces -> True

ATG CTT CTG GTA CGC GTG -> valid dna codon but invalid stop codon -> False

AAT CTA ATT GGC ACT TGA -> remove white spaces, valid DNA codon, but invalid start codon -> False

if start, protein OR stop codon are invalid -> False


"""
# Remove whitespaces
def clean_strand(strand):
    return strand.replace(" ", "")

class DNAStrand:
    def __init__ (self, raw_strand):
        self.raw_sequence = raw_strand
        self.clean_dna_strand = np.array(list(clean_strand(raw_strand.upper())))
        self.strand_list = []
        self.is_strand_mutated = False

        # colors representing codon sequences in a dna strand
        # example strand "ATGTGCCTACTGTAG"
        # green = start codon = ATG
        # cyan = protein region = TGCCTACTG
        # red = stop codon = TAG
        # return a list of tuples ->
        # [("ATG", "green"), ("TGC CTA CTG", "cyan"), ("TAG", "red")]
        self.colors_list = ["green", "cyan",  "red"]


        # reshape the dna strand
        self.dna_array_shape = self.reshape(self.clean_dna_strand)

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


        # codon flags for the strand
        self.start_codon_flag = False
        self.protein_region_flag = False
        self.stop_codon_flag = False

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
        if not self.has_valid_start(self.start_codon):
            # print("Start codon is valid.")
            self.start_codon_flag = True


        # check protein
        if not self.has_valid_protein(self.protein_region_codon):
            # print("Protein region valid.")
            self.protein_region_flag = True



        # check stop codon
        if self.has_valid_stop(self.stop_codon):
            # print("Stop codon is valid.")
            self.stop_codon_flag = True


        # if this returns True, strand is mutated
        # if it returns False, it is not mutated
        self.is_strand_mutated = self.is_mutated(self.start_codon_flag,
                                 self.protein_region_flag,
                                 self.stop_codon_flag)

        return self.is_strand_mutated

    def reshape(self, strand_list):
        try:
            return np.reshape(strand_list, (-1, 3))
        except ValueError as e:
            print(f"{e}. Please check the codon sequence.")
            exit()

    def has_valid_start(self, start_codon):
        start_codon_arr = np.array(['A', 'T', 'G'])
        codon_indices = np.array_equal(start_codon_arr, start_codon)
        return np.any(codon_indices == False)



    def has_valid_protein(self, protein_strand):
        codon = ['A', 'T', 'C', 'G']
        codon_indices = np.isin(protein_strand, codon)
        return np.any(codon_indices == False)



    def has_valid_stop(self, stop_codon):
        stop_codon_arr = np.array([["T", "A", "A"],
                      ["T", "A", "G"],
                      ["T", "G", "A"]
                      ])

        return np.any(np.all(stop_codon_arr == stop_codon, axis=1))


    # check if the strand is mutated, basically an invalid strand
    def is_mutated(self, start_codon, protein_region, stop_codon):
        # print(start_codon, protein_region, stop_codon)
        return np.all(np.array([start_codon, protein_region, stop_codon]))

    def get_strand(self):
        return self.strand_list





"""References used

Didn't use numpy.char.join because it didn't join whitespaces for me
https://numpy.org/doc/2.1/reference/generated/numpy.char.join.html

https://stackoverflow.com/questions/66872545/how-to-get-np-char-add-to-put-a-space-between-the-concatenated-strings

To understand how to use numpy.any()
https://www.geeksforgeeks.org/python/numpy-any-in-python/
"""









