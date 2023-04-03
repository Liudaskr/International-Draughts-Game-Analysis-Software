import sys

import pygame as pg

from images import load_images
from screens import Menu, Window


def main():
    background = load_images()
    pg.init()
    Window()
    menu = Menu(background)
    menu.draw()
    running = True
    current_screen = menu
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            else:
                current_screen = current_screen.handle_event(event)
                pg.display.update()


if __name__ == "__main__":
    main()
