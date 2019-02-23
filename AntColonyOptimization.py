from pygame.locals import *
import pygame
from pygame.locals import *
from random import randint
import pygame
import time


class Home:
    x = 0
    y = 0
    step = 11
 
    def __init__(self,x,y):
        self.x = x 
        self.y = y
 
    def draw(self, surface, image):
        surface.blit(image,(self.x, self.y))
        
class Apple:
    x = 0
    y = 0 
    def __init__(self,x,y):
        self.x = x
        self.y = y
 
    def draw(self, surface, image):
        surface.blit(image,(self.x, self.y)) 
 
 
class Ant:
    x = randint(0,800)
    y = randint(0,800)
    step = 3
    direction = 0
    length = 1
    hasFood = 0
 
    updateCountMax = 2
    updateCount = 0
 
    def __init__(self):
       self.previousX = 0
       self.stepX = randint(-4,4);
       self.stepY = randint(-4,4);
 
    def update(self):
         
        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:
            # update position of head of ant
            if self.direction == 4:
                self.y = self.y + self.stepY
                self.x = self.x + self.stepX
                                            
            self.updateCount = 0

    def changeDirection(self):
        self.stepY = randint(-3,3)
        self.stepX = randint(-3,3)

    def moveRandom(self):
        self.direction = 4
 
    def draw(self, surface, image):
        for i in range(0,self.length):
            surface.blit(image,(self.x,self.y)) 
 
class Game:
    def isCollision(self,x1,y1,x2,y2,bsize):
        if x1 <= x2 and x1 >= x2 - bsize:
            if y1 <= y2 and y1 >= y2 - bsize:
                return True
        return False
 
class App:
 
    windowWidth = 800
    windowHeight = 600
    nAnts = 500
    AntsLst = []
    apple = 0
    
 
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._ant_surf = None
        self._antFood_surf = None
        self._apple_surf = None
        self._home_surf = None
        self.game = Game()
        for i in range (self.nAnts):
            #self.AntsLst[0] = Ant()
            self.AntsLst.append(Ant())
        self.apple = Apple(275,275)
        self.home = Home(50,50)
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
 
        pygame.display.set_caption('Ant Colony Optimization (Github: @AhsanSn)')
        self._running = True
        self._ant_surf = pygame.image.load("ant.png").convert()
        self._antFood_surf = pygame.image.load("antFood.png").convert()
        self._apple_surf = pygame.image.load("block.jpg").convert()
        self._home_surf = pygame.image.load("home.jpg").convert()
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self):
        for i in range (self.nAnts):            
            self.AntsLst[i].update()
 
        # does ant eat apple?
        for ant in range (self.nAnts):
            if self.game.isCollision(self.apple.x,self.apple.y,self.AntsLst[ant].x, self.AntsLst[ant].y,31):
                self.AntsLst[ant].hasFood = 1;

        # does ant reaches home?
        for ant in range (self.nAnts):
            if self.game.isCollision(self.home.x,self.home.y,self.AntsLst[ant].x, self.AntsLst[ant].y,31):
                self.AntsLst[ant].hasFood = 1;      
 
        # does any reaches the border?
        for ant in range (self.nAnts):
            if(self.AntsLst[ant].y>self.windowHeight):
                self.AntsLst[ant].y = 0
            elif(self.AntsLst[ant].y<0):
                self.AntsLst[ant].y = self.windowHeight
            elif(self.AntsLst[ant].x>self.windowWidth):
                self.AntsLst[ant].x = 0
            elif(self.AntsLst[ant].x<0):
                self.AntsLst[ant].x = self.windowWidth
        pass
 
    def on_render(self):
        self._display_surf.fill((0,0,0))
        for ant in range (self.nAnts):
            if(self.AntsLst[ant].hasFood==1):
                self.AntsLst[ant].draw(self._display_surf, self._antFood_surf)
            if(self.AntsLst[ant].hasFood==0):
                self.AntsLst[ant].draw(self._display_surf, self._ant_surf)
        self.apple.draw(self._display_surf, self._apple_surf)
        self.home.draw(self._display_surf, self._home_surf)
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        iteration = 0
        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            if(iteration%100==0):
                #print("iter", iteration)
                for ant in range (self.nAnts):
                    self.AntsLst[ant].changeDirection()
                    self.AntsLst[ant].moveRandom()
            
            self.on_loop()
            self.on_render()
            iteration = iteration +1
            time.sleep (50.0 / 5000.0);
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()

'''
Initial code taken from: https://pythonspot.com/snake-with-pygame/
'''
