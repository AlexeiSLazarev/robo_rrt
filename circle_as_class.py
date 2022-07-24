import pygame
pygame.init()

#Colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

display_width, display_height = 800, 600
screen = pygame.display.set_mode((display_width, display_height))
screen.fill(white)

class Player():
    def __init__(self):
        self.player_surface = screen
        self.player_color = green
        self.player_radius = 25        
        self.player_pos = (int(display_height - self.player_radius * 3), int(display_width/2))
        self.player_width = 0

    def character(self):
        self.player_character = pygame.draw.circle(self.player_surface, self.player_color, self.player_pos, self.player_radius, self.player_width)

#Player Reference
player = Player()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
    #Background
    screen.fill(white)

    #Draw everything in order, each drawn object will be drawn beneath the next drawn object.

    # Draw the player -----------------------------
    player.character()
    # Draw the player -----------------------------

    #Update
    pygame.display.update()