from cmath import tau
from settings import *
import pygame as pg
import math

class Target:
    def __init__(self, game) -> None:
        self.game = game
        self.x, self.y = TARGET_POS

    def draw(self):
        pg.draw.circle(self.game.screen, 'white', (self.x * 100, self.y * 100), 45)

    @property
    def map_pos(self):
        return int(self.x),int(self.y)