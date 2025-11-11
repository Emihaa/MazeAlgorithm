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

# if the sq_width and sq_heights are different values, then take the bigger one
if (sq_width != sq_height):
        if (sq_width > sq_height):
            sq_height = sq_width
        else :
            sq_width = sq_height

screen = pygame.display.set_mode([screen_width, screen_height])

# initialize squares
class Square:
    def __init__(self, pos, wall, room, color, index):
        self._pos = pos
        self._wall = wall
        self._room = room
        self._color = color
        self._width = sq_width
        self._index = index

squares = []

# calculate the initial maze
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

# the actual game loop
running = True
paused = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Toggle pause with spacebar
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused

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
            (x,y) = sq._index
            # if check if removing the square will combine two rooms together
            # if so remove the square
            # if no  rooms are combinet together or more than 2 are combined
            # then dont remove the room
            
            # each time we need to check four different squares above, below, right and left
            # this isnt as simple as this. Because i need to do here the flood fill to check if the rooms
            # are already connected or not. So here is the spot where i need to create the flood fill and see how many rooms
            # i truly have
            rooms = 0
            # above
            next_square = squares[x][y - 1]
            if next_square and next_square._room == True:
                rooms += 1
            # below
            next_square = squares[x][y + 1]
            if next_square and next_square._room == True:
                rooms += 1
            # right
            next_square = squares[x + 1][y]
            if next_square and next_square._room == True:
                rooms += 1
            # left
            next_square = squares[x - 1][y]
            if next_square and next_square._room == True:
                rooms += 1
            
            if rooms == 2:
                sq._room = True
                sq._color = sq_color2

    pygame.display.flip()

pygame.quit()