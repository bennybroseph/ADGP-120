import os
import copy

import Tkinter
import pygame
import pygame.font

from System import System


class Graphics(object):
    s_Self = None  # Singleton instance

    def __init__(self):
        # Prevent the application from creating multiple graphics instances
        if Graphics.s_Self != None:
            raise Exception('This singleton class already exists')

    # Reinitialize the window with the new parameters
    def resize_window(self, dimensions=(0, 0), flags=0, depth=0):
        self.m_Dimensions = dimensions  # Update the 'm_Dimensions' variable
        self.m_Scale = (
            (float(self.m_Dimensions[0]) / float(self.m_Resolution[0])),  # Sets the scale for width
            (float(self.m_Dimensions[1]) / float(self.m_Resolution[1])))  # Sets the scale for height
        # Since the window was changed, update the 'm_Screen' variable to match
        self.m_Screen = pygame.display.set_mode(dimensions, flags,
                                                depth)

        pygame.display.update()  # Lets pygame know the window has been changed

    # Static method which needs to be called in order to initialize the 'Graphics' class
    @staticmethod
    def init():
        Graphics.s_Self = Graphics()  # Create new instance of 'Graphics' and set the singleton variable to it

        root = Tkinter.Tk()  # Grab Tkinter top-level widget in order to grab the monitor's current resolution
        Graphics.s_Self.m_MonitorResolution = (
            root.winfo_screenwidth(), root.winfo_screenheight())  # Store the resolution into 'm_MonitorResolution'

        # Center's the window based on the monitor's resolution
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (
            (Graphics.s_Self.m_MonitorResolution[0] / 2) - (System.Display.WINDOW_WIDTH / 2),
            (Graphics.s_Self.m_MonitorResolution[1] / 2) - (System.Display.WINDOW_HEIGHT / 2))

        pygame.init()  # Initializes everything for pygame including pygame.font

        # 'Graphics' will scale images to a certain resolution set here
        Graphics.s_Self.m_Resolution = System.Display.RESOLUTION_SIZE
        Graphics.s_Self.resize_window(System.Display.WINDOW_SIZE)  # Sets up the window

        Graphics.s_Self.m_IsFullscreen = False  # Keeps track of if the window is full-screen or not

        pygame.display.set_caption("AStar")  # Sets the window caption

    # Toggles the window between windowed and fullscreen
    @staticmethod
    def toggle_fullscreen():
        if Graphics.s_Self.m_IsFullscreen:
            Graphics.s_Self.resize_window(System.Display.WINDOW_SIZE)
        else:
            Graphics.s_Self.resize_window(System.Display.FULLSCREEN_SIZE, pygame.FULLSCREEN)

        Graphics.s_Self.m_IsFullscreen = not Graphics.s_Self.m_IsFullscreen
        pygame.display.update()

    # Draws centered images to the screen scaled to against the resolution
    @staticmethod
    def draw(surface, rect):
        # Attempts to 'smoothscale' the image first, but if it cannot due to color-depth...
        try:
            surface = pygame.transform.smoothscale(surface, (
                int(rect.width * Graphics.s_Self.m_Scale[0]), int(rect.height * Graphics.s_Self.m_Scale[1])))
        # Then it does a standard scale
        except ValueError:
            surface = pygame.transform.scale(surface, (
                int(rect.width * Graphics.s_Self.m_Scale[0]), int(rect.height * Graphics.s_Self.m_Scale[1])))

        # Copy the rect since it is passed by reference automatically and we don't want to change it
        temp_rect = copy.copy(rect)

        temp_rect.x -= rect.width / 2
        temp_rect.y -= rect.height / 2

        temp_rect.x *= Graphics.s_Self.m_Scale[0]
        temp_rect.y *= Graphics.s_Self.m_Scale[1]

        Graphics.s_Self.m_Screen.blit(surface, temp_rect)  # Blit the image to the screen surface

    # Draws a centered rectangle to the screen with the given parameters and scales it against the resolution
    @staticmethod
    def draw_rect(color, rect, width=0):
        # Copy the rect since it is passed by reference automatically and we don't want to change it
        temp_rect = copy.copy(rect)

        temp_rect.x *= Graphics.s_Self.m_Scale[0]
        temp_rect.y *= Graphics.s_Self.m_Scale[1]

        temp_rect.width *= Graphics.s_Self.m_Scale[0]
        temp_rect.height *= Graphics.s_Self.m_Scale[1]

        pygame.draw.rect(Graphics.s_Self.m_Screen, color, temp_rect,
                         width)  # Draw the rectangle to the screen surface

    # Draws a line to the screen with the given parameters and scales it to the resolution
    @staticmethod
    def draw_line(color, start, end, width=1):
        start = (
            start[0] * Graphics.s_Self.m_Scale[0],
            start[1] * Graphics.s_Self.m_Scale[1])
        end = (
            end[0] * Graphics.s_Self.m_Scale[0],
            end[1] * Graphics.s_Self.m_Scale[1])

        pygame.draw.line(Graphics.s_Self.m_Screen, color, start, end, width)

    # Refreshes the window to display the new content
    @staticmethod
    def flip():
        pygame.display.flip()
        Graphics.s_Self.m_Screen.fill(System.Color.BLACK)

    @staticmethod
    def get_dimensions():
        return Graphics.s_Self.m_Dimensions

    @staticmethod
    def get_resolution():
        return Graphics.s_Self.m_Resolution

    @staticmethod
    def get_scale():
        return Graphics.s_Self.m_Scale
