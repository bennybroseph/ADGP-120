import random

from System import *

class Node(object):
    def __init__(self):
        
        self.m_F = 0
        self.m_G = 0
        self.m_H = 0
        
        self.m_Adjacent = []
        self.m_Parent = None
        
        self.m_Index = ()

        self.m_IsTraversable = bool(random.randint(0, 3))

        self.m_Color = System.Color.WHITE if self.m_IsTraversable else System.Color.RED

        self.m_Rect = None

    @property
    def IsTraversable(self):
        return self.m_IsTraversable

    @IsTraversable.setter
    def IsTraversable(self, value):
        self.m_IsTraversable = value
        self.UpdateColor()

    def UpdateF(self):
        self.m_F = self.m_G + self.m_H

    def UpdateColor(self, a_Open = None, a_Closed = None, a_Start = None, a_Goal = None):
        if a_Open == None:
            self.m_Color = System.Color.WHITE if self.m_IsTraversable else System.Color.RED
        else:
            if self == a_Start:
                self.m_Color = System.Color.GREEN
            elif self == a_Goal:
                self.m_Color = System.Color.YELLOW
            elif self in a_Open:
                self.m_Color = System.Color.BLUE
            elif self in a_Closed:
                self.m_Color = System.Color.DARK_GREY
            else:
                self.m_Color = System.Color.WHITE if self.m_IsTraversable else System.Color.RED