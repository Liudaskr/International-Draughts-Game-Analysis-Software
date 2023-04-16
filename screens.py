import sys

import pygame as pg

from board import Board
from game_state import GameState
from gui_elements import Button, Container, RadioButton, RadioButtonGroup


class Window():
    def __init__(self, width, height, window_caption):
        self.width = width
        self.height = height
        self.window_caption = window_caption

    def create_screen(self):
        pg.display.set_caption(self.window_caption)
        return pg.display.set_mode((self.width, self.height))


class Menu():
    def __init__(self, screen, image_manager):
        self.screen = screen
        self.image_manager = image_manager
        self.images = self.image_manager.get_images(["background"])

        self.container = Container(250, 75, 300, 450, (82, 85, 84))

        self.buttons = [
            Button(300, 125, 200, 50, "Play", "constantia", 28, (53, 57, 60), (255, 255, 255)),
            Button(300, 200, 200, 50, "Saved Games", "constantia", 28, (53, 57, 60), (255, 255, 255)),
            Button(300, 275, 200, 50, "Create Analysis", "constantia", 28, (53, 57, 60), (255, 255, 255)),
            Button(300, 350, 200, 50, "View Analysis", "constantia", 28, (53, 57, 60), (255, 255, 255)),
            Button(300, 425, 200, 50, "Quit", "constantia", 28, (53, 57, 60), (255, 255, 255))
        ]

    def draw_background(self):
        self.screen.blit(self.images["background"], (0, 0))

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
                game_options = GameOptions(self.screen, self.image_manager)
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


class GameOptions():
    def __init__(self, screen, image_manager):
        self.screen = screen
        self.image_manager = image_manager
        self.images = self.image_manager.get_images(["background"])
        self.opponent_option = "Human"
        self.side_option = "White"
        self.level_option = 1

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
        self.screen.blit(self.images["background"], (0, 0))

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
            if self.buttons[0].rect.collidepoint(mouse_pos):
                menu = Menu(self.screen, self.image_manager)
                menu.draw()
                return menu
            elif self.buttons[1].rect.collidepoint(mouse_pos):
                game_screen = GameScreen(
                    self.screen, self.image_manager, self.opponent_option, self.side_option, self.level_option)
                game_screen.draw()
                pg.display.update()
                if game_screen.game_state.is_computer_turn():
                    game_screen.game_state.make_computer_move()
                    game_screen.board.draw(self.screen, game_screen.game_state.position)
                    game_screen.game_state.update_game_state()

                return game_screen
            for radio_button_group in self.radio_button_groups:
                for radio_button in radio_button_group:
                    if radio_button.rect.collidepoint(mouse_pos):
                        radio_button_group.manage_select(radio_button, self.screen)
                        if radio_button.text == "Play VS Myself":
                            self.radio_button_groups[2].is_hidden = True
                            self.opponent_option = "Human"
                            self.draw()
                        elif radio_button.text == "Play VS Computer":
                            self.opponent_option = "Computer"
                            self.radio_button_groups[2].is_hidden = False
                            self.draw()
                        elif radio_button.text == "Play as White":
                            self.side_option = "White"
                        elif radio_button.text == "Play as Black":
                            self.side_option = "Black"
                        elif radio_button.text == "Play as White/Black":
                            self.side_option = "Random"
                        elif radio_button.text == "Level: 1":
                            self.level_option = 1
                        elif radio_button.text == "Level: 2":
                            self.level_option = 2
                        elif radio_button.text == "Level: 3":
                            self.level_option = 3
        return self


class GameScreen():
    def __init__(self, screen, image_manager, opponent, playing_color, skill_level):
        self.screen = screen
        self.image_manager = image_manager
        self.images = self.image_manager.get_images(["wp", "bp", "wk", "bk"])
        self.container = Container(0, 0, 800, 600, (82, 85, 84))

        self.game_state = GameState([
            ["++", "bp", "++", "bp", "++", "bp", "++", "bp", "++", "bp"],
            ["bp", "++", "bp", "++", "bp", "++", "bp", "++", "bp", "++"],
            ["++", "bp", "++", "bp", "++", "bp", "++", "bp", "++", "bp"],
            ["bp", "++", "bp", "++", "bp", "++", "bp", "++", "bp", "++"],
            ["++", "--", "++", "--", "++", "--", "++", "--", "++", "--"],
            ["--", "++", "--", "++", "--", "++", "--", "++", "--", "++"],
            ["++", "wp", "++", "wp", "++", "wp", "++", "wp", "++", "wp"],
            ["wp", "++", "wp", "++", "wp", "++", "wp", "++", "wp", "++"],
            ["++", "wp", "++", "wp", "++", "wp", "++", "wp", "++", "wp"],
            ["wp", "++", "wp", "++", "wp", "++", "wp", "++", "wp", "++"]],
            True, opponent, playing_color, skill_level)

        self.board = Board(
            50, 50, 400, self.game_state.players[0] == "User",
            [(238, 213, 183), (139, 115, 85), (139, 76, 57)], (104, 34, 139), 26, self.images)

        self.button = Button(100, 500, 150, 50, "Leave", "constantia", 28, (53, 57, 60), (255, 255, 255))

    def draw_container(self):
        self.container.draw(self.screen)

    def draw_board(self):
        self.board.draw(self.screen, self.game_state.position)

    def draw_buttons(self):
        self.button.draw(self.screen)

    def draw(self):
        self.draw_container()
        self.draw_board()
        self.draw_buttons()

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            mouse_pos = pg.mouse.get_pos()
            if self.board.rect.collidepoint(mouse_pos):
                clicked_square = self.board.get_square(mouse_pos)
                self.board.move_in_progress += clicked_square
                if self.game_state.click_is_legal(self.board.move_in_progress):
                    if self.game_state.move_is_legal(self.board.move_in_progress):
                        self.game_state.make_move(self.board.move_in_progress)
                        self.board.draw(self.screen, self.game_state.position)
                        pg.display.update()
                        self.game_state.update_game_state()
                        if self.game_state.is_computer_turn():
                            self.game_state.make_computer_move()
                            self.board.draw(self.screen, self.game_state.position)
                            self.game_state.update_game_state()
                        self.board.move_in_progress = []
                    else:
                        self.board.draw_with_possible_moves(
                            self.screen, self.game_state.position, self.game_state.legal_moves)
                else:
                    if self.game_state.click_is_legal(clicked_square):
                        self.board.move_in_progress = clicked_square
                        self.board.draw_with_possible_moves(
                            self.screen, self.game_state.position, self.game_state.legal_moves)
                    else:
                        self.board.draw(self.screen, self.game_state.position)
                        self.board.move_in_progress = []
            elif self.button.rect.collidepoint(mouse_pos):
                game_options = GameOptions(self.screen, self.image_manager)
                game_options.draw()
                return game_options
        return self
