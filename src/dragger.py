import pygame

from const import *

class Dragger:
    def __init__(self):
        self.mouse_x = 0 
        self.mouse_y = 0

        self.initial_row = 0
        self.initial_col = 0

        self.pice = None

        self.dragging = False
    
    def update_mousse(self, pos):
        self.mouse_x, self.mouse_y = pos

    def save_initial(self, pos):
        self.initial_row = pos[1] // SQR_SIZE
        
        self.initial_col = pos[0] // SQR_SIZE

    def dragg_pice(self, pice):
        self.pice = pice

        self.dragging = True
    
    def undrag_pice(self):
        self.pice = None

        self.dragging = False

    def update_blit(self, screen):
        self.pice.set_texture(size = 128)

        texture = self.pice.texture

        img = pygame.image.load(texture)
        img_center = (self.mouse_x, self.mouse_y)

        self.pice.texture_rect = img.get_rect(center = img_center) 

        screen.blit(img, self.pice.texture_rect)

