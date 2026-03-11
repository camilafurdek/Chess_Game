import copy
import os

from const import*
from square import Square
from pice import*
from move import Move
from sound import Sound

class Board:

    def __init__(self):
        self.last_move = None

        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self._create()

        self.add_pices('white')
        self.add_pices('black')

        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)
        

    def _create(self):

        for row in range (ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def add_pices(self, color):
        pawn_row, other_row = (6, 7) if color == 'white' else (1, 0)
       
        # add pawns
        for col in range(COLS):
            self.squares[pawn_row][col].pice = Pawn(color)

        # add rooks
        self.squares[other_row][0].pice = Rook(color)
        self.squares[other_row][7].pice = Rook(color)

        # add knights
        self.squares[other_row][1].pice = Knight(color)
        self.squares[other_row][6].pice = Knight(color)

        # add bishops
        self.squares[other_row][2].pice = Bishop(color)
        self.squares[other_row][5].pice = Bishop(color)

        # add queen
        self.squares[other_row][3].pice = Queen(color)

        # add king
        self.squares[other_row][4].pice = King(color)

    def calc_valid_moves(self, pice, row, col, bool = True):
        pice.clear_moves()
        
        def pawn_moves():
            initial_sqr = Square(row, col)

            # vertical moves
            sum = 1  if pice.moved else 2 

            i = 1 * pice.dir
            
            while abs(i) <= sum and Square.in_range(row + i , col):
                if not self.squares[row + i][col].has_pice():
                    final_sqr = Square(row + i, col)

                    move = Move(initial_sqr, final_sqr)

                    if bool:
                        if not self.in_check(pice, move):
                            pice.add_move(move)
                    else:
                        pice.add_move(move)

                    i += 1 * pice.dir
                else:
                    break
            
            # diagonal moves
            possible_moves = [
                (row + pice.dir, col + 1),
                (row + pice.dir, col - 1)
            ]

            for possible_move in possible_moves:
                if Square.in_range(possible_move[0], possible_move[1]):
                    if self.squares[possible_move[0]][possible_move[1]].has_enemy_pice(pice.color):
                        final_pice = self.squares[possible_move[0]][possible_move[1]].pice
                        final_sqr = Square(possible_move[0], possible_move[1], final_pice)

                        move = Move(initial_sqr, final_sqr)

                        # check potential checks
                        if bool:
                            if not self.in_check(pice, move):
                                pice.add_move(move)
                        
                        else:
                            pice.add_move(move)

            # en passant moves
            r = 3 if pice.color == 'white' else 4
            f_r = 2 if pice.color == 'white' else 5

            # left en passant
            if Square.in_range(col - 1) and row == r:
                if self.squares[row][col - 1].has_enemy_pice(pice.color):
                    p = self.squares[row][col - 1].pice

                    if isinstance(p, Pawn):
                        if p.en_passant:
                             final_sqr = Square(f_r, col - 1, p)

                             move = Move(initial_sqr, final_sqr)

                             # check potential checks
                             if bool:
                                if not self.in_check(pice, move):
                                    pice.add_move(move)
                            
                                else:
                                    pice.add_move(move)
            #
             # right en passant
            if Square.in_range(col + 1) and row == r:
                if self.squares[row][col + 1].has_enemy_pice(pice.color):
                    p = self.squares[row][col + 1].pice

                    if isinstance(p, Pawn):
                        if p.en_passant:
                             final_sqr = Square(f_r, col + 1, p)

                             move = Move(initial_sqr, final_sqr)

                             # check potential checks
                             if bool:
                                if not self.in_check(pice, move):
                                    pice.add_move(move)
                            
                                else:
                                    pice.add_move(move)

        def line_moves(dir_row, dir_col):
            r = 1 * dir_row
            c = 1 * dir_col

            initial = Square(row, col)

            while Square.in_range(row + r, col + c):
                final_pice = self.squares[row + r][col + c].pice
                final = Square(row + r, col + c, final_pice)
                move = Move(initial, final)

                if not self.squares[row + r][col + c].has_pice():
                    # check potential checks
                    if bool:
                        if not self.in_check(pice, move):
                            pice.add_move(move)
                        else:
                            break
                    else:
                        pice.add_move(move)

                elif self.squares[row + r][col + c].has_enemy_pice(pice.color):
                    # check potential checks
                    if bool:
                        if not self.in_check(pice, move):
                            pice.add_move(move)
                    else:
                        pice.add_move(move)

                    break

                else:
                    break

                r += 1 * dir_row
                c += 1 * dir_col

        def knight_moves():
            possible_moves = [
                (row - 2, col - 1),
                (row - 1, col + 2),
                (row + 1, col + 2),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row + 1, col - 2),
                (row - 1, col - 2),
                (row - 2, col + 1)
            ]

            initial_sqr = Square(row, col)

            for possible_move in possible_moves:
                if Square.in_range(possible_move[0], possible_move[1]):
                    if not self.squares[possible_move[0]][possible_move[1]].has_pice() or self.squares[possible_move[0]][possible_move[1]].has_enemy_pice(pice.color):
                        final_pice = self.squares[possible_move[0]][possible_move[1]].pice
                        final_sqr = Square(possible_move[0], possible_move[1], final_pice)
                        move = Move(initial_sqr, final_sqr)

                        # check potential checks
                        if bool:
                            if not self.in_check(pice, move):
                                pice.add_move(move)
                            else:
                                break
                        else:
                            pice.add_move(move)

        def king_moves(): 
            # normal moves
            possible_moves = [
                (row,col + 1),
                (row, col - 1),
                (row + 1, col + 1),
                (row + 1, col),
                (row + 1, col - 1),
                (row - 1, col),
                (row - 1, col + 1),
                (row - 1, col - 1)
            ]

            initial_sqr = Square(row, col)

            for possible_move in possible_moves:
                if Square.in_range(possible_move[0], possible_move[1]):
                    if not self.squares[possible_move[0]][possible_move[1]].has_pice() or self.squares[possible_move[0]][possible_move[1]].has_enemy_pice(pice.color) :
                        final_sqr = Square(possible_move[0], possible_move[1])

                        move = Move(initial_sqr, final_sqr)

                        # check potential cheks
                        if bool:
                            if not self.in_check(pice, move):
                                pice.add_move(move)
                        else:
                            pice.add_move(move)
                            
            # castling moves
            if not pice.moved:
                # queen castling
                if self.squares[row][0].has_pice() and not self.squares[row][0].pice.moved:
                    if not self.squares[row][1].has_pice() and not self.squares[row][2].has_pice() and not self.squares[row][3].has_pice():
                        final_sqr = Square(row, 2)

                        move = Move(initial_sqr, final_sqr)

                         # check potential checks
                        if bool:
                            final_2 = Square(row, 3)
                            move_2 = Move(initial_sqr, final_2)

                            if not self.in_check(pice,move) and not self.in_check(pice, move_2):
                                pice.add_move(move)
                        
                        else:
                            pice.add_move(move)

                # king castling
                if self.squares[row][7].has_pice() and not self.squares[row][7].pice.moved:
                    if not self.squares[row][6].has_pice() and not self.squares[row][5].has_pice():
                        final_sqr = Square(row, 6)

                        move = Move(initial_sqr, final_sqr)

                        # check potential checks
                        if bool:
                            final_2 = Square(row, 5)
                            move_2 = Move(initial_sqr, final_2)

                            if not self.in_check(pice,move) and not self.in_check(pice, move_2):
                                pice.add_move(move)
                        
                        else:
                            pice.add_move(move)
            
            
        if isinstance(pice, Pawn):
            pawn_moves()

        if isinstance(pice, Rook):
            line_moves(1, 0)
            line_moves(-1, 0)
            line_moves(0, 1)
            line_moves(0, -1)
        
        if isinstance(pice, Knight):
            knight_moves()

        if isinstance(pice, Bishop):
            line_moves(-1, 1)
            line_moves(-1, -1)
            line_moves(1, 1)
            line_moves(1, -1)

        if isinstance(pice, Queen):
            line_moves(1, 0)
            line_moves(-1, 0)
            line_moves(0, 1)
            line_moves(0, -1)
            line_moves(-1, 1)
            line_moves(-1, -1)
            line_moves(1, 1)
            line_moves(1, -1)

        if isinstance(pice, King):
            king_moves()
    
    def move(self, pice, move, testing = False):
        initial = move.initial_sqr
        final = move.final_sqr

        # en passant aux
        en_passant_aux = not self.squares[final.row][final.col].has_pice()

        # console board move update
        self.squares[initial.row][initial.col].pice = None
        self.squares[final.row][final.col].pice = pice

        if isinstance(pice, Pawn):
            # promotion
            self.check_promotion(pice, final)

            # en passant capture
            diff = final.col - initial.col

            if diff != 0 and en_passant_aux:
                # console board update
                self.squares[initial.row][initial.col + diff].pice = None

                # sound
                if not testing:
                    sound = Sound(os.path.join(
                        'assets/sounds/capture.wav'
                    ))
                    sound.play()

        
        # king castling
        if isinstance(pice, King):
            # castling
            if self.castling(initial, final):
                diff = final.col - initial.col

                if diff < 0 :
                    rook = self.squares[initial.row][0].pice

                    initial = Square(initial.row, 0)
                    final = Square(initial.row, 3)

                    move = Move(initial, final)
                    self.move(rook, move)
                
                else:
                    rook = self.squares[initial.row][7].pice

                    initial = Square(initial.row, 7)
                    final = Square(initial.row, 5)

                    move = Move(initial, final)
                    self.move(rook, move)

            #update king pos
            self.update_king_pos(pice.color, final.row, final.col)

        # pice move attribute update
        pice.moved = True
        # clear valid moves
        pice.clear_moves()

        #update last move
        self.last_move = move

    def valid_move(self, pice, move):
        return move in pice.moves
    
    def check_promotion(self, pice, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].pice = Queen(pice.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) % 2 == 0
    
    def in_check(self, pice, move):
        temp_pice = copy.deepcopy(pice)
        temp_board = copy.deepcopy(self)

        temp_board.move(temp_pice, move, True)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_pice(pice.color):
                    p = copy.deepcopy(temp_board.squares[row][col].pice)

                    temp_board.calc_valid_moves(p, row, col, False)

                    for m in p.moves:
                        if isinstance(m.final_sqr.pice, King):
                            return True
        
        return False
        
    def set_true_en_passant(self, pice):
        if not isinstance(pice, Pawn):
            return

    def update_king_pos(self, color, row, col): 
        if color == 'white':
            self.white_king_pos = (row, col)
        else:
            self.black_king_pos = (row, col)

    def game_over(self, color):
        king_pos = self.black_king_pos if color == 'black' else self.white_king_pos
        king = self.squares[king_pos[0]][king_pos[1]].pice

        self.calc_valid_moves(king, king_pos[0], king_pos[1])

        if not king.moves:
            for row in range(ROWS):
                for col in range(COLS):
                    if self.squares[row][col].has_pice() and self.squares[row][col].pice.color == color:
                        pice = self.squares[row][col].pice

                        self.calc_valid_moves(pice, row, col)

                        if pice.moves:
                            return False
            
            return True
        
        return False
        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].pice, Pawn):
                    self.squares[row][col].pice.en_passant = False
        
        pice.en_passant = True