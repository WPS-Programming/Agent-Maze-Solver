import sys
sys.path.append('../')

import time
from Environment import Env
import settings
import numpy as np
import pygame
import random

grid = np.loadtxt('map.txt')
env = Env(grid)
clock = pygame.time.Clock()
last_tick = 0

env.pygame_init()

while True:

    clock.tick(settings.FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            quit()
    
    if abs(last_tick - pygame.time.get_ticks()) > 500:
        env.draw()
        env.receive((random.randint(-1,1), random.randint(-1,1)))
        print(env)
        last_tick = pygame.time.get_ticks()
