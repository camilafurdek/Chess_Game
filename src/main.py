import pygame
import sys

from const import *
from game import Game
from board import Board
from square import Square
from move import Move
from pice import *

class Main:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        
        self.game = Game()


    def main_loop(self):
        game = self.game
        screen = self.screen

        board = game.board
        dragger = game.dragger

        while True:
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pices(screen)
            game.show_square_index(screen)
            game.show_hover(screen)
            game.show_game_over(screen, game.next_player)

            if not game.game_over:
                if dragger.dragging:
                    dragger.update_blit(screen)

                for event in pygame.event.get():
                    # click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        dragger.update_mousse(event.pos)

                        clicked_row = dragger.mouse_y // SQR_SIZE
                        clicked_col = dragger.mouse_x // SQR_SIZE

                        if board.squares[clicked_row][clicked_col].has_pice():
                            pice = board.squares[clicked_row][clicked_col].pice

                            # validate color
                            if pice.color == game.next_player:
                                board.calc_valid_moves(pice, clicked_row, clicked_col)

                                dragger.save_initial(event.pos)
                                dragger.dragg_pice(pice)

                                # update screen
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_moves(screen)
                                game.show_pices(screen)
                                game.show_square_index(screen)

                    # dragging
                    elif event.type == pygame.MOUSEMOTION:
                        motion_row = event.pos[1] // SQR_SIZE
                        motion_col = event.pos[0] // SQR_SIZE

                        game.set_hover(motion_row, motion_col)
                        
                        if dragger.dragging:
                            dragger.update_mousse(event.pos)

                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_hover(screen)
                            game.show_pices(screen)
                            game.show_square_index(screen)

                            dragger.update_blit(screen)
                
                    # click release
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if dragger.dragging:
                            dragger.update_mousse(event.pos)

                            released_row = dragger.mouse_y // SQR_SIZE
                            released_col = dragger.mouse_x // SQR_SIZE

                            # create possible move
                            initial = Square(dragger.initial_row, dragger.initial_col)
                            final = Square(released_row, released_col)
                            possible_move = Move(initial, final)

                            # check if move is valid
                            if board.valid_move(dragger.pice, possible_move):
                                captured = board.squares[released_row][released_col].has_pice()

                                board.move(dragger.pice,possible_move)

                                board.set_true_en_passant(dragger.pice)

                                # update next turn
                                game.update_next_player()

                                #update screen
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_pices(screen)
                                game.show_square_index(screen)

                                # play sound
                                game.sound_effect(captured)

                        dragger.undrag_pice()
                        
                    # key press
                    if event.type == pygame.KEYDOWN:
                        # change theme
                        if event.key == pygame.K_t:
                            game.change_theme()

                        # restart game
                        if event.key == pygame.K_r:
                            game.restart()

                            game = self.game

                            board = game.board
                            dragger = game.dragger

                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            
            else: 
                for event in pygame.event.get():
                    # restart game
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        game.restart()

                        game = self.game

                        board = game.board
                        dragger = game.dragger

                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            
            pygame.display.update()

main = Main()
main.main_loop()