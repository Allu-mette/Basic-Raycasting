import pygame
import scripts

from settings import *
import objects

class App:
    def __init__(self):
        
        self.screen = pygame.display.set_mode(PLANE_RES)
        
        self.clock = pygame.time.Clock()
        self.time = 0
        self.delta_time = 0.01
        
        self.map = objects.Map()
        self.camera = objects.Camera(vec2(MAP_SIZE)*SIZE/2+vec2(32, 32), pi/2)
        
        self.scene2D = Scene2D(self.map, self.camera)
        self.scene3D = Scene3D(self.map, self.camera)
        self.currentScene = self.scene2D
        
    def handling_events(self):
        for event in pygame.event.get():
            
                # Quit the Game
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
                
                # Change Scene
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.currentScene == self.scene2D:
                    self.currentScene = self.scene3D
                else:
                    self.currentScene = self.scene2D
                    
                # Scene Event
            self.currentScene.handling_events(event)
        
    def update(self):
        self.currentScene.update()
    
    def display(self):
        self.currentScene.display(self.screen)
    
    def run(self):
        while True:
            self.handling_events()
            self.update()
            self.display()
            self.clock.tick(FPS)

class Scene2D():
    
    def __init__(self, map: objects.Map, camera: objects.Camera) -> None:
        
        self.map = map
        self.camera = camera
        
        self.castList = []
    
    def handling_events(self, event: pygame.event.Event):
            
            #Add/Remove Walls
        if event.type == pygame.MOUSEBUTTONDOWN:
            viewPos = self.camera.getPos() - vec2(PLANE_RES)/2
            mouseX, mouseY= vec2(pygame.mouse.get_pos())+viewPos
            ii = int(mouseX // SIZE)
            jj = int(mouseY // SIZE)
            self.map.changeState(ii, jj)
    
    def update(self):
        
            #Moove Camera
        keys = pygame.key.get_pressed()
        dir = vec2(0, 0)
        if keys[pygame.K_q]:
            dir += vec2(-1, 0)
        if keys[pygame.K_d]:
            dir += vec2(1, 0)
        if keys[pygame.K_s]:
            dir += vec2(0, 1)
        if keys[pygame.K_z]:
            dir += vec2(0, -1)
            
        len = dir.length()
        if len != 0:
            dir *= 1/len
            self.camera.setPos(self.camera.getPos() + VEL * dir)
            
        self.castList = scripts.computeCastList(self.map, self.camera)
        self.camera.setDir(scripts.angle(vec2(1, 0), vec2(pygame.mouse.get_pos())-vec2(CENTER)))
            
    def display(self, screen: pygame.Surface):
        screen.fill('black')
        
        viewPos = viewX, viewY = self.camera.getPos() - vec2(PLANE_RES)/2
        
            # Draw the Grid (only for dev)
        for i in range(COL_NUM):
            pos1 = vec2(i*SIZE, 0) - viewPos
            pos2 = vec2(i*SIZE, ROW_NUM*SIZE) - viewPos
            pygame.draw.line(screen, "blue", pos1, pos2)
        for i in range(ROW_NUM):
            pos1 = vec2(0, i*SIZE) - viewPos
            pos2 = vec2(COL_NUM*SIZE, i*SIZE) - viewPos
            pygame.draw.line(screen, "blue", pos1, pos2)
             
             # Draw the Walls
        for i, col in enumerate(self.map.stateList):
            for j, value in enumerate(col):
                if value != False:
                    rect = pygame.Rect(i*SIZE - viewX, j*SIZE - viewY, SIZE, SIZE)
                    pygame.draw.rect(screen, "gray", rect)
             
            # Draw the Casts
        #for cast in self.castList:
        #    pos1, pos2 = self.cast
        #    pygame.draw.line(screen, (254, 120, 120, 1), pos1-viewPos, pos2-viewPos, 1)
            
        pos1, pos2 = self.castList[0]
        pygame.draw.line(screen, (254, 120, 120, 1), pos1-viewPos, pos2-viewPos, 1)
        pos1, pos2 = self.castList[-1]
        pygame.draw.line(screen, (254, 120, 120, 1), pos1-viewPos, pos2-viewPos, 1)
        
        pygame.display.flip()
            
class Scene3D():
    
    def __init__(self, map: objects.Map, camera: objects.Camera):
        
        self.map = map
        self.camera = camera
    
    def handling_events(self, event: pygame.event.Event):
        pass
        
    def update(self):
        
            # Moove the Camera
        keys = pygame.key.get_pressed()
        dir = vec2(0, 0)
        if keys[pygame.K_q]:
            dir += vec2(cos(self.camera.getDir()+pi/2), -sin(self.camera.getDir()+pi/2))
        if keys[pygame.K_d]:
            dir += vec2(cos(self.camera.getDir()-pi/2), -sin(self.camera.getDir()-pi/2))
        if keys[pygame.K_s]:
            dir += vec2(cos(self.camera.getDir()+pi), -sin(self.camera.getDir()+pi))
        if keys[pygame.K_z]:
            dir += vec2(cos(self.camera.getDir()), -sin(self.camera.getDir()))
            
        len = dir.length()
        if len != 0:
            dir *= 1/len
            self.camera.setPos(self.camera.getPos() + VEL * dir)
            
            # Rotate the Camera
           
        theta = vec2(pygame.mouse.get_pos()[0]) - vec2(CENTER)
        self.camera.setDir(self.camera.getDir() + theta.x/WIDTH)
        pygame.mouse.set_pos(CENTER)
            
        self.castList = scripts.computeCastList(self.map, self.camera)
    
    def display(self, screen: pygame.Surface):
        screen.fill('black')
        
            # Draw the Walls
        max_len = sqrt(pow(COL_NUM*SIZE, 2) + pow(ROW_NUM*SIZE, 2))
        for i, cast in enumerate(self.castList):
            len = scripts.length(cast[1] - cast[0])
            h = WALL_HEIGHT/len * PLANE_LEN
            c = (1-scripts.easeOutCubic(len/max_len))*255
            color = (c, c, c, 1)
            pygame.draw.line(screen, color, 
                             CENTER + vec2(WIDTH/2-i, -h/2), 
                             CENTER + vec2(WIDTH/2-i, +h/2))
            
        pygame.display.flip()
    
            
