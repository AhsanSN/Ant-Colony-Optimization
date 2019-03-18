from pygame.locals import *
import pygame
from pygame.locals import *
from random import randint
import pygame
import time
import math

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
        #print("App.simulationSlowness", App.simulationSlowness)
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
    #params
    x = 50
    y = 50
    windowWidth = 800
    windowHeight = 600
    nAnts = 6
    nNodes = 8
    evapoRate = 0.50 #slowness (must be b/w 0 and 1)
    simulationSlowness = 250 #keep is greater than 150 and less than 800


    initx = 300
    initlx = 400
    AntsLst = []
    NodeLst = []
    pheromoneMap = []
    globalMax = 0
    globalMin = 100000
    globalMaxPath = []
    globalMinPath = []
    data = []
    WholepathNode = []
    lastKeyPressed = "";
    
    def __init__(self, autoSim):
        self._running = True
        self._display_surf = None
        self._ant_surf = None
        self._node_surf = None
        self.game = Game()
        if self.on_init() == False:
            self._running = False
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        
        if(autoSim==True):
            #putting ants
            for i in range (self.nAnts):
                self.AntsLst.append(Ant(self.x, self.y))

            #initializing pharamone map
            for i in range (nNodes+1):
                pheromoneMap.append([])
            for i in range (nNodes+1):    
                for j in range (nNodes+1):
                    pheromoneMap[i].append(randint(20, 50))
            
            #putting data points
            App.data = []        
            App.data.append([0, self.x, self.y])

            #configurations
            
            #oval-1 config #reached min 1000 in 570 generations.
            
            App.data.append([1, 200, 150])
            App.data.append([2, 350, 150])
            App.data.append([3, 400, 150])
            App.data.append([4, 550, 150])
            
            App.data.append([5, 350, 400])
            App.data.append([6, 200, 400])
            App.data.append([7, 150, 400])
            App.data.append([8, 100, 400])

            '''
            #oval-2 config
            App.data.append([1, 350, 85])
            App.data.append([2, 550, 70])
            App.data.append([3, 620, 75])
            App.data.append([4, 750, 80])
            
            App.data.append([5, 750, 220])
            App.data.append([6, 500, 320])
            App.data.append([7, 150, 150])
            App.data.append([8, 110, 140]) 
            
            for i in range (App.nNodes):
                App.data.append([i+1, randint(0, 800), randint(0, 600)])     
            '''
            for i in range (len(App.data)):
                self.NodeLst.append(Node(App.data[i][1], App.data[i][2]))
        if(autoSim==False):
            App.data = []
            nPoints = int(input(("Enter number of Markets to place on the Map: ")))
            print("Window opened.")
            print("1st points is home.")
            pointCounter = 0
            App.nNodes = nPoints
            while(pointCounter<nPoints):
                pygame.event.get()
                self._display_surf.fill((0,0,0))       
                myfont = pygame.font.SysFont('Comic Sans MS', 30)
                textsurface = myfont.render('Points Placed: '+str(pointCounter), False, (123, 123, 123))
                self._display_surf.blit(textsurface,(0,0))
                pygame.display.flip()
                    
                if(pygame.mouse.get_pressed()[0]==1):
                    print(pygame.mouse.get_pos())
                    App.data.append([pointCounter, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]])
                    pointCounter = pointCounter +1
                    self._display_surf.fill((0,0,0))       
                    myfont = pygame.font.SysFont('Comic Sans MS', 30)
                    textsurface = myfont.render('Points Placed: '+str(pointCounter), False, (123, 123, 123))
                    self._display_surf.blit(textsurface,(0,0))
                    pygame.display.flip()
                    time.sleep(0.2)

            for i in range (len(App.data)):
                self.NodeLst.append(Node(App.data[i][1], App.data[i][2]))

            events = pygame.event.get()
            isEnterLoop = True
            myfont = pygame.font.SysFont('Adobe Gothic Std B', 50)
            textsurface = myfont.render('Number of Salesmen? (type in Console)', False, (123, 123, 123))
            self._display_surf.blit(textsurface,(100,280))
            pygame.display.flip()
            App.nAnts = int(input("Number of Salesman? :"))
            
            #putting ants
            for i in range (self.nAnts):
                self.AntsLst.append(Ant(self.x, self.y))

            #initializing pharamone map
            for i in range (App.nNodes+1):
                App.pheromoneMap.append([])
            for i in range (App.nNodes+1):    
                for j in range (App.nNodes+1):
                    App.pheromoneMap[i].append(randint(20, 50))
    
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
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    App.lastKeyPressed = "1"
                if event.key == pygame.K_2:
                    App.lastKeyPressed = "2"
            
         
    def on_render(self):
        self._display_surf.fill((0,0,0))       
        for ant in range (self.nAnts):
            self.AntsLst[ant].draw(self._display_surf, self._ant_surf)
        for node in range (len(self.NodeLst)):
            self.NodeLst[node].draw(self._display_surf, self._node_surf)

        #display slider
        redColor = pygame.Color(255,0,0)
        lredColor = pygame.Color(163, 13, 13)
        blueColor = pygame.Color(45,40,211)
        lblueColor = pygame.Color(18,14,124)
        
        pygame.draw.rect(self._display_surf,redColor,Rect(App.initx,5,10,20))
        pygame.draw.rect(self._display_surf,lredColor,Rect(App.initlx,26,10,20))

        if pygame.mouse.get_pressed()[0] != 0:
           if(App.lastKeyPressed=="1"):
               pos = pygame.mouse.get_pos()
               App.initx = pos[0]
               y = pos[1]
               a = App.initx
               if a < 0:
                  a = 0
               App.simulationSlowness = ((a/800)*650)+150
           if(App.lastKeyPressed=="2"):
               pos = pygame.mouse.get_pos()
               App.initlx = pos[0]
               y = pos[1]
               a = App.initlx
               if a < 0:
                  a = 0
               App.evapoRate = ((a/800))           
           
        myfont = pygame.font.SysFont('Adobe Gothic Std B', 30)
        textsurface = myfont.render('Simulation Smoothness:(1)', False, (123, 123, 123))
        ltextsurface = myfont.render('Evaporation Rate:(2)', False, (123, 123, 123))
        self._display_surf.blit(textsurface,(0,0))
        self._display_surf.blit(ltextsurface,(0,25))
        pygame.display.flip()

       
    def on_cleanup(self):
        pygame.quit()

    def selectNodeToTravel(self, selectedNodeFrom, NodesNotTravelled, pheromoneMap):
        selectedNodeIndex = 1
        pheromoneSum = 0
        pheromoneProportion = []
        for i in range(len(NodesNotTravelled)):
            b = NodesNotTravelled[i][0]
            a = pheromoneMap[selectedNodeFrom[0]][b]
            pheromoneSum = pheromoneSum + a

        for i in range(len(NodesNotTravelled)):
            b = NodesNotTravelled[i][0]
            pheromoneProportion.append(pheromoneMap[selectedNodeFrom[0]][b]/pheromoneSum)
        randNo = randint(0,1000000)/1000000
        lower = 0
        for i in range (len(pheromoneProportion)):
            if ((randNo>lower) and (randNo<lower + pheromoneProportion[i])):
                selectedNodeIndex = i
            lower = lower + pheromoneProportion[i]
        return selectedNodeIndex

    def getDistTwoNodes(node1, node2, data):
        return (math.sqrt((float(data[node1][0])-float(data[node2][0]))**2 + (float(data[node1][1])-float(data[node2][1]))**2))

    def getPathLength(path, data):
        total = 0
        for i in range (len(path)-1):
            dist = App.getDistTwoNodes(path[i],path[i+1], data)
            total = total + dist
        #stats
        if(App.globalMax<total):
            App.globalMax=total
            App.globalMaxPath = path
        if(App.globalMin>total):
            App.globalMin=total
            App.globalMinPath = path
        return(total) #the less the total the greater the fitness   
         
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        iteration = 0
        while( self._running ):
            pygame.event.get()
            #check for nearby pheromone
            NodesNotTravelled = [] #for each ant
            selectedNodeFrom = []
            selectedNodeTo = []
            WholepathNode = []
            for ant in range (App.nAnts):
                NodesNotTravelled.append(list(App.data))
                WholepathNode.append(list([0]))
            #select first node
            for ant in range (App.nAnts):
                selectedNodeFrom.append(NodesNotTravelled[ant].pop(0))
                selectedNodeTo.append(1)
            for i in range (len(App.data)-1):
                for ant in range (App.nAnts):
                    #select one random node to go to
                    deleteIndex = self.selectNodeToTravel(selectedNodeFrom[ant], NodesNotTravelled[ant], App.pheromoneMap) #(randint(0, len(NodesNotTravelled[ant])-1))
                    selectedNodeTo[ant] = NodesNotTravelled[ant].pop(deleteIndex)
                    WholepathNode[ant].append(selectedNodeTo[ant][0])
                    self.AntsLst[ant].moveToPoint(selectedNodeFrom[ant][1], selectedNodeFrom[ant][2], selectedNodeTo[ant][1], selectedNodeTo[ant][2])#moveRandom()
                    self.on_loop()
                    self.on_render()
                    pygame.event.get()
                
                while((abs(self.AntsLst[ant].x-selectedNodeTo[ant][1])>1)and(abs(self.AntsLst[ant].y-selectedNodeTo[ant][2]))>1):
                    self.on_loop()
                    self.on_render()
                for ant in range (App.nAnts):
                    #set coods to center of node
                    self.AntsLst[ant].x = selectedNodeTo[ant][1]
                    self.AntsLst[ant].y = selectedNodeTo[ant][2]
                    selectedNodeFrom[ant] = selectedNodeTo[ant]
       
                #evaporating
                for i in range (App.nNodes+1):    
                    for j in range (App.nNodes+1):
                        if(App.evapoRate==0):
                            App.evapoRate = 0.0000001
                        App.pheromoneMap[i][j] = (App.pheromoneMap[i][j]* App.evapoRate)
                
            #reaching home
            for ant in range (App.nAnts):
                self.AntsLst[ant].moveToPoint(selectedNodeFrom[ant][1], selectedNodeFrom[ant][2], App.data[0][1], App.data[0][2])
                WholepathNode[ant].append(0)
            while((abs(self.AntsLst[ant].x-App.data[0][1])>1)and(abs(self.AntsLst[0].y-App.data[0][2]))>1):
                self.on_loop()
                self.on_render()
            for ant in range (App.nAnts):
                self.AntsLst[ant].x = App.data[0][1]
                self.AntsLst[ant].y = App.data[0][2]
            avgScore = 0
            #adding weight to all visited paths
            for ant in range (App.nAnts):
                pathDistance = App.getPathLength(WholepathNode[ant], App.data)
                App.WholepathNode = WholepathNode
                avgScore = avgScore + pathDistance
                for antPath in range (len(WholepathNode[ant])-1):
                    edgeDistance = App.getDistTwoNodes(WholepathNode[ant][antPath],WholepathNode[ant][antPath+1], App.data)
                    if((pathDistance - (edgeDistance/pathDistance))<0):
                        print("errrror")
                    App.pheromoneMap[WholepathNode[ant][antPath]][WholepathNode[ant][antPath+1]] = App.pheromoneMap[WholepathNode[ant][antPath]][WholepathNode[ant][antPath+1]] + (pathDistance - (edgeDistance/pathDistance))# * 100
                    App.pheromoneMap[WholepathNode[ant][antPath+1]][WholepathNode[ant][antPath]] = App.pheromoneMap[WholepathNode[ant][antPath]][WholepathNode[ant][antPath+1]] + (pathDistance - (edgeDistance/pathDistance))# * 100
            avgScore = avgScore/App.nAnts

            #evaporate pheromone
            self.on_loop()
            self.on_render()
            iteration = iteration +1
            
            maxPher = 0
            maxPherPath = []
            for i in range (App.nNodes+1):    
                for j in range (App.nNodes+1):
                    if (App.pheromoneMap[i][j]>maxPher):
                        maxPher = App.pheromoneMap[i][j]
                        maxPherPath = [i, j]
            time.sleep (50.0 / 100000.0);
            if (iteration%10==0):
                print("it:",iteration,"max, min, avgScore", (App.globalMax), (App.globalMin), (avgScore),"maxPath",App.globalMaxPath,  "minPath", App.globalMinPath)
                print("maxPher", maxPher, "maxPherPath", maxPherPath)
                

        self.on_cleanup()
 
if __name__ == "__main__":
    simimp = str(input(("Press 'a' for Scripted Simulation and 'b' for placing points manually.")))
    if(simimp=="b"):
        theApp = App(False)
    else:
        theApp = App(True)
    theApp.on_execute()

'''
Initial code taken from: https://pythonspot.com/snake-with-pygame/
'''
