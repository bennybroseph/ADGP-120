"""
File:           Core.py
Author:         Benjamin Odom
Date Created:   04-24-2016
Brief:      Main file where execution starts. In lue of an event class, this file handles user input
        and passes it along to whatever functions are registered to each action
"""
import sys
import pygame

from Graphics import Graphics
from FPS import FPS

from Drawer import Drawer


def main():
    """
    Main starting point for the program

    :return: N/A
    """
    Graphics.init()
    FPS.init()

    drawer = Drawer()

    key_down_listeners = [drawer.on_key_down]

    mouse_down_listeners = [drawer.on_mouse_down]

    mouse_up_listeners = [drawer.on_mouse_up]

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_F10:
                    Graphics.toggle_fullscreen()

                for delegate in key_down_listeners:
                    delegate(event.key, event.mod)

            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                mouse_position = (event.pos[0] / Graphics.get_scale()[0],
                                  event.pos[1] / Graphics.get_scale()[1])

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for delegate in mouse_down_listeners:
                        delegate(mouse_position, event.button)

                if event.type == pygame.MOUSEBUTTONUP:
                    for delegate in mouse_up_listeners:
                        delegate(mouse_position, event.button)

        drawer.update()

        drawer.draw()

        FPS.update()
        Graphics.flip()


main()
