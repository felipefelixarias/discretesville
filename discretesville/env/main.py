import heapq
import functools

'''Tools bc python is annoying'''
class PQ:
    def __init__(self):
        self.queue = list()
    def insert(self, elem):
        if len(self.queue) == 0:
            self.queue.append(elem)
            return
        for x in range(0,len(self.queue)):
            if(elem < self.queue[x]):
                self.queue.insert(x,elem)
                return
        self.queue.append(elem)
    def pop(self) :
        return self.queue.pop(0)
    def size(self):
        return len(self.queue)

''' Environment Stuff '''
class Env:
    def __init__(self, x=0, y=0, obstacle=None):
        self.xDim = x
        self.yDim = y
        self.obstacle=obstacle
        self.grid = []
        for i in range(y):
            column = []
            for j in range(x):
                column.append(' ')
            self.grid.append(column)


        self.timesteps = []
        self.ExpandTimesteps(1)

    def PrintGrid(self):
        for i in range(self.yDim):
            print(self.grid[i])

    def MarkBlocked(self,x,y):
        self.grid[y][x] = 'X'

    def PrintObstaclePath(self):
        temp = []
        for c in self.grid:
            tempc = []
            for x in c:
                tempc.append(x)
            temp.append(tempc)
        time = self.obstacle.start
        for p in self.obstacle.path:
            x = p[0]
            y = p[1]
            temp[y][x] = str(time)
            time = time + 1
        for i in range(self.yDim):
            print(temp[i])

    def ExpandTimesteps(self,t=1):
        for i in range(t):
            timestep = len(self.timesteps) + i
            temp = []
            for c in self.grid:
                tempC = []
                for v in c:
                    tempC.append(v)
                temp.append(tempC)
            if(self.obstacle != None):
                if(timestep >= self.obstacle.start):
                    if timestep >= self.obstacle.start + len(self.obstacle.path):
                        obsX,obsY = self.obstacle.path[len(self.obstacle.path)-1]
                        temp[obsY][obsX] = 'O'
                    else :
                        obsX,obsY = self.obstacle.path[timestep-self.obstacle.start]
                        temp[obsY][obsX] = 'O'
            self.timesteps.append(temp)

    def PrintTimesteps(self):
        for i,g in enumerate(self.timesteps):
            print("TIMESTEP ", i)
            for j in range(self.yDim):
                print(g[j])

    def CopyGrid(self):
        temp = []
        for c in self.grid:
            tempC = []
            for v in c:
                if v == 'X':
                    tempC.append(v)
                else :
                    tempC.append(' ')
            temp.append(tempC)
        return temp
    def GetValue(self,x,y):
        value = self.grid[y][x]
        if value == ' ':
            return -1
        if value == 'X':
            return -1
        if value == 'O':
            return -1
        else :
            return int(value)


class Obstacle:
    def __init__(self, path, start=0):
        self.path = path
        self.start = start

def NarrowHallway():
    path = [(6,1),(5,1),(4,1),(3,1),(2,1),(1,1),(0,1)]
    obs = Obstacle(path)
    env = Env(7,3,obs)
    env.MarkBlocked(3,0)
    env.MarkBlocked(3,2)
    return env

def NarrowBottomPath():
    path = [(6,3),(5,3),(4,3),(3,3),(2,3),(1,3),(0,3)]
    obs = Obstacle(path)
    env = Env(7,5,obs)
    env.MarkBlocked(3,1)
    env.MarkBlocked(3,4)
    env.MarkBlocked(3,2)
    return env

''' Algorithm Stuff '''
class Vertex:
    def __init__(self,x,y,cost=0):
        self.x = x
        self.y = y
        self.cost = cost

    def AddNeighbor(vertex):
        self.neighbors.append(vertex)

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.x, self.y, self.cost == other.x, other.y, other.cost

