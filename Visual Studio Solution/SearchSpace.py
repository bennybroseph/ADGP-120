import pygame.font

from System import System

from Node import Node


class SearchSpace(object):
    def __init__(self, nodes=None):

        self._nodes = []  # All nodes within the search space

        self._open_list = []  # Open List
        self._closed_list = []  # Closed List

        if nodes is None:
            # Creating nodes, giving them an index in the search space,
            # and defining their destination to be drawn on the screen
            for i in range(0, System.Graph.NUM_NODES_X):
                self._nodes.append([])
                for j in range(0, System.Graph.NUM_NODES_Y):
                    self._nodes[i].append(Node())
                    self._nodes[i][j].graph_index = (i, j)

                    self._nodes[i][j].surface_rect = pygame.Rect(
                        float(System.Graph.REMAINING_SPACE_X / 2) + i * (
                              System.Graph.NODE_WIDTH + System.Graph.LINE_WIDTH),
                        float(System.Graph.REMAINING_SPACE_Y / 2) + j * (
                              System.Graph.NODE_HEIGHT + System.Graph.LINE_HEIGHT),
                        System.Graph.NODE_WIDTH,
                        System.Graph.NODE_HEIGHT)

        self._start_node = self._nodes[0][0]  # The Start Node
        self._end_node = self._nodes[len(self._nodes) - 2][len(self._nodes[0]) - 1]  # The Goal Node

        self._path_found = False  # Whether or not the algorithm has finished or not

        self.calculate_heuristic()  # Sets the heuristic by Manhattan Distance
        self.reset_search_space()

    # region -- PROPERTIES --
    @property
    def nodes(self):
        return self._nodes

    @nodes.setter
    def nodes(self, value):
        self._nodes = value

    @property
    def open_list(self):
        return self._open_list

    @property
    def closed_list(self):
        return self._closed_list

    @property
    def start_node(self):
        return self._start_node

    @start_node.setter
    def start_node(self, value):
        self._start_node = value

    @property
    def end_node(self):
        return self._end_node

    @end_node.setter
    def end_node(self, value):
        self._end_node = value

    @property
    def path_found(self):
        return self._path_found
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
                    if current_node.graph_index[0] + direction[0][0] >= 0 \
                            and current_node.graph_index[1] + direction[0][1] >= 0:

                        adjacent_data.append(
                            {'Node': self._nodes[current_node.graph_index[0]
                                + direction[0][0]][current_node.graph_index[1] + direction[0][1]],
                             'Cost': direction[1]})

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

            yield

        self._path_found = True
