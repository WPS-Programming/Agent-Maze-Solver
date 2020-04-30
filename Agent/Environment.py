import pygame
import numpy as np

import pygame.gfxdraw
from settings import *
from AAfilledRoundedRect import AAfilledRoundedRect


class Env():
	
	def __init__(self, grid):

		self.grid = grid
		self.agent = pygame.math.Vector2(*find_start(grid))
		self.turns = 0
	
	def __str__(self):
		return f'Env(agent={self.agent}, grid={[len(self.grid),len(self.grid[0])]})'

	def pygame_init(self):

		pygame.init()

		self.WIDTH, self.HEIGHT = optimal_size(self.grid)
		self.sq = int( self.HEIGHT / len(self.grid) )
		self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
		pygame.display.set_caption(CAPTION)

	def draw(self):
		def background(self):

			spacer = int( self.HEIGHT / len(self.grid) )
			
			self.screen.fill(Gunmetal)

			# Draw grid lines
			for y, row in enumerate(self.grid):
				for x in range(len(row)):
					pygame.gfxdraw.line(self.screen, x*spacer, 0, x*spacer, self.HEIGHT, Glaucous)
				pygame.gfxdraw.line(self.screen, 0, y*spacer, self.WIDTH-200, y*spacer, Glaucous)

			# Draw border line
			pygame.gfxdraw.line(self.screen, self.WIDTH-200, 0, self.WIDTH-200, self.HEIGHT, Timberwolf) 
		def tiles(self):
			
			sq = self.sq
			shift = int(sq * 0.11)
			roundness = 0.2

			tp_roundness = 0.5
			tp_shift = int(sq * 0.15)

			g = self.grid

			for y, row in enumerate(self.grid):
				for x, item in enumerate(row):

					rect = (x*sq+shift, y*sq+shift, sq-(2*shift), sq-(2*shift))
					tp_rect = (x*sq+tp_shift, y*sq+tp_shift, sq-(2*tp_shift), sq-(2*tp_shift))

					if item == 1:
						# wall
						AAfilledRoundedRect(self.screen, Independence, rect, roundness)
					elif item == 2:
						# start tile
						AAfilledRoundedRect(self.screen, Start, rect, roundness)
					elif item == 3:
						# end tile
						AAfilledRoundedRect(self.screen, End, rect, roundness)
					
					# teleporters
					elif item == 10:
						AAfilledRoundedRect(self.screen, Turquoise_Blue, rect, tp_roundness)
					elif item == 11:
						AAfilledRoundedRect(self.screen, Turquoise_Blue, rect, tp_roundness)
						AAfilledRoundedRect(self.screen, Gunmetal, tp_rect, tp_roundness)
					elif item == 20:
						AAfilledRoundedRect(self.screen, Lavender, rect, tp_roundness)
					elif item == 22:
						AAfilledRoundedRect(self.screen, Lavender, rect, tp_roundness)
						AAfilledRoundedRect(self.screen, Gunmetal, tp_rect, tp_roundness)
					elif item == 30:
						AAfilledRoundedRect(self.screen, Mandy, rect, tp_roundness)
					elif item == 33:
						AAfilledRoundedRect(self.screen, Mandy, rect, tp_roundness)
						AAfilledRoundedRect(self.screen, Gunmetal, tp_rect, tp_roundness)
					elif item == 40:
						AAfilledRoundedRect(self.screen, Porsche, rect, tp_roundness)
					elif item == 44:
						AAfilledRoundedRect(self.screen, Porsche, rect, tp_roundness)
						AAfilledRoundedRect(self.screen, Gunmetal, tp_rect, tp_roundness)
		def agent(self):
			
			sq = self.sq
			shift = int(sq * 0.15)
			roundness = 0.7

			x = self.agent.x
			y = self.agent.y

			rect = (x*sq+shift, y*sq+shift, sq-(2*shift), sq-(2*shift))

			AAfilledRoundedRect(self.screen, Manz, rect, roundness)

		background(self)
		tiles(self)
		agent(self)

		pygame.display.flip()
	
	def receive(self, ipt):

		self.turns += 1

		velocity = pygame.math.Vector2(*ipt)
		if velocity.x not in [-1,0,1]:
			velocity.x = 0
		if velocity.y not in [-1,0,1]:
			velocity.y = 0
		
		if abs(velocity.x) == abs(velocity.y):
			velocity.y = 0

		predicted = self.agent + velocity

		# If trying to move outside borders
		if (predicted.x < 0 or predicted.y < 0) or (predicted.x > self.WIDTH-200 or predicted.y > self.HEIGHT):
			# Do nothing
			return
		
		# Check if hitting wall
		if (self.grid[int(predicted.y)][int(predicted.x)] == 1):
			# Do nothing
			return

		# Make a successful move
		self.agent = predicted