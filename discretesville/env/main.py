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
            print self.grid[i]

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
            print temp[i]

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

            print "TIMESTEP ", i
            for j in range(self.yDim):
                print g[j]

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

''' Algorithm Stuff '''
class Vertex:
    def __init__(self,x,y,cost=0):
        self.x = x
        self.y = y
        self.cost = cost

    def AddNeighbor(vertex):
        self.neighbors.append(vertex)

def StandardSearch(env,s,g):
    print("Finding path from %s to %s using standard search." % (s,g))

    if env.grid[s[1]][s[0]] == 'X':
        print "Start in obstacle."
        return
    if env.grid[g[1]][g[0]] == 'X':
        print "Goal in obstacle."
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
                env.grid[left.y][left.x] = str(top.cost)

        if current.x < maxX:
            right = Vertex(current.x+1,current.y,current.cost+1)
            if env.grid[right.y][right.x] == ' ':
                unvisited.append(right)
                env.grid[right.y][right.x] = str(top.cost)
    env.PrintGrid()

def TwoVariableSearch(env,s,g):
    print("Finding path from %s to %s using standard search." % (s,g))

    if env.grid[s[1]][s[0]] == 'X':
        print "Start in obstacle."
        return
    if env.grid[g[1]][g[0]] == 'X':
        print "Goal in obstacle."
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
    print "Total Nodes Visited: ", visitedCount

def FancySearch(env,s,g):
    print("Finding path from %s to %s using fancy search." % (s,g))

    if env.grid[s[1]][s[0]] == 'X':
        print "Start in obstacle."
        return
    if env.grid[g[1]][g[0]] == 'X':
        print "Goal in obstacle."
        return

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

    visitedCount = 0

    while unvisited or revisitOptions:

        if len(unvisited) == 0:
            print "Evaluating vertex: ", current.x,current.y
            print "At timestep: ", current.cost
            print "Current Grid"
            for i in range(env.yDim):
                print currentGrid[i]
            print " "
            print " "
            print "Timesteps"

            env.PrintTimesteps()
            print " "
            print " "
            currentGrid = env.CopyGrid()
            revisit = revisitOptions.pop(0)
            env.timesteps[revisit.cost][revisit.y][revisit.x] = str(revisit.cost)
            unvisited.append(revisit)

        current = unvisited.pop(0)
        visitedCount = visitedCount + 1
        if(current.x == goal.x and current.y == goal.y):
            break

        if len(env.timesteps) == current.cost + 1:
            env.ExpandTimesteps(1)

        if current.y < maxY:
            top = Vertex(current.x,current.y+1,current.cost+1)
            if env.timesteps[top.cost][top.y][top.x] == ' ':
                if currentGrid[top.y][top.x] == ' ':
                    unvisited.append(top)
                    env.timesteps[top.cost][top.y][top.x] = str(top.cost)
                    currentGrid[top.y][top.x] = str(top.cost)
                else :
                    revisitOptions.append(top)

        if current.y > 0:
            bottom = Vertex(current.x,current.y-1,current.cost+1)
            if env.timesteps[bottom.cost][bottom.y][bottom.x] == ' ':
                if currentGrid[bottom.y][bottom.x] == ' ':
                    unvisited.append(bottom)
                    env.timesteps[bottom.cost][bottom.y][bottom.x] = str(bottom.cost)
                    currentGrid[bottom.y][bottom.x] = str(bottom.cost)
                else :
                    revisitOptions.append(bottom)

        if current.x > 0:
            left = Vertex(current.x-1,current.y,current.cost+1)
            if env.timesteps[left.cost][left.y][left.x] == ' ':
                if currentGrid[left.y][left.x] == ' ':
                    unvisited.append(left)
                    env.timesteps[left.cost][left.y][left.x] = str(left.cost)
                    currentGrid[left.y][left.x] = str(left.cost)
                else :
                    revisitOptions.append(left)

        if current.x < maxX:
            right = Vertex(current.x+1,current.y,current.cost+1)
            if env.timesteps[right.cost][right.y][right.x] == ' ':
                if currentGrid[right.y][right.x] == ' ':
                    unvisited.append(right)
                    env.timesteps[right.cost][right.y][right.x] = str(right.cost)
                    currentGrid[right.y][right.x] = str(right.cost)
                else :
                    revisitOptions.append(right)
    env.PrintTimesteps()
    print "Total Nodes Visited: ", visitedCount


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

    if args.env == 'narrow-hallway':
        env = NarrowHallway()
        env.PrintGrid()
        env.PrintObstaclePath()
    if args.searchalg == 'standard':
        StandardSearch(env,(0,1),(6,1))
    elif args.searchalg == '2v':
        TwoVariableSearch(env,(0,1),(6,1))
    elif args.searchalg == 'fancy':
        FancySearch(env,(0,1),(6,1))
