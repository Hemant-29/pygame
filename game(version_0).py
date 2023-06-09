import pygame
import os
from sys import exit
from building import Building

# Setting up pygame
WIDTH, HEIGHT = 1920, 1080  # resolution of screen
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # setting up a window
pygame.display.set_caption("Web Adventures")

# Defining colours
WHITE = (255, 255, 255)
BLUE = (190, 230, 255)
RED = (255, 0, 0, 0)
# Defining constant variables
FPS = 30
VEL = 20  # velocity of spiderman movement
# Defining variables
jump = False  # checks if w key is pressed
direction = "right"  # current direction of character
border_collide_L = True
border_collide_R = False
spiderman_image_count = 1  # current image to be loaded
animation = "idle"  # current animation
camera_position = [0, 0]

# Loading-in images
SPIDERMAN = pygame.image.load(
    f"./assets/idle/{spiderman_image_count}.png")
SPIDERMAN_WIDTH, SPIDERMAN_HEIGHT = SPIDERMAN.get_size()[
    0], SPIDERMAN.get_size()[1]
# ROAD = pygame.image.load(os.path.join("assets", "road.png")).convert_alpha()
SIDEWALK = pygame.image.load(os.path.join(
    "assets/buildings", "sidewalk.jpg")).convert_alpha()


# Creating masks
SPIDERMAN_MASK = pygame.mask.from_surface(SPIDERMAN)


def draw_collison_bounds(object_position, x_fac, y_fac, width_fac, height_fac):
    object_collision_bound = pygame.Rect(
        object_position.x+x_fac, object_position.y+y_fac, object_position.width+width_fac, object_position.height+height_fac)
    return pygame.draw.rect(WIN, (255, 0, 0), object_collision_bound)


def draw_spiderman(spiderman_position):
    global direction
    if direction != "right":
        WIN.blit(pygame.transform.flip(SPIDERMAN, True, False),
                 (spiderman_position.x, spiderman_position.y))  # draws the character
    else:
        WIN.blit(SPIDERMAN, (spiderman_position.x, spiderman_position.y))


def draw_window(animation, spiderman_position, road_position):
    """print different sprites on the screen

    Args:
        keys_pressed (function): tells which key is pressed
        spiderman_position (function): tells the position and size of the spiderman sprite
        road_position (function): tells the position and sizr of the road sprite
    """
    WIN.fill(WHITE)
    if direction != "right":
        WIN.blit(pygame.transform.flip(SIDEWALK, True, False),
                 (road_position.x, road_position.y))  # draws the character
    else:
        WIN.blit(SIDEWALK, (road_position.x, road_position.y))
    # WIN.blit(ROAD, (road_position.x, road_position.y))  # draws the road

    # collision bounds for spiderman
    if jump:
        draw_collison_bounds(spiderman_position, 190, 250, -350, -600)
    elif animation == "idle":
        draw_collison_bounds(spiderman_position, 210, 350, -410, -560)
    elif animation == "walk":
        draw_collison_bounds(spiderman_position, 200, 340, -400, -560)
    elif animation == "run":
        draw_collison_bounds(spiderman_position, 180, 340, -370, -560)
    elif animation == "sit":
        draw_collison_bounds(spiderman_position, 190, 470, -370, -680)


def load_spiderman_animation(animation):
    global jump, SPIDERMAN, spiderman_image_count
    if jump:
        if animation == "running_jump":
            max_frame = 30
            if spiderman_image_count >= max_frame+1:
                jump = False
                spiderman_image_count = 1
            SPIDERMAN = pygame.image.load(
                f"./assets/running_jump/{spiderman_image_count}.png").convert_alpha()
            spiderman_image_count += 1
        else:
            max_frame = 21
            SPIDERMAN = pygame.image.load(
                f"./assets/standing_jump(full)/{spiderman_image_count}.png").convert_alpha()
            spiderman_image_count += 1
            if spiderman_image_count >= max_frame:
                jump = False
    elif animation == "idle":
        max_frame = 15
        if spiderman_image_count >= max_frame+1:
            spiderman_image_count = 1
        SPIDERMAN = pygame.image.load(
            f"./assets/idle/{spiderman_image_count}.png").convert_alpha()
        spiderman_image_count += 1

    elif animation == "sit":
        max_frame = 1
        SPIDERMAN = pygame.image.load(
            f"./assets/sit/sit.png").convert_alpha()
    elif animation == "walk":
        max_frame = 16
        if spiderman_image_count >= max_frame+1:
            spiderman_image_count = 1
        SPIDERMAN = pygame.image.load(
            f"./assets/walk/{spiderman_image_count}.png").convert_alpha()
        spiderman_image_count += 1
    elif animation == "run":
        max_frame = 16
        if spiderman_image_count >= max_frame+1:
            spiderman_image_count = 1
        SPIDERMAN = pygame.image.load(
            f"./assets/run/{spiderman_image_count}.png").convert_alpha()
        spiderman_image_count += 1


