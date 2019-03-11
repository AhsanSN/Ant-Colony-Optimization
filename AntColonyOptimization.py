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
    evapoRate = 0.55550 #slowness (must be b/w 0 and 1)
    simulationSlowness = 130 #keep is greater than 400


    AntsLst = []
    NodeLst = []
    pheromoneMap = []
    globalMax = 0
    globalMin = 100000
    globalMaxPath = []
    globalMinPath = []
    data = []
    WholepathNode = []
    current_milli_time = lambda: int(round(time.time() * 1000))
    timeNow = current_milli_time()
    #initializing pharamone map
    for i in range (nNodes+1):
        pheromoneMap.append([])
    for i in range (nNodes+1):    
        for j in range (nNodes+1):
            pheromoneMap[i].append(randint(20, 50))

    #pheromoneMap[0][2] = 99999
    #pheromoneMap[2][0] = 99999
    
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._ant_surf = None
        self._node_surf = None
        self.game = Game()
        for i in range (self.nAnts):
            self.AntsLst.append(Ant(self.x, self.y))

        #putting data points
        App.data = []        
        App.data.append([0, self.x, self.y])

        #configurations
        
        #oval config
        App.data.append([1, 200, 150])
        App.data.append([2, 350, 150])
        App.data.append([3, 400, 150])
        App.data.append([4, 550, 150])
        
        App.data.append([5, 350, 400])
        App.data.append([6, 200, 400])
        App.data.append([7, 150, 400])
        App.data.append([8, 100, 400])
        
        '''
        App.data.append([1, 750, 80])
        App.data.append([2, 350, 85])
        App.data.append([3, 550, 70])
        App.data.append([4, 560, 75])
        
        App.data.append([5, 750, 220])
        App.data.append([6, 500, 320])
        App.data.append([7, 150, 150])
        App.data.append([8, 110, 140]) 
        
        for i in range (App.nNodes):
            App.data.append([i+1, randint(0, 800), randint(0, 600)])     
        '''
        for i in range (len(App.data)):
            self.NodeLst.append(Node(App.data[i][1], App.data[i][2]))
        
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
 
    def on_render(self):
        self._display_surf.fill((0,0,0))
        for ant in range (self.nAnts):
            self.AntsLst[ant].draw(self._display_surf, self._ant_surf)
        for node in range (len(self.NodeLst)):
            self.NodeLst[node].draw(self._display_surf, self._node_surf)
        self.on_render_path()
        pygame.display.flip()

    def on_render_path(self):
        pheromoneSum = 0
        pheromoneProportion = []
        maxPher = 0
        #frame
        for i in range (App.nNodes+1):
            pheromoneProportion.append([])
        for i in range (App.nNodes+1):    
            for j in range (App.nNodes+1):
                if (App.pheromoneMap[i][j]>maxPher):
                    maxPher = App.pheromoneMap[i][j]
                pheromoneProportion[i].append(1)

        #print("maxPher", maxPher)
        #proportion
                
        for i in range(len(App.pheromoneMap)):
            for j in range(len(App.pheromoneMap)):
                #print(i, j)
                a= (App.pheromoneMap[i][j]+ (-maxPher+245))
                b = (App.pheromoneMap[i][j]+ (-maxPher+245))
                if(a<0):
                    a=0
                if(b<0):
                    b=0
                pheromoneProportion[i][j] = [int(a) , int(b)]
        #print(pheromoneProportion)
        for i in range (App.nNodes+1):    
            for j in range (App.nNodes+1):
                if ((pheromoneProportion[i][j][0]>255) or (pheromoneProportion[i][j][1]>255)):
                    print(pheromoneProportion[i][j])
                pygame.draw.line(self._display_surf,(pheromoneProportion[i][j][0],0,pheromoneProportion[i][j][1]), [App.NodeLst[i].x,App.NodeLst[i].y],[App.NodeLst[j].x,App.NodeLst[j].y],1)
                #App.pheromoneMap[i][j] = (App.pheromoneMap[i][j])- (((App.pheromoneMap[i][j])/100) * App.evapoRate)
        
    def on_cleanup(self):
        pygame.quit()

    def selectNodeToTravel(self, selectedNodeFrom, NodesNotTravelled, pheromoneMap):
        selectedNodeIndex = 1
        pheromoneSum = 0
        pheromoneProportion = []
        #print("pheromoneMap", pheromoneMap)
        #print("NodesNotTravelled", NodesNotTravelled)
        for i in range(len(NodesNotTravelled)):
            #print("i", i)
            b = NodesNotTravelled[i][0]
            #print("b,", b)
            a = pheromoneMap[selectedNodeFrom[0]][b]
            pheromoneSum = pheromoneSum + a

        for i in range(len(NodesNotTravelled)):
            #print("i1", i)
            b = NodesNotTravelled[i][0]
            pheromoneProportion.append(pheromoneMap[selectedNodeFrom[0]][b]/pheromoneSum)
        randNo = randint(0,1000000)/1000000
        lower = 0
        for i in range (len(pheromoneProportion)):
            if ((randNo>lower) and (randNo<lower + pheromoneProportion[i])):
                selectedNodeIndex = i
            lower = lower + pheromoneProportion[i]
        #print("selectedNodeIndex", selectedNodeIndex)
        return selectedNodeIndex

    def getDistTwoNodes(node1, node2, data):
        return (math.sqrt((float(data[node1][0])-float(data[node2][0]))**2 + (float(data[node1][1])-float(data[node2][1]))**2))

    def getPathLength(path, data):
        total = 0
        for i in range (len(path)-1):
            dist = App.getDistTwoNodes(path[i],path[i+1], data)
            #print("path[i], path[i+1], dist", path[i],path[i+1], dist)
            total = total + dist
        #print("total", total, "path", path)
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
            try:
                pygame.event.pump()
                keys = pygame.key.get_pressed()
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
                        #print("selectedNodeTo[ant]", selectedNodeTo[ant])
                        WholepathNode[ant].append(selectedNodeTo[ant][0])
                        self.AntsLst[ant].moveToPoint(selectedNodeFrom[ant][1], selectedNodeFrom[ant][2], selectedNodeTo[ant][1], selectedNodeTo[ant][2])#moveRandom()
                        #updating Pharmacon
                        #App.pheromoneMap[selectedNodeFrom[ant][0]][selectedNodeTo[ant][0]] = App.pheromoneMap[selectedNodeFrom[ant][0]][selectedNodeTo[ant][0]] + 100
                        #App.pheromoneMap[selectedNodeTo[ant][0]][selectedNodeFrom[ant][0]] = App.pheromoneMap[selectedNodeTo[ant][0]][selectedNodeFrom[ant][0]] + 100

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
                    #print("WholepathNode", WholepathNode)
                    #print("pheromoneMap", App.pheromoneMap)
                    
                #reaching home
                for ant in range (App.nAnts):
                    self.AntsLst[ant].moveToPoint(selectedNodeFrom[ant][1], selectedNodeFrom[ant][2], App.data[0][1], App.data[0][2])#moveRandom()
                    #updating pharmacon
                    #App.pheromoneMap[selectedNodeFrom[ant][0]][App.data[0][0]] = App.pheromoneMap[selectedNodeFrom[ant][0]][App.data[0][0]] + 100
                    #App.pheromoneMap[App.data[0][0]][selectedNodeFrom[ant][0]] = App.pheromoneMap[App.data[0][0]][selectedNodeFrom[ant][0]] + 100
                    WholepathNode[ant].append(0)
                while((abs(self.AntsLst[ant].x-App.data[0][1])>1)and(abs(self.AntsLst[0].y-App.data[0][2]))>1):
                    self.on_loop()
                    self.on_render()
                for ant in range (App.nAnts):
                    self.AntsLst[ant].x = App.data[0][1]
                    self.AntsLst[ant].y = App.data[0][2]
                #print(App.pheromoneMap)
                #print("WholepathNode", WholepathNode)
                avgScore = 0
                #adding weight to all visited paths
                for ant in range (App.nAnts):
                    pathDistance = App.getPathLength(WholepathNode[ant], App.data)
                    App.WholepathNode = WholepathNode
                    avgScore = avgScore + pathDistance
                    for antPath in range (len(WholepathNode[ant])-1):
                        edgeDistance = App.getDistTwoNodes(WholepathNode[ant][antPath],WholepathNode[ant][antPath+1], App.data)
                        if((pathDistance - (edgeDistance/pathDistance))<0):
                            print("asdskjasdkajsdnkajsndkjasndkjasndkjdn")
                        App.pheromoneMap[WholepathNode[ant][antPath]][WholepathNode[ant][antPath+1]] = App.pheromoneMap[WholepathNode[ant][antPath]][WholepathNode[ant][antPath+1]] + (pathDistance - (edgeDistance/pathDistance))# * 100
                        App.pheromoneMap[WholepathNode[ant][antPath+1]][WholepathNode[ant][antPath]] = App.pheromoneMap[WholepathNode[ant][antPath]][WholepathNode[ant][antPath+1]] + (pathDistance - (edgeDistance/pathDistance))# * 100
                #print("App.pheromoneMap", App.pheromoneMap)
                avgScore = avgScore/App.nAnts

                #evaporating
                for i in range (App.nNodes+1):    
                    for j in range (App.nNodes+1):
                        App.pheromoneMap[i][j] = (App.pheromoneMap[i][j]* App.evapoRate)
                #exit()

                
                #print("pheromoneMap", App.pheromoneMap)
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
                    print("it:",iteration,"max, min, avgScore", int(App.globalMax), int(App.globalMin), int(avgScore),"maxPath",App.globalMaxPath,  "minPath", App.globalMinPath)
                    print("maxPher", maxPher, "maxPherPath", maxPherPath)
                    for i in range (len(WholepathNode)):
                        print("Path",i,  WholepathNode[i])
            except:
                print("GAME OVER")
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()

'''
Initial code taken from: https://pythonspot.com/snake-with-pygame/
'''
