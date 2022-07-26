from ctypes import pointer
from tracemalloc import start
from turtle import distance
# from sys import ps
import pygame
import numpy as np
from random import randint, choice
import random
import math
# pygame.init()

screen_w = 1600
screen_h = 1200
WHITE = (255,255,255)
screen = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()
trajectory = None
target_point = None

class Graph:
    # Constructor
    def __init__(self, screen_w, screen_h, obstacle_list):
        self.obstacle_list = obstacle_list
        # self.m_num_of_nodes = num_of_nodes
        # Different representations of a graph
        self.list_of_edges = []
        # self.list_of_vertices = {}
        self.maximum_node_distance = 30
        self.start_point = None #(900,900)
        self.finsh_flag = False
        # self.add_vertex(self.start_point)
        # self.add_edge(self.start_point,self.start_point)
        self.finish_point = None#(300,300)
        self.shortest_path = None
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.trajectory_get_flag = False

	# Class internals interfaces
    def get_finsh_flag(self): return self.finsh_flag
    
    def get_srtart_point(self): return self.start_point

    def get_finish_point(self): return self.finish_point

    def set_start_point(self, point):
        self.start_point = point
        self.add_vertex(self.start_point)
        self.add_edge(self.start_point,self.start_point)

    def set_finish_point(self, point):
        self.finish_point = point

    # Class utilites
    def reset_graph(self, start_point, finish_point):
        self.list_of_edges = []
        self.set_start_point(start_point)
        self.set_finish_point(finish_point)
        self.finsh_flag = False
        self.trajectory_get_flag = False
        self.add_vertex(start_point)
        
    def find_shortest_path(self):
        parent_vertex = (0,0)
        self.shortest_path = []
        child_vertex = self.list_of_edges[-1][1]
        self.shortest_path.append(child_vertex)
        while parent_vertex != self.start_point:
            parent_vertex = self.find_parent(child_vertex)
            if parent_vertex:
                self.shortest_path.append(parent_vertex)
                child_vertex = parent_vertex

    def update(self):
        if not self.finsh_flag and self.finish_point:
            vertex = (randint(0, self.screen_w), randint(0, self.screen_h))
            if not self.check_collision_with_obstacles(vertex):
                # 10% of new vertices is the target vertex
                self.add_vertex(vertex)

    def check_collision_with_obstacles(self, vertex):
        collision_flag = False
        for obs in self.obstacle_list:
            if obs.collidepoint(vertex): 
                collision_flag = True
                break
        return collision_flag

    def add_vertex(self, new_point):
        if not self.finsh_flag:
            nearest_vertex = self.find_nearest_vertex(new_point)            
            if nearest_vertex: 
                distance = self.distance_p2p(new_point, nearest_vertex)
                if distance > self.maximum_node_distance:
                    # create new edge
                    coin = choice([0,0,1])
                    # toward the random point
                    if coin == 0:
                        new_point = self.create_proper_edge(nearest_vertex, new_point)
                    # toward the target point
                    else:
                        new_point = self.create_proper_edge(nearest_vertex, self.finish_point)
                    # add edge
                    if not self.check_collision_with_obstacles(new_point):
                        self.add_edge(nearest_vertex, new_point)
                        self.check_finish_found(new_point)        

    def create_proper_edge(self, p_near,  p_new):
            (xnear, ynear) = p_near
            (xrand, yrand) = p_new
            (px, py) = (xrand - xnear, yrand - ynear)
            theta = math.atan2(py, px)
            (x, y) = (int(xnear + self.maximum_node_distance * math.cos(theta)),
                      int(ynear + self.maximum_node_distance * math.sin(theta)))
            return ((x, y))

    def cross_obstacle(self, p1, p2):
        if self.obstacle_list:
            [x1 ,y1] = p1
            [x2 ,y2] = p2
            obs = self.obstacle_list.copy()
            while len(obs) > 0:
                rectang = obs.pop(0)
                for i in range(0,101):
                    u = i/100
                    x = x1*u + x2*(1-u)
                    y = y1*u + y2*(1-u)
                    if rectang.collidepoint(x,y):
                        return True
        return False

    def add_edge(self, vertex1, vertex2):        
        # Add the edge from node1 to node2
        if not self.cross_obstacle(vertex1, vertex2):
            self.list_of_edges.append([vertex1, vertex2])
    
    def find_parent(self, vertex):
        if self.list_of_edges:
            for edge in self.list_of_edges:
                if edge[1] == vertex:
                    return edge[0]

    def check_finish_found(self, vertex):
        distance = self.distance_p2p(vertex, self.finish_point)
        # print(distance)
        if distance <= self.maximum_node_distance:
            self.finsh_flag = True
            self.add_edge(vertex, self.finish_point)
            self.find_shortest_path()
            
    def find_nearest_vertex(self, p1):
        min_distance = 2000
        closes_vertex = ()
        if self.list_of_edges:
            for edge in self.list_of_edges:
                for p2 in edge:
                    distance = self.distance_p2p(p1, p2)
                    # print(distance)
                    # if distance <= self.maximum_node_distance:
                    # print(f'found {p2}')
                    if distance < min_distance:
                        min_distance = distance
                        closes_vertex = p2

        if closes_vertex:
            return closes_vertex
            print(f'closes_vertex {closes_vertex}')
        
    def distance_p2p(self, p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]

        return np.sqrt(dx**2 + dy**2)

    def find_trajectory(self):
        while not self.finsh_flag:
            graph.update()

    def get_trajectory(self):
        # trajectory = self.find_shortest_path()
        trajectory = []
        trajectory = self.shortest_path.copy()
        self.trajectory_get_flag = True
        # for i in reversed(traj_rev):
        #     trajectory.append(i)
        return trajectory

    def get_trajecory_get_flag(self): return self.trajectory_get_flag

    def draw_graph(self, screen):
        if self.list_of_edges:
            for edge in self.list_of_edges:
                pygame.draw.lines(screen, 'Cyan',False, edge,4)
    
    def draw_trajectory(self):
        if self.finsh_flag and self.list_of_edges:
            trajectory = self.get_trajectory()
            pygame.draw.lines(screen, 'Green',False, trajectory,4)

    def print_edge_list(self):

        num_of_edges = len(self.list_of_edges)
        for i in range(num_of_edges):
            print("edge ", i+1, ": ", self.list_of_edges[i])
    
