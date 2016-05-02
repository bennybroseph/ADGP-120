import os, sys, Tkinter, pygame, pygame.font, copy

from System import *

class Graphics(object):	

    s_Self = None   # Singleton instance
    
    def __init__(self):
        # Prevent the application from creating multiple graphics instances
        if Graphics.s_Self != None:
            raise Exception('This singleton class already exists')

    # Reinitialize the window with the new parameters
    def ResizeWindow(self, a_Dimensions = (0, 0), a_Flags = 0, a_Depth = 0):
        self.m_Dimensions = a_Dimensions    # Update the 'm_Dimensions' variable
        self.m_Scale = ( 
            (float(self.m_Dimensions[0]) / float(self.m_Resolution[0])),    # Sets the scale for width
            (float(self.m_Dimensions[1]) / float(self.m_Resolution[1])))    # Sets the scale for height

        self.m_Screen = pygame.display.set_mode(a_Dimensions, a_Flags, a_Depth) # Since the window was changed, update the 'm_Screen' variable to match

        pygame.display.update() # Lets pygame know the window has been changed

    # Static method which needs to be called in order to initialize the 'Graphics' class
    @staticmethod
    def Init():
        Graphics.s_Self = Graphics()    # Create new instance of 'Graphics' and set the singleton variable to it
        
        root = Tkinter.Tk() # Grab Tkinter toplevel widget in order to grab the monitor's current resolution
        Graphics.s_Self.m_MonitorResolution = (root.winfo_screenwidth(), root.winfo_screenheight()) # Store the resolution into 'm_MonitorResolution'
        
        # Center's the window based on the monitor's resolution
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (
	        (Graphics.s_Self.m_MonitorResolution[0] / 2) - (System.Display.WINDOW_WIDTH / 2),    
	        (Graphics.s_Self.m_MonitorResolution[1] / 2) - (System.Display.WINDOW_HEIGHT / 2))  
        
        pygame.init()   # Initializes everything for pygame including pygame.font
        
        Graphics.s_Self.m_Resolution 	= System.Display.RESOLUTION_SIZE    # 'Graphics' will scale images to a certain resolution set here
        Graphics.s_Self.ResizeWindow(System.Display.WINDOW_SIZE)            # Sets up the window

        Graphics.s_Self.m_IsFullscreen 	= False # Keeps track of if the window is fullscreen or not
        
        pygame.display.set_caption("AStar") # Sets the window caption
    
    # Toggles the window between windowed and fullscreen
    @staticmethod
    def ToggleFullscreen():
        if(Graphics.s_Self.m_IsFullscreen):
            Graphics.s_Self.ResizeWindow(System.Display.WINDOW_SIZE)
        else:
            Graphics.s_Self.ResizeWindow(System.Display.FULLSCREEN_SIZE, pygame.FULLSCREEN)
        
        Graphics.s_Self.m_IsFullscreen = not Graphics.s_Self.m_IsFullscreen
        pygame.display.update()
    
    # Draws centered images to the screen scaled to against the resolution
    @staticmethod
    def Draw(a_Surface, a_Rect):
        # Attempts to 'smoothscale' the image first, but if it cannot due to color-depth...
        try:
            a_Surface = pygame.transform.smoothscale(a_Surface, (int(a_Rect.width * Graphics.s_Self.m_Scale[0]), int(a_Rect.height * Graphics.s_Self.m_Scale[1])))
        # Then it does a standard scale
        except ValueError:
            a_Surface = pygame.transform.scale(a_Surface, (int(a_Rect.width * Graphics.s_Self.m_Scale[0]), int(a_Rect.height * Graphics.s_Self.m_Scale[1])))
        
        # Copy the rect since it is passed by reference automatically and we don't want to change it
        tempRect = copy.copy(a_Rect)

        tempRect.x -= a_Rect.width / 2
        tempRect.y -= a_Rect.height / 2

        tempRect.x *= Graphics.s_Self.m_Scale[0]
        tempRect.y *= Graphics.s_Self.m_Scale[1]

        Graphics.s_Self.m_Screen.blit(a_Surface, tempRect)  # Blit the image to the screen surface
    
    # Draws a centered rectangle to the screen with the given parameters and scales it against the resolution
    @staticmethod
    def DrawRect(a_Color, a_Rect, a_Width = 0):
        # Copy the rect since it is passed by reference automatically and we don't want to change it
        tempRect = copy.copy(a_Rect)

        tempRect.x *= Graphics.s_Self.m_Scale[0]
        tempRect.y *= Graphics.s_Self.m_Scale[1]

        tempRect.width  *= Graphics.s_Self.m_Scale[0]
        tempRect.height *= Graphics.s_Self.m_Scale[1]

        pygame.draw.rect(Graphics.s_Self.m_Screen, a_Color, tempRect, a_Width) # Draw the rectangle to the screen surface
    
    # Draws a line to the screen with the given parameters and scales it to the resolution
    @staticmethod
    def DrawLine(a_Color, a_Start, a_End, a_Width = 1):
        a_Start = (
            a_Start[0] * Graphics.s_Self.m_Scale[0], 
            a_Start[1] * Graphics.s_Self.m_Scale[1])
        a_End = (
            a_End[0] * Graphics.s_Self.m_Scale[0], 
            a_End[1] * Graphics.s_Self.m_Scale[1])

        pygame.draw.line(Graphics.s_Self.m_Screen, a_Color, a_Start, a_End, a_Width)

    # Refreshes the window to display the new content
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

    @staticmethod
    def GetScale():
        return Graphics.s_Self.m_Scale