def spiderman_movement(keys_pressed, spiderman_position):
    global jump, direction, animation, border_collide_L, border_collide_R

    if spiderman_position.x <= 100:
        border_collide_L = True
    if keys_pressed[pygame.K_d] and spiderman_position.x > 100 and not keys_pressed[pygame.K_a]:
        spiderman_position.x -= VEL  # RIGHT
        direction = "right"
        border_collide_L = False
    elif keys_pressed[pygame.K_d] and not keys_pressed[pygame.K_a]:
        animation = "walk"
        camera_position[0] += 40

    if spiderman_position.x >= WIDTH-spiderman_position.width-200:
        border_collide_R = True

    if keys_pressed[pygame.K_a] and spiderman_position.x < WIDTH-spiderman_position.width-200:
        spiderman_position.x += VEL  # LEFT
        direction = "left"
        border_collide_R = False
    elif keys_pressed[pygame.K_a]:
        animation = "walk"
        camera_position[0] -= 40

    if keys_pressed[pygame.K_d] and keys_pressed[pygame.K_LSHIFT] and jump:
        animation = "running_jump"
    elif keys_pressed[pygame.K_a] and keys_pressed[pygame.K_LSHIFT] and jump:
        animation = "running_jump"
    elif keys_pressed[pygame.K_c]:
        animation = "running_jump"

    if keys_pressed[pygame.K_s] and spiderman_position.y < 0:
        spiderman_position.y += VEL  # DOWN

    if keys_pressed[pygame.K_w] and keys_pressed[pygame.K_d] == False and keys_pressed[pygame.K_a] == False:
        animation = "sit"

    if keys_pressed[pygame.K_a] and keys_pressed[pygame.K_d]:
        animation = "idle"


def road_movement(keys_pressed, road_position):
    global animation
    if keys_pressed[pygame.K_d] and keys_pressed[pygame.K_LSHIFT]:
        if not jump:
            road_position.x -= VEL*2
            animation = "run"
        else:
            road_position.x -= VEL*2
    elif keys_pressed[pygame.K_d]:
        road_position.x -= VEL
    if keys_pressed[pygame.K_a] and keys_pressed[pygame.K_LSHIFT]:
        if not jump:
            road_position.x += VEL*2
            animation = "run"
        else:
            road_position.x += VEL*2
    elif keys_pressed[pygame.K_a]:
        road_position.x += VEL


def cam_collision(spiderman_position, road_position):
    global border_collide_R, border_collide_L
    if border_collide_L == False and direction == "right":
        road_position.x -= VEL*20
        spiderman_position.x -= VEL*20
    if border_collide_R == False and direction == "left":
        road_position.x += VEL*20
        spiderman_position.x += VEL*20


def check_collision(player_mask, object_mask, player_position, object_position):
    if player_mask.overlap(object_mask, (object_position.x-player_position.x, object_position.y-player_position.y)):
        player_position.x -= 50


def main():
    """main loop of the game
    """
    global jump, animation, spiderman_image_count

    building1 = Building("4(1).png", -400, -1400)
    building2 = Building("6.png", 2500, -1900)
    building3 = Building("5(1).png", 5000, -3000)
    spiderman_position = pygame.Rect(
        0, 100, SPIDERMAN_HEIGHT, SPIDERMAN_WIDTH)
    road_position = pygame.Rect(0, 0, HEIGHT, WIDTH)
    clock = pygame.time.Clock()
    key_up = None
    gravity = 0
    while True:
        print(animation)
        load_spiderman_animation(animation)
        if spiderman_position.y < 100:
            spiderman_position.y += gravity
            gravity += 3
        else:
            gravity = 0           # implementation of gravity
        clock.tick(FPS)

        for event in pygame.event.get():
            keys_pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT:  # QUIT event handle
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:  # UP released
                if event.key == pygame.K_w and keys_pressed[pygame.K_d] == False and keys_pressed[pygame.K_a] == False and keys_pressed[pygame.K_LSHIFT] == False:
                    jump = True
                    animation = "jump"
                    spiderman_image_count = 1
                elif event.key == pygame.K_w:
                    key_up = "w"
                    jump = True
                    spiderman_image_count = 1
                if event.key == pygame.K_SPACE:
                    key_up = "space"

            if event.type != pygame.KEYDOWN or jump:
                animation = "idle"

        if key_up == "space":
            if spiderman_position.y > -200:
                spiderman_position.y -= 100
            else:
                key_up = None

        draw_window(animation, spiderman_position,
                    road_position)
        building1.draw(WIN, camera_position)  # , 910, 670, 1985, 1450)
        building1.movements(keys_pressed)
        # building1.cam_collision(border_collide_L, border_collide_R, direction)
        building2.draw(WIN, camera_position)  # , 600, 860, 2600, 4220)
        building2.movements(keys_pressed)
        # building2.cam_collision(border_collide_L, border_collide_R, direction)
        building3.draw(WIN, camera_position)  # , 910, 670, 1985, 1450)
        building3.movements(keys_pressed)
        # building3.cam_collision(border_collide_L, border_collide_R, direction)
        draw_spiderman(spiderman_position)
        spiderman_movement(keys_pressed, spiderman_position)
        road_movement(keys_pressed, road_position)
        cam_collision(spiderman_position, road_position)
        pygame.display.update()


if __name__ == "__main__":
    main()
