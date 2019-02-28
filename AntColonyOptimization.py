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
      
    def moveToPoint(self, fromX, fromY, toX, toY):
        # update position of head of ant
        #print(fromX, fromY, toX, toY)
        subtractXFactor = 0
        subtractYFactor = 0
        if(fromX<toX):
            subtractXFactor = -(fromX-toX)
        if(fromX>toX):
            subtractXFactor = -(fromX-toX)
        if(fromY<toY):
            subtractYFactor = -(fromY-toY)
        if(fromY>toY):
            subtractYFactor = -(fromY-toY)
        
        self.stepX = ((subtractXFactor)/App.simulationSlowness)
        self.stepY = ((subtractYFactor)/App.simulationSlowness)
        self.x = self.x + self.stepX
        self.y = self.y + self.stepY
        
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
    nAnts = 5
    AntsLst = []
    NodeLst = []
    nNodes = 4
    apple = 0
    nAntsReachedHome = 0
    pheromoneMap = []
    evapoRate = 0.3
    simulationSlowness = 500 

    data = []
    current_milli_time = lambda: int(round(time.time() * 1000))
    timeNow = current_milli_time()
    #initializing pharamone map
    for i in range (nNodes+1):
        pheromoneMap.append([])
    for i in range (nNodes+1):    
        for j in range (nNodes+1):
            pheromoneMap[i].append(5)

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
        self.data.append([0, self.x, self.y])
        for i in range (App.nNodes):
            self.data.append([i+1, randint(0, 800), randint(0, 600)])     

        for i in range (len(self.data)):
            self.NodeLst.append(Node(self.data[i][1], self.data[i][2]))

        
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
            NodesNotTravelled = [] #for each ant
            selectedNodeFrom = []
            selectedNodeTo = []
            for ant in range (App.nAnts):
                NodesNotTravelled.append(list(self.data))
            #select first node
            for ant in range (App.nAnts):
                selectedNodeFrom.append(NodesNotTravelled[ant].pop(0))
                selectedNodeTo.append(1)
            for i in range (len(self.data)-1):
                for ant in range (App.nAnts):
                    #select one random node to go to
                    deleteIndex = (randint(0, len(NodesNotTravelled[ant])-1))
                    selectedNodeTo[ant] = NodesNotTravelled[ant].pop(deleteIndex)
                    self.AntsLst[ant].moveToPoint(selectedNodeFrom[ant][1], selectedNodeFrom[ant][2], selectedNodeTo[ant][1], selectedNodeTo[ant][2])#moveRandom()
                    #updating Pharmacon
                    App.pheromoneMap[selectedNodeFrom[ant][0]][selectedNodeTo[ant][0]] = App.pheromoneMap[selectedNodeFrom[ant][0]][selectedNodeTo[ant][0]] + 100
                    App.pheromoneMap[selectedNodeTo[ant][0]][selectedNodeFrom[ant][0]] = App.pheromoneMap[selectedNodeTo[ant][0]][selectedNodeFrom[ant][0]] + 100

                    self.on_loop()
                    self.on_render()
                
                while((abs(self.AntsLst[ant].x-selectedNodeTo[ant][1])>1)and(abs(self.AntsLst[ant].y-selectedNodeTo[ant][2]))>1):
                    self.on_loop()
                    self.on_render()
                for ant in range (App.nAnts):
                    #set coods to center of node
                    self.AntsLst[ant].x = selectedNodeTo[ant][1]
                    self.AntsLst[ant].y = selectedNodeTo[ant][2]
                    selectedNodeFrom[ant] = selectedNodeTo[ant]
                
            #reaching home
            for ant in range (App.nAnts):
                self.AntsLst[ant].moveToPoint(selectedNodeFrom[ant][1], selectedNodeFrom[ant][2], self.data[0][1], self.data[0][2])#moveRandom()
                #updating pharmacon
                App.pheromoneMap[selectedNodeFrom[ant][0]][self.data[0][0]] = App.pheromoneMap[selectedNodeFrom[ant][0]][self.data[0][0]] + 100
                App.pheromoneMap[self.data[0][0]][selectedNodeFrom[ant][0]] = App.pheromoneMap[self.data[0][0]][selectedNodeFrom[ant][0]] + 100

            while((abs(self.AntsLst[ant].x-self.data[0][1])>1)and(abs(self.AntsLst[0].y-self.data[0][2]))>1):
                self.on_loop()
                self.on_render()
            for ant in range (App.nAnts):
                self.AntsLst[ant].x = self.data[0][1]
                self.AntsLst[ant].y = self.data[0][2]
            print(App.pheromoneMap)
            exit()
                                    
            #evaporate pheromone
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
