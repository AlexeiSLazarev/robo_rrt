from ast import Return
from curses import KEY_UP
import math
import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        player_walk1 = pygame.image.load('pixel_runner/graphics/Player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('pixel_runner/graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load('pixel_runner/graphics/Player/jump.png').convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('pixel_runner/audio/jump.mp3')
        self.jump_sound.set_volume(0.1)

    def player_input(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity -= 20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            self.gravity = 0
    
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index > len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    
    def update(self) -> None:
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        print(self.gravity)
        
class Obstacle(pygame.sprite.Sprite):

    def __init__(self, type) -> None:
        super().__init__()
        
        if type == 'fly':
            frame1 = pygame.image.load('pixel_runner/graphics/Fly/Fly1.png').convert_alpha()
            frame2 = pygame.image.load('pixel_runner/graphics/Fly/Fly2.png').convert_alpha()
            y_pos = 210
        else: 
            frame1 = pygame.image.load('pixel_runner/graphics/snail/snail1.png').convert_alpha()
            frame2 = pygame.image.load('pixel_runner/graphics/snail/snail2.png').convert_alpha()
            y_pos = 300

        self.frames = [frame1, frame2]
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))
    
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill() 

def display_score():
    current_time = pygame.time.get_ticks() -start_time
    score_surf = test_font.render(f'{current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True
# def obstacle_movement(obstacle_list):
#     global fly_surface, snail_surface
#     if obstacle_list:
#         for obstacle_rect in obstacle_list:
#             obstacle_rect.x -= 5
#             if obstacle_rect.bottom == 210: screen.blit(fly_surface, obstacle_rect)
#             else: screen.blit(snail_surface, obstacle_rect)
        
#         obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > 0]
#         # print(len(obstacle_list))
#     return obstacle_list

# def collision(player_rect, obstacle_list):
#     if obstacle_list:
#         for obstacle_rect in obstacle_list:
#             if player_rect.colliderect(obstacle_rect): return False
#     return True

# def player_animation():
#     global player_index, player_surface
#     if player_rect.bottom < 300:
#         player_surface = player_jump
#     else:
#         player_index += 0.1
#         player_surface = player_walk[int(player_index)]
#         if player_index > 1.2: player_index = 0

        # print(player_index)

    # play animation if player is on the floor
    # play jump surface if is not


pygame.init()
start_time = pygame.time.get_ticks()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Hello pygame")
clock = pygame.time.Clock()
test_font = pygame.font.Font('pixel_runner/font/Pixeltype.ttf', 50)
bg_music = pygame.mixer.Sound('pixel_runner/audio/music.wav')
bg_music.set_volume(0.05)

# test_surface =pygame.Surface((100,200))
# test_surface.fill('Red')
sky_surface = pygame.image.load('pixel_runner/graphics/Sky.png').convert()
ground_surface = pygame.image.load('pixel_runner/graphics/ground.png').convert()
text_surface = test_font.render('My Game', False, 'Black') # AA - Anti Aliasing
text_rect = text_surface.get_rect(topleft = (300,50))

# Obstacles 
# Snail
# snail_frame1 = pygame.image.load('pixel_runner/graphics/snail/snail1.png').convert_alpha()
# snail_frame2 = pygame.image.load('pixel_runner/graphics/snail/snail2.png').convert_alpha()
# snail_frames = [snail_frame1, snail_frame2]
# snail_frame_index = 0
# snail_surface = snail_frames[snail_frame_index]

# Fly
# fly_frame1 = pygame.image.load('pixel_runner/graphics/Fly/Fly1.png').convert_alpha()
# fly_frame2 = pygame.image.load('pixel_runner/graphics/Fly/Fly2.png').convert_alpha()
# fly_frames = [fly_frame1, fly_frame2]
# fly_frame_index = 0
# fly_surface = fly_frames[fly_frame_index]

# obstacle_rect_list = []

# player_walk1 = pygame.image.load('pixel_runner/graphics/Player/player_walk_1.png').convert_alpha()
# player_walk2 = pygame.image.load('pixel_runner/graphics/Player/player_walk_2.png').convert_alpha()
# player_walk = [player_walk1, player_walk2]
# player_index = 0
# player_jump = pygame.image.load('pixel_runner/graphics/Player/jump.png').convert_alpha()
# player_surface = player_walk[player_index]
# player_rect = player_surface.get_rect(bottomleft = (80, 300))
# gravity = 0

game_active = False
score = 0

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()


# Intro screen
player_stand = pygame.image.load('pixel_runner/graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))
game_name = test_font.render('PixelRunner', False, (100,180, 200))
game_name_rect = game_name.get_rect(center = (400,75))
game_message = test_font.render('Press space to run...', False, (100,180, 200))
game_message_rect = game_message.get_rect(center = (400,335))


# Timers
obstacle_time = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_time, 1400)

snail_animation_time = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_time, 200)

