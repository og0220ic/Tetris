import Tkinter
import random
import copy
import sys

BLOCK_SIZE = 30
WIDTH = 10
HEIGHT = 20

moveX, moveY = 5, 2

minoT = [[-1, 0], [0, 0], [1, 0], [0, 1]]
minoJ = [[0, 0], [-1, 0], [1, 0], [-1, -1]]
minoL = [[0, 0], [-1, 0], [1, 0], [1, -1]]
minoS = [[0, 0], [-1, 0], [0, -1], [1, -1]]
minoZ = [[0, 0], [1, 0], [0, -1], [-1, -1]]
minoI = [[0, 0], [0, -1], [0, 1], [0, 2]]
minoO = [[0, 0], [0, 1], [1, 0], [1, 1]]
mino_shapes = [minoT, minoJ, minoL, minoS, minoZ, minoI, minoO]
mino_colors = ["#FF00FF", "#0000FF", "#FF4F02", "#00FF00", "#FF0000", "#00FFFF", "#FFFF00", "black", "white"]
mino_type = random.randint(0, 6)

field = []
for y in range(HEIGHT + 2):
    sub = []
    for x in range(WIDTH + 2):
        if x == 0 or x == 11 or y == 21:
            sub.append(8)
        else:
            sub.append(7)
    field.append(sub)

def drawBlock():
    global mino_type
    for i in range(4):
        x = (mino_shapes[mino_type][i][0]+moveX) * BLOCK_SIZE
        y = (mino_shapes[mino_type][i][1]+moveY) * BLOCK_SIZE
        canvas.create_rectangle(x, y, x+BLOCK_SIZE, y+BLOCK_SIZE, fill = mino_colors[mino_type])

def drawField():
    for y in range(21):
        for x in range(12):
            canvas.create_rectangle(x*BLOCK_SIZE, y*BLOCK_SIZE, (x+1)*BLOCK_SIZE, (y+1)*BLOCK_SIZE, fill = mino_colors[field[y+1][x]])

def judge(nextX, nextY, nextMino):
    global moveX, moveY
    result = True
    for i in range(4):
        x = nextMino[i][0]+nextX
        y = nextMino[i][1]+nextY
        if field[y+1][x] != 7:
            result = False
    if result == True:
        moveX = nextX
        moveY = nextY
        mino_shapes[mino_type] = nextMino
    return result

def keyPress(event):
    global moveX, moveY
    nextX = moveX
    nextY = moveY
    nextMino = copy.copy(mino_shapes[mino_type])
    print(nextMino)
    print("--------------------")
    if event.keysym == "Right":
        nextX += 1
    elif event.keysym == "Left":
        nextX -= 1
    elif event.keysym == "Up":
        nextY -= 1
    elif event.keysym == "Down":
        nextY += 1
    elif event.keysym == "x":
        for i in range(4):
            posX = mino_shapes[mino_type][i][0]
            posY = mino_shapes[mino_type][i][1]
            nextMino[i][0] = posY
            nextMino[i][1] = posX * (-1)
    print(nextMino)
    print("====================")
    judge(nextX, nextY, nextMino)


def dropTetris():
    global moveX, moveY, mino_type
    nextMino = copy.copy(mino_shapes[mino_type])
    result = judge(moveX, moveY + 1, nextMino)
    if result == False:
        for i in range(4):
            x = mino_shapes[mino_type][i][0] + moveX
            y = mino_shapes[mino_type][i][1] + moveY
            field[y+1][x] = mino_type
        deleteLine()
        mino_type = random.randint(0, 6)
        moveX, moveY = 5, 2
    canvas.after(1000, dropTetris)

def deleteLine():
    for i in range(1, 21):
        if 7 not in field[i]:
            for j in range(i):
                for k in range(12):
                    field[i-j][k] = field[i-j-1][k]


def gameLoop():
    canvas.delete("all")
    drawField()
    drawBlock()
    canvas.after(50, gameLoop)

root = Tkinter.Tk()
root.title(u"Tetris")
canvas = Tkinter.Canvas(root, width = (WIDTH+2)*BLOCK_SIZE, height = (HEIGHT+1)*BLOCK_SIZE)
canvas.pack()

root.bind("<KeyPress>", keyPress)
gameLoop()
dropTetris()
root.mainloop()