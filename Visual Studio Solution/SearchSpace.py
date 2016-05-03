import pygame
import pygame.font

from System     import *
from Graphics   import *
from FPS        import *

from Node       import *

class SearchSpace(object):

    def __init__(self):
        
        self.m_Nodes = []   # The search space of nodes

        self.m_Open     = []    # Open List
        self.m_Closed   = []    # Closed List

        # Creating nodes, giving them an index in the search space, and defining their destination to be drawn on the screen
        for i in range(0, System.Graph.NUM_NODES_X):
            self.m_Nodes.append([])
            for j in range(0, System.Graph.NUM_NODES_Y):
                self.m_Nodes[i].append(Node())
                self.m_Nodes[i][j].m_Index = (i, j)

                self.m_Nodes[i][j].m_Rect = pygame.Rect(
                    float(System.Graph.REMAINING_SPACE_X / 2) + i * (System.Graph.NODE_WIDTH + System.Graph.LINE_WIDTH), 
                    float(System.Graph.REMAINING_SPACE_Y / 2) + j * (System.Graph.NODE_HEIGHT + System.Graph.LINE_WIDTH), 
                    System.Graph.NODE_WIDTH, 
                    System.Graph.NODE_HEIGHT)
        
        self.m_Start    = self.m_Nodes[0][0]                                            # The Start Node
        self.m_Goal     = self.m_Nodes[len(self.m_Nodes) - 2][len(self.m_Nodes[0]) - 1] # The Goal Node
        
        self.m_IsPaused = False             # Whether or not the application is paused
        self.m_SolveDelay           = 0.0   # How much time should be put in between each algorithm loop
        self.m_TimeSinceLastUpdate  = 0.0   # How much time has passed since the last pathing algorithm loop

        self.m_PathFound = False    # Whether or not the algorithm has finished or not

        self.CalculateHeuristic()                   # Sets the heuristic by Manhattan Distance
        self.ResetSearchSpace()
        self.PathFindCoroutine = self.PathFind()    # Creates a generator function

        #region -- NODE SURFACE --
        self.m_HelpFont = self.m_Font = pygame.font.SysFont("Pokemon_FireRed.ttf", 28)

        self.m_NodesSurfaceIsDirty  = True   # Whether or not the 'm_NodesSurface' is dirty and needs to be updated
        self.m_DisplayNodes         = True  # Whether or not to display the 'm_NodesSurface'

        self.m_NodesSurface = pygame.Surface(System.Display.RESOLUTION_SIZE, pygame.SRCALPHA, 32)   # Create a transparency enabled surface
        self.m_NodesSurface = self.m_NodesSurface.convert_alpha()
        self.m_NodesSurfaceRect = self.m_NodesSurface.get_rect()                                    # A 'pygame.rect' to use for the surface

        # Center it to the screen
        self.m_NodesSurfaceRect.x = System.Display.RESOLUTION_WIDTH  / 2
        self.m_NodesSurfaceRect.y = System.Display.RESOLUTION_HEIGHT / 2
        #endregion

        #region -- DEBUG SURFACE --
        self.m_DebugSurfaceIsDirty  = True  # Whether or not the 'm_DebugSurface' is dirty and needs to be updated
        self.m_DisplayDebug         = True  # Whether or not to display the 'm_DebugSurface'

        self.m_DebugSurface = pygame.Surface(System.Display.RESOLUTION_SIZE, pygame.SRCALPHA, 32)   # Create a transparency enabled surface
        self.m_DebugSurface = self.m_DebugSurface.convert_alpha()
        self.m_DebugSurfaceRect = self.m_DebugSurface.get_rect()                                    # A 'pygame.rect' to use for the surface

        # Center it to the screen
        self.m_DebugSurfaceRect.x = System.Display.RESOLUTION_WIDTH  / 2
        self.m_DebugSurfaceRect.y = System.Display.RESOLUTION_HEIGHT / 2
        #endregion

        #region -- FONT SURFACE --
        self.m_Font = pygame.font.SysFont("Pokemon_FireRed.ttf", 18)

        self.m_FontSurfaceIsDirty   = True  # Whether or not the 'm_FontSurface' is dirty and needs to be updated
        self.m_DisplayText          = False # Whether or not to display the 'm_FontSurface'

        self.m_FontSurface = pygame.Surface(System.Display.RESOLUTION_SIZE, pygame.SRCALPHA, 32)    # Create a transparency enabled surface
        self.m_FontSurface = self.m_FontSurface.convert_alpha()
        self.m_FontSurfaceRect = self.m_FontSurface.get_rect()                                      # A 'pygame.rect' to use for the surface

        # Center it to the screen
        self.m_FontSurfaceRect.x = System.Display.RESOLUTION_WIDTH  / 2
        self.m_FontSurfaceRect.y = System.Display.RESOLUTION_HEIGHT / 2
        #endregion

        #region -- PAUSE SURFACE --

        pauseFont = pygame.font.SysFont("lucidaconsole", 256)

        pauseText = pauseFont.render("PAUSED", 1, System.Color.WHITE)
        pauseTextRect = pauseText.get_rect()

        self.m_PauseSurface = pygame.Surface(
            (pauseTextRect.width  + 50, 
             pauseTextRect.height + 50), pygame.SRCALPHA, 32)    # Create a transparency enabled surface
        self.m_PauseSurface = self.m_PauseSurface.convert_alpha()
        self.m_PauseSurface.fill((0, 0, 0, 240))
        self.m_PauseSurfaceRect = self.m_PauseSurface.get_rect()            # A 'pygame.rect' to use for the surface

        # Center it to the screen
        self.m_PauseSurfaceRect.x = System.Display.RESOLUTION_WIDTH  / 2
        self.m_PauseSurfaceRect.y = System.Display.RESOLUTION_HEIGHT / 2        

        pauseTextRect.x = (self.m_PauseSurfaceRect.width  / 2) - (pauseTextRect.width  / 2)
        pauseTextRect.y = (self.m_PauseSurfaceRect.height / 2) - (pauseTextRect.height / 2)

        self.m_PauseSurface.blit(pauseText, pauseTextRect)

        #endregion

        #region -- HELP SURFACE

        self.m_DispalyHelp = False
        
        self.m_HelpSurface = pygame.Surface(
            (System.Display.RESOLUTION_WIDTH  / 1.15, 
             System.Display.RESOLUTION_HEIGHT / 1.15), pygame.SRCALPHA, 32)    # Create a transparency enabled surface
        self.m_HelpSurface = self.m_HelpSurface.convert_alpha()
        self.m_HelpSurface.fill((0, 0, 0, 180))
        self.m_HelpSurfaceRect = self.m_HelpSurface.get_rect()            # A 'pygame.rect' to use for the surface

        # Center it to the screen
        self.m_HelpSurfaceRect.x = System.Display.RESOLUTION_WIDTH  / 2
        self.m_HelpSurfaceRect.y = System.Display.RESOLUTION_HEIGHT / 2

        helpFont = pygame.font.SysFont("lucidaconsole", 26)
        
        helpText = []

        helpText.append([])
        helpText[0].append("P = Pause Algorithm")
        helpText[0].append("")
        helpText[0].append("1 = Toggle Node Value Text")
        helpText[0].append("2 = Toggle Debug Lines")
        helpText[0].append("")
        helpText[0].append("F1  = Toggle This Help Screen")
        helpText[0].append("F5  = Refresh Path")
        helpText[0].append("F10 = Toggle FullScreen Mode")
        helpText[0].append("")
        helpText[0].append("Left Mouse   = Move the Start Node")
        helpText[0].append("Right Mouse  = Move the Goal Node")
        helpText[0].append("Middle Mouse = Move the Start Node")
        helpText[0].append("")
        helpText[0].append("Scroll Up   = Extend Algorithm Loop Delay")
        helpText[0].append("Scroll Down = Reduce Algorithm Loop Delay")
        
        helpText.append([])
        helpText[1].append("White Box = Standard Node")
        helpText[1].append("Red Box   = Impassible Node")
        helpText[1].append("")
        helpText[1].append("Green Box  = Start Node")
        helpText[1].append("Yellow Box = Goal Node")
        helpText[1].append("Grey Box   = Closed List")
        helpText[1].append("Blue Box   = Open List")
        helpText[1].append("")
        helpText[1].append("Black Line = Child to Parent")
        helpText[1].append("Green Line = Found Path")

        i = 0.0
        for textList in helpText:

            j = 0.0
            for text in textList:
                tempSurface = helpFont.render(text, 1, System.Color.WHITE)
                tempSurfaceRect = tempSurface.get_rect()

                tempNumOfItems = len(textList) - 1 if len(textList) - 1 > 0 else 1
                tempHeight = (j * float((self.m_HelpSurfaceRect.height - 150) / tempNumOfItems)) + 75

                if i == 0:
                    tempSurfaceRect.x = 10
                    tempSurfaceRect.y = tempHeight - (tempSurfaceRect.height / 2)
                else:
                    tempSurfaceRect.x = self.m_HelpSurfaceRect.width - tempSurfaceRect.width - 10
                    tempSurfaceRect.y = tempHeight - (tempSurfaceRect.height / 2)

                self.m_HelpSurface.blit(tempSurface, tempSurfaceRect)

                j += 1
            i += 1

    #endregion

    def ResetSearchSpace(self):

        self.m_PathFound = False    # We're starting up the pathfinding function, so we have not found the path yet

        currentNode = self.m_Start  # Set the current node to the starting node

        self.m_Open     = [currentNode] # Initialize the open list with the currentNode as the only value
        self.m_Closed   = []            # Initialize the closed list as an empty list

        # Remove all parents from all nodes before starting the pathfinding
        for list in self.m_Nodes:
            for node in list:
                node.m_Parent = None

    # Calculate the Heuristic of each node based on Manhattan Distance
    def CalculateHeuristic(self):
        for x in range(0, len(self.m_Nodes)):
            for y in range(0, len(self.m_Nodes[x])):
                self.m_Nodes[x][y].m_H = (abs(self.m_Nodes[x][y].m_Index[0] - self.m_Goal.m_Index[0]) + abs(self.m_Nodes[x][y].m_Index[1] - self.m_Goal.m_Index[1])) * 10

    def PathFind(self):  

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

            if self.m_SolveDelay > 0:
                yield
        
        self.m_PathFound = True

        self.m_NodesSurfaceIsDirty = True
        self.m_FontSurfaceIsDirty = True
        self.m_DebugSurfaceIsDirty = True

    def OnKeyDown(self, a_Key, a_Mod):

        if a_Key == pygame.K_F1:
            self.m_DispalyHelp = not self.m_DispalyHelp
        if a_Key == pygame.K_F5:
            self.ResetSearchSpace()
            self.PathFindCoroutine = self.PathFind()

        if a_Key == pygame.K_1:
            self.m_DisplayText = not self.m_DisplayText
        if a_Key == pygame.K_2:
            self.m_DisplayDebug = not self.m_DisplayDebug

        if a_Key == pygame.K_p:
            self.m_IsPaused = not self.m_IsPaused

    def OnMouseDown(self, a_MousePos, a_Button):
        
        selectedIndex = (
                int((a_MousePos[0] - float(System.Graph.REMAINING_SPACE_X / 2)) / (System.Graph.NODE_WIDTH  + System.Graph.LINE_WIDTH)),
                int((a_MousePos[1] - float(System.Graph.REMAINING_SPACE_Y / 2)) / (System.Graph.NODE_HEIGHT + System.Graph.LINE_HEIGHT)))

        # Left Click
        if a_Button == 1 and self.m_Nodes[selectedIndex[0]][selectedIndex[1]].IsTraversable:
            self.m_Start = self.m_Nodes[selectedIndex[0]][selectedIndex[1]]
            self.ResetSearchSpace()
            self.PathFindCoroutine = self.PathFind()           

        # Middle Click
        if a_Button == 2:    
            self.m_Nodes[selectedIndex[0]][selectedIndex[1]].IsTraversable = not self.m_Nodes[selectedIndex[0]][selectedIndex[1]].IsTraversable

        # Right Click
        if a_Button == 3:
            self.m_Goal = self.m_Nodes[selectedIndex[0]][selectedIndex[1]]
            self.CalculateHeuristic()
            self.ResetSearchSpace()
            self.PathFindCoroutine = self.PathFind()
        
        # Scroll Up
        if a_Button == 4:
            self.m_SolveDelay += System.Graph.DELAY_INCREMENT

        # Scroll Down
        if a_Button == 5:
            self.m_SolveDelay -= System.Graph.DELAY_INCREMENT

        if a_Button >= 1 and a_Button <= 3:
            self.m_NodesSurfaceIsDirty = True
            self.m_FontSurfaceIsDirty = True
            self.m_DebugSurfaceIsDirty = True
    
    def OnMouseUp(self, a_MousePos, a_Button):
        None

    def Update(self):       
        self.m_TimeSinceLastUpdate += FPS.DeltaTime()
        
        if self.m_TimeSinceLastUpdate >= self.m_SolveDelay and not self.m_IsPaused:
            try:
                self.PathFindCoroutine.next()

                self.m_NodesSurfaceIsDirty = True
                self.m_FontSurfaceIsDirty = True
                self.m_DebugSurfaceIsDirty = True

            except StopIteration:
                None

            self.m_TimeSinceLastUpdate = 0

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
            
            if self.m_NodesSurfaceIsDirty:
                directionList = []
                
                directionList.append(( 1,  0))
                directionList.append(( 0,  1))
                directionList.append((-1,  0))
                directionList.append(( 0, -1))

                directionList.append(( 1,  1))
                directionList.append((-1, -1))
                directionList.append(( 1, -1))
                directionList.append((-1,  1))

                directionList.append((0, 0))

                i = 0
                for direction in directionList:
                    tempText = self.m_HelpFont.render('F1 = Help', 1, System.Color.WHITE if i == len(directionList) - 1 else System.Color.BLACK)
                    tempTextRect = tempText.get_rect()

                    tempTextRect.x += direction[0]
                    tempTextRect.y += direction[1]
                    self.m_NodesSurface.blit(tempText, tempTextRect)

                    i += 1

            if self.m_DebugSurfaceIsDirty:
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

        if (self.m_DispalyHelp):
            Graphics.Draw(self.m_HelpSurface, self.m_HelpSurfaceRect)

        if(self.m_IsPaused):
            Graphics.Draw(self.m_PauseSurface, self.m_PauseSurfaceRect)
        

