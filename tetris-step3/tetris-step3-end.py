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
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    board = getBlankBoard()
    lastFallTime = time.time() 
    score = 0   
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYUP and event.key == K_SPACE:
                generateBox(board)
            if event.type == KEYUP and event.key == K_DOWN:
                accelerateBoxes(board)
            if event.type == KEYUP and event.key == K_RIGHT:
                moveBoxesX(board, 1)
            if event.type == KEYUP and event.key == K_LEFT:
                moveBoxesX(board, -1)        
        DISPLAYSURF.fill(GRAY)
        if time.time() - lastFallTime > 0.25 - (score * 0.02):
            advanceBoxes(board)
            score += clearFullLine(board)
            lastFallTime = time.time()            
        drawBoardFrame()
        drawBoard(board) 
        drawScore(score)   
        pygame.display.update()    
        FPSCLOCK.tick(15)                           

def convertToPixelCoords(boxx, boxy):
    return (XMARGIN + (boxx * BOX_SIZE)), (TOPMARGIN + (boxy * BOX_SIZE))

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % score, True, YELLOW)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOW_W - 150, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def moveBoxesX(board, change):
    moves = {}
    for x in range(BOARD_BLOCK_W):
        for y in reversed(range(BOARD_BLOCK_H)):
            if board[x][y] != BLANK and not finishedFalling(board, x, y):                                             
                nextX = x + change
                if nextX < 0 or nextX > BOARD_BLOCK_W - 1:
                    nextX = x
                moves.update({(nextX,y): board[x][y]})
                board[x][y] = BLANK
    for coords, color in moves.items():
        board[coords[0]][coords[1]] = color
        
def accelerateBoxes(board):
    for x in range(BOARD_BLOCK_W):
        for y in reversed(range(BOARD_BLOCK_H)):
            if board[x][y] != BLANK and not finishedFalling(board, x, y):                                             
                for nextY in range(BOARD_BLOCK_H - 1, y, -1):
                    if board[x][nextY] == BLANK:                        
                        board[x][nextY] = board[x][y]
                        board[x][y] = BLANK
                        break

def drawBoard(board):
    for x in range(BOARD_BLOCK_W):
        for y in range(BOARD_BLOCK_H):
            if board[x][y] != BLANK:
                drawBox(x, y, board[x][y])

def generateBox(board):
    board[random.randint(0, BOARD_BLOCK_W-1)][0] = random.randint(0, len(COLORS)-1)

def finishedFalling(board, x, y):
    nextY = y + 1
    if nextY > BOARD_BLOCK_H - 1:
        nextY = y
    if board[x][nextY] == BLANK:
        return False   
    return True

def clearFullLine(board):
    y = BOARD_BLOCK_H - 1
    removedLines = 0 
    while y >= 0:
        completed = True
        for x in range(BOARD_BLOCK_W):
            if board[x][y] == BLANK or not finishedFalling(board, x, y):
                completed = False
        if completed:
            for pullDownY in range(y, 0, -1):
                for x in range(BOARD_BLOCK_W):                
                    board[x][pullDownY] = board[x][pullDownY-1] 
            removedLines += 1
        y -= 1
    return removedLines

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
