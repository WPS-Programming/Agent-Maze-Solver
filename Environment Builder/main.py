import numpy as np
import pygame
import pygame.gfxdraw

from AAfilledRoundedRect import AAfilledRoundedRect
from colors import *

pygame.init()

WIDTH = 1000
HEIGHT = 800
FPS = 144
OFFSET = 25

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Environment Builder')
clock = pygame.time.Clock()

grid = np.zeros(shape=(50,50))
selector = 'wall'
teleporter = 0

def draw_background(screen):

    screen.fill(Gunmetal)
    pygame.gfxdraw.line(screen, 800, 0, 800, HEIGHT, Timberwolf)
    AAfilledRoundedRect(screen, Independence, (OFFSET, OFFSET ,750,750), 0.025)

    for y in range(1,50):
        for x in range(1,50):

            pygame.gfxdraw.line(screen, OFFSET + (15 * x), y+OFFSET, OFFSET + (15 * x), HEIGHT-OFFSET-1, Timberwolf)
        pygame.gfxdraw.line(screen, OFFSET,  OFFSET + (15 * y), WIDTH-200-OFFSET, OFFSET + (15 * y), Timberwolf)

    # Draw wall selector
    pygame.draw.rect(screen, (30,30,30), (850,25,100,100))
    # Draw eraser selector
    pygame.draw.rect(screen, (220,220,220), (850,150,100,100))

    # start
    pygame.draw.rect(screen, (70, 212, 122), (825,300,75,75))
    # end
    pygame.draw.rect(screen, (68, 156, 212), (900,300,75,75))

    # teleporter button
    pygame.draw.rect(screen, Teleporters[teleporter%4], (850, 500, 100, 100))
    

def draw_grid_items(screen, grid):

    for y, row in enumerate(grid):
        for x, item in enumerate(row):
            
            if item == 1:
                pygame.draw.rect(screen, (0,0,0), (x*15 + OFFSET+1, y*15 + OFFSET+1, 14,14))
            if item == 2:
                pygame.draw.rect(screen, (70, 212, 122), (x*15 + OFFSET+1, y*15 + OFFSET+1, 14,14))
            if item == 3:
                pygame.draw.rect(screen, (68, 156, 212), (x*15 + OFFSET+1, y*15 + OFFSET+1, 14,14))
            if item >= 10 and item % 10 == 0:
                index = int((item/10) -1)
                pygame.draw.rect(screen, Teleporters[index%4], (x*15 + OFFSET+1, y*15 + OFFSET+1, 14,14))
            if item >= 10 and item % 11 == 0:
                index = int((item/10) -1)
                pygame.draw.rect(screen, Teleporters[index%4], (x*15 + OFFSET+1, y*15 + OFFSET+1, 14,14), 2)

running = True
while running:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if (mx >= 850 and mx <= 950) and (my >= 25 and my <= 125):
                print("Wall selected")
                selector = 'wall'
            elif (mx >= 850 and mx <= 950) and (my >= 150 and my <= 250):
                print("Empty Selected")
                selector = 'empty'
            elif (mx >= 825 and mx <= 900) and (my >= 300 and my <= 375):
                print("Start selected")
                selector = 'start'
            elif (mx >= 900 and mx <= 975) and (my >= 300 and my <= 375):
                print("End selected")
                selector = 'end'
            elif (mx >= 850 and mx <= 950) and (my >= 500 and my <= 600):
                if selector == "teleporter":
                    teleporter += 1
                    print("teleporter changed")
                else:
                    selector = "teleporter"
                    print("Teleporter selected")
            
            if (mx > OFFSET and mx < WIDTH-200-OFFSET) and (my > OFFSET and my < HEIGHT-OFFSET):
                row = round(my/15) -2
                if row >= 50: row = 49
                col = round(mx/15) -2
                if col >= 50: col = 49

                if selector == 'start':
                    for y, rowa in enumerate(grid):
                        for x, item in enumerate(rowa):

                            if item == 2:
                                grid[y][x] = 0
                    grid[row][col] = 2 
                if selector == 'end':
                    for y, rowa in enumerate(grid):
                        for x, item in enumerate(rowa):

                            if item == 3:
                                grid[y][x] = 0
                                print(grid[y][x])
                    grid[row][col] = 3 

                if selector == "teleporter":
                    if pygame.mouse.get_pressed()[0]:
                        for y, rowa in enumerate(grid):
                            for x, item in enumerate(rowa):

                                if item == (10 * (teleporter+1)):
                                    grid[y][x] = 0
                        grid[row][col] = 10 * (teleporter +1)
                    
                    if pygame.mouse.get_pressed()[2]:
                        for y, rowa in enumerate(grid):
                            for x, item in enumerate(rowa):

                                if item == (11 * (teleporter+1)):
                                    grid[y][x] = 0
                        grid[row][col] = 11 * (teleporter +1)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                '''
                new_grid = grid.transpose().copy()
                new_grid = new_grid[~np.all(grid == 0, axis=1)]
                mask = (new_grid == 0).all(0)
                column_indices = np.where(mask)[0]
                new_grid = new_grid[:,~mask]

                height = len(new_grid)
                width = len(new_grid[0])
                print(height, width)

                if height > width:
                    width = height
                else:
                    height = width

                final_grid = np.copy(new_grid)
                final_grid.resize((height,width))
                print(height,width)
                '''

                g = grid.copy()
                # Top down cleaning
                while not g[0].any():
                    g = g[1:]
                
                # Down up cleaning
                while not g[-1].any():
                    g = g[:-1]
                
                # Left -> right cleaning
                while not g[:,0].any():
                    g = np.delete(g, 0, 1)

                # Right -> left cleaning
                while not g[:,-1].any():
                    g = np.delete(g, -1, 1)

                sq = max(len(g), len(g[0]))
                g.resize((sq,sq))

                np.savetxt('map.txt',g, fmt="%d")

    if pygame.mouse.get_pressed()[0] == 1:
        mx, my = pygame.mouse.get_pos()
        if (mx > OFFSET and mx < WIDTH-200-OFFSET) and (my > OFFSET and my < HEIGHT-OFFSET):
            row = round(my/15) -2;
            if row >= 50: row = 49;
            col = round(mx/15) -2
            if col >= 50: col = 49
            if selector == 'wall':
                grid[row][col] = 1
            elif selector == 'empty':
                grid[row][col] = 0

    draw_background(screen)
    draw_grid_items(screen, grid)

    pygame.display.flip()

pygame.quit()
