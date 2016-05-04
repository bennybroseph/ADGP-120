import random

from System import System


class Node(object):
    def __init__(self):

        self.f_score = 0
        self.g_score = 0
        self.h_score = 0

        self.adjacent_list = []
        self.parent_node = None

        self._traversable = bool(random.randint(0, 3))

        self.graph_index = ()

        self.surface_color = System.Color.WHITE if self._traversable else System.Color.RED

        self.surface_rect = None

    @property
    def traversable(self):
        return self._traversable

    @traversable.setter
    def traversable(self, value):
        self._traversable = value
        self.update_surface_color()

    def update_f(self):
        self.f_score = self.g_score + self.h_score

    def update_surface_color(self, open_list=None, closed_list=None, start_node=None, end_node=None):
        if open_list is None:
            self.surface_color = System.Color.WHITE if self._traversable else System.Color.RED
        else:
            if self == start_node:
                self.surface_color = System.Color.GREEN
            elif self == end_node:
                self.surface_color = System.Color.YELLOW
            elif not self._traversable:
                self.surface_color = System.Color.RED
            elif self in open_list:
                self.surface_color = System.Color.BLUE
            elif self in closed_list:
                self.surface_color = System.Color.DARK_GREY
            else:
                self.surface_color = System.Color.WHITE
