import pygame, pygame.font

from Graphics   import *
from System     import *
from Node       import *

class SearchSpace(object):

    def __init__(self):
        
        self.m_Nodes = [[]]

        for i in range(0, System.Graph.NUM_NODES_X):
            self.m_Nodes.append([])
            for j in range(0, System.Graph.NUM_NODES_Y):
                self.m_Nodes[i].append(Node())
        
        self.m_Start    = (0, 0)
        self.m_Goal     = (len(self.m_Nodes) - 2, len(self.m_Nodes[0]) - 1)
        
        self.CalculateHeuristic()

        self.m_SurfaceIsDirty = True

        self.m_Surface = pygame.Surface(System.Display.RESOLUTION_SIZE)
        self.m_SurfaceRect = self.m_Surface.get_rect()        

        self.m_SurfaceRect.x = System.Display.RESOLUTION_WIDTH  / 2
        self.m_SurfaceRect.y = System.Display.RESOLUTION_HEIGHT / 2

        self.m_Font = pygame.font.SysFont("Pokemon_FireRed.ttf", 18)

        self.m_FontSurfaceIsDirty = True

        self.m_FontSurface = pygame.Surface(System.Display.RESOLUTION_SIZE, pygame.SRCALPHA, 32)
        self.m_FontSurface = self.m_FontSurface.convert_alpha()
        self.m_FontSurfaceRect = self.m_FontSurface.get_rect()

        self.m_FontSurfaceRect.x = System.Display.RESOLUTION_WIDTH  / 2
        self.m_FontSurfaceRect.y = System.Display.RESOLUTION_HEIGHT / 2

    def CalculateHeuristic(self):
        for i in range(0, len(self.m_Nodes)):
            for j in range(0, len(self.m_Nodes[i])):
                self.m_Nodes[i][j].m_H = (abs(i - self.m_Goal[0]) + abs(j - self.m_Goal[1])) * 10

    def OnMouseDown(self, a_MousePos, a_Button):

        selectedIndex = (
                int((a_MousePos[0] - float(System.Graph.REMAINING_SPACE_X / 2)) / (System.Graph.NODE_WIDTH  + System.Graph.LINE_WIDTH)),
                int((a_MousePos[1] - float(System.Graph.REMAINING_SPACE_Y / 2)) / (System.Graph.NODE_HEIGHT + System.Graph.LINE_HEIGHT)))

        # Left Click
        if a_Button == 1:    
            self.m_Nodes[selectedIndex[0]][selectedIndex[1]].IsTraversable = not self.m_Nodes[selectedIndex[0]][selectedIndex[1]].IsTraversable
            self.m_SurfaceIsDirty = True

        if a_Button == 3:
            self.m_Goal = selectedIndex
            self.CalculateHeuristic()

            self.m_SurfaceIsDirty = True
            self.m_FontSurfaceIsDirty = True
    
    def OnMouseUp(self, a_MousePos, a_Button):
        None

    def Update(self):
        None

    def Draw(self):
        if self.m_SurfaceIsDirty or self.m_FontSurfaceIsDirty:            

            if self.m_FontSurfaceIsDirty:
                self.m_FontSurface.fill(System.Color.TRANSPARENT)

            for i in range(0, len(self.m_Nodes)):
                for j in range(0, len(self.m_Nodes[i])):
                    
                    if self.m_SurfaceIsDirty:        
                        nodeSurface = pygame.Surface((System.Graph.NODE_WIDTH, System.Graph.NODE_HEIGHT))

                        self.m_Nodes[i][j].m_Rect = pygame.Rect(
                                float(System.Graph.REMAINING_SPACE_X / 2) + i * (System.Graph.NODE_WIDTH + System.Graph.LINE_WIDTH), 
                                float(System.Graph.REMAINING_SPACE_Y / 2) + j * (System.Graph.NODE_HEIGHT + System.Graph.LINE_WIDTH), 
                                System.Graph.NODE_WIDTH, 
                                System.Graph.NODE_HEIGHT)

                        nodeSurface.fill(self.m_Nodes[i][j].m_Color)

                        self.m_Surface.blit(nodeSurface, self.m_Nodes[i][j].m_Rect)

                    if self.m_FontSurfaceIsDirty:
                        hTextSurface = self.m_Font.render('H: ' + str(self.m_Nodes[i][j].m_H), 1, System.Color.BLACK)
                        
                        self.m_FontSurface.blit(hTextSurface, self.m_Nodes[i][j].m_Rect)

            if self.m_SurfaceIsDirty:

                startSurface = pygame.Surface((System.Graph.NODE_WIDTH, System.Graph.NODE_HEIGHT))
                startSurface.fill(System.Color.GREEN)

                self.m_Surface.blit(startSurface, self.m_Nodes[self.m_Start[0]][self.m_Start[1]].m_Rect)

                goalSurface = pygame.Surface((System.Graph.NODE_WIDTH, System.Graph.NODE_HEIGHT))
                goalSurface.fill(System.Color.YELLOW)

                self.m_Surface.blit(goalSurface, self.m_Nodes[self.m_Goal[0]][self.m_Goal[1]].m_Rect)
           
                self.m_SurfaceIsDirty = False

            if self.m_FontSurfaceIsDirty:
                self.m_FontSurfaceIsDirty = False

        Graphics.Draw(self.m_Surface, self.m_SurfaceRect)
        Graphics.Draw(self.m_FontSurface, self.m_FontSurfaceRect)

