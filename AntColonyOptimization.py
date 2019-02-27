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
 
class Node:
    x = 0
    y = 0
    def __init__(self, x, y):
       self.x = x
       self.y = y

    def draw(self, surface, image):
        surface.blit(image,(self.x,self.y)) 

 
class Ant:
    x = 0
    y = 0 
    step = 3
    direction = 0
    hasFood = 0
 
    updateCountMax = 2
    updateCount = 0
 
    def __init__(self, x, y):
       self.previousX = 0
       self.stepX = randint(-2,2);
       self.stepY = randint(-2,2);
       self.x = x
       self.y = y
 
    def update(self):
        self.y = self.y + self.stepY#0.1#int(self.stepY/randint(1,5))
        self.x = self.x + self.stepX#0.1#int(self.stepX/randint(1,5))
        if (self.hasFood==1):
            try:
                App.pheromoneMap[self.y][self.x] = App.pheromoneMap[self.y][self.x] + current_milli_time()
            except:
                1;

    def moveToPoint(self, fromX, fromY, toX, toY):
        # update position of head of ant
        subtractXFactor = 0
        if(fromX<toX):
            subtractXFactor = -(fromX-toX)
        if(fromX>toX):
            subtractXFactor = -(fromX-toX)
        if(fromY<toY):
            subtractYFactor = -(fromY-toY)
        if(fromY>toY):
            subtractYFactor = -(fromY-toY)
        
        self.stepX = ((subtractXFactor)/1000)
        self.stepY = ((subtractYFactor)/1000)
        self.x = self.x + self.stepX
        self.y = self.y + self.stepY
        
        if (self.hasFood==1):
            try:
                App.pheromoneMap[self.y][self.x] = App.pheromoneMap[self.y][self.x] + current_milli_time()
            except:
                1;

    def moveRandom(self):
        self.direction = 4
 
    def draw(self, surface, image):
        surface.blit(image,(self.x,self.y)) 
 
class Game:
    def isCollision(self,x1,y1,x2,y2,bsize):
        if x1 <= x2 and x1 >= x2 - bsize:
            if y1 <= y2 and y1 >= y2 - bsize:
                return True
        return False
 
class App:   
    x = 50
    y = 50
    windowWidth = 800
    windowHeight = 600
    nAnts = 1
    AntsLst = []
    NodeLst = []
    apple = 0
    nAntsReachedHome = 0
    pheromoneMap = []
    evapoRate = 0.3

    data = []
    current_milli_time = lambda: int(round(time.time() * 1000))
    timeNow = current_milli_time()
    #initializing pharamone map
    for i in range (windowHeight):
        pheromoneMap.append([])
    for i in range (windowHeight):    
        for j in range (windowWidth):
            pheromoneMap[i].append(0)

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._ant_surf = None
        self._node_surf = None
        self.game = Game()
        for i in range (self.nAnts):
            self.AntsLst.append(Ant(self.x, self.y))

        #putting data points
        self.data = []        
        self.data.append([i, self.x, self.y])
        for i in range (40):
            self.data.append([i, randint(0, 800), randint(0, 600)])     

        for i in range (len(self.data)):
            #print("x, y", (self.data[i][1], self.data[i][2]))
            self.NodeLst.append(Node(self.data[i][1], self.data[i][2]))
            #self.NodeLst.append(Node(800, 600))

        #self.NodeLst.append(Node(50, 50)) 
        
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        pygame.display.set_caption('Ant Colony Optimization (Github: @AhsanSn)')
        self._running = True
        self._ant_surf = pygame.image.load("ant.png").convert()
        self._node_surf = pygame.image.load("node.png").convert()
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self):
        for i in range (self.nAnts):            
            self.AntsLst[i].update()
 
        # does ant eat apple?
        '''
        for ant in range (self.nAnts):
            if self.game.isCollision(self.apple.x,self.apple.y,self.AntsLst[ant].x, self.AntsLst[ant].y,31):
                self.AntsLst[ant].hasFood = 1;

        # does ant reaches home?
        for ant in range (self.nAnts):
            if self.game.isCollision(self.home.x,self.home.y,self.AntsLst[ant].x, self.AntsLst[ant].y,31):
                if (self.AntsLst[ant].hasFood==1):
                    self.AntsLst[ant].hasFood = 0;
                    self.nAntsReachedHome = self.nAntsReachedHome + 1
                    print("nAntsReachedHome,time", self.nAntsReachedHome, App.current_milli_time())
        '''
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
            self.AntsLst[ant].draw(self._display_surf, self._ant_surf)
        for node in range (len(self.NodeLst)):
            self.NodeLst[node].draw(self._display_surf, self._node_surf)
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

            #check for nearby pheromone

            '''
            for ant in range (self.nAnts):
                if(self.AntsLst[ant].hasFood == 0):
                    pheromoneNear = False
                    highConcX = 0
                    highConcY = 0
                    highConc = 0
                    for i in range (-3, 3):
                        for j in range (-3, 3):
                            #print
                            searchY = self.AntsLst[ant].y + i
                            searchX = self.AntsLst[ant].x + i
                            if ((searchY<self.windowHeight and searchY>=0) and (searchX<self.windowWidth and searchX>=0)):
                                if (self.pheromoneMap[searchY][searchX]>highConc):
                                    highConc = self.pheromoneMap[searchY][searchX]
                                    highConcX = searchX
                                    highConcY = searchY
                                    #print("pheromoneNear", highConc);
                            if(highConc>0):
                                self.AntsLst[ant].x = highConcX;
                                self.AntsLst[ant].y = highConcY;
                            else:
                                if(iteration%100==0):
                                #print("iter", iteration)
                                    self.AntsLst[ant].changeDirection()
                                    self.AntsLst[ant].moveRandom()
                else:
                    if(iteration%100==0):
                            #print("iter", iteration)
                            self.AntsLst[ant].changeDirection()
                            self.AntsLst[ant].moveRandom()
            '''
            #self.AntsLst[0].changeDirection() #self.data[0][1], self.data[0][2]
            for i in range (5):
                self.AntsLst[0].moveToPoint( self.data[0][1], self.data[0][2], 50,50)#moveRandom()
            
                                    
            #evaporate pheromone
            '''
            for i in range (self.windowHeight):    
                for j in range (self.windowWidth):
                    if (self.pheromoneMap[i][j]>=1):
                        self.pheromoneMap[i][j] = self.pheromoneMap[i][j] - 1
            '''
            self.on_loop()
            self.on_render()
            iteration = iteration +1
            time.sleep (50.0 / 100000.0);
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()

'''
Initial code taken from: https://pythonspot.com/snake-with-pygame/
'''
