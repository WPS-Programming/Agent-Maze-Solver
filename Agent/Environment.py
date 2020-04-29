import pygame
import numpy as np

import pygame.gfxdraw
from settings import *


class Env():
    
    def __init__(self, grid):

        self.grid = grid
    
    def pygame_init(self):

        pygame.init()

        self.WIDTH, self.HEIGHT = optimal_size(self.grid)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(CAPTION)

    def draw(self):
        def background(self):
            
            self.screen.fill(Gunmetal)
            
            # Draw border line
            pygame.gfxdraw.line(self.screen, self.WIDTH-200, 0, self.WIDTH-200, self.HEIGHT, Glaucous) 



        background(self)

        pygame.display.flip()