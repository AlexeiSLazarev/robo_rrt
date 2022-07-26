import random
from re import S
from turtle import distance
import pygame
from random import randint
import numpy as np
import math

CAPTION = 'My RRT game'

screen_w = 1920 # main window widgth
screen_h = 1080 # main window height
obstacle_side = 100
uav_side = 80
uav_step_size = 30


'''
function RRT(map, startPosition, goalRegion, numIterations):
    tree = initializeEmptyTree()
    
    insertRootNode(tree, startPosition)
    for i = 1 to numIterations:
        randomPosition = sample(map)
        randomNode = createNode(tree, randomPosition)
        nearestNode = findNearestNode(tree, randomPosition)
        path = calculatePath(nearestNode, randomNode)
        if (hasCollision(map, path)):
            continue
        
        insertNewNode(tree, nearestNode, randomNode)
        if (randomPosition is within goalRegion): 
            return tree
    return tree
'''
class RRT_vanilla():
    def __init__(self, uav_rect, target_p, screen_w, screen_h, obstacle_list) -> None:
        self.start = uav_rect.topleft
        self.target_p = target_p
        self.target_found = False
        self.nodes = [(uav_rect.topleft[0], uav_rect.topleft[1], 0)]
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.obstacle_list = obstacle_list
        self.node_length = 100
        self.vertices = []
        self.vertices.append((uav_rect.topleft[0], uav_rect.topleft[1]))

    def grow_tree(self, main_surface):
        # for i in range(10000):
        p_new = self.sample_point()
        print(self.find_nearest(p_new))
        if self.find_nearest(p_new):
            self.vertices.append(self.sample_point())

        if len(self.vertices) > 2:
            for p in self.vertices:
                pygame.draw.circle(main_surface, 'Cyan', p, 10, 4)
        # target_rect = pygame.draw.circle(main_surface, 'Yellow', target_point,10,4)

    def sample_point(self):
        while True:
            x = int(random.uniform(0, self.screen_w))
            y = int(random.uniform(0, self.screen_h))
            collision = False
            for obs in self.obstacle_list:
                if obs.collidepoint((x,y)): 
                    collision = True
                    break
            if not collision: return (x,y)

    def find_nearest(self, p1):
        for p2 in self.vertices:
            d = self.distance(p1, p2)
            if d < self.node_length:
                print(d)
                return 1
        return 0
    
    def distance(self, p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]

        return np.sqrt(dx**2 + dy**2)


def create_vertex(screen_w, screen_h, obstacle_list):
    vertex_ok = False
    while not vertex_ok:
        vertex = (randint(0, screen_w), randint(0, screen_h))
        for obs in obstacle_list:
            if not obs.collidepoint(vertex):
                return vertex

def create_obstacle(screen_w, screen_h, obstacle_side):
    topleft = (int(random.uniform(0, screen_w - obstacle_side)), int(random.uniform(0, screen_h - obstacle_side)))
    obstacle = pygame.Rect(topleft, (obstacle_side, obstacle_side))
    return obstacle

def deploy_uav(screen_w, screen_h, obstacle_list, uav_side):
    while True:
        topleft = (int(random.uniform(0, screen_w - obstacle_side)), int(random.uniform(0, screen_h - obstacle_side)))
        uav_rect = pygame.Rect(topleft, (uav_side, uav_side))
        if not uav_rect.collidelistall(obstacle_list):
            return uav_rect

def UAV_steps_to_target(uav_rect, target_point):
    x0 = uav_rect.topleft[0]
    y0 = uav_rect.topleft[1]

    dx = target_point[0] - x0
    dy = target_point[1] - y0

    distance = np.sqrt(dx**2 + dy**2)
    # cos_x = np.cos(distance/dx)
    # cos_y = np.sin(distance/dy)
    cos_ = dx/distance
    sin_ = dy/distance

    uav_step_x = uav_step_size * cos_
    uav_step_y = uav_step_size * sin_

    uav_rect.x += uav_step_x
    uav_rect.y += uav_step_y
    # print((dx, dy, distance))
    # print((cos_, sin_))
    # print((uav_step_x,uav_step_y, np.sqrt(uav_step_x**2 + uav_step_y**2)))


def find_path_to_target(screen_w, screen_h, obstacle_list, uav_rect, target_p):
    pass