fly_animation_time = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_time, 150)

bg_music.play()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        # if event.type == pygame.MOUSEMOTION:
        #     print(player_rect.collidepoint(event.pos))

        if event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_SPACE and game_active == True:
            #     if player_rect.bottom >= 300: 
            #         gravity -= 20
                # print("jump")
            if event.key == pygame.K_SPACE and game_active == False:
                start_time = pygame.time.get_ticks()
                game_active = True
        
        if event.type == obstacle_time and game_active == True:
            obstacle_group.add(Obstacle(choice(['fly','snail1', 'snail2'])))
            # if randint(0,2):
            #     obstacle_rect_list.append(snail_surface.get_rect(midbottom = (randint(900, 1100), 300)))
            # else:
            #     obstacle_rect_list.append(fly_surface.get_rect(midbottom = (randint(900, 1100), 210)))
            print("Obstacle")

    if game_active:
        
        # if event.type == fly_animation_time:
        #     if fly_frame_index == 0: 
        #         fly_frame_index = 1
        #     else:
        #         fly_frame_index = 0
        #     fly_surface = fly_frames[fly_frame_index]

        # if event.type == snail_animation_time:
        #     if snail_frame_index == 0: 
        #         snail_frame_index = 1
        #     else:
        #         snail_frame_index = 0
        #     snail_surface = snail_frames[snail_frame_index]

        screen.blit(sky_surface, (0,0)) # blit - block image transfer. mean you want to put on surface on another serface
        screen.blit(ground_surface, (0,300))
        # pygame.draw.rect(screen, (255,255,0),text_rect,6)
        # screen.blit(text_surface, (300,50))
        # pygame.draw.line(screen, 'Red', (0, 0), pygame.mouse.get_pos(), 10)
        score = display_score()
        # Player 
        # gravity += 1
        # player_rect.y += gravity
        # player_animation()
        # screen.blit(player_surface, player_rect)
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()

        # if player_rect.bottom >=  300: 
        #     player_rect.bottom = 300
        #     gravity = 0
        
        # Obstacle
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        # game_active = collision(player_rect, obstacle_rect_list)
        game_active = collision_sprite()

    else:

        # obstacle_rect_list = []
        # player_rect.bottom = 300
        # gravity = 0
        screen.fill((32, 64, 128))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)
        
        score_message = test_font.render(f'Your score is: {score}', False, (100,180, 200))
        score_message_rect = score_message.get_rect(center = (400,335))
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint(mouse_pos):
    #     print(pygame.mouse.get_pressed())


    pygame.display.update()
    clock.tick(60)

    '''
    draw ellipse from center
    m_pos = pygame.mouse.get_pos()
    x0 = 400
    y0 = 200
    x1 = m_pos[0]
    y1 = m_pos[1]
    x2 = 2*x0 - x1
    y2 = 2*y0 - y1
    w = (x1-x0) * 2
    h = (y1-y0) * 2
    pygame.draw.ellipse(screen,"Red", pygame.Rect(x2, y2, w, h), 5)
    '''
