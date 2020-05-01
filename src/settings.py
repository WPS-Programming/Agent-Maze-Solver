import pygame

DEV_MODE = False

WIDTH = 1000
HEIGHT = 800
MARGIN = 200
FPS = 144
UPDATE_DEFAULT = 500
OFFSET = 25

COLOR_MAIZE = pygame.Color("#e8c547")
COLOR_GUNMETAL = pygame.Color("#30323d")
COLOR_INDEPENDENCE = pygame.Color("#4d5061")
COLOR_GLAUCOUS = pygame.Color("#5c90bc")
COLOR_TIMBERWOLF = pygame.Color("#cdd1c4")

COLOR_START = pygame.Color("#5ee66c")
COLOR_END = pygame.Color("#4f66e3")

TURQUOISE = pygame.Color("#5ee6c6")
LAVENDER = pygame.Color("#c65ee6")
MANDY = pygame.Color("#e65e5e")
PORSCHE = pygame.Color("#e6a45e")

COLOR_TP = [TURQUOISE, LAVENDER, MANDY, PORSCHE]


Manz = pygame.Color("#eceb65")


def roundedRect(surface, color, rect, radius=0.1):
	rect = pygame.Rect(rect)
	color = pygame.Color(*color)
	alpha = color.a
	color.a = 0
	pos = rect.topleft
	rect.topleft = 0, 0
	rectangle = pygame.Surface(rect.size, pygame.SRCALPHA)

	circle = pygame.Surface([min(rect.size)*3]*2, pygame.SRCALPHA)
	pygame.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
	circle = pygame.transform.smoothscale(circle, [int(min(rect.size)*radius)]*2)

	radius = rectangle.blit(circle, (0, 0))
	radius.bottomright = rect.bottomright
	rectangle.blit(circle, radius)
	radius.topright = rect.topright
	rectangle.blit(circle, radius)
	radius.bottomleft = rect.bottomleft
	rectangle.blit(circle, radius)

	rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
	rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))

	rectangle.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
	rectangle.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)

	return surface.blit(rectangle, pos)
