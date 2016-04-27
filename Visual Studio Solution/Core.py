import sys, pygame, time

from System		import *
from Graphics	import *
from FPS 		import *

from Node           import *
from SearchSpace    import *

def main():
    Graphics.Init()
    FPS.Init()
    
    searchspace = SearchSpace()

    MouseDownListeners = []
    MouseDownListeners.append(searchspace.OnMouseDown)

    MouseUpListeners = []
    MouseUpListeners.append(searchspace.OnMouseUp)

    while True:

        for event in pygame.event.get():            
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:sys.exit()
                if event.key == pygame.K_F10:
                    Graphics.ToggleFullscreen()

            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                mousePos = (event.pos[0] / Graphics.GetScale()[0], event.pos[1] / Graphics.GetScale()[1])

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for delegate in MouseDownListeners:
                        delegate(mousePos, event.button)
               
                if event.type == pygame.MOUSEBUTTONUP:  
                    for delegate in MouseUpListeners:
                        delegate(mousePos, event.button)
        
        searchspace.Update()
        searchspace.Draw()

        FPS.Update()
        Graphics.Flip()

main()