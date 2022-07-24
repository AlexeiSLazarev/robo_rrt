
from my_rrt_utils import *

# Run screen - OK
# Draw random points - OK
# Draw obstacles - OK
# Draw UAV - OK
# Move UAV to the point pointed by mouse - OK
# Make list of arriving points by mouse
# Implement RRT for path findings
# Add fog of war
# Add lines (known vs unknown)
# Add approaching to the lines
# Add multiple UAV

pygame.init()

# Prepare main window
main_surface = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption(CAPTION)
clock = pygame.time.Clock()

# Create obstacles
obstacles_num = 20
obstacle_list = []
for i in range(obstacles_num):
    obstacle_list.append(create_obstalce(screen_w, screen_h, obstacle_side))

# Vertex array
vertex_array = []

# Create UAV
uav_rect = deploy_uav(screen_w, screen_h, obstacle_list, uav_side)
flag_moving = False
target_point = None

while True:
    main_surface.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            # uav_rect.right = event.pos[0]
            # new_x = event.pos[0] - uav_rect.left
            # new_y = event.pos[1] - uav_rect.top
            target_point = (event.pos[0], event.pos[1])

            # print(event.pos)

    # Draw obstacles
    for obs in obstacle_list:
        pygame.draw.rect(main_surface, 'Green', obs)

    # Draw Target point
    if target_point:
        target_rect = pygame.draw.circle(main_surface, 'Yellow', target_point,10,4)

    
    # Move UAV to a target point
    if target_point:
        UAV_steps_to_target(uav_rect, target_point)

    # Collision with obstacle
    if uav_rect.collidelistall(obstacle_list):
        target_point = None

    # Arriving to target point
    if target_point:
        if target_rect.colliderect(uav_rect): 
            target_point = None
            print('Arrived')

    # Draw path line
    if target_point:
        pygame.draw.line(main_surface, 'Yellow', uav_rect.topleft, target_point,4)

    pygame.draw.rect(main_surface, 'White', uav_rect)


    pygame.display.update()
    clock.tick(10)
    




