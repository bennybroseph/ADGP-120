
class System:
    
    # Standard color values
    # Access with 'System.Color'
    class Color:
        
        RED 	    = (244, 67, 54, 255)
        GREEN	    = (76, 175, 80, 255)
        DARK_GREEN  = (56, 142, 60, 255)
        BLUE	    = (33, 150, 243, 255)
        
        YELLOW = (255, 235, 59, 255)
        ORANGE = (255, 152, 0, 255)
        
        WHITE       = (255, 255, 255, 255)
        LIGHT_GREY  = (189, 189, 189, 255)
        GREY        = (158, 158, 158, 255)
        DARK_GREY   = (117, 117, 117, 255)
        BLACK       = (0, 0, 0, 255)

        TRANSPARENT = (0, 0, 0, 0)
       
    # Configuration for default window sizes
    # Access with 'System.Display'
    class Display:
        
        RESOLUTION_WIDTH	= 1700
        RESOLUTION_HEIGHT	= 950
        
        RESOLUTION_SIZE = (RESOLUTION_WIDTH, RESOLUTION_HEIGHT)
        
        WINDOW_WIDTH 	= RESOLUTION_WIDTH
        WINDOW_HEIGHT	= RESOLUTION_HEIGHT
        
        WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
        
        FULLSCREEN_WIDTH 	= 1920
        FULLSCREEN_HEIGHT	= 1080
        
        FULLSCREEN_SIZE = (FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT)
        
        TARGET_FPS = 60.0  # What FPS the application should be aiming for

    class Graph:

        NODE_WIDTH  = 100
        NODE_HEIGHT = 100

        NODE_SIZE = (NODE_WIDTH, NODE_HEIGHT)

        LINE_WIDTH  = 5
        LINE_HEIGHT = 5

    Graph.NUM_NODES_X = Display.RESOLUTION_WIDTH   / Graph.NODE_WIDTH
    Graph.NUM_NODES_Y = Display.RESOLUTION_HEIGHT  / Graph.NODE_HEIGHT

    Graph.NUM_NODES_X = (Display.RESOLUTION_WIDTH  - (Graph.LINE_WIDTH  * Graph.NUM_NODES_X)) / Graph.NODE_WIDTH
    Graph.NUM_NODES_Y = (Display.RESOLUTION_HEIGHT - (Graph.LINE_HEIGHT * Graph.NUM_NODES_Y)) / Graph.NODE_HEIGHT

    Graph.REMAINING_SPACE_X = Display.RESOLUTION_WIDTH  - ((Graph.NODE_WIDTH  * Graph.NUM_NODES_X) + (Graph.LINE_WIDTH  * Graph.NUM_NODES_X))
    Graph.REMAINING_SPACE_Y = Display.RESOLUTION_HEIGHT - ((Graph.NODE_HEIGHT * Graph.NUM_NODES_Y) + (Graph.LINE_HEIGHT * Graph.NUM_NODES_Y))

    Graph.NUM_NODES = (Graph.NUM_NODES_X, Graph.NUM_NODES_Y)