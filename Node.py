from System import *

class Node(object):
	def __init__(self):
		self.m_F = 0
		self.m_G = 0
		self.m_H = 0
		
		self.m_Adjacent = []
		self.m_Parent = None