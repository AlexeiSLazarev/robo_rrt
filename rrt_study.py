import pygame
import numpy as np
from random import randint
# pygame.init()

screen_w = 1600
screen_h = 1200
WHITE = (255,255,255)
screen = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()

class Graph:
    # Constructor
    def __init__(self):
        # self.m_num_of_nodes = num_of_nodes
        # Different representations of a graph
        self.list_of_edges = []
        # self.list_of_vertices = {}
        self.maximum_node_distance = 100
        self.start_point = (100,100)
        self.finsh_flag = False
        self.add_vertex(self.start_point)
        self.finish_point = (700,800)

	
    # Set target

    # Add edge to a graph
    def add_edge(self, vertex1, vertex2):        
        # Add the edge from node1 to node2
        self.list_of_edges.append([vertex1, vertex2])
    
    def find_parent(self, node_index):
        if self.list_of_edges:
            for edge in self.list_of_edges:
                if edge[1] == node_index:
                    print(f'found: {edge[0]}')

    def add_vertex(self, point):
        if not self.finsh_flag:
            nearest_vertex = self.find_nearest_vertex(point)
            if nearest_vertex: 
                self.add_edge(nearest_vertex, point)
                self.check_finish_found(point)

    def check_finish_found(self, vertex):
        distance = self.distance_p2p(vertex, self.finish_point)
        # print(distance)
        if distance <= self.maximum_node_distance:
            self.finsh_flag = True
            self.add_edge(vertex, self.finish_point )
            
    def find_nearest_vertex(self, p1):
        min_distance = 2000
        closes_vertex = ()
        if self.list_of_edges:
            for edge in self.list_of_edges:
                for p2 in edge:
                    distance = self.distance_p2p(p1, p2)
                    # print(distance)
                    if distance <= self.maximum_node_distance:
                        print(f'found {p2}')
                        if distance < min_distance:
                            min_distance = distance
                            closes_vertex = p2
        else:
            self.add_edge(p1,p1)
        if closes_vertex:
            return closes_vertex
            print(f'closes_vertex {closes_vertex}')
        
    def distance_p2p(self, p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]

        return np.sqrt(dx**2 + dy**2)

    def draw_graph(self, screen):
        if self.list_of_edges:
            for edge in self.list_of_edges:
                pygame.draw.lines(screen, 'Cyan',False, edge,4)
            
            pygame.draw.circle(screen, 'Red', self.list_of_edges[0][0], 10, 4)

            if self.finsh_flag:
                pygame.draw.circle(screen, 'Blue', self.finish_point , 10, 4)
            else:
                pygame.draw.circle(screen, 'Red', self.finish_point , 10, 4)

            


    # Print a graph representation
    def print_edge_list(self):

        num_of_edges = len(self.list_of_edges)
        for i in range(num_of_edges):
            print("edge ", i+1, ": ", self.list_of_edges[i])
    
graph = Graph()

# graph.add_edge((0,10), (559,100))
# graph.add_edge((0,130), (45,100))
# graph.add_edge((0,40), (200,100))

# graph.find_nearest_vertex((0,99))

# graph.print_edge_list()



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONUP:
            graph.add_vertex(event.pos)
    vertex = (randint(0, screen_w), randint(0, screen_h))
    graph.add_vertex(vertex)

    screen.fill(WHITE)
    graph.draw_graph(screen)
    pygame.display.update()
    clock.tick(60)
