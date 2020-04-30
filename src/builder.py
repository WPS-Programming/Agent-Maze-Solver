import numpy as np
import pickle
import pygame
import pygame.gfxdraw

from settings import *

VALUE_MAP = {
	'wall': 1,
	'none': 0,
	'start': 2,
	'end': 3
}


def shift_tuple(t, up, left):
	return (t[0] - up, t[1] - left)


class Button:
	def __init__(self, color, rect, value):
		self.rect = rect
		self.color = color
		self.value = value

	# Checks to see if the button is hovering over the button
	# Assumes that mouse click event has already been checked in the mainloop
	def is_clicked(self):
		pos = pygame.mouse.get_pos()
		if self.rect[0] < pos[0] and self.rect[0] + self.rect[2] > pos[0]:
			if self.rect[1] < pos[1] and self.rect[1] + self.rect[3] > pos[1]:
				return True

		return False

	# Renders the button and the centered text
	def render(self, screen):
		pygame.draw.rect(screen, self.color, self.rect)


class Builder:
	def __init__(self):
		self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
		self.clock = pygame.time.Clock()
		self.first_run = True

		pygame.display.set_caption('Environment Builder')

		self.grid = np.zeros(shape=(50, 50))
		self.selector = 'wall'
		self.tp_index = 0

		self.start = None
		self.end = None
		self.tps = [0] * 4

		self.buttons = [
			Button((30, 30, 30), (850, 25, 100, 100), 'wall'),
			Button((220, 220, 220), (850, 150, 100, 100), 'none'),
			Button(COLOR_START, (825, 300, 75, 75), 'start'),
			Button(COLOR_END, (900, 300, 75, 75), 'end'),
			Button(COLOR_TP[self.tp_index], (850, 500, 100, 100), 'tp')
		]

		self.edited = []

	def set_pos(self, r, c, v):
		self.grid[r][c] = v
		self.edited.append((r, c))

	def draw_background(self):

		self.screen.fill(COLOR_GUNMETAL)
		pygame.gfxdraw.line(self.screen, 800, 0, 800, HEIGHT, COLOR_TIMBERWOLF)
		roundedRect(self.screen, COLOR_INDEPENDENCE,
					(OFFSET, OFFSET, 750, 750), 0.025)

		for y in range(1, 50):
			for x in range(1, 50):
				pygame.gfxdraw.line(self.screen, OFFSET + (15 * x), y+OFFSET,
									OFFSET + (15 * x), HEIGHT-OFFSET-1, COLOR_TIMBERWOLF)
			pygame.gfxdraw.line(self.screen, OFFSET,  OFFSET + (15 * y),
								WIDTH-200-OFFSET, OFFSET + (15 * y), COLOR_TIMBERWOLF)

		for button in self.buttons:
			button.render(self.screen)

	def draw_updated(self):
		for i in self.edited:
			y, x = i
			item = self.grid[y][x]

			itemRect = (x*15 + OFFSET+1, y*15 + OFFSET+1, 14, 14)
			tpRect = (x*15 + OFFSET+1, y*15 + OFFSET+1, 13, 13)

			if item == 0:
				pygame.draw.rect(
					self.screen, COLOR_INDEPENDENCE, itemRect)
			elif item == 1:
				pygame.draw.rect(
					self.screen, (0, 0, 0), itemRect)
			elif item == 2:
				pygame.draw.rect(self.screen, (70, 212, 122), itemRect)
			elif item == 3:
				pygame.draw.rect(self.screen, (68, 156, 212), itemRect)
			elif item - 10 < 5:
				index = int((item - 10) % 4)
				pygame.draw.rect(self.screen, COLOR_TP[index], itemRect)
			elif item - 20 < 5:
				index = int((item - 20) % 4)
				pygame.draw.rect(self.screen, COLOR_TP[index], tpRect, 2)

	def get_output(self):
		g = self.grid.copy()

		up_shift = 0
		left_shift = 0

		# Top down cleaning
		while not g[0].any():
			g = g[1:]
			up_shift += 1

		# Down up cleaning
		while not g[-1].any():
			g = g[:-1]

		# Left -> right cleaning
		while not g[:, 0].any():
			g = np.delete(g, 0, 1)
			left_shift += 1

		# Right -> left cleaning
		while not g[:, -1].any():
			g = np.delete(g, -1, 1)

		length = max(len(g), len(g[0]))

		if len(g) < length:
			g = np.append(g, np.zeros(shape=(length - len(g), length)), axis=0)

		if len(g[0]) < length:
			g = np.append(g, np.zeros(
				shape=(length, length - len(g[0]))), axis=1)

		try:

			# TODO: styling of comparative tuples to be (x, y)

			self.start = shift_tuple(self.start, up_shift, left_shift)
			self.end = shift_tuple(self.end, up_shift, left_shift)

			for i in range(len(self.tps)):
				if self.tps[i] == 0:
					continue
				
				tp_start, tp_end = self.tps[i]

				self.tps[i][0] = shift_tuple(tp_start, up_shift, left_shift)
				self.tps[i][1] = shift_tuple(tp_end, up_shift, left_shift)
		except:
			print('Missing required component')
				
		return g

	def get_click(self, mx, my):
		if (mx > OFFSET and mx < WIDTH - 200 - OFFSET) and (my > OFFSET and my < HEIGHT - OFFSET):
			row = round(my/15) - 2
			if row >= 50:
				row = 49
			col = round(mx/15) - 2
			if col >= 50:
				col = 49
			return (True, (row, col))
		return (False, None)

	def mainloop(self):
		pygame.init()

		while True:
			self.clock.tick(FPS)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.cleanup_and_exit()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					for button in self.buttons:
						if button.is_clicked():
							if button.value == 'tp' and self.selector == 'tp':
								print('change')
								self.tp_index = (self.tp_index + 1) % 4
								button.color = COLOR_TP[self.tp_index]
								button.render(self.screen)
								self.selector = button.value
							else:
								self.selector = button.value

							break

					valid, pos = self.get_click(*pygame.mouse.get_pos())

					if valid:
						if self.selector == 'start':
							self.set_pos(*pos, VALUE_MAP['start'])

							if self.start is not None:
								self.set_pos(*self.start, VALUE_MAP['none'])

							self.start = pos
						elif self.selector == 'end':
							self.set_pos(*pos, VALUE_MAP['end'])

							if self.end is not None:
								self.set_pos(*self.end, VALUE_MAP['end'])

							self.end = pos
						elif self.selector == 'tp':
							if self.tps[self.tp_index] == 0:
								self.tps[self.tp_index] = [None, None]
							# Left click => In
							if pygame.mouse.get_pressed()[0]:
								if self.tps[self.tp_index][0] != None:
									self.set_pos(
										*self.tps[self.tp_index][0], 0)

								self.tps[self.tp_index][0] = pos
								self.set_pos(*pos, 10 + self.tp_index)
							# Right click => Out
							if pygame.mouse.get_pressed()[2]:
								if self.tps[self.tp_index][1] != None:
									self.set_pos(
										*self.tps[self.tp_index][1], 0)

								self.tps[self.tp_index][1] = pos
								self.set_pos(*pos, 20 + self.tp_index)
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						np.savetxt('map.txt', self.get_output(), fmt="%d")
						with open('map.pkl', 'wb') as output:
							content = {'grid':self.get_output(), 'start':self.start, 'end': self.end, 'teleporters':self.tps}
							pickle.dump(content, output, pickle.HIGHEST_PROTOCOL)

			if pygame.mouse.get_pressed()[0] == 1:
				valid, pos = self.get_click(*pygame.mouse.get_pos())
				if valid and self.selector != 'tp':
					if self.selector == 'none':
						v = self.grid[pos[0]][pos[1]]

						if self.start == pos:
							self.start = None
						elif self.end == pos:
							self.end = None
						elif v >= 10 and v < 30:
							self.tps[v % 10][v // 10 - 1] = None

					self.set_pos(*pos, VALUE_MAP[self.selector])

			if self.first_run:
				self.draw_background()
				# self.draw_grid_items()
			else:
				self.draw_updated()

			pygame.display.flip()

			self.first_run = False
			self.edited = []

	def cleanup_and_exit(self):
		pygame.quit()
		exit(0)


if __name__ == "__main__":
	builder = Builder()
	builder.mainloop()