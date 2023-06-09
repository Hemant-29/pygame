import math
from sys import exit
import pygame
from building import Building
from pavement import Pavement

# Setting up pygame
WIDTH, HEIGHT = 1.777777 * 900, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spiderman")

# Defining colours
WHITE = (255, 255, 255)
RED = (255, 0, 0, 0)

# Defining constant variables
FPS = 30
VEL = 24
CAMERA_POSITION = [0, 0]


class Player:
    """generates a playable character into the game"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.jump = False  # checks if w key is pressed
        self.direction = "right"  # current direction of character
        self.border_collide_L = True
        self.border_collide_R = False
        self.animation_frame = 1  # Current frame of the animation playback
        self.animation = "idle"
        self.animation_list = [None, None, None]
        self.is_swinging = False
        self.rope_length = 600
        self.swing_end = False

        # defining player
        self.player = pygame.image.load(
            f"./assets/idle/{self.animation_frame}.png")
        self.width = self.player.get_size()[0]
        self.height = self.player.get_size()[1]

    def draw_player(self):
        """Draw the player sprite onto the screen"""
        if self.direction != "right":
            WIN.blit(pygame.transform.flip(self.player, True, False),
                     (self.x, self.y))  # draws the character
        else:
            WIN.blit(self.player, (self.x, self.y))

    def player_animations(self):
        """Adds animations to the player"""

        #  For 'running_jump' animation
        if self.animation == "running_jump":
            max_frame = 30
            if self.animation_frame >= max_frame + 1:
                self.jump = False
                self.animation_frame = 1
            self.player = pygame.image.load(
                f"./assets/running_jump/{self.animation_frame}.png").convert_alpha()
            self.animation_frame += 1

        # For 'jump' animation
        elif self.jump and self.animation != "running jump" and self.animation != "swing":
            CAMERA_POSITION[1] -= 25
            try:
                max_frame = 21
                self.player = pygame.image.load(
                    f"./assets/standing_jump(full)/{self.animation_frame}.png").convert_alpha()
                self.animation_frame += 1
                if self.animation_frame >= max_frame:
                    self.jump = False
                    self.animation = "idle"
            except FileNotFoundError:
                self.animation_frame = 1

        #  For 'idle' animation
        elif self.animation == "idle":
            max_frame = 15
            if self.animation_frame >= max_frame + 1:
                self.animation_frame = 1
            self.player = pygame.image.load(
                f"./assets/idle/{self.animation_frame}.png").convert_alpha()
            self.animation_frame += 1

        #  For 'sit' animation
        elif self.animation == "sit":
            max_frame = 1
            self.player = pygame.image.load(
                "./assets/sit/sit.png").convert_alpha()

        #  For 'walk' animation
        elif self.animation == "walk":
            max_frame = 16
            if self.animation_frame >= max_frame + 1:
                self.animation_frame = 1
            self.player = pygame.image.load(
                f"./assets/walk/{self.animation_frame}.png").convert_alpha()
            self.animation_frame += 1

        #  For 'run' animation
        elif self.animation == "run":
            max_frame = 16
            if self.animation_frame >= max_frame + 1:
                self.animation_frame = 1
            self.player = pygame.image.load(
                f"./assets/run/{self.animation_frame}.png").convert_alpha()
            self.animation_frame += 1

        #  For 'swing' animation
        elif self.animation == "swing":
            max_frame = 52
            self.jump = False
            if CAMERA_POSITION[1] > -80:
                self.animation = "idle"
            if self.animation_frame >= max_frame + 1:
                self.animation_frame = 52
            self.player = pygame.image.load(
                f"./assets/swing/{self.animation_frame}.png").convert_alpha()
            self.animation_frame += 1

    def animation_sequence(self, animation):
        """generates a list of last 3 animations played

        Args:
            animation (string): current playing animation

        Returns:
            list
        """
        if self.animation_list[-1] != animation:
            for i in range(1, 3):
                if self.animation_list[i - 1] != self.animation_list[i]:
                    self.animation_list[i - 1] = self.animation_list[i]
            self.animation_list[-1] = animation
        return self.animation_list

    def player_movements(self, keys_pressed, key_up=None):
        """Adds movements to the player sprite

        Args:
            keys_pressed (pygame_function): tells which key is pressed
        """
        if self.animation_list[-1] == ("swing" or "swing_jump" or "swing_land"):
            keys_pressed = None  # No key press logic during swing

        self.key_up = key_up
        if self.key_up == "w":
            self.jump = True  # Jump variable turns True when w is released
            self.animation_frame = 1
        if keys_pressed is None:
            if self.animation != "swing":
                self.animation = "idle"  # No key pressed logic
            return

        if self.x <= 100:
            self.border_collide_L = True
        if keys_pressed[pygame.K_d] and self.x > 100 and not keys_pressed[pygame.K_a]:
            self.x -= VEL  # RIGHT
            self.direction = "right"
            self.border_collide_L = False
        elif keys_pressed[pygame.K_d] and not keys_pressed[pygame.K_a] and CAMERA_POSITION[1] >= -20:
            self.animation = "walk"
            CAMERA_POSITION[0] += VEL

        if self.x >= WIDTH - self.width - 200:
            self.border_collide_R = True
        if keys_pressed[pygame.K_a] and self.x < WIDTH - self.width - 200:
            self.x += VEL  # LEFT
            self.direction = "left"
            self.border_collide_R = False
        elif keys_pressed[pygame.K_a] and not keys_pressed[pygame.K_d] and CAMERA_POSITION[1] >= -20:
            self.animation = "walk"
            CAMERA_POSITION[0] -= VEL

        if (keys_pressed[pygame.K_d] and not keys_pressed[pygame.K_a] and keys_pressed[pygame.K_LSHIFT] and not self.jump):
            if not self.jump:
                self.animation = "run"
            CAMERA_POSITION[0] += VEL * 2
        elif (keys_pressed[pygame.K_a] and not keys_pressed[pygame.K_d] and keys_pressed[pygame.K_LSHIFT] and not self.jump):
            if not self.jump:
                self.animation = "run"
            CAMERA_POSITION[0] -= VEL * 2

        if (keys_pressed[pygame.K_d] and not keys_pressed[pygame.K_a] and keys_pressed[pygame.K_LSHIFT] and self.jump):
            self.animation = "running_jump"
            CAMERA_POSITION[0] += VEL * 2
        elif (keys_pressed[pygame.K_a] and not keys_pressed[pygame.K_d] and keys_pressed[pygame.K_LSHIFT] and self.jump):
            self.animation = "running_jump"
            CAMERA_POSITION[0] -= VEL * 2

        if keys_pressed[pygame.K_s] and self.y < 0:
            self.y += VEL  # DOWN

        if (keys_pressed[pygame.K_w] and keys_pressed[pygame.K_d] is False and keys_pressed[pygame.K_a] is False):
            self.animation = "sit"

        if keys_pressed[pygame.K_a] and keys_pressed[pygame.K_d]:
            self.animation = "idle"

            # conditions for border collision
        if self.border_collide_L is False and self.direction == "right":
            CAMERA_POSITION[0] += VEL * 20
            self.x -= VEL * 20
        if self.border_collide_R is False and self.direction == "left":
            CAMERA_POSITION[0] -= VEL * 20
            self.x += VEL * 20

    def draw_collison_bounds(self, show=False):
        """draws collision bounds around the character

        Args:
            show (bool, optional): collision bounds become visible during gameplay if True.
            Defaults to False.
        """

        cb_jump = [200, 250, -380, -600]
        cb_idle = [200, 350, -380, -560]
        cb_walk = [200, 340, -380, -560]
        cb_sit = [200, 470, -380, -680]
        cb_run = [140, 360, -320, -580]
        cb_running_jump = [240, 200, -340, -600]
        cb_swing = [100, 280, -200, -700]

        animation_cb_pairs = {"idle": cb_idle, "walk": cb_walk, "sit": cb_sit,
                              "run": cb_run, "running_jump": cb_running_jump, "swing": cb_swing}

        if self.jump:
            active = cb_jump
        else:
            active = animation_cb_pairs[self.animation]

        x_fac, y_fac, width_fac, height_fac = active[0], active[1], active[2], active[3]
        object_collision_bound = pygame.Rect(
            self.x + x_fac, self.y + y_fac, self.width + width_fac, self.height + height_fac)

        if show:
            try:
                return pygame.draw.rect(WIN, (255, 0, 0), object_collision_bound)
            except UnboundLocalError:
                None

    def swing(self, camera, depth_fac):
        self.animation = "swing"
        if self.direction == "right":
            # Defining constants for a single swing
            swing_pivot = {'x': camera[0] +
                           (self.rope_length*depth_fac), 'y': camera[1] - self.rope_length}
            center = {'x': (swing_pivot['x']+camera[0])/2,
                      'y': (swing_pivot['y']+camera[1])/2}
            radius = math.sqrt((swing_pivot['x']-camera[0])**2
                               + (swing_pivot['y']-camera[1])**2)/2
            x_max = {'x': center["x"]+radius, 'y': center["y"]}

            if CAMERA_POSITION[0] >= x_max["x"]+300:
                self.swing_end = True

            # Moving player along the X axis
            if CAMERA_POSITION[0] < x_max['x']:
                CAMERA_POSITION[0] += 50
                if CAMERA_POSITION[0] >= x_max["x"]:
                    CAMERA_POSITION[0] = x_max["x"]
                # Moving player along Y axis according to eqation of circle
                CAMERA_POSITION[1] = center["y"] + \
                    math.sqrt(
                        abs(radius**2-(CAMERA_POSITION[0]-center["x"])**2))

            elif CAMERA_POSITION[0] >= x_max['x'] and CAMERA_POSITION[0] < x_max["x"]+300:
                CAMERA_POSITION[0] += 26
                CAMERA_POSITION[1] -= 25

        else:
            # Defining constants for a single swing
            swing_pivot = {'x': camera[0] -
                           (self.rope_length*1.4), 'y': camera[1] - self.rope_length}
            center = {'x': (swing_pivot['x']+camera[0])/2,
                      'y': (swing_pivot['y']+camera[1])/2}
            radius = math.sqrt((swing_pivot['x']-camera[0])**2
                               + (swing_pivot['y']-camera[1])**2)/2
            x_max = {'x': center["x"]-radius, 'y': center["y"]}

            if CAMERA_POSITION[0] <= x_max["x"]-300:
                self.swing_end = True

            # Moving player along the X axis
            if CAMERA_POSITION[0] > x_max['x']:
                CAMERA_POSITION[0] -= 50
                if CAMERA_POSITION[0] <= x_max["x"]:
                    CAMERA_POSITION[0] = x_max["x"]
                # Moving player along Y axis according to eqation of circle
                CAMERA_POSITION[1] = center["y"] + \
                    math.sqrt(
                        abs(radius**2-(CAMERA_POSITION[0]-center["x"])**2))

            elif CAMERA_POSITION[0] <= x_max['x'] and CAMERA_POSITION[0] > x_max["x"]-300:
                CAMERA_POSITION[0] -= 26
                CAMERA_POSITION[1] -= 25


#  Defining drawable objects
spiderman = Player(100, 100)
pavement = Pavement()
building1 = Building("5(1).png", 0, -1680)
building2 = Building("6(1).png", 2800, -1620)
building3 = Building("7(1).png", 5000, -800)
building4 = Building("8(8).png", -5500, -2920)


def draw_objects(keys_pressed, key_up):
    """Draw all the visible objects onto the screen"""

    # Draws pavement and adjust speed according to player's action
    if (spiderman.is_swinging is True or spiderman.animation == "run" or spiderman.animation == "running_jump"):
        pavement.draw(4, 0, -CAMERA_POSITION[1])
    elif spiderman.animation == "walk" and CAMERA_POSITION[1] >= -20:
        pavement.draw(2, 0, -CAMERA_POSITION[1])
    else:
        pavement.draw(0, 0, -CAMERA_POSITION[1])

    # Draws various buildings
    building1.draw(WIN, CAMERA_POSITION)
    building1.collision_bound(CAMERA_POSITION, 120, 20, 2760, 2310)
    building2.draw(WIN, CAMERA_POSITION)
    building2.collision_bound(CAMERA_POSITION, 186, 7, 1980, 2260)
    building3.draw(WIN, CAMERA_POSITION)
    building3.collision_bound(CAMERA_POSITION, 180, 12, 2030, 1428)
    building4.draw(WIN, CAMERA_POSITION)
    building4.collision_bound(CAMERA_POSITION, 343, 395, 4672, 3175)

    #  Draws spiderman character
    spiderman.draw_collison_bounds()
    spiderman.draw_player()
    spiderman.player_animations()
    spiderman.player_movements(keys_pressed, key_up)


def main():

    clock = pygame.time.Clock()
    keys_used = [pygame.K_w, pygame.K_a,
                 pygame.K_s, pygame.K_d, pygame.K_SPACE]
    gravity = 0  # Not the force but SPEED with which objects will fall

    # Shows the position of camera when a certain key was pressed
    camera_temp = [0, 0]

    # GAME MAIN LOOP #
    while True:
        spiderman.animation_sequence(spiderman.animation)
        key_up = None  # Contains keys which are released
        clock.tick(FPS)
        WIN.fill(WHITE)
        temp_cam_pos = CAMERA_POSITION[0]
        keys_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():  # takes all the keyboard and mouse events
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:  # Button tapped
                if event.key == pygame.K_SPACE:
                    if CAMERA_POSITION[1] <= -80:
                        spiderman.animation_frame = 10
                    camera_temp = CAMERA_POSITION[:]
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

            if event.type == pygame.KEYUP:  # Button released
                if event.key == pygame.K_w:
                    key_up = "w"
                if event.key == pygame.K_SPACE:
                    spiderman.is_swinging = False
                    spiderman.swing_end = False
                    gravity = 0

        # Sets keys_pressed = None when no key is pressed
        for i in keys_used:
            if pygame.key.get_pressed()[i] is False:
                keys_pressed = None
            else:
                keys_pressed = pygame.key.get_pressed()
                break

        #  Draw all the visible objects onto the screen
        draw_objects(keys_pressed, key_up)

        # Implimentation of CAMERA BOUNDARIES
        if CAMERA_POSITION[0] <= -5500:
            pavement.movements(None, 0)
            CAMERA_POSITION[0] = -5500+1
            spiderman.animation = "idle"
        elif CAMERA_POSITION[0] >= 6000:
            pavement.movements(None, 0)
            CAMERA_POSITION[0] = 6000-1
            spiderman.animation = "idle"

        # Implimentation of GRAVITY
        if CAMERA_POSITION[1] <= 0:
            CAMERA_POSITION[1] += gravity
            gravity += 4  # <-- This number indicates the intensity of force
        elif CAMERA_POSITION[1] > 0:
            gravity = 0

        # Space key pressed

        if keys_pressed is not None and keys_pressed[pygame.K_SPACE]:
            if spiderman.swing_end is False:
                if CAMERA_POSITION[1] <= -80 or spiderman.is_swinging is True:
                    gravity = 0
                    spiderman.is_swinging = True
                    spiderman.swing(camera_temp, 1.4)

        if CAMERA_POSITION[1] > -200:
            spiderman.rope_length = 600
        elif CAMERA_POSITION[1] <= -200 and spiderman.is_swinging is False:
            spiderman.rope_length = 1000

        # Checks if the camera has moved in any direction
        if CAMERA_POSITION[0] < temp_cam_pos:
            pavement.movements(keys_pressed, -1)
        elif CAMERA_POSITION[0] > temp_cam_pos:
            pavement.movements(keys_pressed, +1)
        else:
            pavement.movements(keys_pressed, 0)
        pygame.display.update()


# calling the main function
if __name__ == "__main__":
    main()
