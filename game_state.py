import copy
import random

from engine import Engine
from game_logic import GameLogic


class GameState():
    def __init__(self, position, white_to_move, opponent, playing_color, skill_level, move_list):
        self.move_list = move_list
        self.position = position
        self.positions = [copy.deepcopy(position)]
        self.white_to_move = white_to_move
        if not white_to_move and not self.move_list:
            self.move_list.append("...")
        self.legal_moves, self.is_capture = GameLogic.get_legal_moves(self.position, self.white_to_move)
        self.players = self.get_players(opponent, playing_color)

        if opponent == "Computer":
            self.engine = Engine(skill_level)

    def get_players(self, opponent, playing_color):
        if playing_color == "White":
            return ["User", opponent]
        elif playing_color == "Random":
            players = ["User", opponent]
            random.shuffle(players)
            return players
        else:
            return [opponent, "User"]

    def change_legal_moves_and_is_capture(self):
        self.legal_moves, self.is_capture = GameLogic.get_legal_moves(self.position, self.white_to_move)

    def make_move(self, move):
        self.position = GameLogic.get_position(self.position, move, self.is_capture)
        self.move_list.append(self.to_standard_format(move))

    def update_game_state(self):
        self.positions.append(copy.deepcopy(self.position))
        self.white_to_move = not self.white_to_move
        self.change_legal_moves_and_is_capture()

    def is_computer_turn(self):
        if self.white_to_move and self.players[0] == "Computer":
            return True
        if not self.white_to_move and self.players[1] == "Computer":
            return True
        return False

    def make_computer_move(self):
        move = self.engine.generate_move(self.position, self.white_to_move)
        if move is None:
            if self.legal_moves:
                self.make_move(self.legal_moves[0])
            return
        self.make_move(move)

    def click_is_legal(self, partial_move):
        for legal_move in self.legal_moves:
            if legal_move[:len(partial_move)] == partial_move:
                return True
        return False

    def move_is_legal(self, partial_move):
        for legal_move in self.legal_moves:
            if legal_move == partial_move:
                return True
        return False

    def to_standard_format(self, move):
        move = [square // 2 + 1 for square in move]
        separator = "x" if self.is_capture else "-"
        return separator.join(str(square) for square in move)

    def to_program_format(self, move):
        return [int(square) * 2 - 1 - (int(square) - 1) // 5 % 2 for square in move.replace("-", "x").split("x")]

    def standard_to_display_format(self, move_list):
        display_format_move_list = []
        for move in move_list:
            if "x" in move:
                squares = [square for square in move.split("x")]
                display_format_move_list.append(squares[0] + "x" + squares[-1])
            else:
                display_format_move_list.append(move)
        return display_format_move_list

    def game_is_over(self):
        if not self.legal_moves or self.positions.count(self.position) == 3:
            return True
        return False

    def get_result(self):
        if not self.legal_moves:
            return "Black wins!" if self.white_to_move else "White wins!"
        return "Draw!"

    def get_game_dictionary(self, game_name):
        return {"game_name": game_name, "players": self.players,
                "starting_position": self.positions[0], "move_list": self.move_list}

    def get_analysis_dictionary(self, analysis_name):
        return {"analysis_name": analysis_name, "players": self.players,
                "starting_position": self.positions[0], "move_list": self.move_list}

    def get_all_positions_of_game(self):
        positions = []
        position = self.position
        positions.append(position)
        for move in self.move_list:
            if move == "...":
                positions.append(position)
                continue
            program_format_move = self.to_program_format(move)
            is_capture = True if "x" in move else False
            position = GameLogic.get_position(copy.deepcopy(position), program_format_move, is_capture)
            positions.append(position)
        return positions

    @staticmethod
    def is_valid_game(starting_position, white_to_move, moves):
        try:
            position = copy.deepcopy(starting_position)
            game_state = GameState(starting_position, white_to_move, None, None, None, [])
            for move in moves:
                is_capture = True if "x" in move else False
                move = game_state.to_program_format(move)
                position = GameLogic.get_position(copy.deepcopy(position), move, is_capture)
                white_to_move = not white_to_move
            return True
        except:
            return False
