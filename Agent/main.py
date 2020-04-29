import sys
sys.path.append('../')

import time
from Environment import Env
import settings
import numpy as np
import pygame

grid = np.loadtxt('map.txt')
env = Env(grid)
clock = pygame.time.Clock()

env.pygame_init()

while True:

    clock.tick(settings.FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            quit()
    
    env.draw()