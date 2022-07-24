import random
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

def create_vertex(screen_w, screen_h, obstacle_list):
    vertex_ok = False
    while not vertex_ok:
        vertex = (randint(0, screen_w), randint(0, screen_h))
        for obs in obstacle_list:
            if not obs.collidepoint(vertex):
                return vertex

def create_obstalce(screen_w, screen_h, obstacle_side):
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

def create_path_to_target(screen_w, screen_h, obstacle_list):
    pass