import sys, pygame, time

from System		import *
from Graphics	import *
from FPS 		import *

def main():
	Graphics.Init()
	FPS.Init()

	while True:	

		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:sys.exit()
				if event.key == pygame.K_F10:
					Graphics.ToggleFullscreen()
		
		Graphics.Flip()		
		FPS.Update()

main()