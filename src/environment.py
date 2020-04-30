import pygame
import time
import random
import numpy as np
import random
import pygame.gfxdraw
from settings import *


def optimal_size(grid):

	sq_length = len(grid)
	desired_sq = 800

	calculated = desired_sq - (desired_sq % sq_length)

	# 200 is the margin
	return calculated + 200, calculated


def find_start(grid):
	for y, row in enumerate(grid):
		for x, item in enumerate(row):
			if item == 2:
				return (x, y)


class Env:
	def __init__(self, grid):

		self.grid = grid
		self.agent = pygame.math.Vector2(*find_start(grid))
		self.turns = 0

	def __str__(self):
		return f'Env(agent={self.agent}, grid={[len(self.grid),len(self.grid[0])]})'

	def pygame_init(self):

		pygame.init()

		self.WIDTH, self.HEIGHT = optimal_size(self.grid)
		self.sq = int(self.HEIGHT / len(self.grid))
		self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
		pygame.display.set_caption("Maze Agent Environment")

	def draw(self):
		def background(self):

			spacer = int(self.HEIGHT / len(self.grid))

			self.screen.fill(COLOR_GUNMETAL)

			# Draw grid lines
			for y, row in enumerate(self.grid):
				for x in range(len(row)):
					pygame.gfxdraw.line(
						self.screen, x*spacer, 0, x*spacer, self.HEIGHT, COLOR_GLAUCOUS)
				pygame.gfxdraw.line(self.screen, 0, y*spacer,
									self.WIDTH-200, y*spacer, COLOR_GLAUCOUS)

			# Draw border line
			pygame.gfxdraw.line(self.screen, self.WIDTH-200,
								0, self.WIDTH-200, self.HEIGHT, COLOR_TIMBERWOLF)

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
					tp_rect = (x*sq+tp_shift, y*sq+tp_shift,
							   sq-(2*tp_shift), sq-(2*tp_shift))

					if item == 1:
						# wall
						roundedRect(
							self.screen, COLOR_INDEPENDENCE, rect, roundness)
					elif item == 2:
						# start tile
						roundedRect(
							self.screen, COLOR_START, rect, roundness)
					elif item == 3:
						# end tile
						roundedRect(self.screen, COLOR_END, rect, roundness)

					# teleporters
					elif item == 10:
						roundedRect(
							self.screen, TURQUOISE, rect, tp_roundness)
					elif item == 11:
						roundedRect(
							self.screen, TURQUOISE, rect, tp_roundness)
						roundedRect(
							self.screen, COLOR_GUNMETAL, tp_rect, tp_roundness)
					elif item == 20:
						roundedRect(
							self.screen, LAVENDER, rect, tp_roundness)
					elif item == 22:
						roundedRect(
							self.screen, LAVENDER, rect, tp_roundness)
						roundedRect(
							self.screen, COLOR_GUNMETAL, tp_rect, tp_roundness)
					elif item == 30:
						roundedRect(
							self.screen, MANDY, rect, tp_roundness)
					elif item == 33:
						roundedRect(
							self.screen, MANDY, rect, tp_roundness)
						roundedRect(
							self.screen, COLOR_GUNMETAL, tp_rect, tp_roundness)
					elif item == 40:
						roundedRect(
							self.screen, PORSCHE, rect, tp_roundness)
					elif item == 44:
						roundedRect(
							self.screen, PORSCHE, rect, tp_roundness)
						roundedRect(
							self.screen, COLOR_GUNMETAL, tp_rect, tp_roundness)

		def agent(self):

			sq = self.sq
			shift = int(sq * 0.15)
			roundness = 0.7

			x = self.agent.x
			y = self.agent.y

			rect = (x*sq+shift, y*sq+shift, sq-(2*shift), sq-(2*shift))

			roundedRect(self.screen, Manz, rect, roundness)

		background(self)
		tiles(self)
		agent(self)

		pygame.display.flip()

	def receive(self, ipt):

		self.turns += 1

		velocity = pygame.math.Vector2(*ipt)
		if velocity.x not in [-1, 0, 1]:
			velocity.x = 0
		if velocity.y not in [-1, 0, 1]:
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


if __name__ == "__main__":
	grid = np.loadtxt('map.txt')
	env = Env(grid)
	clock = pygame.time.Clock()
	last_tick = 0

	env.pygame_init()

	while True:

		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit()
				quit()

		if abs(last_tick - pygame.time.get_ticks()) > 500:
			env.draw()
			env.receive((random.randint(-1, 1), random.randint(-1, 1)))
			print(env)
			last_tick = pygame.time.get_ticks()
