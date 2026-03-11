import os

class Pice:

    def __init__(self, name, value, color, texture = None, texture_rect = None):
        self.name = name

        self.value = value if color == 'white' else -1 * value

        self.color = color
        
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

        self.moves = []
        self.moved = False

    def set_texture(self, size = 80):
        self.texture = os.path.join(
            f'assets/images/imgs-{size}px/{self.color}_{self.name}.png')

    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []

class Pawn(Pice):
    def __init__(self, color):
        self.en_passant = False
        self.dir = -1 if color == 'white' else 1
        super().__init__('pawn', 1, color)

class Rook(Pice):
    def __init__(self, color):
        super().__init__('rook', 3, color)

class Knight(Pice):
    def __init__(self, color):
        super().__init__('knight', 2, color)

class Bishop(Pice):
    def __init__(self, color):
        super().__init__('bishop', 2, color)

class Queen(Pice):
    def __init__(self, color):
        super().__init__('queen', 10, color)

class King(Pice):
    def __init__(self, color):
        super().__init__('king', 10000, color) 