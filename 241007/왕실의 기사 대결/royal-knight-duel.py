import sys
input = sys.stdin.readline

from collections import deque

blank = 0; trap = 1; wall = 2
# alive = 0; dead = 1

dr, dc = [-1, 0, 1, 0], [0, 1, 0, -1]

flag = 0
answer = 0

l, n, q = map(int, input().split())
boards = [[wall for _ in range(l+2)] for _ in range(l+2)]
visited = [0 for _ in range(n+1)]
for idx in range(1, l+1):
    boards[idx][1:l+1] = list(map(int, input().split()))
knightsBoards = [[blank for _ in range(l+2)] for _ in range(l+2)]
knights = [[0, 0, 0, 0, 0]] + [list(map(int, input().split())) for _ in range(n)] # r, c, w, h, k
cmds = [list(map(int, input().split())) for _ in range(q)]
damages = [0 for _ in range(n+1)]

def setKnights():
    for idx in range(1, n+1):
        knightR, knightC, knightH, knightW, _ = knights[idx]
        for h in range(knightH):
            for w in range(knightW):
                knightsBoards[knightR+h][knightC+w] = idx

def getPoint(knightIdx, dir):
    knightR, knightC, knightH, knightW, knightHP = knights[knightIdx]
    if dir == 0:
        return [[knightR, knightC+c] for c in range(knightW)]
    elif dir == 1:
        return [[knightR+r, knightC+knightW-1] for r in range(knightH)]
    elif dir == 2:
        return [[knightR+knightH-1, knightC+c] for c in range(knightW)]
    return [[knightR+r, knightC] for r in range(knightH)] # dir == 3

def moveKnight(knightIdx, dir):
    # print(f'knightIdx : {knightIdx}, {dir}')
    global visited, flag

    if knights[knightIdx][4] <= 0:
        return True

    points = getPoint(knightIdx, dir)
    # print(points)

    for point in points:
        curR, curC = point
        nextR, nextC = curR + dr[dir], curC + dc[dir]

        if nextR < 1 or nextC < 1 or nextR >= l + 1 or nextC >= l + 1:
            visited[knightIdx] = 0
            flag = 1
            return False
        if boards[nextR][nextC] == wall:
            visited[knightIdx] = 0
            flag = 1
            return False
        if knightsBoards[nextR][nextC] and visited[knightsBoards[nextR][nextC]] == 0:
            visited[knightsBoards[nextR][nextC]] = 1
            if moveKnight(knightsBoards[nextR][nextC], dir) == False:
                visited[knightsBoards[nextR][nextC]] = 0
                flag = 1
                return False
    return True

def getDamage(knightIdx):
    global answer

    for idx in range(1, n+1):
        if not visited[idx]:
            continue

        trapCnt = 0
        knightR, knightC, knightH, knightW, knightHP = knights[idx]
        if knightHP > 0 and knightIdx != idx:
            for r in range(knightH):
                for c in range(knightC):
                    if boards[knightR+r][knightC+c] == trap:
                        trapCnt += 1
        if knightHP - trapCnt <= 0:
            knights[idx][4] = 0
            damages[idx] = 0
        else:
            damages[idx] += trapCnt
    # print(damages)


def isPossible(knightIdx, dir):
    global knights, knightsBoards, visited

    if flag:
        knightsBoards = [knightsBoards[i][:] for i in range(l + 2)]
        return
    knightsBoards = [[blank for _ in range(l + 2)] for _ in range(l + 2)]

    # print(f'flag : {flag}')
    visited[knightIdx] = 1

    for idx in range(1, n+1):
        if visited[idx]:
            curR, curC, knightH, knightW, _ = knights[idx]
            nextR, nextC = curR + dr[dir], curC + dc[dir]
            knights[idx][:2] = nextR, nextC

            for h in range(knightH):
                for w in range(knightW):
                    knightsBoards[nextR+h][nextC+w] = idx
        else:
            curR, curC, knightH, knightW, _ = knights[idx]

            for h in range(knightH):
                for w in range(knightW):
                    knightsBoards[curR + h][curC + w] = idx


def init():
    global visited, flag
    flag = 0
    visited = [0 for _ in range(n + 1)]

setKnights()
for idx in range(q):
    # print(f'step : {idx}')
    init()
    # print(*knightsBoards, sep="\n", end="\n\n")
    knightIdx, dir = cmds[idx]
    moveKnight(knightIdx, dir)
    # print(f'visited : {visited}')

    isPossible(knightIdx, dir)
    # print(*knightsBoards, sep="\n", end="\n\n---------\n\n")
    getDamage(knightIdx)

print(sum(damages))