import copy


class GameLogic():

    def get_legal_piece_moves(position, row, col):
        piece = position[row][col]
        moves = []
        if piece == "wp":
            if col > 0 and row > 0 and position[row-1][col-1] == "--":
                moves.append([row * 10 + col, (row - 1) * 10 + (col - 1)])
            if col < 9 and row > 0 and position[row-1][col+1] == "--":
                moves.append([row * 10 + col, (row - 1) * 10 + (col + 1)])
        elif piece == "bp":
            if col > 0 and row < 9 and position[row+1][col-1] == "--":
                moves.append([row * 10 + col, (row + 1) * 10 + (col - 1)])
            if col < 9 and row < 9 and position[row+1][col+1] == "--":
                moves.append([row * 10 + col, (row + 1) * 10 + (col + 1)])
        return moves

    def get_all_piece_captures(position, white_to_move, row, col):
        captures = []

        def get_all_piece_captures_helper(position, white_to_move, row, col, move_list):
            if white_to_move:
                enemy_piece, enemy_king, enemy_ghost_piece, enemy_ghost_king, capturer = "bp", "bk", "bgp", "bgk", "wp"
            else:
                enemy_piece, enemy_king, enemy_ghost_piece, enemy_ghost_king, capturer = "wp", "wk", "wgp", "wgk", "bp"
            temp_position = position
            temp_list = move_list
            temp_list.append(row * 10 + col)
            counter = 0
            if (row > 1 and col > 1 and position[row-1][col-1] in [enemy_piece, enemy_king]
                    and position[row-2][col-2] == "--"):
                temp_position[row][col] = "--"
                if temp_position[row-1][col-1] == enemy_piece:
                    temp_position[row-1][col-1] = enemy_ghost_piece
                else:
                    temp_position[row-1][col-1] = enemy_ghost_king
                temp_position[row-2][col-2] = capturer
                counter += 1
                get_all_piece_captures_helper(temp_position, white_to_move, row-2, col-2, temp_list)
                temp_position[row][col] = capturer
                if temp_position[row-1][col-1] == enemy_ghost_piece:
                    temp_position[row-1][col-1] = enemy_piece
                else:
                    temp_position[row-1][col-1] = enemy_king
                temp_position[row-2][col-2] = "--"
            if (row > 1 and col < 8 and position[row-1][col+1] in [enemy_piece, enemy_king]
                    and position[row-2][col+2] == "--"):
                temp_position[row][col] = "--"
                if temp_position[row-1][col+1] == enemy_piece:
                    temp_position[row-1][col+1] = enemy_ghost_piece
                else:
                    temp_position[row-1][col+1] = enemy_ghost_king
                temp_position[row-2][col+2] = capturer
                counter += 1
                get_all_piece_captures_helper(temp_position, white_to_move, row-2, col+2, temp_list)
                temp_position[row][col] = capturer
                if temp_position[row-1][col+1] == enemy_ghost_piece:
                    temp_position[row-1][col+1] = enemy_piece
                else:
                    temp_position[row-1][col+1] = enemy_king
                temp_position[row-2][col+2] = "--"
            if (row < 8 and col < 8 and position[row+1][col+1] in [enemy_piece, enemy_king]
                    and position[row+2][col+2] == "--"):
                temp_position[row][col] = "--"
                if temp_position[row+1][col+1] == enemy_piece:
                    temp_position[row+1][col+1] = enemy_ghost_piece
                else:
                    temp_position[row+1][col+1] = enemy_ghost_king
                temp_position[row+2][col+2] = capturer
                counter += 1
                get_all_piece_captures_helper(temp_position, white_to_move, row+2, col+2, temp_list)
                temp_position[row][col] = capturer
                if temp_position[row+1][col+1] == enemy_ghost_piece:
                    temp_position[row+1][col+1] = enemy_piece
                else:
                    temp_position[row+1][col+1] = enemy_king
                temp_position[row+2][col+2] = "--"
            if (row < 8 and col > 1 and position[row+1][col-1] in [enemy_piece, enemy_king]
                    and position[row+2][col-2] == "--"):
                temp_position[row][col] = "--"
                if temp_position[row+1][col-1] == enemy_piece:
                    temp_position[row+1][col-1] = enemy_ghost_piece
                else:
                    temp_position[row+1][col-1] = enemy_ghost_king
                temp_position[row+2][col-2] = capturer
                counter += 1
                get_all_piece_captures_helper(temp_position, white_to_move, row+2, col-2, temp_list)
                temp_position[row][col] = capturer
                if temp_position[row+1][col-1] == enemy_ghost_piece:
                    temp_position[row+1][col-1] = enemy_piece
                else:
                    temp_position[row+1][col-1] = enemy_king
                temp_position[row+2][col-2] = "--"
            if counter == 0 and len(temp_list) > 1:
                captures.append(copy.deepcopy(temp_list))
            return temp_list.pop()
        get_all_piece_captures_helper(position, white_to_move, row, col, [])
        return captures

    def get_all_king_captures(position, white_to_move, row, col):
        captures = []

        def get_all_king_captures_helper(position, white_to_move, row, col, move_list):
            if white_to_move:
                enemy_piece, enemy_king, enemy_ghost_piece, enemy_ghost_king, capturer = "bp", "bk", "bgp", "bgk", "wk"
            else:
                enemy_piece, enemy_king, enemy_ghost_piece, enemy_ghost_king, capturer = "wp", "wk", "wgp", "wgk", "bk"
            temp_list = move_list
            temp_position = position
            temp_row = row
            temp_col = col
            counter = 0
            temp_list.append(row * 10 + col)
            while temp_row > 1 and temp_col < 8:
                if temp_position[temp_row-1][temp_col+1] in [enemy_piece, enemy_king]:
                    if temp_position[temp_row-2][temp_col+2] == "--":
                        new_row = temp_row-2
                        new_c = temp_col+2
                        while new_row >= 0 and new_c <= 9 and temp_position[new_row][new_c] == "--":
                            temp_position[row][col] = "--"
                            if temp_position[temp_row-1][temp_col+1] == enemy_piece:
                                temp_position[temp_row-1][temp_col+1] = enemy_ghost_piece
                            else:
                                temp_position[temp_row-1][temp_col+1] = enemy_ghost_king
                            temp_position[new_row][new_c] = capturer
                            get_all_king_captures_helper(temp_position, white_to_move, new_row, new_c, temp_list)
                            counter += 1
                            temp_position[row][col] = capturer
                            if temp_position[temp_row-1][temp_col+1] == enemy_ghost_piece:
                                temp_position[temp_row-1][temp_col+1] = enemy_piece
                            else:
                                temp_position[temp_row-1][temp_col+1] = enemy_king
                            temp_position[new_row][new_c] = "--"
                            new_row -= 1
                            new_c += 1
                        break
                    else:
                        break
                elif temp_position[temp_row-1][temp_col+1] == "--":
                    temp_row -= 1
                    temp_col += 1
                else:
                    break
            temp_row = row
            temp_col = col

            while temp_row > 1 and temp_col > 1:
                if temp_position[temp_row-1][temp_col-1] in [enemy_piece, enemy_king]:
                    if temp_position[temp_row-2][temp_col-2] == "--":
                        new_row = temp_row - 2
                        new_c = temp_col - 2
                        while new_row >= 0 and new_c >= 0 and temp_position[new_row][new_c] == "--":
                            temp_position[row][col] = "--"
                            if temp_position[temp_row-1][temp_col-1] == enemy_piece:
                                temp_position[temp_row-1][temp_col-1] = enemy_ghost_piece
                            else:
                                temp_position[temp_row-1][temp_col-1] = enemy_ghost_king
                            temp_position[new_row][new_c] = capturer
                            get_all_king_captures_helper(temp_position, white_to_move, new_row, new_c, temp_list)
                            counter += 1
                            temp_position[row][col] = capturer
                            if temp_position[temp_row-1][temp_col-1] == enemy_ghost_piece:
                                temp_position[temp_row-1][temp_col-1] = enemy_piece
                            else:
                                temp_position[temp_row-1][temp_col-1] = enemy_king
                            temp_position[new_row][new_c] = "--"
                            new_row -= 1
                            new_c -= 1
                        break
                    else:
                        break
                elif temp_position[temp_row-1][temp_col-1] == "--":
                    temp_row -= 1
                    temp_col -= 1
                else:
                    break
            temp_row = row
            temp_col = col

            while temp_row < 8 and temp_col > 1:
                if temp_position[temp_row+1][temp_col-1] in [enemy_piece, enemy_king]:
                    if temp_position[temp_row+2][temp_col-2] == "--":
                        new_row = temp_row + 2
                        new_c = temp_col - 2
                        while new_row <= 9 and new_c >= 0 and temp_position[new_row][new_c] == "--":
                            temp_position[row][col] = "--"
                            if temp_position[temp_row+1][temp_col-1] == enemy_piece:
                                temp_position[temp_row+1][temp_col-1] = enemy_ghost_piece
                            else:
                                temp_position[temp_row+1][temp_col-1] = enemy_ghost_king
                            temp_position[new_row][new_c] = capturer
                            get_all_king_captures_helper(temp_position, white_to_move, new_row, new_c, temp_list)
                            counter += 1
                            temp_position[row][col] = capturer
                            if temp_position[temp_row+1][temp_col-1] == enemy_ghost_piece:
                                temp_position[temp_row+1][temp_col-1] = enemy_piece
                            else:
                                temp_position[temp_row+1][temp_col-1] = enemy_king
                            temp_position[new_row][new_c] = "--"
                            new_row += 1
                            new_c -= 1
                        break
                    else:
                        break
                elif temp_position[temp_row+1][temp_col-1] == "--":
                    temp_row += 1
                    temp_col -= 1
                else:
                    break
            temp_row = row
            temp_col = col

            while temp_row < 8 and temp_col < 8:
                if temp_position[temp_row+1][temp_col+1] in [enemy_piece, enemy_king]:
                    if temp_position[temp_row+2][temp_col+2] == "--":
                        new_row = temp_row + 2
                        new_c = temp_col + 2
                        while new_row <= 9 and new_c <= 9 and temp_position[new_row][new_c] == "--":
                            temp_position[row][col] = "--"
                            if temp_position[temp_row+1][temp_col+1] == enemy_piece:
                                temp_position[temp_row+1][temp_col+1] = enemy_ghost_piece
                            else:
                                temp_position[temp_row+1][temp_col+1] = enemy_ghost_king
                            temp_position[new_row][new_c] = capturer
                            get_all_king_captures_helper(temp_position, white_to_move, new_row, new_c, temp_list)
                            counter += 1
                            temp_position[row][col] = capturer
                            if temp_position[temp_row+1][temp_col+1] == enemy_ghost_piece:
                                temp_position[temp_row+1][temp_col+1] = enemy_piece
                            else:
                                temp_position[temp_row+1][temp_col+1] = enemy_king
                            temp_position[new_row][new_c] = "--"
                            new_row += 1
                            new_c += 1
                        break
                    else:
                        break
                elif temp_position[temp_row+1][temp_col+1] == "--":
                    temp_row += 1
                    temp_col += 1
                else:
                    break
            temp_row = row
            temp_col = col
            if counter == 0 and len(temp_list) > 1:
                captures.append(copy.deepcopy(temp_list))
            return temp_list.pop()
        get_all_king_captures_helper(position, white_to_move, row, col, [])
        return captures

    def get_legal_king_moves(position, row, col):
        temp_row = row
        temp_col = col
        temp_row -= 1
        temp_col += 1
        moves = []
        while temp_row >= 0 and temp_col <= 9:
            if position[temp_row][temp_col] == "--":
                moves.append([row * 10 + col, temp_row * 10 + temp_col])
                temp_row -= 1
                temp_col += 1
            else:
                break
        temp_row = row
        temp_col = col
        temp_row -= 1
        temp_col -= 1
        while temp_row >= 0 and temp_col >= 0:
            if position[temp_row][temp_col] == "--":
                moves.append([row * 10 + col, temp_row * 10 + temp_col])
                temp_row -= 1
                temp_col -= 1
            else:
                break
        temp_row = row
        temp_col = col
        temp_row += 1
        temp_col -= 1
        while temp_row <= 9 and temp_col >= 0:
            if position[temp_row][temp_col] == "--":
                moves.append([row * 10 + col, temp_row * 10 + temp_col])
                temp_row += 1
                temp_col -= 1
            else:
                break
        temp_row = row
        temp_col = col
        temp_row += 1
        temp_col += 1
        while temp_row <= 9 and temp_col <= 9:
            if position[temp_row][temp_col] == "--":
                moves.append([row * 10 + col, temp_row * 10 + temp_col])
                temp_row += 1
                temp_col += 1
            else:
                break
        return moves

    def get_only_legal_captures(captures):
        longest_capture_length = max(len(capture) for capture in captures)
        return [capture for capture in captures if len(capture) == longest_capture_length]

    @staticmethod
    def get_legal_moves(position, white_to_move):
        moving_piece = "wp" if white_to_move else "bp"
        moving_king = "wk" if white_to_move else "bk"
        dimension = 10
        legal_moves = []
        for row in range(dimension):
            for col in range(dimension):
                piece = position[row][col]
                if piece == moving_piece:
                    legal_moves.extend(GameLogic.get_all_piece_captures(position, white_to_move, row, col))
                elif piece == moving_king:
                    legal_moves.extend(GameLogic.get_all_king_captures(position, white_to_move, row, col))
        if legal_moves:
            legal_moves = GameLogic.get_only_legal_captures(legal_moves)
        is_capture = True
        if not legal_moves:
            for row in range(dimension):
                for col in range(dimension):
                    piece = position[row][col]
                    if piece == moving_piece:
                        legal_moves.extend(GameLogic.get_legal_piece_moves(position, row, col))
                    elif piece == moving_king:
                        legal_moves.extend(GameLogic.get_legal_king_moves(position, row, col))
            is_capture = False
        return legal_moves, is_capture

    def get_position_with_promotions(position):
        for col in range(10):
            if position[0][col] == "wp":
                position[0][col] = "wk"
            if position[9][col] == "bp":
                position[9][col] = "bk"
        return position

    @staticmethod
    def get_position(position, move, is_capture):
        piece = position[move[0]//10][move[0] % 10]
        if is_capture:
            for i in range(len(move)-1):
                row_1, col_1 = divmod(move[i], 10)
                row_2, col_2 = divmod(move[i+1], 10)
                rows = range(row_1, row_2+1) if row_1 <= row_2 else range(row_1, row_2-1, -1)
                cols = range(col_1, col_2+1) if col_1 <= col_2 else range(col_1, col_2-1, -1)
                for row, col in zip(rows, cols):
                    position[row][col] = "--"
                position[move[i]//10][move[i] % 10] = "--"
                position[move[i+1]//10][move[i+1] % 10] = piece
        else:
            position[move[1]//10][move[1] % 10] = piece
            position[move[0]//10][move[0] % 10] = "--"
        position = GameLogic.get_position_with_promotions(position)
        return position

    @staticmethod
    def get_positions(position, white_to_move):
        moves, is_capture = GameLogic.get_legal_moves(position, white_to_move)
        return [GameLogic.get_position(copy.deepcopy(position), move, is_capture) for move in moves]
