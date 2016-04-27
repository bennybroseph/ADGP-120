import random

from System import *

class Node(object):
    def __init__(self):
        
        self.m_F = 0
        self.m_G = 0
        self.m_H = 0
        
        self.m_Adjacent = []
        self.m_Parent = None
        
        self.m_IsTraversable = bool(random.randint(0, 3))

        self.m_Color = self._UpdateColor()

        self.m_Rect = None

    @property
    def IsTraversable(self):
        return self.m_IsTraversable

    @IsTraversable.setter
    def IsTraversable(self, value):
        self.m_IsTraversable = value
        self.m_Color = self._UpdateColor()

    def _UpdateColor(self):
        return System.Color.WHITE if self.m_IsTraversable else System.Color.RED