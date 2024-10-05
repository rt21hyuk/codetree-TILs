import sys
input = sys.stdin.readline

from collections import deque

R, C, k = map(int, input().split())
infos = [list(map(int, input().split())) for i in range(k)]
area = [[0 for _ in range(C)] for _ in range(R+3)]
visited = [[0 for _ in range(C)] for _ in range(R+3)]
dr, dc = [-1, 0, 1, 0], [0, 1, 0, -1]
answer = 0
cnt = 1
direction = {0:'북', 1:'동', 2:'남', 3:'서'}

def init():
    global area, cnt
    area = [[0 for _ in range(C)] for _ in range(R+3)]
    cnt = 1

def canDown(r, c):
    if r + 2 >= R+3 or c - 1 < 0 or c + 1 >= C:
        return False
    if area[r + 2][c] or area[r + 1][c - 1] or area[r + 1][c + 1]:
        return False
    return True

def canLeft(r, c):
    if r + 2 >= R+3 or c - 2 < 0 or c + 1 >= C:
        return False
    if area[r][c - 2] or area[r - 1][c - 1] or area[r + 1][c - 1]:
        return False
    if area[r + 2][c - 1] or area[r + 1][c - 2]:
        return False
    return True

def canRight(r, c):
    if r + 2 >= R+3 or c - 1 < 0 or c + 2 >= C:
        return False
    if area[r][c + 2] or area[r - 1][c + 1] or area[r + 1][c + 1]:
        return False
    if area[r + 2][c + 1] or area[r + 1][c + 2]:
        return False
    return True

def action(c, dir):
    r = 0
    while 1:
        if canDown(r, c):
            r += 1
        elif canLeft(r, c):
            r += 1
            c -= 1
            dir = (dir + 3) % 4
        elif canRight(r, c):
            r += 1
            c += 1
            dir = (dir + 1) % 4
        else:
            return r, c, dir

def isFull(r, c):
    for i in range(4):
        if (r + dr[i]) < 3 or (c + dc[i]) < 0 or (c + dc[i]) >= C:
            return True
    return False

def bfs(r, c, dirIdx, cnt):
    global answer, exits
    area[r][c] = cnt; area[r-1][c] = cnt; area[r+1][c] = cnt; area[r][c-1] = cnt; area[r][c+1] = cnt; area[r+dr[dirIdx]][c+dc[dirIdx]] = -cnt
    visited[r+dr[dirIdx]][c+dc[dirIdx]] = 1
    q = deque([(r+dr[dirIdx], c+dc[dirIdx])])
    maxR = r+1

    while q:
        cr, cc = q.popleft()
        cur = area[cr][cc]
        maxR = max(maxR, cr)
        if cr == R+2:
            break

        for idx in range(4):
            nr, nc = cr + dr[idx], cc + dc[idx]

            if nr < 0 or nc < 0 or nr >= R+3 or nc >= C:
                continue
            if area[nr][nc] == 0 or visited[nr][nc]:
                continue
            if cur < 0 and area[nr][nc]:
                visited[nr][nc] = 1
                q.append((nr, nc))
            if cur > 0 and (area[nr][nc] == cur or area[nr][nc] == -cur):
                visited[nr][nc] = 1
                q.append((nr, nc))
    answer += maxR-2

for idx in range(k):
    visited = [[0 for _ in range(C)] for _ in range(R+3)]
    start, dir = infos[idx]
    r, c, dir = action(start-1, dir)
    if isFull(r, c):
        init()
        continue
    bfs(r, c, dir, cnt)
    cnt += 1
print(answer)