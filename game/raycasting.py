import pygame as pg
import math
from settings import *

class RayCasting:
    def __init__(self, game) -> None:
        self.game = game
        self.lines = []
        self.ray_distance = [0,0,0,0,0]
        self.ray_arr = []

    def ray_cast(self):
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
    
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        self.ray_distance = []
        self.ray_arr = []
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # horizontals
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            
            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a
            
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # verticals
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # depth
            if depth_vert < depth_hor:
                depth = depth_vert
            else:
                depth = depth_hor
            
            p1 = (x1, y1) = (100 * ox, 100 * oy)
            p2 = (x2, y2) = (100 * ox + 100 * depth * cos_a, 100 * oy + 100 * depth * sin_a)

            self.ray_arr.append([p1,p2])
            # draw for debug
            # pg.draw.line(self.game.screen, 'yellow', (x1, y1), (x2, y2))
            # if math.dist(p1,p2) < 500:
            #     pg.draw.circle(self.game.screen, 'red', p2, 5)

            ray_angle += DELTA_ANGLE
            self.ray_distance.append(math.dist(p1,p2))

    def update(self):
        self.ray_cast()

    def draw(self):
        for ray in self.ray_arr:

            p1 = (x1, y1) = ray[0]
            p2 = (x2, y2) = ray[1]
            pg.draw.line(self.game.screen, 'yellow', (x1, y1), (x2, y2))

            if math.dist(p1,p2) < 500:
                pg.draw.circle(self.game.screen, 'red', p2, 5)

    @property
    def r_d(self):
        return self.ray_distance