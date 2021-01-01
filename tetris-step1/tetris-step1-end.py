import random, time, pygame, sys
from pygame.locals import *

pygame.init()

WINDOW_H = 480
WINDOW_W = 640

BOARD_BLOCK_W = 10
BOARD_BLOCK_H = 20
BOX_SIZE = 20

XMARGIN = int((WINDOW_W - BOARD_BLOCK_W * BOX_SIZE)/2)
TOPMARGIN = WINDOW_H - (BOARD_BLOCK_H * BOX_SIZE) - 5

WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)

COLORS      = (     BLUE,      GREEN,      RED,      YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)

BOARD_BORDER_COLOR = BLUE
BOARD_BK_COLOR = BLACK

BLANK = '.'
MOVED = '*'

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    DISPLAYSURF = pygame.display.set_mode((WINDOW_W, WINDOW_H), 0, 32)
    pygame.display.set_caption('Tetris')
    FPSCLOCK = pygame.time.Clock()
    board = getBlankBoard()
    lastFallTime = time.time()
    board[0][0] = random.randint(0, len(COLORS)-1)
    board[1][1] = random.randint(0, len(COLORS)-1)
    board[2][2] = random.randint(0, len(COLORS)-1)
    board[3][3] = random.randint(0, len(COLORS)-1)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        DISPLAYSURF.fill(GRAY)                            
        if time.time() - lastFallTime > 0.3:
            advanceBoxes(board)
            lastFallTime = time.time()
            print("step")
        drawBoardFrame()
        drawBoard(board)    
        pygame.display.update()    
        FPSCLOCK.tick(25)                           

def convertToPixelCoords(boxx, boxy):
    return (XMARGIN + (boxx * BOX_SIZE)), (TOPMARGIN + (boxy * BOX_SIZE))

def drawBoard(board):
    for x in range(BOARD_BLOCK_W):
        for y in range(BOARD_BLOCK_H):
            if board[x][y] != BLANK:
                drawBox(x, y, board[x][y])

def advanceBoxes(board):
    moves = []
    for x in range(BOARD_BLOCK_W):
        for y in reversed(range(BOARD_BLOCK_H)):
            if board[x][y] != BLANK and y+1 < BOARD_BLOCK_H and board[x][y+1] == BLANK:
                moves.append((x,y))
    for (x,y) in moves:
        board[x][y+1] = board[x][y]
        board[x][y] = BLANK

def getBlankBoard():
    board = []
    for i in range(BOARD_BLOCK_W):
        board.append([BLANK] * BOARD_BLOCK_H)
    return board

def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOX_SIZE - 1, BOX_SIZE - 1))
    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOX_SIZE - 4, BOX_SIZE - 4))

def drawBoardFrame():
    pygame.draw.rect(DISPLAYSURF, YELLOW, (XMARGIN - 3, TOPMARGIN - 3, (BOARD_BLOCK_W * BOX_SIZE) + 5, (BOARD_BLOCK_H * BOX_SIZE) + 5), 3)
    pygame.draw.rect(DISPLAYSURF, BOARD_BK_COLOR, (XMARGIN, TOPMARGIN, BOX_SIZE * BOARD_BLOCK_W, BOX_SIZE * BOARD_BLOCK_H))

if __name__ == '__main__':
    main()
