from const import *

class Square:

    ALPHA_COL = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

    def __init__(self, row, col,  pice = None):
        self.size = SQR_SIZE
        self.pice = pice
        self.row = row
        self.col = col
        self.alpha_col = self.ALPHA_COL[col]

    def __eq__(self, other_sqr):
        return self.row == other_sqr.row and self.col == other_sqr.col

    def has_pice(self):
        return self.pice != None
    
    def has_enemy_pice(self, color):
        return self.has_pice() and self.pice.color != color
    
    @staticmethod

    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True
    
    def get_alpha_col(col):
        ALPHA_COL = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

        return ALPHA_COL[col]