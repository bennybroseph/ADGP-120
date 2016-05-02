import pygame, pygame.font

from Graphics   import *
from System     import *
from Node       import *

class SearchSpace(object):

    def __init__(self):
        
        self.m_Nodes = []

        self.m_Open     = []
        self.m_Closed   = []

        for i in range(0, System.Graph.NUM_NODES_X):
            self.m_Nodes.append([])
            for j in range(0, System.Graph.NUM_NODES_Y):
                self.m_Nodes[i].append(Node())
                self.m_Nodes[i][j].m_Index = (i, j)
        
        self.m_Start    = self.m_Nodes[0][0]
        self.m_Goal     = self.m_Nodes[len(self.m_Nodes) - 2][len(self.m_Nodes[0]) - 1]
        
        self.m_SolveSpeed = 1
        self.m_PathFound = False

        self.CalculateHeuristic()
        self.PathFindCoroutine = self.PathFind()

        self.m_NodesSurfaceIsDirty = True
        self.m_DisplayNodes = True

        self.m_NodesSurface = pygame.Surface(System.Display.RESOLUTION_SIZE, pygame.SRCALPHA, 32)
        self.m_NodesSurface = self.m_NodesSurface.convert_alpha()
        self.m_NodesSurfaceRect = self.m_NodesSurface.get_rect()  

        self.m_NodesSurfaceRect.x = System.Display.RESOLUTION_WIDTH  / 2
        self.m_NodesSurfaceRect.y = System.Display.RESOLUTION_HEIGHT / 2

        self.m_DebugSurfaceIsDirty = True
        self.m_DisplayDebug = True

        self.m_DebugSurface = pygame.Surface(System.Display.RESOLUTION_SIZE, pygame.SRCALPHA, 32)
        self.m_DebugSurface = self.m_DebugSurface.convert_alpha()
        self.m_DebugSurfaceRect = self.m_DebugSurface.get_rect()        

        self.m_DebugSurfaceRect.x = System.Display.RESOLUTION_WIDTH  / 2
        self.m_DebugSurfaceRect.y = System.Display.RESOLUTION_HEIGHT / 2

        self.m_Font = pygame.font.SysFont("Pokemon_FireRed.ttf", 18)

        self.m_FontSurfaceIsDirty = True
        self.m_DisplayText = True

        self.m_FontSurface = pygame.Surface(System.Display.RESOLUTION_SIZE, pygame.SRCALPHA, 32)
        self.m_FontSurface = self.m_FontSurface.convert_alpha()
        self.m_FontSurfaceRect = self.m_FontSurface.get_rect()

        self.m_FontSurfaceRect.x = System.Display.RESOLUTION_WIDTH  / 2
        self.m_FontSurfaceRect.y = System.Display.RESOLUTION_HEIGHT / 2

    def CalculateHeuristic(self):
        for x in range(0, len(self.m_Nodes)):
            for y in range(0, len(self.m_Nodes[x])):
                self.m_Nodes[x][y].m_H = (abs(self.m_Nodes[x][y].m_Index[0] - self.m_Goal.m_Index[0]) + abs(self.m_Nodes[x][y].m_Index[1] - self.m_Goal.m_Index[1])) * 10

    def PathFind(self):
        
        self.m_PathFound = False

        #set the current node
        currentNode = self.m_Start

        #self.m_Nodes -> the graph
        #currentNode -> current node
        #create open list
        #add 
        self.m_Open     = [currentNode]
        self.m_Closed   = []

        for list in self.m_Nodes:
            for node in list:
                node.m_Parent = None

        while True:

            self.m_Open.sort(key = lambda node: node.m_F)
            currentNode = self.m_Open[0]
            self.m_Open.remove(currentNode)
            self.m_Closed.append(currentNode)

            directionData = []

            directionData.append((( 0, -1), 10))
            directionData.append((( 0,  1), 10))
            directionData.append((( 1,  0), 10))
            directionData.append(((-1,  0), 10))

            directionData.append((( 1,  1), 14))
            directionData.append(((-1, -1), 14))
            directionData.append((( 1, -1), 14))
            directionData.append(((-1,  1), 14))
             
            adjacentData = []

            for direction in directionData:
                try:
                    if currentNode.m_Index[0] + direction[0][0] >= 0 and currentNode.m_Index[1] + direction[0][1] >= 0:
                        adjacentData.append({'Node': self.m_Nodes[currentNode.m_Index[0] + direction[0][0]][currentNode.m_Index[1] + direction[0][1]], 'Cost': direction[1]})
                except IndexError:
                    continue

            for adjacent in adjacentData:
                if adjacent['Node'].IsTraversable:
                    if adjacent['Node'] not in self.m_Open and adjacent['Node'] not in self.m_Closed:
                        self.m_Open.append(adjacent['Node'])

                        adjacent['Node'].m_G = adjacent['Cost']
                        adjacent['Node'].UpdateF()
                    
                        adjacent['Node'].m_Parent = currentNode
                    else:
                        if(currentNode.m_G + adjacent['Cost'] < adjacent['Node'].m_G):
                            adjacent['Node'].m_G = adjacent['Cost']
                            adjacent['Node'].UpdateF()

                            adjacent['Node'].m_Parent = currentNode
                        
                                    
            if len(self.m_Open) == 0 or self.m_Goal in self.m_Open:
                break

            if self.m_SolveSpeed > 0:
                yield
        
        self.m_PathFound = True

        self.m_NodesSurfaceIsDirty = True
        self.m_FontSurfaceIsDirty = True
        self.m_DebugSurfaceIsDirty = True

        if self.m_SolveSpeed == 0:
            yield

    def OnKeyDown(self, a_Key, a_Mod):
        if a_Key == pygame.K_F1:
            self.m_DisplayText = not self.m_DisplayText

    def OnMouseDown(self, a_MousePos, a_Button):

        selectedIndex = (
                int((a_MousePos[0] - float(System.Graph.REMAINING_SPACE_X / 2)) / (System.Graph.NODE_WIDTH  + System.Graph.LINE_WIDTH)),
                int((a_MousePos[1] - float(System.Graph.REMAINING_SPACE_Y / 2)) / (System.Graph.NODE_HEIGHT + System.Graph.LINE_HEIGHT)))

        # Left Click
        if a_Button == 1 and self.m_Nodes[selectedIndex[0]][selectedIndex[1]].IsTraversable:
            self.m_Start = self.m_Nodes[selectedIndex[0]][selectedIndex[1]]
            self.PathFindCoroutine = self.PathFind()           

        # Middle Click
        if a_Button == 2:    
            self.m_Nodes[selectedIndex[0]][selectedIndex[1]].IsTraversable = not self.m_Nodes[selectedIndex[0]][selectedIndex[1]].IsTraversable
            self.PathFindCoroutine = self.PathFind()

        # Right Click
        if a_Button == 3:
            self.m_Goal = self.m_Nodes[selectedIndex[0]][selectedIndex[1]]
            self.CalculateHeuristic()
            self.PathFindCoroutine = self.PathFind()
    
    def OnMouseUp(self, a_MousePos, a_Button):
        None

    def Update(self):
        #print self.m_PathFound
        
        try:
            self.PathFindCoroutine.next()

            self.m_NodesSurfaceIsDirty = True
            self.m_FontSurfaceIsDirty = True
            self.m_DebugSurfaceIsDirty = True
        except StopIteration:
            None

    def Draw(self):
        if self.m_NodesSurfaceIsDirty or self.m_FontSurfaceIsDirty or self.m_DebugSurfaceIsDirty:

            if self.m_NodesSurfaceIsDirty:
                self.m_NodesSurface.fill(System.Color.TRANSPARENT)
            if self.m_FontSurfaceIsDirty:
                self.m_FontSurface.fill(System.Color.TRANSPARENT)
            if self.m_DebugSurfaceIsDirty:
                self.m_DebugSurface.fill(System.Color.TRANSPARENT)

            for x in range(0, len(self.m_Nodes)):
                for y in range(0, len(self.m_Nodes[x])):
                    
                    if self.m_NodesSurfaceIsDirty:        
                        nodeSurface = pygame.Surface((System.Graph.NODE_WIDTH, System.Graph.NODE_HEIGHT))

                        self.m_Nodes[x][y].m_Rect = pygame.Rect(
                                float(System.Graph.REMAINING_SPACE_X / 2) + x * (System.Graph.NODE_WIDTH + System.Graph.LINE_WIDTH), 
                                float(System.Graph.REMAINING_SPACE_Y / 2) + y * (System.Graph.NODE_HEIGHT + System.Graph.LINE_WIDTH), 
                                System.Graph.NODE_WIDTH, 
                                System.Graph.NODE_HEIGHT)

                        self.m_Nodes[x][y].UpdateColor(self.m_Open, self.m_Closed, self.m_Start, self.m_Goal)
                        nodeSurface.fill(self.m_Nodes[x][y].m_Color)

                        self.m_NodesSurface.blit(nodeSurface, self.m_Nodes[x][y].m_Rect)

                    if self.m_DebugSurfaceIsDirty and self.m_Nodes[x][y].m_Parent != None:
                    
                        pygame.draw.line(
                            self.m_DebugSurface,
                            System.Color.BLACK, 
                            (
                                self.m_Nodes[x][y].m_Rect.x + (self.m_Nodes[x][y].m_Rect.width  / 2), 
                                self.m_Nodes[x][y].m_Rect.y + (self.m_Nodes[x][y].m_Rect.height / 2)), 
                            (
                                self.m_Nodes[x][y].m_Parent.m_Rect.x + (self.m_Nodes[x][y].m_Parent.m_Rect.width  / 2), 
                                self.m_Nodes[x][y].m_Parent.m_Rect.y + (self.m_Nodes[x][y].m_Parent.m_Rect.height / 2)))
                   

                    if self.m_FontSurfaceIsDirty and self.m_Nodes[x][y].m_IsTraversable:
                        textColor = System.Color.BLACK if self.m_Nodes[x][y] in self.m_Open else System.Color.LIGHT_GREY

                        hTextSurface = self.m_Font.render('H: ' + str(self.m_Nodes[x][y].m_H), 1, textColor)
                        hTextSurfaceRect = hTextSurface.get_rect()
                        hTextSurfaceRect = (
                            self.m_Nodes[x][y].m_Rect.x + self.m_Nodes[x][y].m_Rect.width  - hTextSurfaceRect.width, 
                            self.m_Nodes[x][y].m_Rect.y + self.m_Nodes[x][y].m_Rect.height - hTextSurfaceRect.height)

                        gTextSurface = self.m_Font.render('G: ' + str(self.m_Nodes[x][y].m_G), 1, textColor)
                        gTextSurfaceRect = hTextSurface.get_rect()
                        gTextSurfaceRect = (
                            self.m_Nodes[x][y].m_Rect.x, 
                            self.m_Nodes[x][y].m_Rect.y + self.m_Nodes[x][y].m_Rect.height - gTextSurfaceRect.height)

                        fTextSurface = self.m_Font.render('F: ' + str(self.m_Nodes[x][y].m_F), 1, textColor)
                        fTextSurfaceRect = self.m_Nodes[x][y].m_Rect

                        self.m_FontSurface.blit(hTextSurface, hTextSurfaceRect)
                        self.m_FontSurface.blit(gTextSurface, gTextSurfaceRect)
                        self.m_FontSurface.blit(fTextSurface, fTextSurfaceRect)
            
            if self.m_DisplayDebug and self.m_DebugSurfaceIsDirty:
                currentPathNode = self.m_Goal
                while currentPathNode.m_Parent != None:
                    pygame.draw.line(
                        self.m_DebugSurface,
                        System.Color.DARK_GREEN, 
                        (
                            currentPathNode.m_Rect.x + (currentPathNode.m_Rect.width  / 2), 
                            currentPathNode.m_Rect.y + (currentPathNode.m_Rect.height / 2)), 
                        (
                            currentPathNode.m_Parent.m_Rect.x + (currentPathNode.m_Parent.m_Rect.width  / 2), 
                            currentPathNode.m_Parent.m_Rect.y + (currentPathNode.m_Parent.m_Rect.height / 2)),
                        5)

                    currentPathNode = currentPathNode.m_Parent

            
            self.m_NodesSurfaceIsDirty  = False
            self.m_FontSurfaceIsDirty   = False
            self.m_DebugSurfaceIsDirty  = False

        Graphics.Draw(self.m_NodesSurface, self.m_NodesSurfaceRect)        

        if (self.m_DisplayDebug):
            Graphics.Draw(self.m_DebugSurface, self.m_DebugSurfaceRect)

        if (self.m_DisplayText):
            Graphics.Draw(self.m_FontSurface, self.m_FontSurfaceRect)
        

