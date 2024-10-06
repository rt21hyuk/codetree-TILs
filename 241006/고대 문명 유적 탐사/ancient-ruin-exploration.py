import sys
input = sys.stdin.readline

from collections import deque

k, m = map(int, input().split())
area = [list(map(int, input().split())) for _ in range(5)]
pieces = deque(map(int, input().split()))
visited = [[0 for _ in range(5)] for _ in range(5)]
dr, dc = [-1, 0, 1, 0], [0, -1, 0, 1]
answers = []
answer = piecesIdx = 0
findCoords = []

def rotate(r, c):
    rotateNum = 1
    rotate90(r, c) # 90도
    maxScore = findRelics('get')

    rotate90(r, c) # 180도
    score = findRelics('get')
    if maxScore < score:
        rotateNum = 2
        maxScore = score

    rotate90(r, c) # 270도
    score = findRelics('get')
    if maxScore < score:
        rotateNum = 3
        maxScore = score

    rotate90(r, c) # 원상복구

    return maxScore, rotateNum

def rotate90(r, c):
    global area
    tempArea = [area[i][:] for i in range(5)]
    for i in range(-1, 2, 1):
        for j in range(1, -2, -1):
            area[r+i][c-j] = tempArea[r+j][c+i]

def bfs(r, c, mode):
    global area

    q = deque([(r, c)])
    visited[r][c] = 1
    cur = area[r][c]
    cnt = 1

    if mode == 'remove':
        findCoords = [(r, c)]

    while q:
        cr, cc = q.popleft()
        for idx in range(4):
            nr, nc = cr + dr[idx], cc + dc[idx]
            if nr < 0 or nc < 0 or nr >= 5 or nc >= 5:
                continue
            if visited[nr][nc] or area[nr][nc] != cur:
                continue
            q.append((nr, nc))
            visited[nr][nc] = 1
            if mode == 'remove':
                findCoords.append((nr, nc))
            cnt += 1

    if cnt <= 2:
        return 0

    if mode == 'remove':
        for r, c in findCoords:
            area[r][c] = 0

    return cnt

def findRelics(mode):
    global visited
    score = 0
    visited = [[0 for _ in range(5)] for _ in range(5)]

    for i in range(5):
        for j in range(5):
            if not visited[i][j]:
                score += bfs(i, j, mode)

    return score

def rotateAll():
    global answers, answer
    answer = 0
    bestR, bestC, rotateNum = 1, 1, 1

    for c in range(1, 4):
        for r in range(1, 4):
            score, num = rotate(r, c)
            if answer < score:
                bestR, bestC, rotateNum = r, c, num
                answer = score
            elif answer == score:
                if rotateNum > num:
                    bestR, bestC, rotateNum = r, c, num
                    answer = score

    if answer == 0:
        return 1

    for _ in range(rotateNum):
        rotate90(bestR, bestC)

    findRelics('remove')
    answers.append(answer)
    return 0

def fillPieces():
    global piecesIdx

    for i in range(5):
        for j in range(4, -1, -1):
            if area[j][i] == 0:
                area[j][i] = pieces[piecesIdx]
                piecesIdx += 1

for idx in range(k):
    flag = rotateAll()
    if flag:
        break

    while 1:
        fillPieces()
        score = findRelics('remove')
        answers[idx] += score
        if score == 0:
            break

print(*answers)