class UAV:
    def __init__(self, screen_w, screen_h, obstacle_list, uav_side = 40) -> None:
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.obstacle_list = obstacle_list
        self.uav_side = uav_side
        self.step_size = 5
        self.target_point = ()
        self.uav_rect = self.deploy_uav()
        self.position = self.uav_rect.center
        self.color = 'Black'
        self.trajectory = []

    def get_uav_position(self): return self.uav_rect.center
    
    def deploy_uav(self):
        while True:
            topleft = (int(random.uniform(0, screen_w - self.uav_side)), int(random.uniform(0, screen_h - self.uav_side)))
            uav_rect = pygame.Rect(topleft, (self.uav_side, self.uav_side))
            if not uav_rect.collidelistall(obstacle_list):
                return uav_rect

    def step_toward_target_point(self):

        if self.target_point:
            if self.distance_p2p(self.uav_rect.center, self.target_point) < self.step_size: 
                # self.uav_rect.x = self.target_point[0] - self.uav_rect.center[0]
                # self.uav_rect.y = self.target_point[1] - self.uav_rect.center[1]
                self.target_point = ()
            else:
                x0 = self.uav_rect.center[0]
                y0 = self.uav_rect.center[1]

                dx = self.target_point[0] - x0
                dy = self.target_point[1] - y0

                distance = np.sqrt(dx**2 + dy**2)
                
                cos_ = dx/distance
                sin_ = dy/distance

                uav_step_x = self.step_size * cos_
                uav_step_y = self.step_size * sin_

                self.uav_rect.x += uav_step_x
                self.uav_rect.y += uav_step_y

    def distance_p2p(self, p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]

        return np.sqrt(dx**2 + dy**2)
    
    def set_target_point(self, point):
        self.target_point = point

    def set_trajectory(self, trajectory):
        self.trajectory = trajectory
        self.target_point = self.trajectory.pop()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.uav_rect)
        if len(self.trajectory) > 1:
            pygame.draw.lines(screen, 'Green',False, trajectory,4)

    def update(self):
        if self.target_point:
            self.step_toward_target_point()
        else:
            if self.trajectory:
                self.target_point = self.trajectory.pop()

class Obstacles:
    def __init__(self, screen_w, screen_h, obstacles_num = 20, obstacle_side = 150) -> None:
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.obstacles_num = obstacles_num
        self.obstacle_side = obstacle_side
        self.obstacle_list = []
        self.create_obstacle_list()
        self.color = 'Green'
    
    def create_obstacle_list(self):
        for i in range(self.obstacles_num):
            self.obstacle_list.append(self.create_obstacle())
    
    def create_obstacle(self):
        topleft = (int(random.uniform(0, self.screen_w - self.obstacle_side)), int(random.uniform(0, self.screen_h - self.obstacle_side)))
        obstacle = pygame.Rect(topleft, (self.obstacle_side, self.obstacle_side))
        return obstacle

    def get_obstacle_list(self): return self.obstacle_list

    def draw(self, screen):
        for obs in self.obstacle_list:
            pygame.draw.rect(screen, self.color, obs)

class FogOfWar():
    def __init__(self, screen_w, screen_h) -> None:
        pass

# Create graph
obstacles = Obstacles(screen_w, screen_h)
obstacle_list = obstacles.get_obstacle_list()
graph = Graph(screen_w, screen_h, obstacle_list)

# Create UAV
uav = UAV(screen_w, screen_h, obstacle_list)

# flag_moving = False
# target_point = None
graph.set_start_point(uav.get_uav_position())


i = 0
while True:
    
    # Process events
    i += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONUP:
            # pos = uav.get_uav_position()
            print(uav.get_uav_position())
            graph.reset_graph(uav.get_uav_position(), event.pos)
            graph.find_trajectory()
            trajectory = graph.get_trajectory()
            uav.set_trajectory(trajectory)
            # uav.set_target_point(event.pos)
    
    # Drawing

    # Surface
    screen.fill(WHITE)
    # Obstacles
    obstacles.draw(screen)
    # Graph
    graph.draw_graph(screen)
    # UAV
    uav.draw(screen)
    # Draw Target point
    if graph.get_finish_point():
        target_rect = pygame.draw.circle(screen, 'Red', graph.get_finish_point(),10,4)
    
    uav.update()
    graph.update()

    pygame.display.update()
    clock.tick(60)