def StandardSearch(env,s,g):
    print("Finding path from %s to %s using standard search." % (s,g))

    if env.grid[s[1]][s[0]] == 'X':
        print("Start in obstacle.")
        return
    if env.grid[g[1]][g[0]] == 'X':
        print("Goal in obstacle.")
        return

    start = Vertex(s[0],s[1],0)
    env.grid[start.y][start.x] = '0'
    goal = Vertex(g[0],g[1])
    current = start
    unvisited = [start]

    maxY = env.yDim - 1
    maxX = env.xDim - 1


    while unvisited and (current.x != goal.x or current.y != goal.y):
        current = unvisited.pop(0)
        if current.y < maxY:
            top = Vertex(current.x,current.y+1,current.cost+1)
            if env.grid[top.y][top.x] == ' ':
                unvisited.append(top)
                env.grid[top.y][top.x] = str(top.cost)

        if current.y > 0:
            bottom = Vertex(current.x,current.y-1,current.cost+1)
            if env.grid[bottom.y][bottom.x] == ' ':
                unvisited.append(bottom)
                env.grid[bottom.y][bottom.x] = str(bottom.cost)

        if current.x > 0:
            left = Vertex(current.x-1,current.y,current.cost+1)
            if env.grid[left.y][left.x] == ' ':
                unvisited.append(left)
                env.grid[left.y][left.x] = str(left.cost)

        if current.x < maxX:
            right = Vertex(current.x+1,current.y,current.cost+1)
            if env.grid[right.y][right.x] == ' ':
                unvisited.append(right)
                env.grid[right.y][right.x] = str(right.cost)
    env.PrintGrid()
    return env

def TwoVariableSearch(env,s,g):
    print("Finding path from %s to %s using standard search." % (s,g))

    if env.grid[s[1]][s[0]] == 'X':
        print("Start in obstacle.")
        return
    if env.grid[g[1]][g[0]] == 'X':
        print("Goal in obstacle.")
        return

    start = Vertex(s[0],s[1],0)
    env.timesteps[0][start.y][start.x] = '0'
    goal = Vertex(g[0],g[1])
    current = start
    unvisited = [start]

    maxY = env.yDim - 1
    maxX = env.xDim - 1

    visitedCount = 0

    while unvisited :
        current = unvisited.pop(0)
        visitedCount = visitedCount + 1
        if(current.x == goal.x and current.y == goal.y):
            break

        if len(env.timesteps) == current.cost + 1:
            env.ExpandTimesteps(1)

        if current.y < maxY:
            top = Vertex(current.x,current.y+1,current.cost+1)
            if env.timesteps[top.cost][top.y][top.x] == ' ':
                unvisited.append(top)
                env.timesteps[top.cost][top.y][top.x] = str(top.cost)

        if current.y > 0:
            bottom = Vertex(current.x,current.y-1,current.cost+1)
            if env.timesteps[bottom.cost][bottom.y][bottom.x] == ' ':
                unvisited.append(bottom)
                env.timesteps[bottom.cost][bottom.y][bottom.x] = str(bottom.cost)

        if current.x > 0:
            left = Vertex(current.x-1,current.y,current.cost+1)
            if env.timesteps[left.cost][left.y][left.x] == ' ':
                unvisited.append(left)
                env.timesteps[left.cost][left.y][left.x] = str(left.cost)

        if current.x < maxX:
            right = Vertex(current.x+1,current.y,current.cost+1)
            if env.timesteps[right.cost][right.y][right.x] == ' ':
                unvisited.append(right)
                env.timesteps[right.cost][right.y][right.x] = str(right.cost)
    env.PrintTimesteps()
    print("Total Nodes Visited: ", visitedCount)

