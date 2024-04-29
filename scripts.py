import pygame
from settings import *
from math import *

def updateCastList(N, screen):
    castList = []
    delta = 2*pi/N
    start = vec2(pygame.mouse.get_pos())
    for i in range(N):
        angle = i*delta
        end = computeCast(start, angle, screen)
        castList.append([start, end])
    return castList
    
def computeCast(start, angle, screen):
    end = start.copy()
    while(True):
        vec = 8*vec2(cos(angle), sin(angle))
        if canContinue(end, vec, screen):
            end += vec
        else:
            vec = vec2(cos(angle), sin(angle))
            while(canContinue(end, vec, screen)):
                end += vec
            return end

def canContinue(pos, vec, screen):
    point = (int(max(0, min(SCREEN_RES[0]-1, (pos+vec)[0]))), int(max(0, min(SCREEN_RES[1]-1, (pos+vec)[1]))))
        # Check the screen
    if not pygame.Rect(0, 0, SCREEN_RES[0], SCREEN_RES[1]).collidepoint(pos+vec):
        return False
        # Check for walls
    elif screen.get_at(point)[0] == 255:
        return False
    else:
        return True
        
def displayCast(screen: pygame.Surface, castList):
    for cast in castList:
        pos1, pos2 = cast
        pygame.draw.line(screen, (254, 255, 255, 255), pos1, pos2, 1)
        
        
    