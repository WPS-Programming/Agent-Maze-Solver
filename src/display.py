import pygame

COLOR_MAIZE = pygame.Color("#e8c547")
COLOR_GUNMETAL = pygame.Color("#30323d")
COLOR_INDEPENDENCE = pygame.Color("#4d5061")
COLOR_GLAUCOUS = pygame.Color("#5c90bc")
COLOR_TIMBERWOLF = pygame.Color("#cdd1c4")

COLOR_TP = [(135, 251, 255), (247, 135, 255), (255, 135, 135), (253, 255, 135)]


def roundedRect(surface, color, rect, radius=0.1):
    """
    AAfilledRoundedRect(surface,rect,color,radius=0.4)

    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """

    rect = pygame.Rect(rect)
    color = pygame.Color(*color)
    alpha = color.a
    color.a = 0
    pos = rect.topleft
    rect.topleft = 0, 0
    rectangle = pygame.Surface(rect.size, pygame.SRCALPHA)

    circle = pygame.Surface([min(rect.size)*3]*2, pygame.SRCALPHA)
    pygame.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
    circle = pygame.transform.smoothscale(
        circle, [int(min(rect.size)*radius)]*2)

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
