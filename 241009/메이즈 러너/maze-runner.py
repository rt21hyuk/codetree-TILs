import sys
input = sys.stdin.readline

blank = 0; alive = 1; exited = 0
N_MAX = 11; M_MAX = 11

dr, dc = [-1, 1, 0, 0], [0, 0, -1, 1]

r = [0 for _ in range(M_MAX)]
c = [0 for _ in range(M_MAX)]
dist = [0 for _ in range(M_MAX)]
state = [alive for _ in range(M_MAX)]

n, m, k = map(int, input().split())
maze = [[0 for _ in range(N_MAX)] for _ in range(N_MAX)]
for i in range(1, n+1):
    maze[i][1:] = map(int, input().split())
for i in range(1, m+1):
    r[i], c[i] = map(int, input().split())
exit = list(map(int, input().split()))

def getDistance(r1, c1, r2, c2):
    return abs(r1-r2) + abs(c1-c2)

def movePlayers():
    for i in range(1, m+1):
        if state[i] == exited:
            continue
        dir = -1
        minDist = getDistance(exit[0], exit[1], r[i], c[i])
        for j in range(4):
            nr, nc = r[i] + dr[j], c[i] + dc[j]

            if nr < 1 or nc < 1 or nr > n or nc > n:
                continue

            if maze[nr][nc]:
                continue

            curDist = getDistance(exit[0], exit[1], nr, nc)
            if curDist < minDist:
                minDist = curDist
                dir = j

        if dir != - 1:
            dist[i] += 1
            r[i], c[i] = r[i] + dr[dir], c[i] + dc[dir]
            if exit[0] == r[i] and exit[1] == c[i]:
                state[i] = exited

def getSmallSquare():
    minSide = N_MAX
    squares = {}
    for i in range(1, m+1):
        if state[i] == exited:
            continue
        height, width = abs(exit[0] - r[i]), abs(exit[1] - c[i])
        side = max(height, width)
        if side < minSide:
            minSide = side
            squares = {}

            minR, minC = min(exit[0], r[i]), min(exit[1], c[i])
            maxR, maxC = max(exit[0], r[i]), max(exit[1], c[i])

            for x in range(-side, side + 1):
                for y in range(-side, side + 1):
                    nr, nc = minR+x, minC+y
                    if nr < 1 or nc < 1 or nr+side > n or nc+side > n:
                        continue
                    if not (nr <= r[i] <= nr+side and nr <= exit[0] <= nr+side):
                        continue
                    if not (nc <= c[i] <= nc+side and nc <= exit[1] <= nc+side):
                        continue

                    squareCoord = f'{nr},{nc}'
                    squares[squareCoord] = side

    squareR, squareC = N_MAX, N_MAX
    for coord in squares:
        curR, curC = map(int, coord.split(','))
        if curR < squareR:
            squareR = curR; squareC = curC
        elif curR == squareR:
            if curC < squareC:
                squareC = curC

    return squareR, squareC, minSide

def rotateSquare(curR, curC, side):
    global maze, exit
    originalMaze = [maze[curR+i][curC:curC+side+1] for i in range(side+1)]
    nr = r[:]
    nc = c[:]
    nextExit = exit[:]

    for i in range(side+1):
        for j in range(side+1):
            if originalMaze[side - j][i]:
                maze[curR+i][curC+j] = originalMaze[side - j][i] - 1
            else:
                maze[curR + i][curC + j] = 0

            for k in range(1, m+1):
                if state[k] == exited:
                    continue
                if side - j + curR == r[k] and i + curC == c[k]:
                    nr[k], nc[k] = curR+i, curC+j
            if side - j + curR == exit[0] and i + curC == exit[1]:
                nextExit[0], nextExit[1] = curR + i, curC + j

    for i in range(1, m + 1):
        if state[k] == exited:
            continue
        r[i], c[i] = nr[i], nc[i]
    exit = nextExit

for step in range(k):
    movePlayers()
    if sum(state[1:m+1]) == exited:
        break
    curR, curC, side = getSmallSquare()
    rotateSquare(curR, curC, side)

print(sum(dist))
print(*exit)