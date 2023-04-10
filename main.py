import sys

import pygame as pg

from managers import ImageManager
from screens import Menu, Window


def main():
    pg.init()
    window = Window(800, 600, "Draughts Game Analysis")
    screen = window.create_screen()
    image_manager = ImageManager()
    image_manager.load_images()
    menu = Menu(screen, image_manager)
    menu.draw()
    current_screen = menu
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            else:
                current_screen = current_screen.handle_event(event)
                pg.display.update()


if __name__ == "__main__":
    main()
