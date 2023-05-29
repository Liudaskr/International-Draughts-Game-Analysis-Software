import json
import tkinter as tk
import tkinter.messagebox as messagebox

import pygame as pg

from game_state import GameState


class ImageManager():
    def __init__(self):
        self.images = {}

    def load_images(self):
        self.images["background"] = pg.image.load("images/background.png")
        self.images["wp"] = pg.image.load("images/wp.png")
        self.images["bp"] = pg.image.load("images/bp.png")
        self.images["wk"] = pg.image.load("images/wk.png")
        self.images["bk"] = pg.image.load("images/bk.png")
        self.images["delete"] = pg.image.load("images/delete.png")

    def get_images(self, images):
        return {image: self.images[image] for image in images}


class JsonManager():
    @staticmethod
    def load_from_json(file_name):
        try:
            with open(file_name, 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = []
        return data

    @staticmethod
    def save_to_json(data, file_name):
        games = JsonManager.load_from_json(file_name)
        games.append(data)
        with open(file_name, 'w') as file:
            json.dump(games, file, indent=4)


class PDNManager():
    @staticmethod
    def import_game():
        folder_path = "pdns"
        window = tk.Tk()
        window.title("Save Raw Game PDN")
        game_name_label = tk.Label(window, text="Game Name:")
        game_name_label.pack()

        game_name_entry = tk.Entry(window)
        game_name_entry.pack()

        text_widget = tk.Text(window)
        text_widget.pack()

        def save_file():
            content = text_widget.get("1.0", "end-1c")
            game_names = [game['game_name'] for game in JsonManager.load_from_json("games.json")]
            game_name = game_name_entry.get()
            if game_name in game_names:
                messagebox.showerror("Error", "The game name is not unique.")
                return

            file_name = game_name + ".pdn"
            file_path = folder_path + "/" + file_name
            with open(file_path, "w") as file:
                file.write(content)
            window.destroy()
            file_path = folder_path + "/" + game_name + ".pdn"
            with open(file_path, "r") as file:
                lines = file.readlines()
                PDNManager.convert_to_json(game_name, lines)

        save_button = tk.Button(window, text="Save", command=save_file)
        save_button.pack()

        window.mainloop()

    @staticmethod
    def convert_to_json(game_name, lines):
        for i, line in enumerate(lines):
            if "]" in line:
                some_line = i
        moves = []
        data_list = lines[some_line + 2].split()
        for item in data_list:
            move = item.strip()
            if "-" in move or "x" in move:
                moves.append(move)
        moves.pop()
        for move in moves:
            if "x" in move:
                squares = move.split("x")
            elif "-" in move:
                squares = move.split("-")
            else:
                return
            for square in squares:
                if not 0 <= int(square) <= 50:
                    messagebox.showerror("Error", "The game PDN is invalid.")
                    return
        starting_position = [
            ["++", "bp", "++", "bp", "++", "bp", "++", "bp", "++", "bp"],
            ["bp", "++", "bp", "++", "bp", "++", "bp", "++", "bp", "++"],
            ["++", "bp", "++", "bp", "++", "bp", "++", "bp", "++", "bp"],
            ["bp", "++", "bp", "++", "bp", "++", "bp", "++", "bp", "++"],
            ["++", "--", "++", "--", "++", "--", "++", "--", "++", "--"],
            ["--", "++", "--", "++", "--", "++", "--", "++", "--", "++"],
            ["++", "wp", "++", "wp", "++", "wp", "++", "wp", "++", "wp"],
            ["wp", "++", "wp", "++", "wp", "++", "wp", "++", "wp", "++"],
            ["++", "wp", "++", "wp", "++", "wp", "++", "wp", "++", "wp"],
            ["wp", "++", "wp", "++", "wp", "++", "wp", "++", "wp", "++"]]
        if not GameState.is_valid_game(starting_position, True, moves):
            messagebox.showerror("Error", "The game PDN is invalid.")
            return

        data = {"game_name": game_name, "players": ["User", "Human"],
                "starting_position": starting_position, "move_list": moves}
        JsonManager.save_to_json(data, "games.json")

    @staticmethod
    def export_game(game_name, moves):
        PDNManager.convert_to_pdn(game_name, moves)
        folder_path = "pdns"
        file_name = game_name + ".pdn"
        file_path = folder_path + "/" + file_name
        window = tk.Tk()
        window.title("Open Raw Game PDN")
        text_widget = tk.Text(window)
        text_widget.pack()
        with open(file_path, "r") as file:
            content = file.read()
            text_widget.insert("1.0", content)
        window.mainloop()

    @staticmethod
    def convert_to_pdn(game_name, moves):
        folder_path = "pdns"
        file_name = game_name + ".pdn"
        file_path = folder_path + "/" + file_name

        with open(file_path, "w") as file:
            for move in moves:
                file.write(move + "\n")
