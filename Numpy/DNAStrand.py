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
        # clean the raw strand
        self.clean_dna_strand = np.array(list(clean_strand(raw_strand.upper())))

        # colors representing codon sequences in a dna strand
        # example strand "ATGTGCCTACTGTAG"
        # green = start codon = ATG
        # cyan = protein region = TGCCTACTG
        # red = stop codon = TAG
        # return a list of tuples ->
        # [("ATG", "green"), ("TGC CTA CTG", "cyan"), ("TAG", "red")]
        self.colors_list = np.array(["green", "cyan", "red"])

        # reshape the dna strand
        self.dna_array_shape = self.reshape(self.clean_dna_strand)



        # need to validate for 3 letter seq - MUST DO

        # break the strand into smaller strands for validation
        self.start_codon = self.dna_array_shape[0]
        self.protein_region_codon = self.dna_array_shape[1:-1]





        self.stop_codon = self.dna_array_shape[-1]

        # codon flags for the strand
        self.start_codon_flag = False
        self.protein_region_flag = False
        self.stop_codon_flag = False

        # final result
        self.mutated = False

        # Function to validate strand
        self.validate_strand()

        if self.mutated:
            print("Strand is valid.")
            return

        print("Invalid Strand.")
        return


    def validate_strand(self):
        """
        This function will check each codon - Start, Protein, Stop
        If any return False,

        """
        # check start codon
        if self.has_valid_start(self.start_codon):
            print("Start codon invalid.")
            return

        self.start_codon_flag = True
        print("Start codon is valid.")

        # check protein
        if self.has_valid_protein(self.protein_region_codon):
            print("Protein region invalid.")
            return

        self.protein_region_flag = True
        print("Protein region valid.")

        # check stop codon
        if not self.has_valid_stop(self.stop_codon):
            print("Stop codon invalid.")
            return

        self.stop_codon_flag = True
        print("Stop codon is valid.")


        # if this returns True, it means the strand is valid
        # if it returns False, it is Mutated and invalid
        strand_result = self.is_strand_mutated(self.start_codon_flag,
                                 self.protein_region_flag,
                                 self.stop_codon_flag)
        if strand_result:
            self.mutated = True
            return

        return


    def reshape(self, strand_list):
        try:
            return np.reshape(strand_list, (-1, 3))
        except ValueError as e:
            print(f"{e}. Please check the codon sequence.")
            exit()

    def has_valid_start(self, start_codon):
        start_codon_arr = np.array(['A', 'T', 'G'])
        codon_indices = np.array_equal(start_codon_arr, start_codon)
        # print(codon_indices)
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
    def is_strand_mutated(self, start_codon, protein_region, stop_codon):
        print(start_codon, protein_region, stop_codon)
        return np.all(np.array([start_codon, protein_region, stop_codon]))














