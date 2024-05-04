import pygame
from math import *
from settings import *
import objects

def computeCastList(map: objects.Map, camera: objects.Camera):
    
    castList = []
    source = camera.pos
    angle = camera.dir - FOV_ANGLE/2
    for _ in range(int(WIDTH)):
        angle %= 2*pi
        castEnd = computeCast(source, angle, map.stateList)
        castList.append([source, castEnd])
        angle += DELTA_ANGLE
    return castList
    
def computeCast(source: vec2, angle: float, stateList: list):
    
    castEnd1 = horizontalCollision(source, angle, stateList)
    castEnd2 = verticalCollision(source, angle, stateList)
    
    if length(castEnd1-source) < length(castEnd2-source):
        return castEnd1
    else:
        return castEnd2
        
def horizontalCollision(source: vec2, angle: float, stateList: list):
    
    P1 = vec2()
        # TOP
    if angle >= 0 and angle < pi:
        vx = SIZE/tan(angle)
        vy = -SIZE
        P1.y = int(source.y/SIZE)*SIZE - 1
        P1.x = source.x + abs(source.y-P1.y)/tan(angle)
        # BOTTOM
    else:
        vx = SIZE/tan(pi-angle)
        vy = SIZE
        P1.y = int(source.y/SIZE)*SIZE + SIZE
        P1.x = source.x + abs(source.y-P1.y)/tan(pi-angle)
        
    v = vec2(vx, vy)
    while(True):
        if placeIsFree(P1, stateList):
            P1 += v
        else:
            return P1
        
def verticalCollision(source: vec2, angle: float, stateList: list):
    
    P1 = vec2()
        # LEFT
    if angle >= pi/2 and angle < 3*pi/2:
        vx = -SIZE
        vy = -SIZE*tan(pi-angle)
        P1.x = int(source.x/SIZE)*SIZE - 1
        P1.y = source.y - abs(source.x-P1.x)*tan(pi-angle)
        # RIGHT
    else:
        vx = SIZE
        vy = -SIZE*tan(angle)
        P1.x = int(source.x/SIZE)*SIZE + SIZE
        P1.y = source.y - abs(source.x-P1.x)*tan(angle)

    v = vec2(vx, vy)
    while(True):
        if placeIsFree(P1, stateList):
            P1 += v
        else:
            return P1
        
def placeIsFree(pos: vec2, stateList: list):
    
    ii, jj = (int(pos[0] // SIZE), int(pos[1] // SIZE))
        # Check the screen
    if ii<0 or jj<0 or ii>COL_NUM-1 or jj>ROW_NUM-1:
        return False
        # Check for walls
    elif stateList[ii][jj] != 0:
        return False
    else:
        return True
    
def dotProduct(v1: vec2, v2: vec2):
    return v1.x*v2.x + v1.y*v2.y
    
def length(v: vec2):
    return sqrt(dotProduct(v, v))

def angle(v1: vec2, v2: vec2):
    if length(v1) > 0 and length(v2) > 0:
        v1_u = v1/length(v1)
        v2_u = v2/length(v2)
    else:
        return 0
        
    return copysign(acos(min(max(dotProduct(v1_u, v2_u), -1), 1)), -v2.y) % (2*pi) 

def easeOutCubic(x: float):
    return 1 - pow(1 - x, 3)
        