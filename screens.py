import sys

import pygame as pg

from board import Board
from game_state import GameState
from gui_elements import Button, Container, GameList, InputTextField, MoveList, RadioButton, RadioButtonGroup
from managers import JsonManager


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
                saved_games = SavedGames(self.screen, self.image_manager)
                saved_games.draw()
                return saved_games
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
                    game_screen.draw_move_list()
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
            True, opponent, playing_color, skill_level, [])

        self.board = Board(
            50, 50, 400, self.game_state.players[0] == "User",
            [(238, 213, 183), (139, 115, 85), (139, 76, 57)], (104, 34, 139), 26, self.images)

        self.buttons = [
            Button(100, 500, 150, 50, "Leave", "constantia", 28, (53, 57, 60), (255, 255, 255)),
            Button(550, 500, 150, 50, "Save Game", "constantia", 28, (53, 57, 60), (255, 255, 255)),
            Button(325, 525, 150, 50, "Submit", "constantia", 28, (53, 57, 60), (255, 255, 255))
        ]
        self.game_over_messages = [
            pg.font.SysFont("constantia", 30).render("White wins!", True, (255, 255, 255)),
            pg.font.SysFont("constantia", 30).render("Black wins!", True, (255, 255, 255)),
            pg.font.SysFont("constantia", 30).render("Draw!", True, (255, 255, 255))
        ]

        self.validation_error_messages = [
            pg.font.SysFont("constantia", 16).render("The name is too long!", True, (210, 43, 43)),
            pg.font.SysFont("constantia", 16).render("The name is not unique!", True, (210, 43, 43))
        ]

        self.move_list = MoveList(500, 150, 250, 300, "Courier New", 16, (220, 220, 220), (0, 0, 0))

        self.input_text_field = InputTextField(
            300, 475, 200, 30, "Courier", 15, (220, 220, 220), (0, 0, 0), "Provide a name")

    def draw_container(self):
        self.container.draw(self.screen)

    def draw_board(self):
        self.board.draw(self.screen, self.game_state.position)

    def draw_buttons(self):
        self.buttons[0].draw(self.screen)
        self.buttons[1].draw(self.screen)

    def draw_move_list(self):
        self.move_list.draw(self.screen, self.game_state.standard_to_display_format(self.game_state.move_list))

    def draw(self):
        self.draw_container()
        self.draw_board()
        self.draw_buttons()
        self.draw_move_list()

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            mouse_pos = pg.mouse.get_pos()
            if self.board.rect.collidepoint(mouse_pos) and event.button == 1:
                clicked_square = self.board.get_square(mouse_pos)
                self.board.move_in_progress += clicked_square
                if self.game_state.click_is_legal(self.board.move_in_progress):
                    if self.game_state.move_is_legal(self.board.move_in_progress):
                        self.game_state.make_move(self.board.move_in_progress)
                        self.board.draw(self.screen, self.game_state.position)
                        self.game_state.update_game_state()
                        self.draw_move_list()
                        pg.display.update()
                        self.board.move_in_progress = []
                        if self.game_state.game_is_over():
                            result = self.game_state.get_result()
                            if result == "White wins!":
                                self.screen.blit(self.game_over_messages[0], (180, 15))
                            elif result == "Black wins!":
                                self.screen.blit(self.game_over_messages[1], (180, 15))
                            else:
                                self.screen.blit(self.game_over_messages[2], (210, 15))
                            self.game_state.legal_moves = []
                        if self.game_state.is_computer_turn():
                            self.game_state.make_computer_move()
                            self.board.draw(self.screen, self.game_state.position)
                            self.game_state.update_game_state()
                            self.draw_move_list()
                            if self.game_state.game_is_over():
                                result = self.game_state.get_result()
                                if result == "White wins!":
                                    self.screen.blit(self.game_over_messages[0], (180, 15))
                                elif result == "Black wins!":
                                    self.screen.blit(self.game_over_messages[1], (180, 15))
                                else:
                                    self.screen.blit(self.game_over_messages[2], (210, 15))
                                self.game_state.legal_moves = []
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
                self.input_text_field.make_inactive()
            elif self.buttons[0].rect.collidepoint(mouse_pos):
                game_options = GameOptions(self.screen, self.image_manager)
                game_options.draw()
                return game_options
            elif self.buttons[1].rect.collidepoint(mouse_pos):
                self.input_text_field.draw(self.screen)
                self.buttons[2].draw(self.screen)
                self.input_text_field.make_inactive()
            elif self.input_text_field.rect.collidepoint(mouse_pos):
                self.input_text_field.make_active()
            elif self.move_list.rect.collidepoint(mouse_pos):
                if event.button == 4:
                    self.move_list.scroll_up()
                    self.draw_move_list()
                elif event.button == 5:
                    self.move_list.scroll_down()
                    self.draw_move_list()
                self.input_text_field.make_inactive()
            elif self.buttons[2].rect.collidepoint(mouse_pos):
                file_name = "games.json"
                game_names = [game['game_name'] for game in JsonManager.load_from_json(file_name)]
                if self.input_text_field.input_is_unique_game_name(game_names):
                    game_name = self.input_text_field.input_text
                    data = self.game_state.get_game_state_dictionary(game_name)
                    JsonManager.save_to_json(data, file_name)
                    self.draw()
                    self.input_text_field.make_inactive()
                else:
                    self.screen.fill((82, 85, 84), (315, 455, 200, 20))
                    self.screen.blit(self.validation_error_messages[1], (315, 455))
            else:
                self.input_text_field.make_inactive()
        elif event.type == pg.KEYDOWN and self.input_text_field.is_active:
            if self.input_text_field.is_active:
                if event.key == pg.K_BACKSPACE:
                    self.input_text_field.remove_character_from_text()
                    self.input_text_field.draw(self.screen)
                    self.screen.fill((82, 85, 84), (315, 455, 200, 20))
                else:
                    if self.input_text_field.input_is_too_long():
                        self.screen.fill((82, 85, 84), (315, 455, 200, 20))
                        self.screen.blit(self.validation_error_messages[0], (325, 455))
                    else:
                        self.input_text_field.add_character_to_text(event.unicode)
                        self.input_text_field.draw(self.screen)
        return self


