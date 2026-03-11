class Move:
    def __init__(self, initial_sqr, final_sqr, final_pice = None):
        self.initial_sqr = initial_sqr
        self.final_sqr = final_sqr
        self.final_pice = final_pice

    def __eq__(self, other_move):
        return self.initial_sqr == other_move.initial_sqr and self.final_sqr == other_move.final_sqr