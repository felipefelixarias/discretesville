import heapq
import sys

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

        ##clean up
        for vertices in self.grid.vertices:
            for vertex in vertices:
                vertex.visited = False
                vertex.previous = None
                vertex.distance = sys.maxsize

        return path

    def shortest(self, v, path):
        if v.previous is not None:
            path.append(v.previous.pos)
            self.shortest(v.previous, path)
        return

    def h(self, start, goal):
        x1, y1 = start.pos
        x2, y2 = goal.pos
        return abs(x2-x1) + abs(y2-y1)

    def reconstructPath(self, parent, curr):
        totalPath = [curr.pos]
        curr = parent[curr.pos]

        while parent[curr] is not None:
            totalPath.insert(0, curr)
            curr = parent[curr]

        totalPath.insert(0, curr)
        return totalPath

    def aStar(self):
        parent = {}
        gScore = {}
        fScore = {}

        start = self.robot.task.start
        goal = self.robot.task.goal

        for v in self.grid.getAll():
            gScore[v.pos] = sys.maxsize
            fScore[v.pos] = sys.maxsize
        
        gScore[start.pos] = 0
        fScore[start.pos] = self.h(start, goal)
        parent[start.pos] = None


        openSet = [(0, start)]
        heapq.heapify(openSet)

        
        while len(openSet) > 0:
            _, curr = heapq.heappop(openSet)

            if curr is goal:
                return self.reconstructPath(parent, curr)

            for n in self.grid.getNeighbors(curr):
                tempGScore = gScore[curr.pos] + 1

                if tempGScore < gScore[n.pos]:
                    parent[n.pos] = curr.pos
                    gScore[n.pos] = tempGScore
                    fScore[n.pos] = gScore[n.pos] + self.h(n, goal)

                    if (fScore[n.pos], n) not in openSet:
                        heapq.heappush(openSet, (fScore[n.pos], n))

        return ["NOPE"]

    def dynamicAStar(self):
        parent = {}
        gScore = {}
        fScore = {}

        start = self.robot.task.start
        goal = self.robot.task.goal


        #This wont work as we dont know what vertices will exist as they are infinite?
        #x.pos will have to become (x.pos[0], x.pos[1], timestep)
        #for v in self.grid.getAll():

        #    gScore[v.pos] = sys.maxsize
        #    fScore[v.pos] = sys.maxsize
        
        gScore[(start.pos[0], start.pos[1], 0)] = 0
        fScore[(start.pos[0], start.pos[1], 0)] = self.h(start, goal)
        parent[(start.pos[0], start.pos[1], 0)] = None


        #might have to change this so that each element in the queue is a cost, vertex, and time step
        openSet = [(0, 0, start)]
        heapq.heapify(openSet)

        
        while len(openSet) > 0:
            _, timestep, curr = heapq.heappop(openSet)

            if curr is goal and timestep not in curr.occupied:
                t=timestep
                ret = [curr.pos]

                c = parent[(curr.pos[0], curr.pos[1], timestep)]

                while parent[(c[0], c[1], t-1)] is not None:
                    ret.insert(0, c)
                    t = t-1
                    c = parent[(c[0], c[1], t)]

                ret.insert(0, c)
                return ret

            #here we might have to chek if neighborhood is occupied at timestep 

            for n in self.grid.getNeighbors(curr):

                if timestep + 1 in n.occupied:
                    print("YP")
                    continue

                tempGScore = gScore[(curr.pos[0], curr.pos[1], timestep)] + 1

                if (n.pos[0], n.pos[1], timestep+1) not in gScore:
                    gScore[(n.pos[0], n.pos[1], timestep+1)] = sys.maxsize

                if tempGScore < gScore[(n.pos[0], n.pos[1], timestep+1)]:
                    parent[(n.pos[0], n.pos[1], timestep+1)] = curr.pos
                    gScore[(n.pos[0], n.pos[1], timestep+1)] = tempGScore
                    fScore[(n.pos[0], n.pos[1], timestep+1)] = gScore[(n.pos[0], n.pos[1], timestep+1)] + self.h(n, goal)

                    if (fScore[(n.pos[0], n.pos[1], timestep+1)], timestep+1, n) not in openSet:
                        heapq.heappush(openSet, (fScore[(n.pos[0], n.pos[1], timestep+1)], timestep+1, n))

        return ["NOPE"]






        


    