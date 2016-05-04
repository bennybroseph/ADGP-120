"""
File:           Graphics.py
Author:         Benjamin Odom
Date Created:   04-24-2016
Brief:      Graphics class used to draw surfaces, rectangles and lines to the screen
        scaled against a resolution. Handles setting up a window and anything else related to the
        window after creation
"""
import os
import copy

import Tkinter
import pygame
import pygame.font

from System import System


class Graphics(object):

    _resolution = None
    _screen = None
    _dimensions = None

    _in_fullscreen = None

    _scale = None

    @staticmethod
    def init():
        """
        Required to initialize the class and set up a window based on the variables defined in
        the 'System' class

        :return: N/A
        """
        # Grab Tkinter top-level widget in order to grab the monitor's current resolution
        root = Tkinter.Tk()
        monitor_resolution = (
            root.winfo_screenwidth(), root.winfo_screenheight())

        # Center's the window based on the monitor's resolution
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (
            (monitor_resolution[0] / 2) - (System.Display.WINDOW_WIDTH / 2),
            (monitor_resolution[1] / 2) - (System.Display.WINDOW_HEIGHT / 2))

        pygame.init()  # Initializes everything for pygame including pygame.font

        # 'Graphics' will scale images to a certain resolution set here
        Graphics._resolution = System.Display.RESOLUTION_SIZE
        Graphics._resize_window(System.Display.WINDOW_SIZE)  # Sets up the window

        Graphics._in_fullscreen = False  # Keeps track of if the window is full-screen or not

        pygame.display.set_caption("AStar")  # Sets the window caption

    @staticmethod
    def _resize_window(dimensions=(0, 0), flags=0, depth=0):
        """
        Reinitialize the window with the new parameters

        :param dimensions: new size of the window
        :param flags: pygame flags used when creating the window
        :param depth: the color depth
        :return: N/A
        """
        Graphics._dimensions = dimensions  # Update the '_dimensions' variable
        Graphics._scale = (
            (float(Graphics._dimensions[0]) / float(Graphics._resolution[0])),
            (float(Graphics._dimensions[1]) / float(Graphics._resolution[1])))
        # Since the window was changed, update the '_screen' variable to match
        Graphics._screen = pygame.display.set_mode(dimensions, flags, depth)

        pygame.display.update()  # Lets pygame know the window has been changed

    @staticmethod
    def toggle_fullscreen():
        """
        Toggles the window in and out of fullscreen using the current dimensions

        :return: N/A
        """
        if Graphics._in_fullscreen:
            Graphics._resize_window(System.Display.WINDOW_SIZE)
        else:
            Graphics._resize_window(System.Display.FULLSCREEN_SIZE, pygame.FULLSCREEN)

        Graphics._in_fullscreen = not Graphics._in_fullscreen
        pygame.display.update()

    @staticmethod
    def draw(surface, rect):
        """
        Draws centered images to the screen scaled to against the resolution

        :param surface: the surface to blit to the screen
        :param rect: the position and size of the rectangle
        :return: N/A
        """
        # Attempts to 'smoothscale' the image first, but if it cannot due to color-depth...
        try:
            surface = pygame.transform.smoothscale(surface, (
                int(rect.width * Graphics._scale[0]), int(rect.height * Graphics._scale[1])))
        # Then it does a standard scale
        except ValueError:
            surface = pygame.transform.scale(surface, (
                int(rect.width * Graphics._scale[0]), int(rect.height * Graphics._scale[1])))

        # Copy the rect since it is passed by reference automatically and we don't want to change it
        temp_rect = copy.copy(rect)

        temp_rect.x -= rect.width / 2
        temp_rect.y -= rect.height / 2

        temp_rect.x *= Graphics._scale[0]
        temp_rect.y *= Graphics._scale[1]

        Graphics._screen.blit(surface, temp_rect)  # Blit the image to the screen surface

    @staticmethod
    def draw_rect(color, rect, width=0):
        """
        Draws a centered rectangle to the screen with the
        given parameters and scales it against the resolution

        :param color: color of the rectangle to draw
        :param rect: the position and size of the rectangle
        :param width: if 0 fill rectangle otherwise defines the size of the outline
        :return: N/A
        """
        # Copy the rect since it is passed by reference automatically and we don't want to change it
        temp_rect = copy.copy(rect)

        temp_rect.x *= Graphics._scale[0]
        temp_rect.y *= Graphics._scale[1]

        temp_rect.width *= Graphics._scale[0]
        temp_rect.height *= Graphics._scale[1]

        pygame.draw.rect(Graphics._screen, color, temp_rect,
                         width)  # Draw the rectangle to the screen surface

    @staticmethod
    def draw_line(color, start, end, width=1):
        """
        Draws a line to the screen with the given parameters and scales it to the resolution

        :param color: the color of the line to draw
        :param start: where the starting point of the line is
        :param end: when the line should end
        :param width: the width of the line
        :return: N/A
        """
        start = (
            start[0] * Graphics._scale[0],
            start[1] * Graphics._scale[1])
        end = (
            end[0] * Graphics._scale[0],
            end[1] * Graphics._scale[1])

        pygame.draw.line(Graphics._screen, color, start, end, width)

    # Refreshes the window to display the new content
    @staticmethod
    def flip():
        """
        Clears the screen and displays the new content

        :return: N/A
        """
        pygame.display.flip()
        Graphics._screen.fill(System.Color.BLACK)

    @staticmethod
    def get_dimensions():
        """
        Getter for the '_dimensions' variable

        :return: N/A
        """
        return Graphics._dimensions

    @staticmethod
    def get_resolution():
        """
        Getter for the '_resolution' variable

        :return: N/A
        """
        return Graphics._resolution

    @staticmethod
    def get_scale():
        """
        Getter for the '_scale' variable

        :return: N/A
        """
        return Graphics._scale
