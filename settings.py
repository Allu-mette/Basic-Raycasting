import pygame
from math import *

vec2 = pygame.math.Vector2

# App Cst
FPS = 60

# Map Cst
SIZE = 32
MAP_SIZE = COL_NUM, ROW_NUM = (16, 16)

# Plane Cst
PLANE_RES = WIDTH, HEIGHT = (600, 600)
CENTER = (WIDTH/2, HEIGHT/2)
FOV_ANGLE = pi/3 # [0, pi]
DELTA_ANGLE = FOV_ANGLE/WIDTH
PLANE_LEN = WIDTH/(2*tan(FOV_ANGLE/2))

WALL_HEIGHT = 64
VIEW_HEIGHT = WALL_HEIGHT/2
VEL = SIZE/8
