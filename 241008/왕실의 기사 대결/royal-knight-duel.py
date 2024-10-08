import sys
input = sys.stdin.readline

from collections import deque

blank = 0; trap = 1; wall = 2

N_MAX = 31
L_MAX = 41

r = [0 for _ in range(N_MAX)]
c = [0 for _ in range(N_MAX)]
h = [0 for _ in range(N_MAX)]
w = [0 for _ in range(N_MAX)]
k = [0 for _ in range(N_MAX)]
hp = [0 for _ in range(N_MAX)]
dmg = [0 for _ in range(N_MAX)]
nr = [0 for _ in range(N_MAX)]
nc = [0 for _ in range(N_MAX)]
isMoved = [0 for _ in range(N_MAX)]

dr, dc = [-1, 0, 1, 0], [0, 1, 0, -1]

def tryMove(kIdx, dir):
    q = deque()
    for i in range(1, n+1):
        dmg[i] = 0
        isMoved[i] = 0
        nr[i] = r[i]
        nc[i] = c[i]
    q.append(kIdx)
    isMoved[kIdx] = 1

    while q:
        x = q.popleft()

        nr[x] += dr[dir]
        nc[x] += dc[dir]

        if nr[x] < 1 or nc[x] < 1 or nr[x] + h[x] > l+1 or nc[x] + w[x] > l+1:
            return False

        for i in range(nr[x], nr[x] + h[x]):
            for j in range(nc[x], nc[x] + w[x]):
                if boards[i][j] == trap:
                    dmg[x] += 1
                if boards[i][j] == wall:
                    return False

        for i in range(1, n+1):
            if isMoved[i] or k[i] <= 0:
                continue
            if r[i] > nr[x] + h[x] - 1 or nr[x] > r[i] + h[i] - 1:
                continue
            if c[i] > nc[x] + w[x] - 1 or nc[x] > c[i] + w[i] - 1:
                continue

            isMoved[i] = 1
            q.append(i)

    dmg[kIdx] = 0
    return True

def tryCommand(kIdx, dir):
    if k[kIdx] <= 0:
        return
    if tryMove(kIdx, dir):
        for i in range(1, n+1):
            r[i] = nr[i]
            c[i] = nc[i]
            k[i] -= dmg[i]

l, n, q = map(int, input().split())
boards = [[0 for _ in range(L_MAX)] for _ in range(L_MAX)]
for i in range(1, l+1):
    boards[i][1:] = map(int, input().split())
for i in range(1, n+1):
    r[i], c[i], h[i], w[i], k[i] = map(int, input().split())
    hp[i] = k[i]
cmds = [list(map(int, input().split())) for _ in range(q)]

for idx in range(q):
    kIdx, dir = cmds[idx]
    tryCommand(kIdx, dir)

ans = sum([hp[i] - k[i] for i in range(1, n+1) if k[i] > 0])
print(ans)