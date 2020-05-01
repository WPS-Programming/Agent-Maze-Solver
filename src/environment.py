import pygame
import pickle
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

	return calculated + MARGIN, calculated


class Env:
	def __init__(self, build):

		self._build = build
		self._grid = build['grid']
		self._agent = pygame.math.Vector2(*build['start'])
		self._prev = pygame.math.Vector2(-1, -1)
		self._turns = 0
		self._completed = False

	def __str__(self):
		return f'Env(agent={self._agent}, grid={self._grid.shape}, turns={self._turns})'

	def pygame_init(self):

		pygame.init()
		pygame.font.init()

		self.font = pygame.font.Font(pygame.font.get_default_font(), 30)

		self.WIDTH, self.HEIGHT = optimal_size(self._grid)
		self.sq = int(self.HEIGHT / len(self._grid))
		self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
		pygame.display.set_caption("Maze Agent Environment")

	def draw(self):
		# Draws the screen background

		self.screen.fill(COLOR_GUNMETAL)

		# Draw grid lines
		for y, row in enumerate(self._grid):
			for x in range(len(row)):
				pygame.gfxdraw.line(
					self.screen, x * self.sq, 0, x * self.sq, self.HEIGHT, COLOR_GLAUCOUS)
			pygame.gfxdraw.line(self.screen, 0, y * self.sq,
								self.WIDTH - MARGIN, y * self.sq, COLOR_GLAUCOUS)

		# Draw border line
		pygame.gfxdraw.line(self.screen, self.WIDTH - MARGIN,
							0, self.WIDTH - MARGIN, self.HEIGHT, COLOR_TIMBERWOLF)

		# Draw text
		text = self.font.render(
			"Turns: " + str(self._turns), True, (COLOR_MAIZE))
		self.screen.blit(text, (805, 20))

		# Draws the screen tiles

		shift = int(self.sq * 0.11)
		roundness = 0.2

		tp_roundness = 0.5
		tp_shift = int(self.sq * 0.15)

		g = self._grid

		for y, row in enumerate(self._grid):
			for x, item in enumerate(row):

				rect = (x * self.sq + shift, y * self.sq +
						shift, self.sq - 2 * shift, self.sq - 2 * shift)
				tp_rect = (x * self.sq + tp_shift, y * self.sq + tp_shift,
						   self.sq - 2 * tp_shift, self.sq - 2 * tp_shift)

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
				elif item >= 10:
					roundedRect(
						self.screen, COLOR_TP[int(item % 10)], rect, tp_roundness)

					if item // 10 > 1:
						roundedRect(self.screen, COLOR_GUNMETAL,
									tp_rect, tp_roundness)

		# Draw the agent

		shift = int(self.sq * 0.15)
		roundness = 0.7

		x = self._agent.x
		y = self._agent.y

		rect = (x * self.sq + shift, y * self.sq + shift,
				self.sq - 2 * shift, self.sq - 2 * shift)

		roundedRect(self.screen, COLOR_MAIZE, rect, roundness)

		pygame.display.flip()

	def receive(self, ipt):

		# Records the previous position
		self._prev = self._agent

		if self._completed:
			return

		self._turns += 1

		velocity = pygame.math.Vector2(*ipt)

		# Ensures movements are not skipping tiles		AND are cardinal directions
		if (abs(velocity.x) > 1 or abs(velocity.y) > 1) and velocity.x ^ velocity.y != 0:
			velocity.x = 0
			velocity.y = 0

		predicted = self._agent + velocity

		try:
			if (predicted.y < 0 or predicted.x < 0):
				# Prevents negative indexes from wrapping around grid.
				raise IndexError

			if (self._grid[int(predicted.y)][int(predicted.x)] == 1):
				# Checks if hitting wall and terminates without movement
				return
		except:
			# Catches an out of bounds error and terminates without movement
			return

		# Make a successful move
		self._agent = predicted
		self.analyze_position()

	def analyze_position(self):

		# Method which checks and interacts with non
		# empty or wall cells

		A = self._agent
		pos = (int(A.x), int(A.y))
		grid_item = self._grid[pos[1]][pos[0]]

		# If reached end
		if pos == self._build['end']:
			print("Maze Completed")
			self._completed = True

		# If on teleporter IN
		elif grid_item >= 10 and grid_item < 20:
			tp_group = self._build['teleporters'][grid_item % 10]

			# Sends agent to teleporter OUT
			self._agent = pygame.math.Vector2(*tp_group[1])

	def get_state(self):

		def get_radius(self, radius=1):
			diameter = (2 * radius) + 1
			fov = np.ones((diameter, diameter), dtype=np.intc)

			fov[radius][radius] = 9  # 9 indicates agent

			# Center is the agent position
			cx, cy = self._agent.x, self._agent.y

			for y in range(-radius, radius + 1):
				for x in range(-radius, radius + 1):

					# FOV positions
					fx, fy = x + radius, y + radius

					# "Real" x and y (relative to grid)
					rx, ry = x + cx, y + cy

					# Checks for out of bounds errors
					try:
						if rx < 0 or ry < 0:
							raise IndexError
						fov[fy][fx] = self._grid[ry][rx]
					except:
						fov[fx][fx] = -1
			return fov

		agent_position = (int(self._agent.x), int(self._agent.y))
		has_moved = self._agent is not self._prev

		return {
			"position": agent_position,
			"moved": has_moved,
			"grid": get_radius(self),
			"complete": self._completed
		}


if __name__ == "__main__":
	with open('map.pkl', 'rb') as inp:
		build = pickle.load(inp)

	env = Env(build)
	clock = pygame.time.Clock()
	last_tick = 0
	update_on = UPDATE_DEFAULT

	dev_mode = True

	env.pygame_init()

	while True:

		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit()
				quit()
			if event.type == pygame.KEYDOWN:

				if dev_mode:
					if event.key == pygame.K_RIGHT:
						env.receive((1, 0))
					elif event.key == pygame.K_LEFT:
						env.receive((-1, 0))
					elif event.key == pygame.K_UP:
						env.receive((0, -1))
					elif event.key == pygame.K_DOWN:
						env.receive((0, 1))

				# Forces a drawing update on next tick ~12 raw delay
				if event.key in [
						pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN]:
					update_on = 0

		if abs(last_tick - pygame.time.get_ticks()) > update_on:
			env.draw()

			# Implementation
			# input = env.get_state()
			# move = agent.make_move(input)
			# env.receive(move)

			ctx = env.get_state()

			# Moves the agent in a random direction
			#env.receive((random.randint(-1, 1), random.randint(-1, 1)))

			last_tick = pygame.time.get_ticks()
			if update_on != UPDATE_DEFAULT:
				update_on = UPDATE_DEFAULT
