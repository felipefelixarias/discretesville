from heapq import heapify, heappop, heappush
from sys import maxsize

class SSSP():
    """
    Class in charge of all single source shortest path algorithms
    
    Parameters
    ----------
    grid
        A grid object containing the graph.
    robot
        A robot object with a moving task from a start to an end vertex.

    Attributes
    ----------
    grid
        A grid object containing the graph.
    robot
        A robot object with a moving task from a start to an end vertex.

    """
    def __init__(self, grid, robot):
        self.grid = grid
        self.robot = robot



    def dijkstra(self):
        """ Dijkstra Single Source Shortest Path algorithm, computes shortest path to each node in graph.
        Returns
        ----------
        goal.pos
            Key to the goal vertex
        parent
            Dictionary storing each node's parent.
        """
        parent = {}
        score = {}
        #TODO change this visited from a dic to a set (faster?)
        visited = {}
        #TODO Raise a ValueError if start or goal are None

        start = self.robot.task.start
        goal = self.robot.task.goal

        score[start.pos] = 0
        parent[start.pos] = None 
        unvisited = [(0, start)]
        heapify(unvisited)

        while(len(unvisited) > 0):

            uv = heappop(unvisited)
            current = uv[1]
            visited[current.pos] = True
            
            for n in self.grid.getNeighbors(current):

                if n.pos in visited:
                    continue

                if n.pos not in score:
                    score[n.pos] = maxsize
                    parent[n.pos] = None

                newDist = score[current.pos] + 1
                
                if newDist < score[n.pos]:
                    score[n.pos] = newDist
                    parent[n.pos] = current.pos

                heappush(unvisited, (score[n.pos], n))

        if goal.pos not in parent:
            #print("Could not find path")
            return None, parent
        else:
            return goal.pos, parent

    def extractPath(self, goal, parent):
        """
        Extracts path from the Dictionary storing each node's parent.
        
        Parameters
        ----------
        goal
            Key of the goal vertex in the parent dictionary.
        parent
            Dictionary storing each parent's node.

        Returns
        ----------
        ret
            List of path taken to get to goal from start, whose parent is None.

        """
        ret = []
        temp = goal

        while temp is not None:
            ret.insert(0, (temp[0], temp[1]))
            temp = parent[temp]
        
        return ret

    def extractSIPPPath(self, goal, parent):
        """
        Extracts path from the Dictionary storing each node's parent. Stores additional nodes for waiting in place for SIPP.
        
        Parameters
        ----------
        goal
            Key of the goal vertex in the parent dictionary.
        parent
            Dictionary storing each parent's node.

        Returns
        ----------
        ret
            List of path taken to get to goal from start, whose parent is None.

        """
        ret = []
        c = goal
        past = None

        while c is not None:
             
            if past is None:
                ret.insert(0,(c[0],c[1]))
            else:
                for _ in range(past[2]-c[2]):
                    ret.insert(0, (c[0],c[1]))

            past = c
            c = parent[c]
 
        return ret

    def h(self, start, goal):
        """
        Manhattan distance, used a heuristic for A*.
        
        Parameters
        ----------
        start
            Vertex object number one.
        goal 
            Vertex object number two.

        Returns
        ----------
        int
            The Manhattan distance between the two vertices.
        """

        x1, y1 = start.pos
        x2, y2 = goal.pos
        m = abs(x2-x1) + abs(y2-y1)  
        return m   

    def aStar(self):
        """ 
        A* algorithm, computes shortest path from one vertex to another.
        Returns
        ----------
        goal.pos
            Key to the goal vertex
        parent
            Dictionary storing each node's parent.
        """
        parent = {}
        gScore = {}
        fScore = {}

        start = self.robot.task.start
        goal = self.robot.task.goal

        for v in self.grid.getAll():
            gScore[v.pos] = maxsize
            fScore[v.pos] = maxsize
        
        gScore[start.pos] = 0
        fScore[start.pos] = self.h(start, goal)
        parent[start.pos] = None

        openSet = [(0, start)]
        heapify(openSet)
        
        while len(openSet) > 0:
            _, curr = heappop(openSet)

            if curr is goal:
                #return self.extractPath(curr.pos, parent)
                return curr.pos, parent

            for n in self.grid.getNeighbors(curr):
                tempGScore = gScore[curr.pos] + 1

                if tempGScore < gScore[n.pos]:
                    parent[n.pos] = curr.pos
                    gScore[n.pos] = tempGScore
                    fScore[n.pos] = gScore[n.pos] + self.h(n, goal)

                    if (fScore[n.pos], n) not in openSet:
                        heappush(openSet, (fScore[n.pos], n))

        #print("Could not find path")
        return []

    #Have to fix bug where collision happens in edge.
    def dynamicAStar(self):
        """ 
        A* algorithm, computes shortest path from one vertex to another.
        Returns
        ----------
        [(int,int)]
            List of indices/ids of all vertices in path.
        """
        parent = {}
        gScore = {}
        fScore = {}

        start = self.robot.task.start
        goal = self.robot.task.goal
        
        gScore[(start.pos[0], start.pos[1], 0)] = 0
        fScore[(start.pos[0], start.pos[1], 0)] = self.h(start, goal)
        parent[(start.pos[0], start.pos[1], 0)] = None

        openSet = [(0, 0, start)]
        heapify(openSet)
        
        while len(openSet) > 0:
            _, timestep, curr = heappop(openSet)

            if curr is goal and timestep not in curr.occupied:
                return self.extractPath((curr.pos[0], curr.pos[1], timestep), parent)

            neighbors = self.grid.getNeighbors(curr)
            neighbors.append(curr)

            for n in neighbors:

                if timestep + 1 in n.occupied:
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
                    gScore[(n.pos[0], n.pos[1], timestep+1)] = maxsize

                if tempGScore < gScore[(n.pos[0], n.pos[1], timestep+1)]:
                    parent[(n.pos[0], n.pos[1], timestep+1)] = (curr.pos[0], curr.pos[1], timestep)
                    gScore[(n.pos[0], n.pos[1], timestep+1)] = tempGScore
                    fScore[(n.pos[0], n.pos[1], timestep+1)] = gScore[(n.pos[0], n.pos[1], timestep+1)] + self.h(n, goal)

                    if (fScore[(n.pos[0], n.pos[1], timestep+1)], timestep+1, n) not in openSet:
                        heappush(openSet, (fScore[(n.pos[0], n.pos[1], timestep+1)], timestep+1, n))

        #print("Could not find path")
        return []

    def SIPPAStar(self):
        """ 
        Safe Interval Path Planning A* algorithm, computes shortest path from one vertex to another using safe intervals.
        Returns
        ----------
        goal.pos, timestep
            Key to the goal vertex.
        parent
            Dictionary storing each node's parent.
        """
        parent = {}
        gScore = {}
        fScore = {}

        start = self.robot.task.start
        goal = self.robot.task.goal
        
        gScore[(start.pos[0], start.pos[1], 0)] = 0
        fScore[(start.pos[0], start.pos[1], 0)] = self.h(start, goal)
        parent[(start.pos[0], start.pos[1], 0)] = None

        openSet = [(0, 0, start)]
        heapify(openSet)
        
        #print("Starting sippa*")
        while len(openSet) > 0:
            _, timestep, curr = heappop(openSet)

            if curr is goal and timestep not in curr.occupied:
                return (curr.pos[0], curr.pos[1], timestep), parent
                #self.extractSIPPPath((curr.pos[0], curr.pos[1], timestep), parent)

            successors = self.getSuccessors(curr, timestep)
            #print(str(len(successors)))

            for cfg, si, t in successors:               
                tempGScore = gScore[(curr.pos[0], curr.pos[1], timestep)] + t - timestep

                if (cfg.pos[0], cfg.pos[1], t) not in gScore:
                    gScore[(cfg.pos[0], cfg.pos[1], t)] = maxsize
                #else:
                #    print("Vertex was previously visited")

                if tempGScore < gScore[(cfg.pos[0], cfg.pos[1], t)]:
                    parent[(cfg.pos[0], cfg.pos[1], t)] = (curr.pos[0], curr.pos[1], timestep)
                    gScore[(cfg.pos[0], cfg.pos[1], t)] = tempGScore
                    fScore[(cfg.pos[0], cfg.pos[1], t)] = tempGScore + self.h(cfg, goal)
                    if (fScore[(cfg.pos[0], cfg.pos[1], t)], t, cfg) not in openSet:
                        heappush(openSet, (fScore[(cfg.pos[0], cfg.pos[1], t)], t, cfg))

        #print("Could not find path")
        return None, parent

    def getSuccessors(self, s, timestep):
        """ 
        Function for SIPP A* as implemented in the publication.
        
        Parameters
        ----------
        s
            The vertex for which you want successors.
        timestep
            The timestep for which to check for successors.

        Returns
        ----------
        Successors
            List of vertex, safe interval, timestep successors.
        """
        
        successors = []
        ms = self.grid.getNeighbors(s)
        currInterval = s.getSafeInterval(timestep)

        for m in ms:
            
            start = timestep + 1
            end = currInterval.end + 1

            for si in m.safeIntervals:  #next vertex's safe intervals

                if si.start > end or si.end < start:
                    continue

                t = self.getEarliestArrivalTime(currInterval, si, start)
                
                if t is None:
                    continue
            
                #TODO No longer return safe interval
                s = (m, si, t)              
                successors.append(s)

        return successors

    def getEarliestArrivalTime(self, currSI, targetSI, timestep):
        """ 
        Function to determine the earliest arrival time to go from one safe interval to another

        Parameters
        ----------
        currSI
            Safe interval object to begin from.
        targetSI
            Target safe interval object.
        timestep
            The current timestep.
        Returns
        ----------
        int
            None if you cannot transition between safe intervals or the earliest arrival time.
        """

        if currSI.end + 1 == targetSI.start and currSI.obsAfter == targetSI.obsBefore:
            return None
        elif targetSI.start < timestep:
            return timestep
        else:
            return targetSI.start   


        
        
                 




        


    