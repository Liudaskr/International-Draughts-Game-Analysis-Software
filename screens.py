import sys

import pygame as pg


class Window():
    def __init__(self):
        self.width = 800
        self.height = 600
        self.window_caption = "Draughts Game Analysis"

        pg.display.set_caption(self.window_caption)
        self.screen = pg.display.set_mode((self.width, self.height))


class Menu(Window):
    def __init__(self, background):
        super().__init__()
        self.background = background

        self.button_backdrop_color = (82, 85, 84)
        self.button_backdrop_width = 300
        self.button_backdrop_height = 450
        self.button_backdrop_x = 250
        self.button_backdrop_y = 75
        self.button_font = pg.font.SysFont("constantia", 28)

        self.button_color = (53, 57, 60)
        self.button_width = 200
        self.button_height = 50
        self.button_x = 300
        self.button_y = (125, 200, 275, 350, 425)
        self.button_play = pg.Rect(self.button_x, self.button_y[0], self.button_width, self.button_height)
        self.button_saved_games = pg.Rect(self.button_x, self.button_y[1], self.button_width, self.button_height)
        self.button_create_analysis = pg.Rect(self.button_x, self.button_y[2], self.button_width, self.button_height)
        self.button_view_analysis = pg.Rect(self.button_x, self.button_y[3], self.button_width, self.button_height)
        self.button_quit = pg.Rect(self.button_x, self.button_y[4], self.button_width, self.button_height)

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))

    def draw_button_backdrop(self):
        button_backdrop = pg.Rect(
            self.button_backdrop_x, self.button_backdrop_y, self.button_backdrop_width, self.button_backdrop_height)
        pg.draw.rect(self.screen, self.button_backdrop_color, button_backdrop)

    def draw_buttons(self):
        buttons = [
            (self.button_play, "Play"),
            (self.button_saved_games, "Saved Games"),
            (self.button_create_analysis, "Create Analysis"),
            (self.button_view_analysis, "View Analysis"),
            (self.button_quit, "Quit")
            ]
        white = (255, 255, 255)

        for button, _ in buttons:
            pg.draw.rect(self.screen, self.button_color, button)

        for button, text in buttons:
            pg.draw.rect(self.screen, self.button_color, button)
            button_text = self.button_font.render(text, True, white)
            button_text_rect = button_text.get_rect(center=button.center)
            self.screen.blit(button_text, button_text_rect)

    def draw_menu(self):
        self.draw_background()
        self.draw_button_backdrop()
        self.draw_buttons()

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            mouse_pos = pg.mouse.get_pos()
            if self.button_play.collidepoint(mouse_pos):
                print("You clicked Play")
            elif self.button_saved_games.collidepoint(mouse_pos):
                print("You clicked Save Game")
            elif self.button_create_analysis.collidepoint(mouse_pos):
                print("You clicked Create Analysis")
            elif self.button_view_analysis.collidepoint(mouse_pos):
                print("You clicked View Analysis")
            elif self.button_quit.collidepoint(mouse_pos):
                sys.exit()
        return self
