import random

from System import System


class Node(object):
    def __init__(self):

        self._f_score = 0
        self._g_score = 0
        self._h_score = 0

        self._parent_node = None

        self._traversable = bool(random.randint(0, 3))

        self._graph_index = ()

        self._surface_color = System.Color.WHITE if self._traversable else System.Color.RED

        self._surface_rect = None

    # region -- PROPERTIES --
    @property
    def f_score(self):
        return self._f_score

    @f_score.setter
    def f_score(self, value):
        self._f_score = value

    @property
    def g_score(self):
        return self._g_score

    @g_score.setter
    def g_score(self, value):
        self._g_score = value

    @property
    def h_score(self):
        return self._h_score

    @h_score.setter
    def h_score(self, value):
        self._h_score = value

    @property
    def graph_index(self):
        return self._graph_index

    @graph_index.setter
    def graph_index(self, value):
        self._graph_index = value

    @property
    def traversable(self):
        return self._traversable

    @traversable.setter
    def traversable(self, value):
        self._traversable = value
        self.update_surface_color()

    @property
    def surface_color(self):
        return self._surface_color

    @property
    def surface_rect(self):
        return self._surface_rect

    @surface_rect.setter
    def surface_rect(self, value):
        self._surface_rect = value

    @property
    def parent_node(self):
        return self._parent_node

    @parent_node.setter
    def parent_node(self, value):
        self._parent_node = value
    # endregion

    def update_f(self):
        self.f_score = self.g_score + self.h_score

    def update_surface_color(self,
                             open_list=None, closed_list=None, start_node=None, end_node=None):
        if open_list is None:
            self._surface_color = System.Color.WHITE if self._traversable else System.Color.RED
        else:
            if self == start_node:
                self._surface_color = System.Color.GREEN
            elif self == end_node:
                self._surface_color = System.Color.YELLOW
            elif not self._traversable:
                self._surface_color = System.Color.RED
            elif self in open_list:
                self._surface_color = System.Color.BLUE
            elif self in closed_list:
                self._surface_color = System.Color.DARK_GREY
            else:
                self._surface_color = System.Color.WHITE