def FancySearch(env,s,g):
    print("Finding path from %s to %s using fancy search." % (s,g))

    if env.grid[s[1]][s[0]] == 'X':
        print("Start in obstacle.")
        return
    if env.grid[g[1]][g[0]] == 'X':
        print("Goal in obstacle.")
        return


    initialValueEnv = Env(env.xDim,env.yDim)
    initialValueEnv.grid = env.CopyGrid()
    print("Copied grid")
    StandardSearch(initialValueEnv,g,(-1,-1))
    #initialValueEnv.PrintGrid()



    start = Vertex(s[0],s[1],0)
    env.timesteps[0][start.y][start.x] = '0'
    goal = Vertex(g[0],g[1])
    current = start
    unvisited = [start]

    maxY = env.yDim - 1
    maxX = env.xDim - 1

    revisitOptions = []

    currentGrid = env.CopyGrid()
    currentGrid[start.y][start.x] = '0'

    current = start

    visitedCount = 0
    minGoal = 1000000000000

    while (unvisited or revisitOptions):# and current.x != goal.x or current.y != goal.y:


        if len(unvisited) == 0:
            print("Evaluating vertex: ", current.x,current.y)
            print("At timestep: ", current.cost)
            #print("Current Grid")
            #for i in range(env.yDim):
            #    print(currentGrid[i])
            print(" ")
            print(" ")
            print("Timesteps")

            env.PrintTimesteps()
            print(" ")
            print(" ")
            currentGrid = env.CopyGrid()
            #revisit = revisitOptions.pop(0)


            found = False
            while found == False :
                revisit = heapq.heappop(revisitOptions)
                print("Revisit cost",revisit[0], revisit[1].x, revisit[1].y)
                print(revisit)
                #if env.timesteps[revisit[1].cost][revisit[1].y][revisit[1].x] == ' ':
                found = True
            if(revisit[0] >= minGoal) :
                break
            env.timesteps[revisit[1].cost][revisit[1].y][revisit[1].x] = str(revisit[1].cost)
            #print(env[12])
            unvisited.append(revisit[1])


        heapq.heapify(revisitOptions)
        if(len(revisitOptions) == 0 or unvisited[0].cost <= revisitOptions[0][0]):
            current = unvisited.pop(0)
        else :
            current = heapq.heappop(revisitOptions)[1]
            print("")
            print("")
            print("")
            print("")
            print("New weird circumvent thing",unvisited[0].cost,current.cost)
            print("")
            print("")
            print("")
            print("")
            print("")
        if(current.cost + initialValueEnv.GetValue(current.x,current.y) >= minGoal):
            continue

        print("Evaluating: ",current.x,current.y," at: ", current.cost)
        print("Current Grid")
        for i in range(env.yDim):
            print(currentGrid[i])

        visitedCount = visitedCount + 1
        if(current.x == goal.x and current.y == goal.y):
            if(current.cost < minGoal):
                minGoal = current.cost
                print(" ")
                print(" ")
                print("Resetting minGoal",minGoal)
                print(" ")
                print(" ")
            heapq.heapify(revisitOptions)
            print(" ")
            print(" ")
            print("Revisit cost",revisitOptions[0][0], "CurrentCost: ",current.cost)
            print(" ")
            print(" ")
            if revisitOptions[0][0] >= minGoal:
                break

        if len(env.timesteps) == current.cost + 1:
            env.ExpandTimesteps(1)

        newVerts = []

        if current.y < maxY:
            top = Vertex(current.x,current.y+1,current.cost+1)
            newVerts.append(top)
        if current.y > 0:
            bottom = Vertex(current.x,current.y-1,current.cost+1)
            newVerts.append(bottom)
        if current.x > 0:
            left = Vertex(current.x-1,current.y,current.cost+1)
            newVerts.append(left)
        if current.x < maxX:
            right = Vertex(current.x+1,current.y,current.cost+1)
            newVerts.append(right)

        for v in newVerts:

            if env.timesteps[v.cost][v.y][v.x] == ' ':
                if currentGrid[v.y][v.x] == ' ':
                    unvisited.append(v)
                    env.timesteps[v.cost][v.y][v.x] = str(right.cost)
                    currentGrid[v.y][v.x] = str(right.cost)
                else :
                    print(v.x,v.y,v.cost,initialValueEnv.GetValue(v.x,v.y))
                    revisitOptions.append((v.cost+initialValueEnv.GetValue(v.x,v.y),v))
                    env.timesteps[v.cost][v.y][v.x] = str(right.cost)
                    #revisitOptions.append(right)
                    #pq.put((right.cost+initialValueEnv.GetValue(right.x,right.y),right))
    env.PrintTimesteps()
    print(initialValueEnv.GetValue(0,0))
    print("Total Nodes Visited: ", visitedCount)
    initialValueEnv.PrintGrid()

