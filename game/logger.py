from settings import *
import math

class Logger:
    def __init__(self, game) -> None:
        self.game = game
    
    def log_step(self):
        # print(self.game.player.pos) 
        # print(self.game.player.angle) 
        # print(self.game.player.d2t)
        print(self.game.raycasting.r_d)
        # print(self.game.player.exit_found)