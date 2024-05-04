import pygame
import random
from settings import *
import scripts


class Map:
    
    def __init__(self):
        self.stateList = []
        for i in range(COL_NUM):
            self.stateList.append([])
            for j in range(ROW_NUM):
                if i==0 or j==0 or i==COL_NUM-1 or j==ROW_NUM-1:
                    self.stateList[i].append(True)
                else:
                    self.stateList[i].append(False)
                    
    def changeState(self, i: int, j: int):
        if i>=0 and i<COL_NUM and j>=0 and j<ROW_NUM:
            self.stateList[i][j] = not self.stateList[i][j]
                    
class Camera:
    def __init__(self, pos: vec2, dir: float):
        self.pos = pos
        self.dir = dir
        
    def getDir(self):
        return self.dir
        
    def getPos(self):
        return self.pos
        
    def setDir(self, newDir: float):
        self.dir = newDir
        
    def setPos(self, newPos: vec2):
        self.pos = newPos

class Wall:
    def __init__(self,screen:pygame.Surface, xx=None, yy=None, width=None, height=None, angle=None) -> None:
        
        if xx == None:
            xx = random.randint(0, WIDTH)
        if yy == None:
            yy = random.randint(0, HEIGHT)
        if width == None:
            width = random.randint(1, 4)*SIZE
        if height == None:
            height = random.randint(1, 4)*SIZE
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
        
class Wall2:
    
    def __init__(self,screen:pygame.Surface, xx=None, yy=None, width=None, height=None) -> None:
        
        if xx == None:
            xx = random.randint(0, 8)*SIZE
        if yy == None:
            yy = random.randint(0, 8)*SIZE
        if width == None:
            width = random.randint(1, 4)*SIZE
        if height == None:
            height = random.randint(1, 4)*SIZE
            
        
        self.pos = vec2(xx, yy)
        self.size = vec2(width, height)
        
        self.rect = pygame.Rect(xx, yy, width, height)
        
    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, "white", self.rect)