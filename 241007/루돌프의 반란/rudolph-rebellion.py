import sys
input = sys.stdin.readline

rudolph = -1
alive = 0
stun = 1
nextWake = 2
dead = 3

n, m, p, c, d = map(int, input().split())
rudolphR, rudolphC = map(int, input().split())
santaList = sorted([list(map(int, input().split())) for _ in range(p)], key=lambda x:x[0])
santaState = [alive for _ in range(p)] # 0:alive, 1:stun, 2:dead
santaScore = [0 for _ in range(p)]
aliveNum = p
area = [[0 for _ in range(n)] for _ in range(n)]

# 상 우 하 좌 좌상, 우상, 좌하, 우하
dr, dc = [-1, 0, 1, 0, -1, -1, 1, 1], [0, 1, 0, -1, -1, 1, -1, 1]

def setArea():
    global area
    area[rudolphR - 1][rudolphC - 1] = rudolph
    for idx in range(p):
        area[santaList[idx][1] - 1][santaList[idx][2] - 1] = santaList[idx][0]

def getDistance(r1, c1, r2, c2):
    return (r1-r2)**2 + (c1-c2)**2

def findMinSantaIdx():
    minDist = float('inf')
    minSantaIdx = minR = minC = -1

    for idx in range(p):
        if santaState[idx] != dead:
            santaNum, santaR, santaC = santaList[idx]
            dist = getDistance(rudolphR, rudolphC, santaR, santaC)
            if dist < minDist:
                minDist = dist
                minSantaIdx = santaNum - 1
                minR, minC = santaR, santaC
            elif dist == minDist:
                if minR < santaR:
                    minR, minC = santaR, santaC
                    minSantaIdx = santaNum - 1
                elif minR == santaR and minC < santaC:
                    minC = santaC
                    minSantaIdx = santaNum - 1

    return minSantaIdx

def pushSanta(santaIdx, dirIdx, pushType):
    global santaList, aliveNum, area
    _, santaR, santaC = santaList[santaIdx]
    nextR, nextC = santaR, santaC

    iter = 1
    if pushType == 'r':
        iter = c
    elif pushType == 's':
        iter = d-1

    nextR, nextC = nextR + iter*dr[dirIdx], nextC + iter*dc[dirIdx]
    if nextR < 1 or nextC < 1 or nextR > n or nextC > n:
        santaState[santaIdx] = dead
        aliveNum -= 1
        area[santaR-1][santaC-1] = 0
        return
    if area[nextR-1][nextC-1] > 0 and area[nextR-1][nextC-1] != santaIdx+1:
        otherSantaIdx = area[nextR-1][nextC-1] - 1
        pushSanta(otherSantaIdx, dirIdx, 'x')

    area[santaR-1][santaC-1] = 0
    area[nextR-1][nextC-1] = santaIdx + 1 # 제자리 튕기면 순서 중요 초기화 먼저하고 할당
    santaList[santaIdx][1], santaList[santaIdx][2] = nextR, nextC

    if pushType != 'x':
        santaState[santaIdx] = stun

def moveRudolph():
    global rudolphR, rudolphC
    nextR, nextC = rudolphR, rudolphC
    minDist = float('inf')
    minSantaIdx = findMinSantaIdx()
    minDirIdx = 0

    for dirIdx in range(8):
        tempR, tempC = rudolphR + dr[dirIdx], rudolphC + dc[dirIdx]
        dist = getDistance(tempR, tempC, santaList[minSantaIdx][1], santaList[minSantaIdx][2])
        if dist < minDist:
            minDist = dist
            minDirIdx = dirIdx
            nextR, nextC = tempR, tempC

    if minDist == 0:
        pushSanta(minSantaIdx, minDirIdx, 'r') # rudolph
        santaScore[minSantaIdx] += c
    # print(santaScore)
    area[nextR-1][nextC-1] = rudolph
    area[rudolphR-1][rudolphC-1] = 0
    rudolphR, rudolphC = nextR, nextC

def moveSantas():
    global santaList, area
    for idx in range(p):
        if santaState[idx] == alive:
            _, santaR, santaC = santaList[idx]
            minDist = getDistance(santaR, santaC, rudolphR, rudolphC)
            nextR = nextC = -1
            minDirIdx = -1

            for dirIdx in range(4):
                tempR, tempC = santaR+dr[dirIdx], santaC+dc[dirIdx]

                if tempR < 1 or tempC < 1 or tempR > n or tempC > n:
                    continue
                if area[tempR-1][tempC-1] > 0:
                    continue

                dist = getDistance(tempR, tempC, rudolphR, rudolphC)
                if dist < minDist:
                    minDist = dist
                    nextR, nextC = tempR, tempC
                    minDirIdx = dirIdx
                if dist == 0:
                    break

            if minDirIdx == -1:
                continue
            elif minDist == 0:
                pushSanta(idx, (minDirIdx + 2) % 4, 's') # santa
                santaScore[idx] += d
            else:
                area[nextR-1][nextC-1] = santaList[idx][0]
                area[santaList[idx][1]-1][santaList[idx][2]-1] = 0
                santaList[idx][1], santaList[idx][2] = nextR, nextC

def getScoreAliveSantas():
    global scoreList

    for idx in range(p):
        if santaState[idx] != dead:
            santaScore[idx] += 1

def printArea():
    # areaTest = [area[i][:] for i in range(n)]
    # areaTest[rudolphR-1][rudolphC-1] = rudolph
    # for idx in range(p):
    #     if santaState[idx] != dead:
    #         areaTest[santaList[idx][1]-1][santaList[idx][2]-1] = santaList[idx][0]
    print(*area, sep="\n", end="\n\n")

def setWake():
    global santaState
    for idx in range(p):
        if santaState[idx] == stun:
            santaState[idx] = nextWake

def setAlive():
    global santaState
    for idx in range(p):
        if santaState[idx] == nextWake:
            santaState[idx] = alive

setArea()
for idx in range(m):
    # print(f'Step : {idx}')

    setWake()
    # print('루돌프 이동 전')
    # printArea()

    moveRudolph()
    # print('루돌프 이동 후')
    # printArea()

    # print('산타 이동 후')
    moveSantas()
    # printArea()

    if aliveNum == 0:
        break
    getScoreAliveSantas()
    # print(santaScore, end="\n\n---------------------\n\n")
    setAlive()
print(*santaScore)