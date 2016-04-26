import os, sys, Tkinter, pygame, pygame.font

from System import *

class Graphics(object):	

	s_Self = None
	
	def __init__(self):
		if Graphics.s_Self != None:
			raise Exception('This singleton class already exists')

	@staticmethod
	def Init():
		Graphics.s_Self = Graphics()
		
		root = Tkinter.Tk()
		Graphics.s_Self.m_MonitorResolution = (root.winfo_screenwidth(), root.winfo_screenheight())
		
		os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (
			(Graphics.s_Self.m_MonitorResolution[0] / 2) - (System.Display.WINDOW_WIDTH / 2), 
			(Graphics.s_Self.m_MonitorResolution[1] / 2) - (System.Display.WINDOW_HEIGHT / 2))
		
		pygame.init()
		
		Graphics.s_Self.m_Resolution 	= System.Display.RESOLUTION_SIZE
		Graphics.s_Self.m_Ratio 		= Graphics.s_Self.m_Resolution[0] / Graphics.s_Self.m_Resolution[1]
		Graphics.s_Self.m_Dimensions 	= System.Display.WINDOW_SIZE
		Graphics.s_Self.m_Screen 		= pygame.display.set_mode(Graphics.s_Self.m_Dimensions, pygame.NOFRAME)
		Graphics.s_Self.m_IsFullscreen 	= False
		
		pygame.display.update()
		pygame.display.set_caption("AStar")
	
	@staticmethod
	def ToggleFullscreen():
		if(Graphics.s_Self.m_IsFullscreen):
			Graphics.s_Self.m_Dimensions 	= System.Display.WINDOW_SIZE
			Graphics.s_Self.m_Screen 		= pygame.display.set_mode(Graphics.s_Self.m_Dimensions, pygame.NOFRAME)
		else:
			Graphics.s_Self.m_Dimensions 	= System.Display.FULLSCREEN_SIZE
			Graphics.s_Self.m_Screen 		= pygame.display.set_mode(Graphics.s_Self.m_Dimensions, pygame.FULLSCREEN)
		
		Graphics.s_Self.m_IsFullscreen = not Graphics.s_Self.m_IsFullscreen
		pygame.display.update()
	
	@staticmethod
	def Draw(a_Surface, a_Rect):
		a_Surface = pygame.transform.scale(a_Surface, (a_Rect.width * Graphics.s_Self.m_Ratio, a_Rect.height * Graphics.s_Self.m_Ratio))
		Graphics.s_Self.m_Screen.blit(a_Surface, (a_Rect.x - (a_Rect.width / 2), a_Rect.y - (a_Rect.height / 2)))
		
	@staticmethod
	def Flip():
		pygame.display.flip()
		Graphics.s_Self.m_Screen.fill(System.Color.BLACK)
		
	@staticmethod
	def GetDimensions():
		return Graphics.s_Self.m_Dimensions
	
	@staticmethod
	def GetResolution():
		return Graphics.s_Self.m_Resolution
		