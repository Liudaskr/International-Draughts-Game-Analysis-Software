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

    def find_selected_button(self):
        for radio_button in self.radio_buttons:
            if radio_button.is_selected:
                return radio_button

    def manage_select(self, radio_button, screen):
        if not radio_button.is_selected and not self.is_hidden:
            is_selected_radio_button = self.find_selected_button()
            is_selected_radio_button.unselect(screen)
            radio_button.select(screen)
