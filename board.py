import pygame as pg


class Board():
    def __init__(self, x, y, size, white_at_bottom, square_colors, possible_move_color, piece_size, images):
        self.x = x
        self.y = y
        self.size = size
        self.rect = pg.Rect(self.x, self.y, self.size, self.size)
        self.white_at_bottom = white_at_bottom
        self.square_colors = square_colors
        self.possible_move_color = possible_move_color
        self.piece_size = piece_size
        self.images = images
        self.move_in_progress = []

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
                    if self.white_at_bottom:
                        rect_pos = (col * rect_size + self.x, row * rect_size + self.y)
                    else:
                        rect_pos = ((9 - col) * rect_size + self.x, (9 - row) * rect_size + self.y)
                    img_rect = scaled_image.get_rect(center=pg.Rect(*rect_pos, rect_size, rect_size).center)
                    screen.blit(scaled_image, img_rect)

    def draw(self, screen, position):
        self.draw_board(screen)
        self.draw_pieces(screen, position)

    def get_possible_squares(self, legal_moves):
        possible_squares = []
        for move in legal_moves:
            if move[:len(self.move_in_progress)] == self.move_in_progress:
                possible_squares.append(move[len(self.move_in_progress)])
        return possible_squares

    def draw_possible_squares(self, screen, possible_squares):
        dimension = 10
        rect_size = self.size // dimension
        for square in possible_squares:
            row, col = square // 10, square % 10
            if self.white_at_bottom:
                circle_pos = (col * rect_size + self.x + rect_size // 2, row * rect_size + self.y + rect_size // 2)
            else:
                circle_pos = (
                    (9 - col) * rect_size + self.x + rect_size // 2, (9 - row) * rect_size + self.y + rect_size // 2)
            pg.draw.circle(screen, self.possible_move_color, circle_pos, self.piece_size // 4)

    def draw_current_squares(self, screen, current_squares):
        dimension = 10
        rect_size = self.size // dimension
        for square in current_squares:
            row, col = square // 10, square % 10
            if self.white_at_bottom:
                rect_pos = (col * rect_size + self.x, row * rect_size + self.y)
            else:
                rect_pos = ((9 - col) * rect_size + self.x, (9 - row) * rect_size + self.y)
            pg.draw.rect(screen, self.square_colors[2], pg.Rect(*rect_pos, rect_size, rect_size))

    def draw_possible_moves(self, screen, legal_moves):
        possible_squares = self.get_possible_squares(legal_moves)
        self.draw_possible_squares(screen, possible_squares)
        self.draw_current_squares(screen, self.move_in_progress)

    def draw_with_possible_moves(self, screen, position, legal_moves):
        self.draw_board(screen)
        self.draw_possible_moves(screen, legal_moves)
        self.draw_pieces(screen, position)

    def get_square(self, mouse_pos):
        dimension = 10
        square_size = self.size // dimension
        if self.white_at_bottom:
            col = (mouse_pos[0] - self.x) // square_size
            row = (mouse_pos[1] - self.y) // square_size
        else:
            col = 9 - (mouse_pos[0] - self.x) // square_size
            row = 9 - (mouse_pos[1] - self.y) // square_size
        return [row * dimension + col]
