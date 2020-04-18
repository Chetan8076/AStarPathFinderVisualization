import pygame
from pygame.locals import*
import sys


Text_Font=("Verdana", 12)
SCREEN=pygame.display.set_mode((600,620))
WIDTH=15
HEIGHT=15
BOXES=40
MARGIN=0
BLACK=(30,40,3)
BLUE=(0,0,255)
RED=(255,0,0)
color=BLACK
WHITE=(255,255,255)
BACKGROUND=[102, 255, 204]
PATHCOLOUR = [255, 0, 151]

graph=[[0 for x in range(40)] for i in range(40)]
luke=graph
    
move_cost = 1

class Node:
    def __init__(self,value,point):
        self.value=value
        self.point=point
        self.H=0
        self.G=0
        self.parent=None
    # def move_cost(self):
    #   return 0 if self.value=="X" else 1





def children(node,graph):
    x,y = node.point[0], node.point[1]
    listOfChildren=[]
    diagonalFlag=False
    # listOfChildren=[graph[x[0]][x[1]] for x in [(x-1,y),(x+1,y),(x,y+1),(x,y-1)]]
    for i in [-1,1]:
        if x+i >= 0 and x+i<BOXES :
            if graph[x+i][y] == 0:
                
                listOfChildren.append(Node(1,[x+i,y]))
        if y+i >= 0 and y+i <BOXES:
            if graph[x][y+i] == 0:

                listOfChildren.append(Node(1,[x,y+i]))
        # if x+i >= 0 and x+i<BOXES and y+i >= 0 and y+i <BOXES:
        #     if graph[x+i][y+i]==0:
        #         listOfChildren.append(Node(1,[x+i,y+i]))
        # if x+i >= 0 and x+i<BOXES and y-i >= 0 and y-i <BOXES and diagonalFlag:
        #     if graph[x+i][y-i]==0:
        #         listOfChildren.append(Node(1,[x+i,y-i]))



    return listOfChildren

# Manhatten is used for the heuristic function

def Heuristic(source, goal):
    return int(((abs(source.point[0]-goal.point[0]))**2 + (abs(source.point[1]-goal.point[1]))**2)**(.5))

def aStarPathFinder(graph,start,goal):
    openSetNode = set()
    closedSet = set()
    


    # start position is current postition presently
    current=start
    openSetNode.add(current)




    while openSetNode:
        


        current=min(openSetNode,key=lambda x : x.G + x.H)

        if current.point == goal.point:


            path=[]
            path.append(current)

            while current.parent:
                path.append(current.parent)
                current = current.parent
            for i in range(len(graph)):
                print(graph[i])
            return path[::-1]

        openSetNode.remove(current)

        graph[current.point[0]][current.point[1]]=1


        closedSet.add(current)
        redrawAlgorithm(closedSet,start,goal)

        for node in children(current,graph):

            if node.point  in [i.point for i in closedSet]:
                continue

            if node.point in [i.point for i in openSetNode]:


                newCost = current.G + move_cost

                if node.G > current.G:

                    node.G=newCost

                    node.parent = current
            else:


                node.G = current.G + move_cost

                node.H = Heuristic(node,goal)

                node.parent = current

                openSetNode.add(node)
    


def WelcomeScreen():
    global graph
    flag=True
    while True:
        x,y=pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
               
                sys.exit()

            elif y< 600 and x<600 and flag and pygame.mouse.get_pressed()[0]:
                if [((y)//WIDTH),(x)//HEIGHT] == start.point or [((y)//WIDTH),(x)//HEIGHT] == goal.point :
                    continue
                graph[((y)//WIDTH)][(x)//HEIGHT]=2
                
                pygame.draw.rect(SCREEN,
                                     BLACK,
                                     [(MARGIN + WIDTH) * (((x)//WIDTH)) + MARGIN,
                                      (MARGIN + HEIGHT) * ((y//HEIGHT))+ MARGIN,
                                      WIDTH,
                                      HEIGHT])
            elif y> 600 and y<620 and x<600 and pygame.mouse.get_pressed()[0]:
                flag = False
                a=aStarPathFinder(graph, start, goal)
                if a == None:
                    SCREEN.blit(pygame.image.load('download.jpg'),(40,40))
                    for i in range(len(graph)):
                        print(graph[i])
                else:

                    for i in a:
                        redrawRectangles(i.point,start,goal)
                        pygame.time.wait(50)
                    # 
                    


        pygame.display.update()





def redrawAlgorithm(closedSet,start,goal):
    
    for i in closedSet:
        if i.point == start.point or i.point == goal.point  :
            color = RED
        else:
            color = BLUE
        pygame.draw.rect(SCREEN,
                             color,
                             [(MARGIN + WIDTH) * i.point[1] + MARGIN,
                              (MARGIN + HEIGHT) * i.point[0] + MARGIN,
                              WIDTH,
                              HEIGHT])
    for i in range(BOXES+1):
            pygame.draw.line(SCREEN,BLACK,(WIDTH*i,0),(HEIGHT*i,600))
            pygame.draw.line(SCREEN,BLACK,(0,HEIGHT*i),(600,WIDTH*i))


    pygame.display.update()



def redrawRectangles(a,start,goal):
    if a==start.point or a== goal.point:
        color = RED
    else:

        color = PATHCOLOUR
    pygame.draw.rect(SCREEN,
                             color,
                             [(MARGIN + WIDTH) * a[1] + MARGIN,
                              (MARGIN + HEIGHT) * a[0] + MARGIN,
                              WIDTH,
                              HEIGHT])
    pygame.display.update() 



def redraw(a, start, goal):
    
    for row in range(BOXES):
            for column in range(BOXES):
                


                if [row,column] == start.point or [row,column] == goal.point :
                    
                    color = RED

                elif [row,column] == a :
                    color=WHITE
                elif graph[row][column]==2:
                    color = BLACK
                    
                else:
                    
                    color=BACKGROUND

                pygame.draw.rect(SCREEN,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])  
            for i in range(BOXES+1):
                pygame.draw.line(SCREEN,BLACK,(WIDTH*i,0),(HEIGHT*i,600))
                pygame.draw.line(SCREEN,BLACK,(0,HEIGHT*i),(600,WIDTH*i))
            count=0


    pygame.display.update()
    


if __name__ == '__main__':

    start = Node(1,[0,0])
    graph[0][4]=1

    goal = Node(1,[25,25])

    pygame.init()
    SCREEN.fill(WHITE)
    myFont = pygame.font.SysFont("Times New Roman", 10)
    redraw([], start, goal)
    WelcomeScreen()
 


