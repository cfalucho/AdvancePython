class Segment:
    def __init__(self, raw_strand):
        self.strand = raw_strand


class DNA(Segment):
    def __init__(self, strand):
        super().__init__(strand)

class RNA(Segment):
    def __init__(self,strand):
        super().__init__(strand)