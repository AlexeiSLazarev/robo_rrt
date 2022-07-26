from distutils.ccompiler import gen_preprocess_options
import pygame
from RRTBasePy import RRTGraph
from RRTBasePy import RRTMap
import time

def main():
    dimensions = (600, 1000)
    start = (50,50)
    goal = (510,510)
    # obsdim = 30
    obsdim = 50
    obsnum = 80
    iteration = 0
    t1 = 0
    
    pygame.init()
    map = RRTMap(start, goal, dimensions, obsdim, obsnum)
    graph = RRTGraph(start, goal, dimensions, obsdim, obsnum)
    
    obstacles = graph.makeobs()
    map.drawMap(obstacles)
    clock = pygame.time.Clock()
    
    t1 = time.time()
    while (not graph.path_to_goal()):
        elapsed = time.time() - t1
        t1 = time.time()
        if elapsed > 10:
            raise
        
        if iteration % 10 == 0:
            X, Y, Parent = graph.bias(goal)
            pygame.draw.circle(map.map, map.grey, (X[-1], Y[-1]), map.nodeRad, 0)
            pygame.draw.line(map.map, map.blue, (X[-1], Y[-1]), (X[Parent[-1]], Y[Parent[-1]]), map.edgeThickness)
            pygame.display.update()
        else:
            X, Y, Parent = graph.expand()
            pygame.draw.circle(map.map, map.grey, (X[-1], Y[-1]), map.nodeRad + 2, 0)
            pygame.draw.line(map.map, map.blue, (X[-1], Y[-1]), (X[Parent[-1]], Y[Parent[-1]]), map.edgeThickness)
            pygame.display.update()
            
        if iteration % 10 == 0:
            pygame.display.update()
        iteration += 1
        # time.sleep(0.1)
    map.drawPath(graph.getPathCoords())
    pygame.display.update()
    pygame.event.clear()
    pygame.event.wait()
    clock.tick(20)
    
    # while(True):
    #     x,y = graph.sample_envir()
    #     n = graph.number_of_nodes()
    #     graph.add_node(n, x, y)
    #     graph.add_edge(n-1,n)
    #     x1,y1 = graph.x[n], graph.y[n]
    #     x2,y2 = graph.x[n-1], graph.y[n-1]
    #     if (graph.isFree()):
    #         pygame.draw.circle(map.map, map.Red, (graph.x[n], graph.y[n]), map.nodeRad, map.nodeThickness)
    #         if not graph.crossObstacle(x1,x2,y1,y2):
    #             pygame.draw.line(map.map, map.blue, (x1, y1), (x2, y2), map.edgeThickness)
                
    #     pygame.display.update()
    #     # time.sleep(0.1)
    # pygame.event.clear()
    # pygame.event.wait()
    
    
if __name__ == '__main__':
    main()
