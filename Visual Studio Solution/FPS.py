import pygame.font, time

from System 	import *
from Graphics	import *

class FPS(object):
	
    s_Self = None
    
    def __init__(self):
        if FPS.s_Self != None:
            raise Exception('This singleton class already exists')
        
    @staticmethod
    def Init():
        FPS.s_Self = FPS()
        
        FPS.s_Self.m_Clock = pygame.time.Clock()
        
        FPS.s_Self.m_CurrentTime	= time.time()
        FPS.s_Self.m_PrevTime 		= FPS.s_Self.m_CurrentTime
        FPS.s_Self.m_DeltaTime 		= 0

        FPS.s_Self.m_CurrentFrames 			= 0
        FPS.s_Self.m_CurrentFPS 			= FPS.s_Self.m_CurrentFrames
        FPS.s_Self.m_TimeSinceLastUpdate 	= 0
        
        FPS.s_Self.m_Font = pygame.font.SysFont("Pokemon_FireRed.ttf", 22)

        FPS.s_Self.m_FpsText = pygame.Surface((0, 0))
        FPS.s_Self.m_FpsTextRect = FPS.s_Self.m_FpsText.get_rect()
        
    @staticmethod
    def Update():
        FPS.s_Self.m_CurrentFrames += 1
        
        FPS.s_Self.m_PrevTime = FPS.s_Self.m_CurrentTime
        FPS.s_Self.m_CurrentTime = time.time()
        
        FPS.s_Self.m_DeltaTime = FPS.s_Self.m_CurrentTime - FPS.s_Self.m_PrevTime
        FPS.s_Self.m_TimeSinceLastUpdate += FPS.s_Self.m_DeltaTime
        
        if(FPS.s_Self.m_TimeSinceLastUpdate >= 1):
            FPS.s_Self.m_CurrentFPS = FPS.s_Self.m_CurrentFrames
            
            FPS.s_Self.m_CurrentFrames = 0
            FPS.s_Self.m_TimeSinceLastUpdate = 0	
            
            FPS.s_Self.m_FpsText = FPS.s_Self.m_Font.render("FPS: " + str(FPS.s_Self.m_CurrentFPS), 1, System.Color.GREEN)
            
            FPS.s_Self.m_FpsTextRect = FPS.s_Self.m_FpsText.get_rect()		
            FPS.s_Self.m_FpsTextRect.move_ip(Graphics.GetResolution()[0] / 2, 10)
        
        Graphics.Draw(FPS.s_Self.m_FpsText, FPS.s_Self.m_FpsTextRect)
        
        FPS.s_Self.m_Clock.tick(System.Display.TARGET_FPS)