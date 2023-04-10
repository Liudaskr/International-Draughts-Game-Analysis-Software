import copy

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
            evaluation = self.minimax(some_position, not white_to_move, self.skill_level*2-1)
            if white_to_move and evaluation > best_evaluation:
                best_evaluation = evaluation
                best_move = move
            elif not white_to_move and evaluation < best_evaluation:
                best_evaluation = evaluation
                best_move = move
        return best_move

    def minimax(self, position, white_to_move, depth, alpha=-float("inf"), beta=float("inf")):
        if depth == 0:
            return self.evaluate_position(position)

        if white_to_move:
            max_evaluation = -float("inf")
            for position in GameLogic.get_positions(position, white_to_move):
                evaluation = self.minimax(position, False, depth-1, alpha, beta)
                max_evaluation = max(max_evaluation, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_evaluation
        else:
            min_evaluation = float("inf")
            for position in GameLogic.get_positions(position, white_to_move):
                evaluation = self.minimax(position, True, depth-1, alpha, beta)
                min_evaluation = min(min_evaluation, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_evaluation

    def evaluate_position(self, position):
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