def Fancy2(env,s,g):
    print("Finding path from %s to %s using fancy search." % (s,g))

    if env.grid[s[1]][s[0]] == 'X':
        print("Start in obstacle.")
        return
    if env.grid[g[1]][g[0]] == 'X':
        print("Goal in obstacle.")
        return


    initialValueEnv = Env(env.xDim,env.yDim)
    initialValueEnv.grid = env.CopyGrid()
    print("Copied grid")
    StandardSearch(initialValueEnv,g,(-1,-1))
    #initialValueEnv.PrintGrid()


    start = Vertex(s[0],s[1],0)
    env.timesteps[0][start.y][start.x] = '0'
    goal = Vertex(g[0],g[1])
    current = start

    maxY = env.yDim - 1
    maxX = env.xDim - 1

    currentGrid = env.CopyGrid()
    currentGrid[start.y][start.x] = '0'

    pq = PQ()
    revisit = PQ()

    visitedCount = 1

    minGoal = 1000000000000

    a_bool = True
    while a_bool or pq or revisit :
        a_bool = False

        if len(env.timesteps) == current.cost + 1:
            env.ExpandTimesteps(1)

        neighbors = []
        if current.y < maxY:
            top = Vertex(current.x,current.y+1,current.cost+1)
            neighbors.append(top)
        if current.y > 0:
            bottom = Vertex(current.x,current.y-1,current.cost+1)
            neighbors.append(bottom)
        if current.x > 0:
            left = Vertex(current.x-1,current.y,current.cost+1)
            neighbors.append(left)
        if current.x < maxX:
            right = Vertex(current.x+1,current.y,current.cost+1)
            neighbors.append(right)

        for v in neighbors:
            if env.timesteps[v.cost][v.y][v.x] == ' ' :
                if currentGrid[v.y][v.x] == v.cost:
                    continue
                elif currentGrid[v.y][v.x] == ' ' :
                    currentGrid[v.y][v.x] = v.cost
                    pq.insert(v)
                else :
                    revisit.insert((v.cost + initialValueEnv.GetValue(v.x,v.y),v))
                env.timesteps[v.cost][v.y][v.x] = v.cost


        if revisit.size() == 0 or pq.queue[0].cost <= revisit.queue[0][0] :
            if pq.size() > 0 :
                current = pq.pop()
                print("From PQ: ", current.x, current.y, current.cost)
                if revisit.size() > 0 :
                    print("Instead of: ", revisit.queue[0][1].x, revisit.queue[0][1].y, revisit.queue[0][0])
                visitedCount = visitedCount + 1

        else :
            current = revisit.pop()
            print("From revisit: ",current[1].x,current[1].y,current[0])
            print("Instead of: ", pq.queue[0].cost)
            visitedCount = visitedCount + 1
            current = current[1]

        if current.x == goal.x and current.y == goal.y :
            print("Reached goal: ", current.x, current.y, current.cost)
            if minGoal > current.cost :
                minGoal = current.cost
            if minGoal <= revisit.queue[0][0] :
                break

    print("Final vertex: ", current.x, current.y, current.cost)
    env.PrintTimesteps()
    print("Total Nodes Visited: ", visitedCount)
    initialValueEnv.PrintGrid()

if __name__ == '__main__':
    import argparse
    env = Env(2,2)
    print(env)
    parser = argparse.ArgumentParser(description='Select Search Algorithm and Environment')
    parser.add_argument('--searchalg', metavar='path', required=True,
                        help='the path to workspace')
    parser.add_argument('--env', metavar='path', required=True,
                        help='path to schema')
    args = parser.parse_args()

    env = Env(0,0)

    if args.env == 'narrow-hallway' or args.env == '1':
        env = NarrowHallway()
        env.PrintGrid()
        env.PrintObstaclePath()
    if args.env == 'hallway-bottom' or args.env == '2':
        env = NarrowBottomPath()
        env.PrintGrid()
        env.PrintObstaclePath()
    if args.searchalg == 'standard':
        if args.env == args.env == 'hallway-bottom' or args.env == '2':
            StandardSearch(env,(0,3),(6,3))
        else :
            StandardSearch(env,(0,1),(6,1))
    elif args.searchalg == '2v':
        if args.env == args.env == 'hallway-bottom' or args.env == '2':
            TwoVariableSearch(env,(0,3),(6,3))
        else :
            TwoVariableSearch(env,(0,1),(6,1))
    elif args.searchalg == 'fancy':
        if args.env == args.env == 'hallway-bottom' or args.env == '2':
            Fancy2(env,(0,3),(6,3))
        else :
            Fancy2(env,(0,1),(6,1))
