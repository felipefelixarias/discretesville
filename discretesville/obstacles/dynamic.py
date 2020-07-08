class DynamicObstacle():
    """
    Dynamic Obstacle class.

    Attributes
    ----------
    path
        A list of vertices that the dynamic obstacle occupies (one per time step).
    """
    def __init__(self):
        self.path = []