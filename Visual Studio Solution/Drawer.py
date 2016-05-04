import pygame

from FPS import FPS
from System import System
from Graphics import Graphics

from SearchSpace import SearchSpace


class Drawer:
    def __init__(self):

        self._search_space = SearchSpace()  # Create a 'SearchSpace' object
        self.path_find_generator = self._search_space.path_find()  # Create a generator function

        self._paused = False  # Whether or not the application is _paused
        self._solve_delay = 0.0  # How much time should be put in between each algorithm loop
        self._last_update = 0.0  # How much time has passed since the last pathing algorithm loop

        # region -- NODE SURFACE --
        self._help_font = pygame.font.SysFont("Pokemon_FireRed.ttf", 28)

        self._nodes_surface_dirty = True  # True when the surface needs to be updated
        self._display_nodes = True  # Whether or not to display the '_nodes_surface'

        # Create a transparency enabled surface
        self._nodes_surface = pygame.Surface(System.Display.RESOLUTION_SIZE, pygame.SRCALPHA, 32)
        self._nodes_surface = self._nodes_surface.convert_alpha()  # Enables transparency
        self._nodes_surface_rect = self._nodes_surface.get_rect()

        # Center it to the screen
        self._nodes_surface_rect.x = System.Display.RESOLUTION_WIDTH / 2
        self._nodes_surface_rect.y = System.Display.RESOLUTION_HEIGHT / 2
        # endregion

        # region -- DEBUG SURFACE --
        self._debug_surface_dirty = True  # True when the surface needs to be updated
        self._display_debug = True  # Whether or not to display the '_debug_surface'

        # Create a transparency enabled surface
        self._debug_surface = pygame.Surface(System.Display.RESOLUTION_SIZE, pygame.SRCALPHA, 32)
        self._debug_surface = self._debug_surface.convert_alpha()  # Enables transparency
        self._debug_surface_rect = self._debug_surface.get_rect()

        # Center it to the screen
        self._debug_surface_rect.x = System.Display.RESOLUTION_WIDTH / 2
        self._debug_surface_rect.y = System.Display.RESOLUTION_HEIGHT / 2
        # endregion

        # region -- FONT SURFACE --
        self._font = pygame.font.SysFont("Pokemon_FireRed.ttf", 18)

        self._font_surface_dirty = True  # True when the surface needs to be updated
        self._display_text = False  # Whether or not to display the '_font_surface'

        # Create a transparency enabled surface
        self._font_surface = pygame.Surface(System.Display.RESOLUTION_SIZE, pygame.SRCALPHA, 32)
        self._font_surface = self._font_surface.convert_alpha()  # Enables transparency
        self._font_surface_rect = self._font_surface.get_rect()

        # Center it to the screen
        self._font_surface_rect.x = System.Display.RESOLUTION_WIDTH / 2
        self._font_surface_rect.y = System.Display.RESOLUTION_HEIGHT / 2
        # endregion

        # region -- PAUSE SURFACE --

        pause_font = pygame.font.SysFont("lucidaconsole", 256)

        pause_text = pause_font.render("PAUSED", 1, System.Color.WHITE)
        pause_text_rect = pause_text.get_rect()

        # Create a transparency enabled surface
        self._pause_surface = pygame.Surface(
            (pause_text_rect.width + 50,
             pause_text_rect.height + 50), pygame.SRCALPHA, 32)
        self._pause_surface = self._pause_surface.convert_alpha()  # Enables transparency
        self._pause_surface.fill((0, 0, 0, 240))  # Transparent black color
        self._pause_surface_rect = self._pause_surface.get_rect()

        # Center it to the screen
        self._pause_surface_rect.x = System.Display.RESOLUTION_WIDTH / 2
        self._pause_surface_rect.y = System.Display.RESOLUTION_HEIGHT / 2

        pause_text_rect.x = (self._pause_surface_rect.width / 2) - (pause_text_rect.width / 2)
        pause_text_rect.y = (self._pause_surface_rect.height / 2) - (pause_text_rect.height / 2)

        self._pause_surface.blit(pause_text, pause_text_rect)

        # endregion

        # region -- HELP SURFACE --
        self._display_help = False

        # Create a transparency enabled surface
        self._help_surface = pygame.Surface(
            (System.Display.RESOLUTION_WIDTH / 1.15,
             System.Display.RESOLUTION_HEIGHT / 1.15), pygame.SRCALPHA, 32)
        self._help_surface = self._help_surface.convert_alpha()  # Enables transparency
        self._help_surface.fill((0, 0, 0, 180))
        self._help_surface_rect = self._help_surface.get_rect()

        # Center it to the screen
        self._help_surface_rect.x = System.Display.RESOLUTION_WIDTH / 2
        self._help_surface_rect.y = System.Display.RESOLUTION_HEIGHT / 2

        help_font = pygame.font.SysFont("lucidaconsole", 26)

        help_text = [["Actions", "----------------------------------"],
                     ["Color Code", "----------------------------------"]]

        help_text[0].append("Esc = Exit Application")
        help_text[0].append("P   = Pause Algorithm")
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
                temp_height = \
                    (j * float((self._help_surface_rect.height - 150) / temp_num_items)) + 75

                if i == 0:
                    temp_surface_rect.x = 10
                    temp_surface_rect.y = temp_height - (temp_surface_rect.height / 2)
                else:
                    temp_surface_rect.x = \
                        self._help_surface_rect.width - temp_surface_rect.width - 10
                    temp_surface_rect.y = temp_height - (temp_surface_rect.height / 2)

                self._help_surface.blit(temp_surface, temp_surface_rect)

                j += 1
            i += 1

        None
        # endregion

    @property
    def search_space(self):
        return self._search_space

    def on_key_down(self, key, mod):

        if key == pygame.K_F1:
            self._display_help = not self._display_help
            self._nodes_surface_dirty = True
        if key == pygame.K_F5:
            self._search_space.reset_search_space()
            self.path_find_generator = self._search_space.path_find()

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
        if mouse_button == 1 \
                and self._search_space.nodes[selected_index[0]][selected_index[1]].traversable:
            self._search_space.start_node = \
                self._search_space.nodes[selected_index[0]][selected_index[1]]
            self._search_space.reset_search_space()
            self.path_find_generator = self._search_space.path_find()

            # Middle Click
        if mouse_button == 2:
            self._search_space.nodes[selected_index[0]][selected_index[1]].traversable \
                = not self._search_space.nodes[selected_index[0]][selected_index[1]].traversable

        # Right Click
        if mouse_button == 3:
            self._search_space.end_node = \
                self._search_space.nodes[selected_index[0]][selected_index[1]]
            self._search_space.calculate_heuristic()
            self._search_space.reset_search_space()
            self.path_find_generator = self._search_space.path_find()

        # Scroll Up
        if mouse_button == 4:
            self._solve_delay += System.Graph.DELAY_INCREMENT

        # Scroll Down
        if mouse_button == 5:
            self._solve_delay -= System.Graph.DELAY_INCREMENT
            if self._solve_delay < 0:
                self._solve_delay = 0

        if 1 <= mouse_button <= 3:
            self._nodes_surface_dirty = True
            self._font_surface_dirty = True
            self._debug_surface_dirty = True

    def on_mouse_up(self, mouse_position, mouse_button):
        None

    def update(self):
        self._last_update += FPS.delta_time()

        if self._last_update >= self._solve_delay \
                and not self._paused \
                and not self._search_space.path_found:
            try:
                if self._solve_delay == 0:
                    while True:
                        self.path_find_generator.next()
                else:
                    self.path_find_generator.next()

            except StopIteration:
                None

            self._nodes_surface_dirty = True
            self._font_surface_dirty = True
            self._debug_surface_dirty = True

            self._last_update = 0

    def draw(self):
        if self._nodes_surface_dirty or self._font_surface_dirty or self._debug_surface_dirty:

            if self._nodes_surface_dirty:
                self._nodes_surface.fill(System.Color.TRANSPARENT)
            if self._font_surface_dirty:
                self._font_surface.fill(System.Color.TRANSPARENT)
            if self._debug_surface_dirty:
                self._debug_surface.fill(System.Color.TRANSPARENT)

            for x in range(0, len(self._search_space.nodes)):
                for y in range(0, len(self._search_space.nodes[x])):

                    if self._nodes_surface_dirty:
                        node_surface = pygame.Surface(
                            (System.Graph.NODE_WIDTH, System.Graph.NODE_HEIGHT))

                        self._search_space.nodes[x][y].update_surface_color(
                            self._search_space.open_list, self._search_space.closed_list,
                            self._search_space.start_node, self._search_space.end_node)
                        node_surface.fill(self._search_space.nodes[x][y].surface_color)

                        self._nodes_surface.blit(
                            node_surface, self._search_space.nodes[x][y].surface_rect)

                    if self._debug_surface_dirty \
                            and self._search_space.nodes[x][y].parent_node is not None:
                        pygame.draw.line(
                            self._debug_surface,
                            System.Color.BLACK,
                            (self._search_space.nodes[x][y].surface_rect.x +
                             (self._search_space.nodes[x][y].surface_rect.width / 2),
                             self._search_space.nodes[x][y].surface_rect.y +
                             (self._search_space.nodes[x][y].surface_rect.height / 2)),
                            (self._search_space.nodes[x][y].parent_node.surface_rect.x +
                             (self._search_space.nodes[x][y].parent_node.surface_rect.width / 2),
                             self._search_space.nodes[x][y].parent_node.surface_rect.y +
                             (self._search_space.nodes[x][y].parent_node.surface_rect.height / 2)
                            ))

                    if self._font_surface_dirty and self._search_space.nodes[x][y].traversable:
                        text_color = \
                            System.Color.BLACK \
                            if self._search_space.nodes[x][y] in self._search_space.open_list \
                            else System.Color.LIGHT_GREY

                        h_text_surface = self._font.render(
                            'H: ' + str(self._search_space.nodes[x][y].h_score), 1, text_color)

                        h_text_surface_rect = h_text_surface.get_rect()
                        h_text_surface_rect = (
                            self._search_space.nodes[x][y].surface_rect.x +
                            self._search_space.nodes[x][y].surface_rect.width -
                            h_text_surface_rect.width,
                            self._search_space.nodes[x][y].surface_rect.y +
                            self._search_space.nodes[x][y].surface_rect.height -
                            h_text_surface_rect.height)

                        g_text_surface = self._font.render(
                            'G: ' + str(self._search_space.nodes[x][y].g_score), 1, text_color)

                        g_text_surface_rect = h_text_surface.get_rect()
                        g_text_surface_rect = (
                            self._search_space.nodes[x][y].surface_rect.x,
                            self._search_space.nodes[x][y].surface_rect.y +
                            self._search_space.nodes[x][y].surface_rect.height -
                            g_text_surface_rect.height)

                        f_text_surface = self._font.render(
                            'F: ' + str(self._search_space.nodes[x][y].f_score), 1, text_color)

                        f_text_surface_rect = self._search_space.nodes[x][y].surface_rect

                        self._font_surface.blit(h_text_surface, h_text_surface_rect)
                        self._font_surface.blit(g_text_surface, g_text_surface_rect)
                        self._font_surface.blit(f_text_surface, f_text_surface_rect)

            if self._nodes_surface_dirty and not self._display_help:
                direction_list = [(1, 0), (0, 1), (-1, 0), (0, -1),
                                  (1, 1), (-1, -1), (1, -1), (-1, 1), (0, 0)]

                i = 0
                for direction in direction_list:
                    temp_text = self._help_font.render(
                        'F1 = Help', 1,
                        System.Color.WHITE if i == len(direction_list) - 1 else System.Color.BLACK)
                    temp_text_rect = temp_text.get_rect()

                    temp_text_rect.x += direction[0]
                    temp_text_rect.y += direction[1]
                    self._nodes_surface.blit(temp_text, temp_text_rect)

                    i += 1

            if self._debug_surface_dirty:
                current_path_node = self._search_space.end_node
                while current_path_node.parent_node is not None:
                    pygame.draw.line(
                        self._debug_surface,
                        System.Color.DARK_GREEN,
                        (
                            current_path_node.surface_rect.x +
                            (current_path_node.surface_rect.width / 2),
                            current_path_node.surface_rect.y +
                            (current_path_node.surface_rect.height / 2)),
                        (
                            current_path_node.parent_node.surface_rect.x +
                            (current_path_node.parent_node.surface_rect.width / 2),
                            current_path_node.parent_node.surface_rect.y +
                            (current_path_node.parent_node.surface_rect.height / 2)),
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
