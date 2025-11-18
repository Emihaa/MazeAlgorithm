import pygame
import random
import time

# "py -3.11 maze.py" to run the script

# todo:
# - change screen resolution
# - clean up the code, maybe like atleast two files
# create a maze class and add all the globals there maybe instead?

pygame.init()

screen_width    = 500
screen_height   = 500
seed            = 9
seed_i          = 0
delay_time      = 50

# Maze info
rows        = 10
columns     = 20
space       = 2
margin      = 10
sq_color1   = [155,70,100]
sq_color2   = [240,240,240]
sq_color3   = [200,200,200]
bg_color    = [255,255,255]

# we want there always be uneven number of rows and columns
if rows % 2 == 0:
    rows += 1
if columns % 2 == 0:
    columns += 1

# calculate the width of sq_width and sq_height
sq_width    = ((screen_width - margin/2) / rows) - space
sq_height   = ((screen_height - margin/2) / columns) - space

# if the sq_width and sq_heights are different values, then take the smaller one
if (sq_width != sq_height):
        if (sq_width > sq_height):
            sq_width = sq_height
        else :
            sq_height = sq_width

screen  = pygame.display.set_mode([screen_width, screen_height])

# initialize squares
class Square: #instead of index could be point
    def __init__(self, pos, border, room, color, spot):
        self._pos = pos
        self._border = border
        self._room = room
        self._color = color
        self._width = sq_width
        self._spot = spot

def GenerateSeed():
    random.seed(seed)
    grid = random.sample(range(0, rows * columns), rows * columns)
    return grid

# calculate the initial maze
def GenerateMaze():

    squares = []
    x = margin/2
    for i in range(rows):
        row = []
        y = margin/2
        for j in range(columns):
            color = sq_color1
            wall = False
            room = False
            if j == 0 or j == columns - 1 or i == 0 or i == rows - 1: # if first or last then it is border
                wall = True
                color = sq_color3
            if (wall != True and j % 2 != 0 and i % 2 != 0): # if it is odd then it is a room
                room = True
                color = sq_color2
            sq = Square((x,y), wall, room, color, [i,j])
            row.append(sq)
            y += space + sq_width
        squares.append(row)
        x += space + sq_width
    return squares

squares = GenerateMaze()
grid    = GenerateSeed()

def FloodFillRoom(x, y, list):
    sq = squares[x][y]
    if sq._room == True:
        FloodFill(sq, list)
    return list

# do FloodFill from the given square
def FloodFill(square, list):
    if square in list:
        return list
    
    list.append(square)
    (x, y) = square._spot

    # above
    if y > 0:
        FloodFillRoom(x, y - 1, list)
    # below
    if y < columns - 1:
        FloodFillRoom(x, y + 1, list)
    # right
    if x < rows - 1:
        FloodFillRoom(x + 1, y, list)
    # left
    if x > 0:
        FloodFillRoom(x - 1, y, list)
    
    return list


def BuildMaze(sq):
    (x, y) = sq._spot
    if sq._border == False and sq._room == False:
        rooms = 0

        # above
        listA = []
        if y > 0:
            listA = FloodFillRoom(x, y - 1, listA)

        if listA: # check if there is content inside the list
            rooms += 1

        # below
        listB = []
        if y < columns - 1:
            listB = FloodFillRoom(x, y + 1, listB)
        
        # then we check if the list is empthy and if it shares same elements with listA
        if listB and not (set(listA) & set(listB)):
            rooms += 1

        # right
        listC = []
        if x < rows - 1:
            listC = FloodFillRoom(x + 1, y, listC)
        
        if listC and not (set(listA) & set(listC)) and not (set(listB) & set(listC)):
            rooms += 1

        # left
        listD = []
        if x > 0:
            listD = FloodFillRoom(x - 1, y, listD)

        if listD and not (set(listA) & set(listD)) and not (set(listB) & set(listD)) and not (set(listC) & set(listD)):
            rooms += 1

        if rooms == 2:
            sq._color = sq_color2
            sq._room = True

# get square from the seed
def PickSquare(i):
    index = grid[i]
    #y = (int)math.floor(index / columns)
    y = (int)(index / rows)
    x = index - (y * rows)
    sq = squares[x][y]
    return sq

# the actual game loop
running = True
paused = False

delay = pygame.USEREVENT + 0
pygame.time.set_timer(delay, delay_time)

def KeyButtonEvents():
    global running, paused, seed, squares, grid, seed_i, delay_time

    if event.key == pygame.K_q:
        running = False
    if event.key == pygame.K_SPACE:
        paused = not paused
        if paused == True:
            pygame.time.set_timer(delay, 0)
        else:
            pygame.time.set_timer(delay, delay_time)
    if event.key == pygame.K_r:
        seed_i = 0
        squares.clear()
        squares = GenerateMaze()
        pygame.time.set_timer(delay, delay_time)
    if event.key == pygame.K_UP:
        seed_i = 0
        seed += 1
        squares.clear()
        grid = GenerateSeed()
        squares = GenerateMaze()
        if paused == True:
            paused = False
            pygame.time.set_timer(delay, delay_time)
    if event.key == pygame.K_DOWN:
        seed_i = 0
        seed -= 1
        squares.clear()
        grid = GenerateSeed()
        squares = GenerateMaze()
        if paused == True:
            paused = False
            pygame.time.set_timer(delay, delay_time)
    if event.key == pygame.K_RIGHT:
        if (delay_time > 30):
            delay_time -= 30
            pygame.time.set_timer(delay, delay_time)
        print(delay_time)
    if event.key == pygame.K_LEFT:
        if (delay_time < 3000):
            delay_time += 30
            pygame.time.set_timer(delay, delay_time)
        print(delay_time)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
           KeyButtonEvents()
        if event.type == delay:
            if seed_i < len(grid):
                sq = PickSquare(seed_i)
                BuildMaze(sq)
                seed_i += 1
            else:
                print("done")
                pygame.time.set_timer(delay, 0)
                paused = True

    screen.fill(bg_color)
    # draw the squares
    for row in squares:
        for sq in row:
            x,y = sq._pos
            pygame.draw.rect(screen, sq._color, [x, y, sq._width, sq._width])

    pygame.display.flip()

pygame.quit()