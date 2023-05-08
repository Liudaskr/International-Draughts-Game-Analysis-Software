import json

import pygame as pg


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
