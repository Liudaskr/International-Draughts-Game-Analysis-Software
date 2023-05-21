import copy
import random

from game_logic import GameLogic


class Engine():
    def __init__(self, skill_level):
        self.skill_level = skill_level

    def generate_move(self, position, white_to_move):
        best_evaluation = -float("inf") if white_to_move else float("inf")
        best_move = None
        legal_moves, is_capture = GameLogic.get_legal_moves(position, white_to_move)
        for move in legal_moves:
            some_position = GameLogic.get_position(copy.deepcopy(position), move, is_capture)
            evaluation = Engine.minimax(some_position, not white_to_move, self.skill_level*2-1)
            if white_to_move and evaluation > best_evaluation:
                best_evaluation = evaluation
                best_move = move
            elif not white_to_move and evaluation < best_evaluation:
                best_evaluation = evaluation
                best_move = move
        return best_move

    @staticmethod
    def generate_moves_and_evaluations(position, white_to_move):
        moves_and_evaluations = {}
        legal_moves, is_capture = GameLogic.get_legal_moves(position, white_to_move)
        for move in legal_moves:
            some_position = GameLogic.get_position(copy.deepcopy(position), move, is_capture)
            move = [square // 2 + 1 for square in move]
            separator = "x" if is_capture else "-"
            move = separator.join(str(square) for square in move)
            if "x" in move:
                squares = [square for square in move.split("x")]
                move = squares[0] + "x" + squares[-1]
            moves_and_evaluations[move] = Engine.minimax(some_position, not white_to_move, 3)
        return moves_and_evaluations

    @staticmethod
    def minimax(position, white_to_move, depth, alpha=-float("inf"), beta=float("inf")):
        if depth == 0:
            return Engine.evaluate_position(position)

        if white_to_move:
            max_evaluation = -float("inf")
            for next_position in GameLogic.get_positions(position, white_to_move):
                evaluation = Engine.minimax(next_position, False, depth-1, alpha, beta)
                max_evaluation = max(max_evaluation, evaluation)
                alpha = max(alpha, max_evaluation)
                if beta <= alpha:
                    break
            return max_evaluation
        else:
            min_evaluation = float("inf")
            for next_position in GameLogic.get_positions(position, white_to_move):
                evaluation = Engine.minimax(next_position, True, depth-1, alpha, beta)
                min_evaluation = min(min_evaluation, evaluation)
                beta = min(beta, min_evaluation)
                if beta <= alpha:
                    break
            return min_evaluation

    @staticmethod
    def evaluate_position(position):
        dimension = 10
        evaluation = 0
        for row in range(dimension):
            for col in range(dimension):
                piece = position[row][col]
                if piece == "wp":
                    evaluation += 1
                elif piece == "bp":
                    evaluation -= 1
                elif piece == "wk":
                    evaluation += 2
                elif piece == "bk":
                    evaluation -= 2
        return evaluation
