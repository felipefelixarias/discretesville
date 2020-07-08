import numpy as np
from agent.task import Task

class Robot:
    """Class for a simple robot.

    Attributes
    ----------

    task
        The task the robot has to perform, initialized as an empty task.
    """
    def __init__(self):
        self.task = Task()

