USE_IMAGE = True

if USE_IMAGE:
    WIN_HEIGHT = 560
    WIN_WIDTH = 895
    REST_Y = 472
else:
    WIN_HEIGHT = 600
    WIN_WIDTH = 1000
    REST_Y = 600

BG_COL = (50, 170, 90)
BALL_COL = (200, 50, 50)
BLACK = (0, 0, 0)
FIELD_STRENGTH = 9.8
VEL_SCALE = 0.02
FPS = 120
TIME_SCALE = 1 / FPS
REBOUND_SCALE = 0.8
STOPPING_LIM = 25  # the minimum velocity before the ball stops
DRAW_PATH = False
DRAG_COEF = 0.01
DATA_PRECISION = 2  # the number of decimal places of the data
