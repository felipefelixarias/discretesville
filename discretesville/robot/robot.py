import numpy as np
from vertex import Vertex

class Robot:
    def __init__(self, start, goal):
        self.fuel = 100
        self.start = start
        self.goal = goal
        self.sssp = None
        