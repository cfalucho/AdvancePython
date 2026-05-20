import numpy as np


class Strand:
    def __init__(self, raw_line):
        self.raw_chunks = raw_line

        self.segments = []

        for chunk in self.raw_chunks:
            segment_obj = StrandFactory.create_segment(chunk)
            self.segments.append(segment_obj)


    def render(self):
        return " ".join(str(segment) for segment in self.segments)

    def __str__(self):
        return self.render()


class StrandFactory:
    @staticmethod
    def create_segment(raw_strand):
        print(f"Check if {raw_strand} is DNA...")
        if DNA.is_valid(raw_strand):
            print(DNA(raw_strand))
            return DNA(raw_strand)

        print(f"Check if {raw_strand} is RNA...")
        if RNA.is_valid(raw_strand):
            print(RNA(raw_strand))
            return RNA(raw_strand)

        print(f"Check if {raw_strand} is a Mutation...")
        # print(raw_strand)
        if Mutation.is_valid(raw_strand):
            print(Mutation(raw_strand))
            return Mutation(raw_strand)

        print(f"Check if {raw_strand} is Noise...")
        print(Noise(raw_strand))
        return Noise(raw_strand)


class Segment:
    # biological characters (A, T, C, G, U)
    biological_chars = np.array(['A', 'T', 'C', 'G', 'U'])



    def __init__(self, raw_strand):
        self.raw_strand = raw_strand.upper()
        self.np_arr = np.array(list(self.raw_strand))
        self.base_np_arr = None
        remainder = len(raw_strand) % 3
        if remainder == 0:
            self.base_np_arr = np.reshape(self.np_arr, (-1, 3))
        else:
            padding_needed = 3 - remainder
            # will use '0' as a placeholder for empty strings
            self.pad_arr = np.pad(self.np_arr, (0, padding_needed),
                                  constant_values="0")
            self.base_np_arr = np.reshape(self.pad_arr, (-1, 3))

        #
        # self.strand = ""
        # for base in self.base_np_arr:
        #     codon = "".join(base)
        #     self.strand += codon + " "


    @classmethod
    def is_valid(cls, raw_strand):
        pass


    def to_str(self) -> str:
        return self.raw_strand

    def __str__(self) -> str:
        return self.to_str()


class DNA(Segment):
    def __init__(self, raw_strand: str):
        super().__init__(raw_strand)
        # self.base_np_arr = np.reshape(self.np_arr, (-1, 3))

        self.strand = ""
        for base in self.base_np_arr:
            codon = "".join(base)
            self.strand += codon + " "


    @classmethod
    def is_valid(cls, raw_strand):
        strand = raw_strand.upper().strip()

        # if not a strand return False
        if not strand:
            return False

        # convert to numpy array
        base_object_arr = np.array(list(strand))

        # slice to grab first 3 index and last 3 index
        # for start and stop codon
        start_base_object_arr = base_object_arr[:3]
        stop_base_object_arr = base_object_arr[-3:]
        # print(start_base_object_arr)
        # print(stop_base_object_arr)

        # valid DNA characters are ['A', 'T', 'C', 'G']
        valid_chars = np.array(['A', 'T', 'C', 'G'])
        all_chars_valid = np.all(np.isin(base_object_arr, valid_chars))

        # valid start codon
        start_codon = np.array(['A', 'T', 'G'])
        start_codon_valid = np.array_equal(start_codon, start_base_object_arr)
        # print(start_codon_valid)

        # valid stop codon - TAA, TAG, TGA
        stop_codon = np.array([['T', 'A', 'A'],
                               ['T', 'A', 'G'],
                               ['T', 'G', 'A']])

        stop_codon_valid = np.any(np.all(stop_codon == stop_base_object_arr, axis=1))
        # print(stop_codon_valid)
        # return true if Start codon, stop codon and all chars are valid
        return all_chars_valid and start_codon_valid and stop_codon_valid

    def to_str(self):
        return f'[DNA] {self.strand}'




class RNA(Segment):
    def __init__(self, raw_strand):
        super().__init__(raw_strand)
        # self.base_np_arr = np.reshape(self.np_arr, (-1, 3))

        self.strand = ""
        for base in self.base_np_arr:
            codon = "".join(base)
            self.strand += codon + " "
        # print(self.strand)


    @classmethod
    def is_valid(cls, raw_strand: str) -> bool:
        strand = raw_strand.upper().strip()
        if not strand:
            return False

            # convert to numpy array
        base_object_arr = np.array(list(strand))

        # slice to grab first 3 index and last 3 index
        # for start and stop codon
        start_base_object_arr = base_object_arr[:3]
        stop_base_object_arr = base_object_arr[-3:]
        # print(start_base_object_arr)
        # print(stop_base_object_arr)

        # valid DNA characters are ['A', 'T', 'C', 'G']
        valid_chars = np.array(['A', 'U', 'C', 'G'])
        all_chars_valid = np.all(np.isin(base_object_arr, valid_chars))

        # valid start codon
        start_codon = np.array(['A', 'U', 'G'])
        start_codon_valid = np.array_equal(start_codon, start_base_object_arr)
        # print(start_codon_valid)

        # valid stop codon - TAA, TAG, TGA
        stop_codon = np.array([['U', 'A', 'A'],
                               ['U', 'A', 'G'],
                               ['U', 'G', 'A']])

        stop_codon_valid = np.any(np.all(stop_codon == stop_base_object_arr, axis=1))
        # print(stop_codon_valid)

        # return true if Start codon, stop codon and all chars are valid
        return all_chars_valid and start_codon_valid and stop_codon_valid

    def to_str(self):
        return f'[RNA] {self.strand}'


class Mutation(Segment):
    def __init__(self, raw_strand):
        super().__init__(raw_strand)

    @classmethod
    def is_valid(cls, raw_strand):
        strand = raw_strand.upper().strip()
        if not strand:
            return False

        # convert to numpy array
        base_object_arr = np.array(list(strand))

        # check if characters are valid
        all_chars_valid = np.all(np.isin(base_object_arr, cls.biological_chars))

        # return true if Start codon, stop codon and all chars are valid
        return all_chars_valid


    def to_str(self) -> str:
        return f"[MUT] {self.raw_strand}"


class Noise(Segment):
    def __init__(self, raw_strand):
        super().__init__(raw_strand)
        # self.base_np_arr = np.reshape(self.np_arr, (-1, 3))

        self.strand = ""
        for base in self.base_np_arr:
            codon = "".join(base)
            self.strand += codon + " "
        # print(self.strand)

    @classmethod
    def is_valid(cls, raw_strand):
        return True

    def to_str(self) -> str:
        return f"[NOI] {self.raw_strand}"