import time

import pygame.font

from System import System
from Graphics import Graphics


class FPS(object):
    s_Self = None

    def __init__(self):
        if FPS.s_Self is not None:
            raise Exception('This singleton class already exists')

    @staticmethod
    def init():
        FPS.s_Self = FPS()

        FPS.s_Self.m_Clock = pygame.time.Clock()

        FPS.s_Self.m_CurrentTime = time.time()
        FPS.s_Self.m_PrevTime = FPS.s_Self.m_CurrentTime
        FPS.s_Self.m_DeltaTime = 0

        FPS.s_Self.m_CurrentFrames = 0
        FPS.s_Self.m_CurrentFPS = FPS.s_Self.m_CurrentFrames
        FPS.s_Self.m_TimeSinceLastUpdate = 0

        FPS.s_Self.m_Font = pygame.font.SysFont("Pokemon_FireRed.ttf", 24)

        FPS.s_Self.m_FpsText = pygame.Surface((0, 0))
        FPS.s_Self.m_FpsTextRect = FPS.s_Self.m_FpsText.get_rect()

        FPS.s_Self.m_FpsTextOutline = pygame.Surface((0, 0))
        FPS.s_Self.m_FpsTextOutlineRect = FPS.s_Self.m_FpsText.get_rect()

    @staticmethod
    def delta_time():
        return FPS.s_Self.m_DeltaTime

    @staticmethod
    def update():
        FPS.s_Self.m_CurrentFrames += 1

        FPS.s_Self.m_PrevTime = FPS.s_Self.m_CurrentTime
        FPS.s_Self.m_CurrentTime = time.time()

        FPS.s_Self.m_DeltaTime = FPS.s_Self.m_CurrentTime - FPS.s_Self.m_PrevTime
        FPS.s_Self.m_TimeSinceLastUpdate += FPS.s_Self.m_DeltaTime

        if FPS.s_Self.m_TimeSinceLastUpdate >= 1:
            FPS.s_Self.m_CurrentFPS = FPS.s_Self.m_CurrentFrames

            FPS.s_Self.m_CurrentFrames = 0
            FPS.s_Self.m_TimeSinceLastUpdate = 0

            FPS.s_Self.m_FpsText = FPS.s_Self.m_Font.render("FPS: " + str(FPS.s_Self.m_CurrentFPS), 1,
                                                            System.Color.WHITE)
            FPS.s_Self.m_FpsTextOutline = FPS.s_Self.m_Font.render("FPS: " + str(FPS.s_Self.m_CurrentFPS), 1,
                                                                   System.Color.BLACK)

            FPS.s_Self.m_FpsTextRect = FPS.s_Self.m_FpsText.get_rect()
            FPS.s_Self.m_FpsTextRect.move_ip(Graphics.get_resolution()[0] / 2, 15)

            FPS.s_Self.m_FpsTextOutlineRect = FPS.s_Self.m_FpsText.get_rect()

        # Draws an outline for the FPS 
        Graphics.draw(FPS.s_Self.m_FpsTextOutline,
                      pygame.Rect(FPS.s_Self.m_FpsTextRect.x + 1, FPS.s_Self.m_FpsTextRect.y,
                                  FPS.s_Self.m_FpsTextRect.width, FPS.s_Self.m_FpsTextRect.height))
        Graphics.draw(FPS.s_Self.m_FpsTextOutline,
                      pygame.Rect(FPS.s_Self.m_FpsTextRect.x - 1, FPS.s_Self.m_FpsTextRect.y,
                                  FPS.s_Self.m_FpsTextRect.width, FPS.s_Self.m_FpsTextRect.height))
        Graphics.draw(FPS.s_Self.m_FpsTextOutline,
                      pygame.Rect(FPS.s_Self.m_FpsTextRect.x, FPS.s_Self.m_FpsTextRect.y + 1,
                                  FPS.s_Self.m_FpsTextRect.width, FPS.s_Self.m_FpsTextRect.height))
        Graphics.draw(FPS.s_Self.m_FpsTextOutline,
                      pygame.Rect(FPS.s_Self.m_FpsTextRect.x, FPS.s_Self.m_FpsTextRect.y - 1,
                                  FPS.s_Self.m_FpsTextRect.width, FPS.s_Self.m_FpsTextRect.height))

        Graphics.draw(FPS.s_Self.m_FpsTextOutline,
                      pygame.Rect(FPS.s_Self.m_FpsTextRect.x + 1, FPS.s_Self.m_FpsTextRect.y + 1,
                                  FPS.s_Self.m_FpsTextRect.width, FPS.s_Self.m_FpsTextRect.height))
        Graphics.draw(FPS.s_Self.m_FpsTextOutline,
                      pygame.Rect(FPS.s_Self.m_FpsTextRect.x - 1, FPS.s_Self.m_FpsTextRect.y - 1,
                                  FPS.s_Self.m_FpsTextRect.width, FPS.s_Self.m_FpsTextRect.height))
        Graphics.draw(FPS.s_Self.m_FpsTextOutline,
                      pygame.Rect(FPS.s_Self.m_FpsTextRect.x - 1, FPS.s_Self.m_FpsTextRect.y + 1,
                                  FPS.s_Self.m_FpsTextRect.width, FPS.s_Self.m_FpsTextRect.height))
        Graphics.draw(FPS.s_Self.m_FpsTextOutline,
                      pygame.Rect(FPS.s_Self.m_FpsTextRect.x + 1, FPS.s_Self.m_FpsTextRect.y - 1,
                                  FPS.s_Self.m_FpsTextRect.width, FPS.s_Self.m_FpsTextRect.height))
        # End of Outline

        Graphics.draw(FPS.s_Self.m_FpsText, FPS.s_Self.m_FpsTextRect)

        FPS.s_Self.m_Clock.tick(System.Display.TARGET_FPS)
