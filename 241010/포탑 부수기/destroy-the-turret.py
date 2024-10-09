import sys
input = sys.stdin.readline

from collections import deque

n, m, k = map(int, input().split())
area = [list(map(int, input().split())) for _ in range(n)]
time = [[0 for _ in range(m)] for _ in range(n)]
visited = [[0 for _ in range(m)] for _ in range(n)]
attacker = target = (-1, -1)
trajectory = {}
dr, dc = [0, 1, 0, -1], [1, 0, -1, 0]
dr2, dc2 = [0, 1, 0, -1, 1, -1, 1, -1], [1, 0, -1, 0, 1, 1, -1, -1]
isActive = [[0 for _ in range(m)] for _ in range(n)]
backR = [[0 for _ in range(m)] for _ in range(n)]
backC = [[0 for _ in range(m)] for _ in range(n)]

def selectTarget():
    dmg = 0

    r, c = -1, -1
    old = float('inf')
    minSum = minR = float('inf')
    # 공격력이 가장 낮은 포탑
    for i in range(n):
        for j in range(m):
            if area[i][j] == 0:
                continue

            if area[i][j] > dmg:
                dmg = area[i][j]
                old = time[i][j]
                minSum = i + j
                minR = -1
                r, c = i, j

            elif area[i][j] == dmg:  # 가장 최근에 공격한 포탑
                if old > time[i][j]:
                    old = time[i][j]
                    minSum = i + j
                    minR = -1
                    r, c = i, j
                elif old == time[i][j]:  # 가장 행과 열의 합이 가장 큰 포탑
                    if minSum > i + j:
                        old = time[i][j]
                        minSum = i + j
                        minR = -1
                        r, c = i, j
                    elif minSum == i + j:  # 가장 열 값이 큰 포탑
                        if minR > i:
                            old = time[i][j]
                            minSum = i + j
                            minR = -1
                            r, c = i, j
    return r, c

def selectAttacker():
    dmg = float('inf')
    towers = {}

    r, c = -1, -1
    recent = -1
    maxSum = maxR = -1
    # 공격력이 가장 낮은 포탑
    for i in range(n):
        for j in range(m):
            if area[i][j] == 0:
                continue

            if area[i][j] < dmg:
                dmg = area[i][j]
                recent = time[i][j]
                maxSum = i+j
                maxR = -1
                towers = {}
                towers[f'({i},{j})'] = 1
                r, c = i, j

            elif area[i][j] == dmg: # 가장 최근에 공격한 포탑
                if recent < time[i][j]:
                    recent = time[i][j]
                    maxSum = i + j
                    maxR = -1
                    towers = {}
                    towers[f'({i},{j})'] = 1
                    r, c = i, j
                elif recent == time[i][j]: # 가장 행과 열의 합이 가장 큰 포탑
                    if maxSum < i + j:
                        recent = time[i][j]
                        maxSum = i + j
                        maxR = -1
                        towers = {}
                        towers[f'({i},{j})'] = 1
                        r, c = i, j
                    elif maxSum == i + j: # 가장 열 값이 큰 포탑
                        if maxR < i:
                            recent = time[i][j]
                            maxSum = i + j
                            maxR = -1
                            towers = {}
                            towers[f'({i},{j})'] = 1
                            r, c = i, j
    return r, c

def attackLaser(attacker, target):
    global visited
    tR, tC = target
    aR, aC = attacker

    q = deque()
    q.append(attacker)
    visited[aR][aC] = 1
    isActive[aR][aC] = 1
    isPossible = False

    while q:
        r, c = q.popleft()

        if r == tR and c == tC:
            isPossible = True
            break

        for idx in range(4):
            nr, nc = (r + dr[idx] + n) % n, (c + dc[idx] + m) % m

            if visited[nr][nc] or area[nr][nc] == 0:
                continue

            visited[nr][nc] = 1
            backR[nr][nc] = r
            backC[nr][nc] = c
            q.append((nr, nc))

    if isPossible:
        area[tR][tC] -= area[aR][aC]
        if area[tR][tC] < 0:
            area[tR][tC] = 0
        isActive[tR][tC] = 1

        cR, cC = backR[tR][tC], backC[tR][tC]

        while 1:
            if cR == aR and cC == aC:
                break

            area[cR][cC] -= area[aR][aC] // 2
            if area[cR][cC] < 0:
                area[cR][cC] = 0
            isActive[cR][cC] = 1

            cR, cC = backR[cR][cC], backC[cR][cC]

    return isPossible

def attackCannon(attacker, target):
    global visited
    tR, tC = target
    aR, aC = attacker

    isActive[tR][tC] = 1
    area[tR][tC] -= area[aR][aC] // 2
    if area[tR][tC] < 0:
        area[tR][tC] = 0

    for idx in range(8):
        nr, nc = (tR + dr[idx] + n) % n, (tC + dc[idx] + m) % m
        isActive[nr][nc] = 1
        area[nr][nc] -= area[aR][aC] // 2
        if area[nr][nc] < 0:
            area[nr][nc] = 0


def repairTower():
    for i in range(n):
        for j in range(m):
            if isActive[i][j] == 0 and area[i][j]:
                area[i][j] += 1

def attack(step):
    global attacker, target
    attacker = selectAttacker()
    target = selectTarget()
    area[attacker[0]][attacker[1]] += n + m
    time[attacker[0]][attacker[1]] = step
    if attackLaser(attacker, target):
        pass
    else:
        attackCannon(attacker, target)
    repairTower()
    # print(*area, sep="\n", end="\n\n")

def init():
    global visited, isActive, backR, backC
    visited = [[0 for _ in range(m)] for _ in range(n)]
    isActive = [[0 for _ in range(m)] for _ in range(n)]
    backR = [[0 for _ in range(m)] for _ in range(n)]
    backC = [[0 for _ in range(m)] for _ in range(n)]


for step in range(1, k+1):
    init()
    attack(step)
    repairTower()

ans = 0
for i in range(n):
    for j in range(m):
        ans = max(ans, area[i][j])
print(ans)