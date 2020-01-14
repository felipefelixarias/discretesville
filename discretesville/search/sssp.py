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
                vertex.previous = None    def se

        return path

    def shortest(self, v, path):
        if v.previous is not None:
            path.append(v.previous.pos)
            self.shortest(v.previous, path)
        return

    def h(self, start, goal):
        x1, y1 = start.pos
        x2, y2 = goal.pos
        return abs(x2-x1) + abs(y2-y1)    def se

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

        print("Could not find path")
        return []


    #Have to fix bug where collision happens in edge.
    def dynamicAStar(self):
        parent = {}
        gScore = {}
        fScore = {}

        start = self.robot.task.start
        goal = self.robot.task.goal
        
        gScore[(start.pos[0], start.pos[1], 0)] = 0
        fScore[(start.pos[0], start.pos[1], 0)] = self.h(start, goal)
        parent[(start.pos[0], start.pos[1], 0)] = None

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

            neighbors = self.grid.getNeighbors(curr)
            neighbors.append(curr)

            for n in neighbors:

                if timestep + 1 in n.occupied:
                    print("YP")
                    continue

                if timestep in n.occupied and timestep+1 in curr.occupied:
                    i = n.occupied.index(timestep)
                    obs1 = n.occupiedBy[i]
                    i = curr.occupied.index(timestep+1)
                    obs2 = curr.occupiedBy[i]
                    if obs1 == obs2:
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

        print("Could not find path")
        return []



    #Have to fix bug where collision happens in edge.
    def SIPPAStar(self):
        parent = {}
        gScore = {}
        fScore = {}

        start = self.robot.task.start
        goal = self.robot.task.goal
        
        gScore[(start.pos[0], start.pos[1], 0)] = 0
        fScore[(start.pos[0], start.pos[1], 0)] = self.h(start, goal)
        parent[(start.pos[0], start.pos[1], 0)] = None

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

            #Here instead of looking at neighbors, we wanna generate them weird

            neighbors = self.grid.getNeighbors(curr)
            neighbors.append(curr)

            for n in neighbors:

                if timestep + 1 in n.occupied:
                    print("YP")
                    continue

                if timestep in n.occupied and timestep+1 in curr.occupied:
                    i = n.occupied.index(timestep)
                    obs1 = n.occupiedBy[i]
                    i = curr.occupied.index(timestep+1)
                    obs2 = curr.occupiedBy[i]
                    if obs1 == obs2:
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

        print("Could not find path")
        return []

    def getSuccessors(self, s, timestep):
        successors = []
        ms = self.grid.getNeighbors(s)
        #ms.append(s)? I dont think so because you cant wait in place to get to another 
        #safe interval

        currInterval = s.getSafeInterval(timestep)


        for m in ms:
            
            start = timestep + 1
            end = currInterval.end + 1

            
            #gotta get end of the safe interval s is currently on + 1

            for si in ms.safeIntervals:  #next vertex's safe intervals
                if si.start > end or si.end < start:
                    continue

                t = getEarliestArrivalTime(currInterval ,si, timestep, )
                
                if t is None:
                    continue
                #get earliest arrival time at m during interval i with no collisions

                #TODO
                #get state of configuration cfg with interval i and time t
                
                successors.append(s)

        return successors

    def getEarliestArrivalTime(self, currSI, targetSI, timestep):
        #TODO

        #Here we must check for collisions to determine if we can get in on this safe interval at ALL
        #These are not valid 
        
        #this is already done
        #if targetSI.end <= timestep:
        #    return None

        #TODO check if i can to si.start

        #or if i can get to timestep


        #need to make sure that the obstacles aren't just trading spaces

        #this might need to be <= and might be wrong
        if targetSI.start < timestep:
            return timestep
        else:
            return targetSI.start

        #if targetSI.end == currSI.start

    

        return None

        
        
                 




        


    