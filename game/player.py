from cmath import tau

from numpy import random
from settings import *
import pygame as pg
import math

class Player:
    def __init__(self, game) -> None:
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.exit_found = False
        self.distance_to_target = 100000

    def get_action(self):

        return (random.choice(['LEFT', 'RIGHT', 'FORWARD', 'BACKWARD']))

    def virtual_movement(self):
        ''' '''
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        # keys = pg.key.get_pressed()
        action = self.get_action()
    
        if action == 'FORWARD':
            dx += speed_cos
            dy += speed_sin
        if action == 'BACKWARD':
            dx += -speed_cos
            dy += -speed_sin

        self.check_wall_collision(dx, dy)
        # self.x += dx
        # self.y += dy

        if action == 'LEFT':
            self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        if action == 'RIGHT':
            self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        self.angle %= tau

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
    
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        # if keys[pg.K_a]:
        #     dx += speed_sin
        #     dy += -speed_cos
        # if keys[pg.K_d]:
        #     dx += -speed_sin
        #     dy += speed_cos

        self.check_wall_collision(dx, dy)
        # self.x += dx
        # self.y += dy

        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        self.angle %= tau
        self.check_exit()

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_exit(self):
        if  self.distance_to_target < 1:
            self.exit_found = True
        else:
            self.exit_found = False

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy)):
            self.y += dy

    def draw(self):
        # pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
        #                 (self.x * 100 + WIDTH * math.cos(self.angle),
        #                 self.y * 100 + WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def update(self):
        self.virtual_movement()
        # self.movement()
    
    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x),int(self.y)

    @property
    def d2t(self):
        '''Distance to target'''
        p1 = self.game.target.map_pos
        p2 = (int(self.x),int(self.y))
        d = math.dist(p1,p2)
        self.distance_to_target = d
        return d