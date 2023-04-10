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

    def get_images(self, images):
        return {image: self.images[image] for image in images}
