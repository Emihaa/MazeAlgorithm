import pygame
import random

# py -3.11 maze.py to run the script

# todo:
# - change screen resolution
# - exit from Q
# - many other

pygame.init()

screen_width    = 500
screen_height   = 500

# Maze info
rows        = 20
columns     = 20
space       = 2
border      = 10
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
sq_width    = ((screen_width - border/2) / rows) - space
sq_height   = ((screen_height - border/2) / columns) - space

# if the sq_width and sq_heights are different values, then take the smaller one
if (sq_width != sq_height):
        if (sq_width > sq_height):
            sq_width = sq_height
        else :
            sq_height = sq_width

screen = pygame.display.set_mode([screen_width, screen_height])

# initialize squares
class Square: #instead of index could be point
    def __init__(self, pos, wall, room, color, spot):
        self._pos = pos
        self._wall = wall
        self._room = room
        self._color = color
        self._width = sq_width
        self._spot = spot


# calculate the initial maze
def GenerateMaze():
    squares = []
    x = border/2
    for i in range(rows):
        row = []
        y = border/2
        for j in range(columns):
            color = sq_color1
            wall = False
            room = False
            if j == 0 or j == columns - 1 or i == 0 or i == rows - 1:
                wall = True
                color = sq_color3
            if (wall != True and j % 2 != 0 and i % 2 != 0):
                room = True
                color = sq_color2
            sq = Square((x,y), wall, room, color, [i,j])
            row.append(sq)
            y += space + sq_width
        squares.append(row)
        x += space + sq_width
    return squares

squares = GenerateMaze()

def FloodFillRoom(x, y, list):
    sq = squares[x][y]
    if sq._room == True:
        FloodFill(sq, list)


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


# the actual game loop
running = True
paused = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # button events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_SPACE:
                paused = not paused
            if event.key == pygame.K_r:
                squares.clear()
                squares = GenerateMaze()

    screen.fill(bg_color)
    for row in squares:
        for sq in row:
            x,y = sq._pos
            pygame.draw.rect(screen, sq._color, [x, y, sq._width, sq._width])

    if paused == False:
        # randomly pick a square
        row = random.choice(squares)
        sq = random.choice(row)
        if sq._wall == False and sq._room == False:
            rooms = 0
            (x, y) = sq._spot

            # above
            listA = []
            if y > 0:
                new_sq = squares[x][y - 1]
                if new_sq._room == True:
                    listA = FloodFill(new_sq, listA)

            if listA: # check if there is content inside the list
                rooms += 1

            # below
            listB = []
            if y < columns - 1:
                new_sq = squares[x][y + 1]
                if new_sq._room == True:
                    listB = FloodFill(new_sq, listB)
            
            # then we check if the list is empthy and if it shares same elements with listA
            if listB and not (set(listA) & set(listB)):
                rooms += 1

            # right
            listC = []
            if x < rows - 1:
                new_sq = squares[x + 1][y]
                if new_sq._room == True:
                    listC = FloodFill(new_sq, listC)
            
            if listC and not (set(listA) & set(listC)) and not (set(listB) & set(listC)):
                rooms += 1

            # left
            listD = []
            if x > 0:
                new_sq = squares[x - 1][y]
                if new_sq._room == True:
                    listD = FloodFill(new_sq, listD)

            if listD and not (set(listA) & set(listD)) and not (set(listB) & set(listD)) and not (set(listC) & set(listD)):
                rooms += 1

            if rooms == 2:
                sq._color = sq_color2
                sq._room = True
            
            # if check if removing the square will combine two rooms together
            # if so remove the square
            # if no  rooms are combinet together or more than 2 are combined
            # then dont remove the room
            


    pygame.display.flip()

pygame.quit()