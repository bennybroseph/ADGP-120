import time

import pygame.font

from System import System
from Graphics import Graphics


class FPS(object):

    _clock = None

    _current_time = None
    _previous_time = None
    _delta_time = None

    _current_frames = None

    _current_fps = None

    _last_update = None

    _font = None

    _surface = None
    _surface_rect = None

    _outline_surface = None
    _outline_surface_rect = None

    @staticmethod
    def init():
        FPS._clock = pygame.time.Clock()

        FPS._current_time = time.time()
        FPS._previous_time = FPS._current_time
        FPS._delta_time = 0

        FPS._current_frames = 0
        FPS._current_fps = FPS._current_frames
        FPS._last_update = 0

        FPS._font = pygame.font.SysFont("Pokemon_FireRed.ttf", 24)

        FPS._surface = pygame.Surface((0, 0))
        FPS._surface_rect = FPS._surface.get_rect()

        FPS._outline_surface = pygame.Surface((0, 0))
        FPS._outline_surface_rect = FPS._surface.get_rect()

    @staticmethod
    def delta_time():
        return FPS._delta_time

    @staticmethod
    def update():
        FPS._current_frames += 1

        FPS._previous_time = FPS._current_time
        FPS._current_time = time.time()

        FPS._delta_time = FPS._current_time - FPS._previous_time
        FPS._last_update += FPS._delta_time

        if FPS._last_update >= 1:
            FPS._current_fps = FPS._current_frames

            FPS._current_frames = 0
            FPS._last_update = 0

            FPS._surface = FPS._font.render("FPS: " + str(FPS._current_fps), 1, System.Color.WHITE)
            FPS._outline_surface = FPS._font.render("FPS: " + str(FPS._current_fps), 1, System.Color.BLACK)

            FPS._surface_rect = FPS._surface.get_rect()
            FPS._surface_rect.move_ip(Graphics.get_resolution()[0] / 2, 15)

            FPS._outline_surface_rect = FPS._surface.get_rect()

        # Draws an outline for the FPS 
        Graphics.draw(FPS._outline_surface,
                      pygame.Rect(FPS._surface_rect.x + 1, FPS._surface_rect.y,
                                  FPS._surface_rect.width, FPS._surface_rect.height))
        Graphics.draw(FPS._outline_surface,
                      pygame.Rect(FPS._surface_rect.x - 1, FPS._surface_rect.y,
                                  FPS._surface_rect.width, FPS._surface_rect.height))
        Graphics.draw(FPS._outline_surface,
                      pygame.Rect(FPS._surface_rect.x, FPS._surface_rect.y + 1,
                                  FPS._surface_rect.width, FPS._surface_rect.height))
        Graphics.draw(FPS._outline_surface,
                      pygame.Rect(FPS._surface_rect.x, FPS._surface_rect.y - 1,
                                  FPS._surface_rect.width, FPS._surface_rect.height))

        Graphics.draw(FPS._outline_surface,
                      pygame.Rect(FPS._surface_rect.x + 1, FPS._surface_rect.y + 1,
                                  FPS._surface_rect.width, FPS._surface_rect.height))
        Graphics.draw(FPS._outline_surface,
                      pygame.Rect(FPS._surface_rect.x - 1, FPS._surface_rect.y - 1,
                                  FPS._surface_rect.width, FPS._surface_rect.height))
        Graphics.draw(FPS._outline_surface,
                      pygame.Rect(FPS._surface_rect.x - 1, FPS._surface_rect.y + 1,
                                  FPS._surface_rect.width, FPS._surface_rect.height))
        Graphics.draw(FPS._outline_surface,
                      pygame.Rect(FPS._surface_rect.x + 1, FPS._surface_rect.y - 1,
                                  FPS._surface_rect.width, FPS._surface_rect.height))
        # End of Outline

        Graphics.draw(FPS._surface, FPS._surface_rect)

        FPS._clock.tick(System.Display.TARGET_FPS)
