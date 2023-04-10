import pygame as pg


class Board():
    def __init__(self, x, y, size, square_colors, piece_size, images):
        self.x = x
        self.y = y
        self.size = size
        self.rect = pg.Rect(self.x, self.y, self.size, self.size)
        self.square_colors = square_colors
        self.piece_size = piece_size
        self.images = images
        self.move_in_progress = []

    def find_possible_squares(self, legal_moves):
        next_moves = []
        for move in legal_moves:
            if move[:len(self.move_in_progress)] == self.move_in_progress:
                next_moves.append(move[len(self.move_in_progress)])
        return next_moves

    def draw_possible_squares(self, screen, possible_squares):
        dimension = 10
        rect_size = self.size // dimension
        for square in possible_squares:
            row = square // 10
            col = square % 10
            circle_pos = (col * rect_size + self.x + rect_size // 2, row * rect_size + self.y + rect_size // 2)
            pg.draw.circle(screen, (104, 34, 139), circle_pos, self.piece_size // 4)

    def draw_current_square(self, screen, current_square):
        dimension = 10
        rect_size = self.size // dimension
        row = current_square // 10
        col = current_square % 10
        rect_pos = (col * self.size // dimension + self.x, row * self.size // dimension + self.y)
        pg.draw.rect(screen, (139, 76, 57), pg.Rect(*rect_pos, rect_size, rect_size))

    def draw_possible_moves(self, screen, legal_moves):
        possible_squares = self.find_possible_squares(legal_moves)
        self.draw_possible_squares(screen, possible_squares)
        current_square = self.move_in_progress[-1]
        self.draw_current_square(screen, current_square)

    def draw_board(self, screen):
        dimension = 10
        rect_size = self.size // dimension
        for row in range(dimension):
            for col in range(dimension):
                color = self.square_colors[((row + col) % 2)]
                rect_pos = (col * rect_size + self.x, row * rect_size + self.y)
                pg.draw.rect(screen, color, pg.Rect(*rect_pos, rect_size, rect_size))

    def draw_pieces(self, screen, position):
        dimension = 10
        rect_size = self.size // dimension
        for row in range(dimension):
            for col in range(dimension):
                piece = position[row][col]
                if piece not in ["++", "--"]:
                    scaled_image = pg.transform.smoothscale(self.images[piece], (self.piece_size, self.piece_size))
                    rect_pos = (col * self.size // dimension + self.x, row * self.size // dimension + self.y)
                    img_rect = scaled_image.get_rect(center=pg.Rect(*rect_pos, rect_size, rect_size).center)
                    screen.blit(scaled_image, img_rect)

    def draw(self, screen, position):
        self.draw_board(screen)
        self.draw_pieces(screen, position)

    def get_square(self, mouse_pos):
        dimension = 10
        square_size = self.size // dimension
        col = (mouse_pos[0] - self.x) // square_size
        row = (mouse_pos[1] - self.y) // square_size
        return [row * dimension + col]
