import pygame as pg


class Container():
    def __init__(self, x, y, width, height, color):
        self.rect = pg.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)


class Button():
    def __init__(self, x, y, width, height, text, font, font_size, rect_color, text_color):
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.font = pg.font.SysFont(font, font_size)
        self.rect_color = rect_color
        self.text_color = text_color

    def draw_rect(self, screen):
        pg.draw.rect(screen, self.rect_color, self.rect)

    def draw_text(self, screen):
        text = self.font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def draw(self, screen):
        self.draw_rect(screen)
        self.draw_text(screen)


class RadioButton():
    def __init__(
            self, x, y, width, height, text, text_color, font, font_size,
            outer_circle_radius, outer_circle_color, inner_circle_color, is_selected):

        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.text_color = text_color
        self.font = pg.font.SysFont(font, font_size)
        self.outer_circle_radius = outer_circle_radius
        self.outer_circle_color = outer_circle_color
        self.inner_circle_color = inner_circle_color
        self.is_selected = is_selected

    def draw_button(self, screen):
        circle_start_pos = (self.rect.left + self.outer_circle_radius, self.rect.centery)
        pg.draw.circle(screen, self.outer_circle_color, circle_start_pos, self.outer_circle_radius)
        if self.is_selected:
            pg.draw.circle(screen, self.inner_circle_color, circle_start_pos, self.outer_circle_radius // 2)

    def draw_text(self, screen):
        text = self.font.render(self.text, True, self.text_color)
        text_start_pos = (self.rect.left + self.outer_circle_radius*2 + 10, self.rect.centery)
        text_rect = text.get_rect(midleft=text_start_pos)
        screen.blit(text, text_rect)

    def draw(self, screen):
        self.draw_button(screen)
        self.draw_text(screen)

    def select(self, screen):
        self.is_selected = True
        self.draw_button(screen)

    def unselect(self, screen):
        self.is_selected = False
        self.draw_button(screen)


class RadioButtonGroup():
    def __init__(self, radio_buttons, is_hidden):
        self.radio_buttons = radio_buttons
        self.is_hidden = is_hidden

    def __iter__(self):
        return iter(self.radio_buttons)

    def get_selected_button(self):
        for radio_button in self.radio_buttons:
            if radio_button.is_selected:
                return radio_button

    def manage_select(self, radio_button, screen):
        if not radio_button.is_selected and not self.is_hidden:
            is_selected_radio_button = self.get_selected_button()
            is_selected_radio_button.unselect(screen)
            radio_button.select(screen)


class MoveList():
    def __init__(self, x, y, width, height, font, font_size, rect_color, text_color):
        self.scroll_depth = 0
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pg.Rect(x, y, width, height)
        self.font = pg.font.SysFont(font, font_size)
        self.rect_color = rect_color
        self.text_color = text_color
        self.move_number_rects = []
        self.move_notation_rects = []

    def draw_rect(self, screen):
        pg.draw.rect(screen, self.rect_color, self.rect)
        pg.draw.rect(screen, (0, 0, 0), self.rect, 2)

    def draw_move_text(self, screen, move_list):
        y = self.y
        number_of_moves = len(move_list)
        move_number_rects = []
        move_notation_rects = []
        for i in range(self.scroll_depth, self.scroll_depth + 12):
            if 2*i < number_of_moves:
                move_number_rects.append(pg.Rect(self.x, y, self.rect.width - 200, 25))
                text = self.font.render(str(i + 1) + ".", True, self.text_color)
                text_rect = text.get_rect()
                text_rect.center = move_number_rects[-1].center
                screen.blit(text, text_rect)
                move_notation_rects.append(pg.Rect(self.x + 50, y, self.rect.width - 150, 25))
                text = self.font.render(move_list[2*i], True, self.text_color)
                text_rect = text.get_rect()
                text_rect.center = move_notation_rects[-1].center
                screen.blit(text, text_rect)
            if 2*i + 1 < number_of_moves:
                move_notation_rects.append(pg.Rect(self.x + 150, y, self.rect.width - 150, 25))
                text = self.font.render(move_list[2*i + 1], True, self.text_color)
                text_rect = text.get_rect()
                text_rect.center = move_notation_rects[-1].center
                screen.blit(text, text_rect)
            y += 25
        self.move_number_rects = move_number_rects
        self.move_notation_rects = move_notation_rects

    def draw_move_number_rects(self, screen):
        for number_rect in self.move_number_rects:
            pg.draw.rect(screen, (0, 0, 0), number_rect, 1)

    def draw_move_notation_rects(self, screen):
        for notation_rects in self.move_notation_rects:
            pg.draw.rect(screen, (0, 0, 0), notation_rects, 1)

    def draw_current_move_rect(self, screen, move_number):
        first_move_number = self.scroll_depth * 2 + 1
        if first_move_number <= move_number < first_move_number + 24:
            pg.draw.rect(screen, (44, 140, 64), self.move_notation_rects[move_number-first_move_number], 3)

    def draw(self, screen, move_list, move_number):
        self.draw_rect(screen)
        self.draw_move_text(screen, move_list)
        self.draw_move_number_rects(screen)
        self.draw_move_notation_rects(screen)
        self.draw_current_move_rect(screen, move_number)

    def scroll_up(self):
        if self.scroll_depth > 0:
            self.scroll_depth -= 1

    def scroll_down(self):
        self.scroll_depth += 1


class InputTextField():
    def __init__(self, x, y, width, height, font, font_size, rect_color, text_color, input_text):
        self.x = x
        self.y = y
        self.rect = pg.Rect(x, y, width, height)
        self.font = pg.font.SysFont(font, font_size)
        self.rect_color = rect_color
        self.text_color = text_color
        self.is_active = False
        self.is_visible = False
        self.input_text = input_text

    def draw_input_box(self, screen):
        pg.draw.rect(screen, self.rect_color, self.rect)

    def draw_input_text(self, screen):
        text = self.font.render(self.input_text, True, self.text_color)
        screen.blit(text, (self.x + 5, self.y + 5))

    def draw(self, screen):
        self.draw_input_box(screen)
        self.draw_input_text(screen)

    def make_active(self):
        self.is_active = True

    def make_inactive(self):
        self.is_active = False

    def make_visible(self):
        self.is_visible = True

    def make_invisible(self):
        self.is_visible = False

    def add_character_to_text(self, character):
        self.input_text += character

    def remove_character_from_text(self):
        self.input_text = self.input_text[:-1]

    def input_is_empty(self):
        return not bool(self.input_text)

    def input_is_too_long(self):
        return self.font.render(self.input_text + " ", True, self.text_color).get_size()[0] > self.rect.width - 5

    def input_is_unique_game_name(self, game_names):
        if self.input_text in game_names:
            return False
        return True


class GameList():
    def __init__(self, x, y, width, height, font, font_size, rect_color, text_color):
        self.x = x
        self.y = y
        self.rect = pg.Rect(x, y, width, height)
        self.font = pg.font.SysFont(font, font_size)
        self.rect_color = rect_color
        self.text_color = text_color
        self.scroll_depth = 0

    def draw_rect(self, screen):
        pg.draw.rect(screen, self.rect_color, self.rect)

    def draw_games(self, screen, games):
        y = self.y
        number_of_games = len(games)
        game_rects = []
        for i in range(self.scroll_depth, self.scroll_depth + 10):
            if i < number_of_games:
                game_rects.append(pg.Rect(self.x, y, self.rect.width, 40))
                text = self.font.render(str(i + 1) + ".", True, self.text_color)
                screen.blit(text, (self.x + 5, y))
                text = self.font.render(games[i], True, self.text_color)
                screen.blit(text, (self.x + 50, y))
            y += 40
        self.game_rects = game_rects

    def draw(self, screen, games):
        self.draw_rect(screen)
        self.draw_games(screen, games)

    def scroll_up(self):
        if self.scroll_depth > 0:
            self.scroll_depth -= 1

    def scroll_down(self):
        self.scroll_depth += 1

    def get_game_clicked(self, mouse_pos):
        for i, game_rect in enumerate(self.game_rects):
            if game_rect.collidepoint(mouse_pos):
                return i + self.scroll_depth
        return None


class ImageRadioButton():
    def __init__(self, x, y, width, height, rect_color, selected_border_color, image, is_selected):
        self.rect = pg.Rect(x, y, width, height)
        self.rect_color = rect_color
        self.selected_border_color = selected_border_color
        self.image = image
        self.is_selected = is_selected

    def draw_rect(self, screen):
        pg.draw.rect(screen, self.rect_color, self.rect)
        if self.is_selected:
            pg.draw.rect(screen, self.selected_border_color, self.rect, 2)

    def draw_image(self, screen):
        image_rect = self.image.get_rect()
        image_rect.width = self.rect.width - 10
        image_rect.height = self.rect.height - 10
        image_rect.center = self.rect.center
        screen.blit(pg.transform.smoothscale(self.image, (image_rect.width, image_rect.height)), image_rect)

    def draw(self, screen):
        self.draw_rect(screen)
        self.draw_image(screen)

    def select(self, screen):
        self.is_selected = True
        self.draw(screen)

    def unselect(self, screen):
        self.is_selected = False
        self.draw(screen)
