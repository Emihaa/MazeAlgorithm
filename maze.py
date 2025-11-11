import pygame

pygame.init()

screen_width    = 500
screen_height   = 500

# Maze info
rows        = 6
columns     = 6
space       = 2
border      = 10
sq_color1   = [155,70,100]
sq_color2   = [240,240,240]
bg_color    = [255,255,255]

# lets first just initialize something
sq_width    = ((screen_width - border/2) / rows) - space
sq_height   = ((screen_height - border/2) / columns) - space

# the squares are well squares so lets take the biggest side
if (screen_width is not screen_height):
    if (screen_width > screen_height):
        sq_width = screen_width / rows
        sq_height = sq_width
    else :
        sq_height = screen_height / columns
        sq_width = sq_height




screen = pygame.display.set_mode([screen_width, screen_height])

class Square:
    def __init__(self, pos, wall, fill, color):
        self.pos = pos
        self.wall = wall
        self.fill = fill
        self.color = color
        self.width = sq_width
        self.draw()
    
    def draw(self):
        x,y = self.pos
        if wall is True:
            self.color = sq_color2
        pygame.draw.rect(screen, self.color, [x, y, self.width, self.width])


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255,255,255))
    
    x = border/2
    for i in range(rows):
        y = border/2
        for j in range(columns):
            wall = False
            if j == 0 or j == columns - 1 or i == 0 or i == rows - 1:
                wall = True
            sq = Square((x,y), wall, False, sq_color1)
            y += space + sq_width
        x += space + sq_width
        

    pygame.display.flip()

pygame.quit()