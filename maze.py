import pygame

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

class Square:
    def __init__(self, pos, wall, room, color):
        self.pos = pos
        self.wall = wall
        self.room = room
        self.color = color
        self.width = sq_width

squares = []

x = border/2
for i in range(rows):
    y = border/2
    for j in range(columns):
        wall = False
        room = False
        if j == 0 or j == columns - 1 or i == 0 or i == rows - 1:
            wall = True
        if (wall != True and j % 2 != 0 and i % 2 != 0):
            room = True
        sq = Square((x,y), wall, room, sq_color1)
        squares.append(sq)
        y += space + sq_width
    x += space + sq_width

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(bg_color)
    for sq in squares:
        x,y = sq.pos
        if sq.room is True:
            sq.color = sq_color2
        if sq.wall is True:
            sq.color = sq_color3
        pygame.draw.rect(screen, sq.color, [x, y, sq.width, sq.width])

    pygame.display.flip()

pygame.quit()