import pygame.font

from System import System
from Graphics import Graphics
from FPS import FPS

from Node import Node


class SearchSpace(object):
    def __init__(self):

        self._nodes = []  # All nodes within the search space

        self._open_list = []  # Open List
        self._closed_list = []  # Closed List

        # Creating nodes, giving them an index in the search space,
        # and defining their destination to be drawn on the screen
        for i in range(0, System.Graph.NUM_NODES_X):
            self._nodes.append([])
            for j in range(0, System.Graph.NUM_NODES_Y):
                self._nodes[i].append(Node())
                self._nodes[i][j].graph_index = (i, j)

                self._nodes[i][j].surface_rect = pygame.Rect(
                    float(System.Graph.REMAINING_SPACE_X / 2) + i * (
                        System.Graph.NODE_HEIGHT + System.Graph.LINE_WIDTH),
                    float(System.Graph.REMAINING_SPACE_Y / 2) + j * (
                        System.Graph.NODE_HEIGHT + System.Graph.LINE_WIDTH),
                    System.Graph.NODE_WIDTH,
                    System.Graph.NODE_HEIGHT)

        self._start_node = self._nodes[0][0]  # The Start Node
        self._end_node = self._nodes[len(self._nodes) - 2][len(self._nodes[0]) - 1]  # The Goal Node

        self._paused = False  # Whether or not the application is _paused
        self._solve_delay = 0.0  # How much time should be put in between each algorithm loop
        self._last_update = 0.0  # How much time has passed since the last pathing algorithm loop

        self._path_found = False  # Whether or not the algorithm has finished or not

        self.calculate_heuristic()  # Sets the heuristic by Manhattan Distance
        self.reset_search_space()
        self.path_find_generator = self.path_find  # Creates a generator function

        # region -- NODE SURFACE --
        self._help_font = pygame.font.SysFont("Pokemon_FireRed.ttf", 28)

        self._nodes_surface_dirty = True  # Whether or not the '_nodes_surface' is dirty and needs to be updated
        self._display_nodes = True  # Whether or not to display the '_nodes_surface'

        self._nodes_surface = pygame.Surface(System.Display.RESOLUTION_SIZE, pygame.SRCALPHA,
                                             32)  # Create a transparency enabled surface
        self._nodes_surface = self._nodes_surface.convert_alpha()
        self._nodes_surface_rect = self._nodes_surface.get_rect()  # A 'pygame.rect' to use for the surface

        # Center it to the screen
        self._nodes_surface_rect.x = System.Display.RESOLUTION_WIDTH / 2
        self._nodes_surface_rect.y = System.Display.RESOLUTION_HEIGHT / 2
        # endregion

        # region -- DEBUG SURFACE --
        self._debug_surface_dirty = True  # Whether or not the '_debug_surface' is dirty and needs to be updated
        self._display_debug = True  # Whether or not to display the '_debug_surface'

        self._debug_surface = pygame.Surface(System.Display.RESOLUTION_SIZE, pygame.SRCALPHA,
                                             32)  # Create a transparency enabled surface
        self._debug_surface = self._debug_surface.convert_alpha()
        self._debug_surface_rect = self._debug_surface.get_rect()  # A 'pygame.rect' to use for the surface

        # Center it to the screen
        self._debug_surface_rect.x = System.Display.RESOLUTION_WIDTH / 2
        self._debug_surface_rect.y = System.Display.RESOLUTION_HEIGHT / 2
        # endregion

        # region -- FONT SURFACE --
        self._font = pygame.font.SysFont("Pokemon_FireRed.ttf", 18)

        self._font_surface_dirty = True  # Whether or not the '_font_surface' is dirty and needs to be updated
        self._display_text = False  # Whether or not to display the '_font_surface'

        self._font_surface = pygame.Surface(System.Display.RESOLUTION_SIZE, pygame.SRCALPHA,
                                            32)  # Create a transparency enabled surface
        self._font_surface = self._font_surface.convert_alpha()
        self._font_surface_rect = self._font_surface.get_rect()  # A 'pygame.rect' to use for the surface

        # Center it to the screen
        self._font_surface_rect.x = System.Display.RESOLUTION_WIDTH / 2
        self._font_surface_rect.y = System.Display.RESOLUTION_HEIGHT / 2
        # endregion

        # region -- PAUSE SURFACE --

        pause_font = pygame.font.SysFont("lucidaconsole", 256)

        pause_text = pause_font.render("PAUSED", 1, System.Color.WHITE)
        pause_text_rect = pause_text.get_rect()

        self._pause_surface = pygame.Surface(
            (pause_text_rect.width + 50,
             pause_text_rect.height + 50), pygame.SRCALPHA, 32)  # Create a transparency enabled surface
        self._pause_surface = self._pause_surface.convert_alpha()
        self._pause_surface.fill((0, 0, 0, 240))
        self._pause_surface_rect = self._pause_surface.get_rect()  # A 'pygame.rect' to use for the surface

        # Center it to the screen
        self._pause_surface_rect.x = System.Display.RESOLUTION_WIDTH / 2
        self._pause_surface_rect.y = System.Display.RESOLUTION_HEIGHT / 2

        pause_text_rect.x = (self._pause_surface_rect.width / 2) - (pause_text_rect.width / 2)
        pause_text_rect.y = (self._pause_surface_rect.height / 2) - (pause_text_rect.height / 2)

        self._pause_surface.blit(pause_text, pause_text_rect)

        # endregion

        # region -- HELP SURFACE

        self._display_help = False

        self._help_surface = pygame.Surface(
            (System.Display.RESOLUTION_WIDTH / 1.15,
             System.Display.RESOLUTION_HEIGHT / 1.15), pygame.SRCALPHA, 32)  # Create a transparency enabled surface
        self._help_surface = self._help_surface.convert_alpha()
        self._help_surface.fill((0, 0, 0, 180))
        self._help_surface_rect = self._help_surface.get_rect()  # A 'pygame.rect' to use for the surface

        # Center it to the screen
        self._help_surface_rect.x = System.Display.RESOLUTION_WIDTH / 2
        self._help_surface_rect.y = System.Display.RESOLUTION_HEIGHT / 2

        help_font = pygame.font.SysFont("lucidaconsole", 26)

        help_text = [[], []]

        help_text[0].append("P = Pause Algorithm")
        help_text[0].append("")
        help_text[0].append("1 = Toggle Node Value Text")
        help_text[0].append("2 = Toggle Debug Lines")
        help_text[0].append("")
        help_text[0].append("F1  = Toggle This Help Screen")
        help_text[0].append("F5  = Refresh Path")
        help_text[0].append("F10 = Toggle FullScreen Mode")
        help_text[0].append("")
        help_text[0].append("Left Mouse   = Move the Start Node")
        help_text[0].append("Right Mouse  = Move the Goal Node")
        help_text[0].append("Middle Mouse = Move the Start Node")
        help_text[0].append("")
        help_text[0].append("Scroll Up   = Extend Algorithm Loop Delay")
        help_text[0].append("Scroll Down = Reduce Algorithm Loop Delay")

        help_text[1].append("White Box =   Standard Node")
        help_text[1].append("Red Box = Impassible Node")
        help_text[1].append("")
        help_text[1].append("Green Box =  Start Node")
        help_text[1].append("Yellow Box =   Goal Node")
        help_text[1].append("Grey Box = Closed List")
        help_text[1].append("Blue Box =   Open List")
        help_text[1].append("")
        help_text[1].append("Black Line = Child to Parent")
        help_text[1].append("Green Line =      Found Path")

        i = 0.0
        for text_list in help_text:

            j = 0.0
            for text in text_list:
                temp_surface = help_font.render(text, 1, System.Color.WHITE)
                temp_surface_rect = temp_surface.get_rect()

                temp_num_items = len(text_list) - 1 if len(text_list) - 1 > 0 else 1
                temp_height = (j * float((self._help_surface_rect.height - 150) / temp_num_items)) + 75

                if i == 0:
                    temp_surface_rect.x = 10
                    temp_surface_rect.y = temp_height - (temp_surface_rect.height / 2)
                else:
                    temp_surface_rect.x = self._help_surface_rect.width - temp_surface_rect.width - 10
                    temp_surface_rect.y = temp_height - (temp_surface_rect.height / 2)

                self._help_surface.blit(temp_surface, temp_surface_rect)

                j += 1
            i += 1

    # endregion
    def reset_search_space(self, current_node=None):

        self._path_found = False  # We're starting up the pathfinding function, so we have not found the path yet

        if current_node is None:
            current_node = self._start_node  # Set the current node to the starting node by default

        self._open_list = [current_node]  # Initialize the open list with the currentNode as the only value
        self._closed_list = []  # Initialize the closed list as an empty list

        # Remove all parents from all nodes before starting the pathfinding
        for list in self._nodes:
            for node in list:
                node.parent_node = None

    # Calculate the Heuristic of each node based on Manhattan Distance
    def calculate_heuristic(self):
        for x in range(0, len(self._nodes)):
            for y in range(0, len(self._nodes[x])):
                self._nodes[x][y].h_score = (
                    (
                          abs(self._nodes[x][y].graph_index[0] - self._end_node.graph_index[0]) 
                        + abs(self._nodes[x][y].graph_index[1] - self._end_node.graph_index[1])) 
                    * 10)

    @property
    def path_find(self):

        while True:

            self._open_list.sort(key=lambda node: node.f_score)
            current_node = self._open_list[0]

            self._open_list.remove(current_node)
            self._closed_list.append(current_node)

            direction_data = [((0, -1), 10), ((0, 1), 10), ((1, 0), 10), ((-1, 0), 10),
                              ((1, 1), 14), ((-1, -1), 14), ((1, -1), 14), ((-1, 1), 14)]

            adjacent_data = []

            for direction in direction_data:
                try:
                    if current_node.graph_index[0] + direction[0][0] >= 0 and current_node.graph_index[1] + \
                            direction[0][1] >= 0:
                        adjacent_data.append({'Node': self._nodes[current_node.graph_index[0] + direction[0][0]][
                            current_node.graph_index[1] + direction[0][1]], 'Cost': direction[1]})
                except IndexError:
                    continue

            for adjacent in adjacent_data:
                if adjacent['Node'].traversable:
                    if adjacent['Node'] not in self._open_list and adjacent['Node'] not in self._closed_list:
                        self._open_list.append(adjacent['Node'])

                        adjacent['Node'].g_score = adjacent['Cost']
                        adjacent['Node'].update_f()

                        adjacent['Node'].parent_node = current_node
                    else:
                        if current_node.g_score + adjacent['Cost'] < adjacent['Node'].g_score:
                            adjacent['Node'].g_score = adjacent['Cost']
                            adjacent['Node'].update_f()

                            adjacent['Node'].parent_node = current_node

            if len(self._open_list) == 0 or self._end_node in self._open_list:
                break

            if self._solve_delay > 0:
                yield

        self._path_found = True

        self._nodes_surface_dirty = True
        self._font_surface_dirty = True
        self._debug_surface_dirty = True

    def on_key_down(self, key, mod):

        if key == pygame.K_F1:
            self._display_help = not self._display_help
            self._nodes_surface_dirty = True
        if key == pygame.K_F5:
            self.reset_search_space()
            self.path_find_generator = self.path_find

        if key == pygame.K_1:
            self._display_text = not self._display_text
        if key == pygame.K_2:
            self._display_debug = not self._display_debug

        if key == pygame.K_p:
            self._paused = not self._paused

    def on_mouse_down(self, mouse_position, mouse_button):

        selected_index = (
            int((mouse_position[0] - float(System.Graph.REMAINING_SPACE_X / 2)) / (
                System.Graph.NODE_WIDTH + System.Graph.LINE_WIDTH)),
            int((mouse_position[1] - float(System.Graph.REMAINING_SPACE_Y / 2)) / (
                System.Graph.NODE_HEIGHT + System.Graph.LINE_HEIGHT)))

        # Left Click
        if mouse_button == 1 and self._nodes[selected_index[0]][selected_index[1]].traversable:
            self._start_node = self._nodes[selected_index[0]][selected_index[1]]
            self.reset_search_space()
            self.path_find_generator = self.path_find

            # Middle Click
        if mouse_button == 2:
            self._nodes[selected_index[0]][selected_index[1]].traversable = not self._nodes[selected_index[0]][
                selected_index[1]].traversable

        # Right Click
        if mouse_button == 3:
            self._end_node = self._nodes[selected_index[0]][selected_index[1]]
            self.calculate_heuristic()
            self.reset_search_space()
            self.path_find_generator = self.path_find

        # Scroll Up
        if mouse_button == 4:
            self._solve_delay += System.Graph.DELAY_INCREMENT

        # Scroll Down
        if mouse_button == 5:
            self._solve_delay -= System.Graph.DELAY_INCREMENT

        if 1 <= mouse_button <= 3:
            self._nodes_surface_dirty = True
            self._font_surface_dirty = True
            self._debug_surface_dirty = True

    def on_mouse_up(self, mouse_position, mouse_button):
        None

    def update(self):
        self._last_update += FPS.delta_time()

        if self._last_update >= self._solve_delay and not self._paused:
            try:
                self.path_find_generator.next()

                self._nodes_surface_dirty = True
                self._font_surface_dirty = True
                self._debug_surface_dirty = True

            except StopIteration:
                None

            self._last_update = 0

    def draw(self):
        if self._nodes_surface_dirty or self._font_surface_dirty or self._debug_surface_dirty:

            if self._nodes_surface_dirty:
                self._nodes_surface.fill(System.Color.TRANSPARENT)
            if self._font_surface_dirty:
                self._font_surface.fill(System.Color.TRANSPARENT)
            if self._debug_surface_dirty:
                self._debug_surface.fill(System.Color.TRANSPARENT)

            for x in range(0, len(self._nodes)):
                for y in range(0, len(self._nodes[x])):

                    if self._nodes_surface_dirty:
                        node_surface = pygame.Surface((System.Graph.NODE_WIDTH, System.Graph.NODE_HEIGHT))

                        self._nodes[x][y].update_surface_color(self._open_list, self._closed_list, self._start_node,
                                                               self._end_node)
                        node_surface.fill(self._nodes[x][y].surface_color)

                        self._nodes_surface.blit(node_surface, self._nodes[x][y].surface_rect)

                    if self._debug_surface_dirty and self._nodes[x][y].parent_node is not None:
                        pygame.draw.line(
                            self._debug_surface,
                            System.Color.BLACK,
                            (
                                self._nodes[x][y].surface_rect.x + (self._nodes[x][y].surface_rect.width / 2),
                                self._nodes[x][y].surface_rect.y + (self._nodes[x][y].surface_rect.height / 2)),
                            (
                                self._nodes[x][y].parent_node.surface_rect.x + (
                                    self._nodes[x][y].parent_node.surface_rect.width / 2),
                                self._nodes[x][y].parent_node.surface_rect.y + (
                                    self._nodes[x][y].parent_node.surface_rect.height / 2)))

                    if self._font_surface_dirty and self._nodes[x][y].traversable:
                        text_color = System.Color.BLACK if self._nodes[x][y] in self._open_list \
                            else System.Color.LIGHT_GREY

                        h_text_surface = self._font.render('H: ' + str(self._nodes[x][y].h_score), 1, text_color)
                        h_text_surface_rect = h_text_surface.get_rect()
                        h_text_surface_rect = (
                            self._nodes[x][y].surface_rect.x + self._nodes[x][
                                y].surface_rect.width - h_text_surface_rect.width,
                            self._nodes[x][y].surface_rect.y + self._nodes[x][
                                y].surface_rect.height - h_text_surface_rect.height)

                        g_text_surface = self._font.render('G: ' + str(self._nodes[x][y].g_score), 1, text_color)
                        g_text_surface_rect = h_text_surface.get_rect()
                        g_text_surface_rect = (
                            self._nodes[x][y].surface_rect.x,
                            self._nodes[x][y].surface_rect.y + self._nodes[x][
                                y].surface_rect.height - g_text_surface_rect.height)

                        f_text_surface = self._font.render('F: ' + str(self._nodes[x][y].f_score), 1, text_color)
                        f_text_surface_rect = self._nodes[x][y].surface_rect

                        self._font_surface.blit(h_text_surface, h_text_surface_rect)
                        self._font_surface.blit(g_text_surface, g_text_surface_rect)
                        self._font_surface.blit(f_text_surface, f_text_surface_rect)

            if self._nodes_surface_dirty and not self._display_help:
                direction_list = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1), (0, 0)]

                i = 0
                for direction in direction_list:
                    temp_text = self._help_font.render('F1 = Help', 1, System.Color.WHITE if i == len(
                        direction_list) - 1 else System.Color.BLACK)
                    temp_text_rect = temp_text.get_rect()

                    temp_text_rect.x += direction[0]
                    temp_text_rect.y += direction[1]
                    self._nodes_surface.blit(temp_text, temp_text_rect)

                    i += 1

            if self._debug_surface_dirty:
                current_path_node = self._end_node
                while current_path_node.parent_node is not None:
                    pygame.draw.line(
                        self._debug_surface,
                        System.Color.DARK_GREEN,
                        (
                            current_path_node.surface_rect.x + (current_path_node.surface_rect.width / 2),
                            current_path_node.surface_rect.y + (current_path_node.surface_rect.height / 2)),
                        (
                            current_path_node.parent_node.surface_rect.x + (
                                current_path_node.parent_node.surface_rect.width / 2),
                            current_path_node.parent_node.surface_rect.y + (
                                current_path_node.parent_node.surface_rect.height / 2)),
                        5)

                    current_path_node = current_path_node.parent_node

            self._nodes_surface_dirty = False
            self._font_surface_dirty = False
            self._debug_surface_dirty = False

        Graphics.draw(self._nodes_surface, self._nodes_surface_rect)

        if self._display_debug:
            Graphics.draw(self._debug_surface, self._debug_surface_rect)

        if self._display_text:
            Graphics.draw(self._font_surface, self._font_surface_rect)

        if self._display_help:
            Graphics.draw(self._help_surface, self._help_surface_rect)

        if self._paused:
            Graphics.draw(self._pause_surface, self._pause_surface_rect)
