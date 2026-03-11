import pygame

from const import *
from config import Config
from sound import Sound
from board import Board
from square import Square
from dragger import Dragger

class Game:

    def __init__(self):
        self.config = Config()
        self.board = Board()
        self.hovered_sqr = None
        self.dragger = Dragger()
        self.next_player = 'white'
        self.game_over = False

    def update_next_player(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'   

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col] if Square.in_range(row, col) else None

    def show_bg(self, screen):
        theme = self.config.theme

        for row in range(ROWS):
            for col in range(COLS):
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                rect = (col * SQR_SIZE, row * SQR_SIZE, SQR_SIZE, SQR_SIZE)

                pygame.draw.rect(screen, color, rect)

    def show_square_index(self, screen):
        theme = self.config.theme
        for i in range(8):
            # row index
            color = theme.bg.dark if i % 2 == 0 else theme.bg.light

            label = self.config.font.render(str(ROWS - i), 1, color)
            label_pos = (5, 5 + i * SQR_SIZE)

            screen.blit(label, label_pos)

            # col index
            color = theme.bg.dark if (i + 7) % 2 == 0 else theme.bg.light

            label = self.config.font.render(Square.get_alpha_col(i), 1, color)
            label_pos = (i * SQR_SIZE + SQR_SIZE - 20, HEIGHT - 20)

            screen.blit(label, label_pos)


    def show_pices(self, screen):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_pice() and self.board.squares[row][col].pice is not self.dragger.pice:
                    pice = self.board.squares[row][col].pice
                    pice.set_texture(size = 80)

                    img = pygame.image.load(pice.texture)
                    img_center = col * SQR_SIZE + SQR_SIZE // 2, row * SQR_SIZE + SQR_SIZE // 2

                    pice.texture_rect = img.get_rect(center = img_center)

                    screen.blit(img, pice.texture_rect)

    def show_moves(self, screen):
        theme = self.config.theme

        if self.dragger.dragging:
            pice = self.dragger.pice

            for move in pice.moves:

                color = theme.moves.light if (move.final_sqr.row + move.final_sqr.col) % 2 == 0 else theme.moves.dark

                rect = (move.final_sqr.col * SQR_SIZE, move.final_sqr.row * SQR_SIZE, SQR_SIZE, SQR_SIZE)

                pygame.draw.rect(screen, color, rect)

    def show_last_move(self, screen):
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial_sqr
            final = self.board.last_move.final_sqr

            for position in [initial, final]:
                color = theme.trace.light if (position.row + position.col) // 2 == 0 else theme.trace.dark

                rect = (position.col * SQR_SIZE, position.row * SQR_SIZE, SQR_SIZE, SQR_SIZE)

                pygame.draw.rect(screen, color, rect)

    def show_hover(self, screen):
        if self.hovered_sqr:
            color = (180, 180, 180)

            rect = (self.hovered_sqr.col  * SQR_SIZE, self.hovered_sqr.row * SQR_SIZE, SQR_SIZE, SQR_SIZE)

            pygame.draw.rect(screen, color, rect, width = 3)

    def show_game_over(self, screen, color):
        winner = 'black' if color == 'white' else 'white'
        if self.board.game_over(color):
            font = pygame.font.SysFont('Arial', 50, True)
            text = f"{winner} wins by checkmate!"
            label = font.render(text, True, (0, 0, 0)) 

            box_width = WIDTH - 30
            box_height = HEIGHT // 4

            box_rect = pygame.Rect((WIDTH - box_width) // 2, (HEIGHT - box_height) // 2, box_width, box_height)

            pygame.draw.rect(screen, (255, 255, 255), box_rect)

            text_rect = label.get_rect(center=box_rect.center)

            screen.blit(label, text_rect)

            self.game_over = True

    def change_theme(self):
        self.config.change_themes()

    def sound_effect(self, capture = False):
        if capture:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()
    
    def restart(self):
        self.__init__()