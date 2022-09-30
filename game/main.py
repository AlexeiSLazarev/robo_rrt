import imp
from selectors import SelectorKey
import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from target import *
from logger import *
import os

class Environment:
    def __init__(self) -> None:
        if not RENDER:
            os.environ["SDL_VIDEODRIVER"] = "dummy"
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.new_env()

    def new_env(self):
        self.map = Map(self)
        self.player = Player(self)
        self.raycasting = RayCasting(self)
        self.target = Target(self)
        self.logger = Logger(self)

    def update(self):
        self.player.update()
        self.raycasting.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
        self.logger.log_step()
        self.check_end_game()

    def draw(self):
        self.screen.fill('Black')
        self.map.draw()
        self.player.draw()
        self.target.draw()
        self.raycasting.draw()
    
    def check_end_game(self):
        if self.player.exit_found:
            pg.quit()
            sys.exit()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Environment()
    game.run()