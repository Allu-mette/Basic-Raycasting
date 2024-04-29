import pygame
from settings import *
import random

class wall:
    def __init__(self,screen:pygame.Surface, xx=None, yy=None, width=None, height=None, angle=None) -> None:
        
        if xx == None:
            xx = random.randint(0, SCREEN_RES[0])
        if yy == None:
            yy = random.randint(0, SCREEN_RES[1])
        if width == None:
            width = 8*random.randint(8, 24)
        if height == None:
            height = 8*random.randint(8, 24)
        if angle == None:
            angle = random.randint(0, 180)
        
        self.pos = vec2(xx, yy)
        self.size = vec2(width, height)
        self.angle = angle
        
        self.surf = pygame.Surface((screen.get_width(), screen.get_height()))
        self.surf.set_colorkey("black")
        self.surf.fill("black")
        
        image = pygame.Surface(self.size)
        image.set_colorkey("black")
        image.fill('white')
        image = pygame.transform.rotate(image, angle)
        rect = image.get_rect()
        rect.center = self.pos
        self.surf.blit(image, rect)
        
    def draw(self, screen: pygame.Surface):
        screen.blit(self.surf, (0, 0))