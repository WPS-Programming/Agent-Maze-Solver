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

	# 200 is the margin
	return calculated + 200, calculated

class Env:
	def __init__(self, build):

		self.build = build
		self.grid = build['grid']
		self.agent = pygame.math.Vector2(*build['start'])
		self.prev = pygame.math.Vector2(-1,-1)
		self.turns = 0
		self.completed = False

	def __str__(self):
		return f'Env(agent={self.agent}, grid={[len(self.grid),len(self.grid[0])]})'

	def pygame_init(self):

		pygame.init()
		pygame.font.init()

		self.font = pygame.font.Font(pygame.font.get_default_font(), 30)

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

			# Draw text
			text = "Turns: " + str(self.turns)
			text = self.font.render(text, True, (COLOR_MAIZE))
			self.screen.blit(text, (805, 20))

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
					elif item == 20:
						roundedRect(
							self.screen, TURQUOISE, rect, tp_roundness)
						roundedRect(
							self.screen, COLOR_GUNMETAL, tp_rect, tp_roundness)
					elif item == 11:
						roundedRect(
							self.screen, LAVENDER, rect, tp_roundness)
					elif item == 21:
						roundedRect(
							self.screen, LAVENDER, rect, tp_roundness)
						roundedRect(
							self.screen, COLOR_GUNMETAL, tp_rect, tp_roundness)
					elif item == 12:
						roundedRect(
							self.screen, MANDY, rect, tp_roundness)
					elif item == 22:
						roundedRect(
							self.screen, MANDY, rect, tp_roundness)
						roundedRect(
							self.screen, COLOR_GUNMETAL, tp_rect, tp_roundness)
					elif item == 13:
						roundedRect(
							self.screen, PORSCHE, rect, tp_roundness)
					elif item == 23:
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

			roundedRect(self.screen, COLOR_MAIZE, rect, roundness)

		background(self)
		tiles(self)
		agent(self)

		pygame.display.flip()

	def receive(self, ipt):

		self.prev = self.agent

		if self.completed:
			return

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
		try:
			if (self.grid[int(predicted.y)][int(predicted.x)] == 1):
				# Do nothing
				return
		except:
			return

		# Make a successful move
		self.agent = predicted
		self.analyze_position()

	def analyze_position(self):

		# Method which checks and interacts with non
		# empty or wall cells

		A = self.agent
		pos = (int(A.x), int(A.y))
		grid_item = self.grid[int(A.y)][int(A.x)]

		# If reached end
		if pos == self.build['end']:
			print("Maze Completed")
			self.completed = True
		
		# If on teleporter
		elif grid_item >= 10 and grid_item < 20:
			find_index = [i[0] if type(i) != int \
				else i for i in self.build['teleporters']]

			for index, item in enumerate(find_index):
				if pos == item:
					new_pos = self.build['teleporters'][index][1]
					self.agent = pygame.math.Vector2(*new_pos)
					return
	
	def get_state(self):

		def get_radius(self, radius = 1):
			sq = (2 * radius) + 1
			fov = np.ones((sq, sq))
			
			fov[radius][radius] = 9 # Indicates center

			ax, ay = self.agent.x, self.agent.y

			for y in range(-radius, radius+1):
				for x in range(-radius, radius+1):

					xr, yr = x+radius, y+radius
					if fov[yr][xr] == 9:
						continue

					try:
						fov[yr][xr] = self.grid[int(y+ay)][int(x+ax)]
					except:
						fov[xr][xr] = -1
			return fov

		agent_position = (int(self.agent.x), int(self.agent.y))
		has_moved = self.agent is not self.prev
		print(self.agent, self.prev)

		return {"position" : agent_position, "moved" : has_moved, "grid" : get_radius(self)}

if __name__ == "__main__":
	with open('map.pkl', 'rb') as inp:
		build = pickle.load(inp)
	
	env = Env(build)
	clock = pygame.time.Clock()
	last_tick = 0
	update_default = 500
	update_on = update_default

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
						env.receive((1,0))
					elif event.key == pygame.K_LEFT:
						env.receive((-1,0))
					elif event.key == pygame.K_UP:
						env.receive((0,-1))
					elif event.key == pygame.K_DOWN:
						env.receive((0,1))

				# Forces a drawing update on next tick ~12 raw delay
				if event.key in [
					pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN]:
					update_on = 0

		if abs(last_tick - pygame.time.get_ticks()) > update_on:
			env.draw()

			#TODO:
			# input = env.get_state()
			# move = agent.make_move(input)
			# env.receive(move)
			#env.receive((random.randint(-1, 1), random.randint(-1, 1)))
			print(env.get_state()['moved'])

			last_tick = pygame.time.get_ticks()
			if update_on != update_default: update_on = update_default