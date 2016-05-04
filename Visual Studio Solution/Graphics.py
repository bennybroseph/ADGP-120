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
        root = Tkinter.Tk()  # Grab Tkinter top-level widget in order to grab the monitor's current resolution
        monitor_resolution = (
            root.winfo_screenwidth(), root.winfo_screenheight())  # Store the resolution into 'monitor_resolution'

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

    # Reinitialize the window with the new parameters
    @staticmethod
    def _resize_window(dimensions=(0, 0), flags=0, depth=0):
        Graphics._dimensions = dimensions  # Update the '_dimensions' variable
        Graphics._scale = (
            (float(Graphics._dimensions[0]) / float(Graphics._resolution[0])),  # Sets the scale for width
            (float(Graphics._dimensions[1]) / float(Graphics._resolution[1])))  # Sets the scale for height
        # Since the window was changed, update the '_screen' variable to match
        Graphics._screen = pygame.display.set_mode(dimensions, flags, depth)

        pygame.display.update()  # Lets pygame know the window has been changed

    # Toggles the window between windowed and fullscreen
    @staticmethod
    def toggle_fullscreen():
        if Graphics._in_fullscreen:
            Graphics._resize_window(System.Display.WINDOW_SIZE)
        else:
            Graphics._resize_window(System.Display.FULLSCREEN_SIZE, pygame.FULLSCREEN)

        Graphics._in_fullscreen = not Graphics._in_fullscreen
        pygame.display.update()

    # Draws centered images to the screen scaled to against the resolution
    @staticmethod
    def draw(surface, rect):
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

    # Draws a centered rectangle to the screen with the given parameters and scales it against the resolution
    @staticmethod
    def draw_rect(color, rect, width=0):
        # Copy the rect since it is passed by reference automatically and we don't want to change it
        temp_rect = copy.copy(rect)

        temp_rect.x *= Graphics._scale[0]
        temp_rect.y *= Graphics._scale[1]

        temp_rect.width *= Graphics._scale[0]
        temp_rect.height *= Graphics._scale[1]

        pygame.draw.rect(Graphics._screen, color, temp_rect,
                         width)  # Draw the rectangle to the screen surface

    # Draws a line to the screen with the given parameters and scales it to the resolution
    @staticmethod
    def draw_line(color, start, end, width=1):
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
        pygame.display.flip()
        Graphics._screen.fill(System.Color.BLACK)

    @staticmethod
    def get_dimensions():
        return Graphics._dimensions

    @staticmethod
    def get_resolution():
        return Graphics._resolution

    @staticmethod
    def get_scale():
        return Graphics._scale
