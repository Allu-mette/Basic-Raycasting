import pygame
import scripts
from settings import *
import objects
import random

class App:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode(SCREEN_RES)
        
        self.clock = pygame.time.Clock()
        self.time = 0
        self.delta_time = 0.01
        
        self.castNum = 64
        self.castList = []
        self.wallList = [objects.wall(self.screen),
                         objects.wall(self.screen),
                         objects.wall(self.screen)]
    
    def handling_events(self):
        for event in pygame.event.get():
                # Quit the Game
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.restart()
    
    def update(self):
        self.castList = scripts.updateCastList(self.castNum, self.screen)
            
    def display(self):
        self.screen.fill('black')
        
        scripts.displayCast(self.screen, self.castList)
        for wall in self.wallList:
             wall.draw(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        while True:
            self.handling_events()
            self.update()
            self.display()
            self.clock.tick(FPS)
    
    def restart(self):
        self.wallList = [objects.wall(self.screen),
                         objects.wall(self.screen),
                         objects.wall(self.screen)]
    
if __name__ == "__main__":
    app = App()
    app.run()