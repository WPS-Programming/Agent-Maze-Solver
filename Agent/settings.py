from pygame import Color

FPS = 60
CAPTION = "Maze Agent Environment"
MARGIN = 200

Maize = Color("#e8c547")
Gunmetal = Color("#30323d")
Independence = Color("#4d5061")
Glaucous = Color("#5c90bc")
Timberwolf = Color("#cdd1c4")

Start = Color("#5ee66c")
End = Color("#4f66e3")

Turquoise_Blue = Color("#5ee6c6")
Lavender = Color("#c65ee6")
Mandy = Color("#e65e5e")
Porsche = Color("#e6a45e")

Teleporters = [ (135, 251, 255), (247, 135, 255), (255, 135, 135), (253, 255, 135)  ]

def optimal_size(grid):

    sq_length = len(grid)
    desired_sq = 800

    calculated = desired_sq - (desired_sq % sq_length)

    return calculated + MARGIN, calculated