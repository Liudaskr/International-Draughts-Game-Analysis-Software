import sys

import pygame as pg

from gui_elements import Button, Container, RadioButton, RadioButtonGroup


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

        self.container = Container(250, 75, 300, 450, (82, 85, 84))

        self.buttons = [
            Button(300, 125, 200, 50, "Play", "constantia", 28, (53, 57, 60), (255, 255, 255)),
            Button(300, 200, 200, 50, "Saved Games", "constantia", 28, (53, 57, 60), (255, 255, 255)),
            Button(300, 275, 200, 50, "Create Analysis", "constantia", 28, (53, 57, 60), (255, 255, 255)),
            Button(300, 350, 200, 50, "View Analysis", "constantia", 28, (53, 57, 60), (255, 255, 255)),
            Button(300, 425, 200, 50, "Quit", "constantia", 28, (53, 57, 60), (255, 255, 255))
        ]

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))

    def draw_container(self):
        self.container.draw(self.screen)

    def draw_buttons(self):
        for button in self.buttons:
            button.draw(self.screen)

    def draw(self):
        self.draw_background()
        self.draw_container()
        self.draw_buttons()

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            mouse_pos = pg.mouse.get_pos()
            if self.buttons[0].rect.collidepoint(mouse_pos):
                game_options = GameOptions(self.background)
                game_options.draw()
                return game_options
            elif self.buttons[1].rect.collidepoint(mouse_pos):
                print("You clicked Save Game")
            elif self.buttons[2].rect.collidepoint(mouse_pos):
                print("You clicked Create Analysis")
            elif self.buttons[3].rect.collidepoint(mouse_pos):
                print("You clicked View Analysis")
            elif self.buttons[4].rect.collidepoint(mouse_pos):
                sys.exit()
        return self


class GameOptions(Window):
    def __init__(self, background):
        super().__init__()
        self.background = background

        self.container = Container(100, 50, 600, 500, (82, 85, 84))

        self.radio_button_groups = [
            RadioButtonGroup([
                RadioButton(
                    150, 100, 200, 30, "Play VS Myself", (255, 255, 255),
                    "gadugi", 18, 15, (0, 0, 0), (53, 57, 60), True),
                RadioButton(
                    150, 150, 200, 30, "Play VS Computer", (255, 255, 255),
                    "gadugi", 18, 15, (0, 0, 0), (53, 57, 60), False)
            ], False),
            RadioButtonGroup([
                RadioButton(
                    400, 100, 200, 30, "Play as White", (255, 255, 255),
                    "gadugi", 18, 15, (0, 0, 0), (53, 57, 60), True),
                RadioButton(
                    400, 150, 200, 30, "Play as Black", (255, 255, 255),
                    "gadugi", 18, 15, (0, 0, 0), (53, 57, 60), False),
                RadioButton(
                    400, 200, 200, 30, "Play as White/Black", (255, 255, 255),
                    "gadugi", 18, 15, (0, 0, 0), (53, 57, 60), False)
            ], False),
            RadioButtonGroup([
                RadioButton(
                    200, 200, 100, 30, "Level: 1", (255, 255, 255),
                    "gadugi", 18, 15, (0, 0, 0), (53, 57, 60), True),
                RadioButton(
                    200, 250, 100, 30, "Level: 2", (255, 255, 255),
                    "gadugi", 18, 15, (0, 0, 0), (53, 57, 60), False),
                RadioButton(
                    200, 300, 100, 30, "Level: 3", (255, 255, 255),
                    "gadugi", 18, 15, (0, 0, 0), (53, 57, 60), False)
            ], True)
        ]

        self.buttons = [
            Button(150, 450, 150, 50, "Cancel", "constantia", 28, (53, 57, 60), (255, 255, 255)),
            Button(500, 450, 150, 50, "Play", "constantia", 28, (53, 57, 60), (255, 255, 255))
        ]

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))

    def draw_container(self):
        self.container.draw(self.screen)

    def draw_radio_buttons(self):
        for radio_button_group in self.radio_button_groups:
            for radio_button in radio_button_group:
                if not radio_button_group.is_hidden:
                    radio_button.draw(self.screen)

    def draw_buttons(self):
        for button in self.buttons:
            button.draw(self.screen)

    def draw(self):
        self.draw_background()
        self.draw_container()
        self.draw_radio_buttons()
        self.draw_buttons()

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            mouse_pos = pg.mouse.get_pos()
            for radio_button_group in self.radio_button_groups:
                for radio_button in radio_button_group:
                    if radio_button.rect.collidepoint(mouse_pos):
                        radio_button_group.manage_select(radio_button, self.screen)
                        if radio_button.text == "Play VS Myself":
                            self.radio_button_groups[2].is_hidden = True
                            self.draw()
                        elif radio_button.text == "Play VS Computer":
                            self.radio_button_groups[2].is_hidden = False
                            self.draw()

            if self.buttons[0].rect.collidepoint(mouse_pos):
                menu = Menu(self.background)
                menu.draw()
                return menu
            elif self.buttons[1].rect.collidepoint(mouse_pos):
                print("You clicked Play")

        return self
