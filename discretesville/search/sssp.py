import heapq

class SSSP():
    def __init__(self, grid, robot):
        self.grid = grid
        self.robot = robot

    def dijkstra(self):
        start = self.robot.task.start
        goal = self.robot.task.goal

        start.distance = 0
        unvisited = [(v.distance, v) for v in self.grid.getAll()]
        heapq.heapify(unvisited)

        while(len(unvisited) > 0):
            uv = heapq.heappop(unvisited)
            current = uv[1]
            current.visited = True

            for n in self.grid.getNeighbors(current):
                if n.visited:
                    continue
                newDist = current.distance + 1
                
                if newDist < n.distance:
                    n.distance = newDist
                    n.previous = current
                
            while len(unvisited) > 0:
                heapq.heappop(unvisited)

            unvisited = [(v.distance, v) for v in self.grid.getAll()]
            heapq.heapify(unvisited)


        
        path = [goal.pos]
        self.shortest(goal, path)

        return path


    def shortest(self, v, path):
        if v.previous is not None:
            path.append(v.previous.pos)
            self.shortest(v.previous, path)
        return