class SavedGames():
    def __init__(self, screen, image_manager):
        self.screen = screen
        self.image_manager = image_manager
        self.container = Container(0, 0, 800, 600, (82, 85, 84))
        self.games = JsonManager.load_from_json("games.json")
        self.button = Button(100, 500, 150, 50, "Cancel", "constantia", 28, (53, 57, 60), (255, 255, 255))
        self.game_list = GameList(150, 25, 400, 400, "Courier New", 25, (220, 220, 220), (0, 0, 0))

    def draw_container(self):
        self.container.draw(self.screen)

    def draw_game_list(self):
        game_names = [game['game_name'] for game in self.games]
        self.game_list.draw(self.screen, game_names)

    def draw_button(self):
        self.button.draw(self.screen)

    def draw(self):
        self.draw_container()
        self.draw_game_list()
        self.draw_button()

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            mouse_pos = pg.mouse.get_pos()
            if self.game_list.rect.collidepoint(mouse_pos):
                if event.button == 4:
                    self.game_list.scroll_up()
                    self.draw_game_list()
                elif event.button == 5:
                    self.game_list.scroll_down()
                    self.draw_game_list()
                if event.button == 1:
                    game_number = self.game_list.get_game_clicked(mouse_pos)
                    if game_number is not None:
                        game = self.games[game_number]
                        starting_position = game["starting_position"]
                        moves = game["move_list"]
                        if moves:
                            white_to_move = False if game["move_list"][0] == "..." else True
                        else:
                            white_to_move = None
                        playing_color = "White" if game["players"][0] == "User" else "Black"
                        view_game = ViewGame(
                            self.screen, self.image_manager, starting_position, moves, white_to_move, playing_color)
                        view_game.draw()
                        return view_game
            elif self.button.rect.collidepoint(mouse_pos) and event.button == 1:
                menu = Menu(self.screen, self.image_manager)
                menu.draw()
                return menu
        return self


class ViewGame():
    def __init__(self, screen, image_manager, starting_position, moves, white_to_move, playing_color):
        self.screen = screen
        self.image_manager = image_manager
        self.images = self.image_manager.get_images(["wp", "bp", "wk", "bk"])
        self.starting_position = starting_position
        self.moves = moves
        self.white_to_move = white_to_move
        self.playing_color = playing_color
        self.current_position_index = 0

        self.container = Container(0, 0, 800, 600, (82, 85, 84))

        self.game_state = GameState(
            self.starting_position, self.white_to_move, None, self.playing_color, None, self.moves)
        self.positions = self.game_state.get_all_positions_of_game()

        self.board = Board(
            50, 50, 400, self.game_state.players[0] == "User",
            [(238, 213, 183), (139, 115, 85), (139, 76, 57)], (104, 34, 139), 26, self.images)

        self.buttons = [
            Button(100, 500, 150, 50, "Leave", "constantia", 28, (53, 57, 60), (255, 255, 255)),
            Button(520, 450, 40, 30, "<<", "constantia", 28, (53, 57, 60), (255, 255, 255)),
            Button(565, 450, 40, 30, "<", "constantia", 28, (53, 57, 60), (255, 255, 255)),
            Button(640, 450, 40, 30, ">", "constantia", 28, (53, 57, 60), (255, 255, 255)),
            Button(685, 450, 40, 30, ">>", "constantia", 28, (53, 57, 60), (255, 255, 255))
        ]

        self.move_list = MoveList(500, 150, 250, 300, "Courier New", 16, (220, 220, 220), (0, 0, 0))

    def draw_container(self):
        self.container.draw(self.screen)

    def draw_board(self):
        self.board.draw(self.screen, self.game_state.position)

    def draw_buttons(self):
        for button in self.buttons:
            button.draw(self.screen)

    def draw_move_list(self):
        self.move_list.draw(self.screen, self.game_state.standard_to_display_format(self.game_state.move_list))

    def draw(self):
        self.draw_container()
        self.draw_board()
        self.draw_buttons()
        self.draw_move_list()

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            mouse_pos = pg.mouse.get_pos()
            if event.button == 1:
                if self.buttons[0].rect.collidepoint(mouse_pos):
                    saved_games = SavedGames(self.screen, self.image_manager)
                    saved_games.draw()
                    return saved_games
                elif self.buttons[1].rect.collidepoint(mouse_pos):
                    self.current_position_index = 0
                elif self.buttons[2].rect.collidepoint(mouse_pos):
                    if self.current_position_index > 0:
                        self.current_position_index -= 1
                elif self.buttons[3].rect.collidepoint(mouse_pos):
                    if self.current_position_index < len(self.moves):
                        self.current_position_index += 1
                elif self.buttons[4].rect.collidepoint(mouse_pos):
                    self.current_position_index = len(self.moves)
                self.board.draw(self.screen, self.positions[self.current_position_index])
            elif self.move_list.rect.collidepoint(mouse_pos):
                if event.button == 4:
                    self.move_list.scroll_up()
                    self.draw_move_list()
                elif event.button == 5:
                    self.move_list.scroll_down()
                    self.draw_move_list()
        return self
