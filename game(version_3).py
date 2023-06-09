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
RED = (255, 0, 0)
BLUE = (0, 100, 255)

# Defining constant variables
FPS = 30
VEL = 24


class Camera:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.temp_x = x
        # Indicates the position of camera when swing is initiated
        self.temp_pos = [0, 0]
        self.gravitational_vel = 0  # SPEED with which objects would fall

    def check_movement(self):
        """Checks if the camera has moved in any direction"""
        if CAMERA.x < self.temp_x:
            return -1
        elif CAMERA.x > self.temp_x:
            return 1
        else:
            return 0

    def set_boundary(self, start, end):
        """Set boundaries beyond which the camera cannot move

        Args:
            start (int): left boundary x-coordinates
            end (int): right boundary x-coordinates
        """
        if self.x <= start:
            # self.y = 0
            pavement.movements(None, 0)
            self.x = start+1
            spiderman.animation = "idle"
        elif self.x >= end:
            # self.y = 0
            pavement.movements(None, 0)
            self.x = end-1
            spiderman.animation = "idle"

    def set_gravity(self, acceleration):
        """Camera falls down under the influence of gravity

        Args:
            acceleration (int): gravitational acceleration
        """
        if self.y <= 0:
            self.y += self.gravitational_vel
            self.gravitational_vel += acceleration
        elif self.y > 0:
            self.gravitational_vel = 0

    def set_momentum(self):
        None


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
        # Just tap the key to play these animations
        self.one_tap_animations = [
            "swing", "land", "cross_punch", "punch_combo", "hook_punch"]
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
        elif self.jump and self.animation != "running_jump" and self.animation != "swing":
            CAMERA.y -= 25
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
                "./assets/sit/1.png").convert_alpha()

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
            max_frame = 74
            self.jump = False
            if CAMERA.y > -80:
                self.animation = "idle"
            if self.animation_frame >= max_frame + 1:
                self.animation_frame = max_frame
            self.player = pygame.image.load(
                f"./assets/swing/{self.animation_frame}.png").convert_alpha()
            self.animation_frame += 1

        #  For 'land' animation
        elif self.animation == "land":
            max_frame = 17
            self.jump = False
            if self.animation_frame >= max_frame + 1:
                self.animation_frame = max_frame
                self.animation = "idle"
            self.player = pygame.image.load(
                f"./assets/land/{self.animation_frame}.png").convert_alpha()
            self.animation_frame += 1

        #  For "cross_punch" animation
        elif self.animation == "cross_punch":
            max_frame = 22
            if self.animation_frame >= max_frame + 1:
                self.animation_frame = 1
                self.animation = "idle"
            self.player = pygame.image.load(
                f"./assets/cross_punch/{self.animation_frame}.png").convert_alpha()
            self.animation_frame += 1

        #  For "punch_combo" animation
        elif self.animation == "punch_combo":
            max_frame = 20
            if self.animation_frame >= max_frame + 1:
                self.animation_frame = 1
                self.animation = "idle"
            self.player = pygame.image.load(
                f"./assets/punch_combo/{self.animation_frame}.png").convert_alpha()
            self.animation_frame += 1

        #  For "hook_punch" animation
        elif self.animation == "hook_punch":
            max_frame = 17
            if self.animation_frame >= max_frame + 1:
                self.animation_frame = 1
                self.animation = "idle"
            self.player = pygame.image.load(
                f"./assets/hook_punch/{self.animation_frame}.png").convert_alpha()
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
        self.key_up = key_up
        if self.key_up == "w":
            self.jump = True  # Jump variable turns True when w is released
            self.animation_frame = 1

        # Animation = idle when no key pressed
        if keys_pressed is None:
            if self.animation not in self.one_tap_animations:
                self.animation = "idle"
            return

        if keys_pressed[pygame.K_d] and self.x > 100 and not keys_pressed[pygame.K_a]:
            self.x -= VEL  # RIGHT
            self.direction = "right"
            self.border_collide_L = False
        elif keys_pressed[pygame.K_d] and not keys_pressed[pygame.K_a] and CAMERA.y >= -20:
            self.animation = "walk"
            CAMERA.x += VEL

        if keys_pressed[pygame.K_a] and self.x < WIDTH - self.width - 200:
            self.x += VEL  # LEFT
            self.direction = "left"
            self.border_collide_R = False
        elif keys_pressed[pygame.K_a] and not keys_pressed[pygame.K_d] and CAMERA.y >= -20:
            self.animation = "walk"
            CAMERA.x -= VEL

        if (keys_pressed[pygame.K_d] and not keys_pressed[pygame.K_a] and keys_pressed[pygame.K_LSHIFT] and not self.jump):
            if not self.jump:
                self.animation = "run"
            CAMERA.x += VEL * 2
        elif (keys_pressed[pygame.K_a] and not keys_pressed[pygame.K_d] and keys_pressed[pygame.K_LSHIFT] and not self.jump):
            if not self.jump:
                self.animation = "run"
            CAMERA.x -= VEL * 2

        if (keys_pressed[pygame.K_d] and not keys_pressed[pygame.K_a] and keys_pressed[pygame.K_LSHIFT] and self.jump):
            self.animation = "running_jump"
            CAMERA.x += VEL * 2
        elif (keys_pressed[pygame.K_a] and not keys_pressed[pygame.K_d] and keys_pressed[pygame.K_LSHIFT] and self.jump):
            self.animation = "running_jump"
            CAMERA.x -= VEL * 2

        if keys_pressed[pygame.K_s] and self.y < 0:
            self.y += VEL  # DOWN

        if (keys_pressed[pygame.K_w] and keys_pressed[pygame.K_d] is False and keys_pressed[pygame.K_a] is False):
            self.animation = "sit"

        if keys_pressed[pygame.K_a] and keys_pressed[pygame.K_d]:
            self.animation = "idle"

    def player_settings(self, keys_pressed):
        """Miscellaneous player settings.
        Note - order of these settings is important
        """

        #  Implimentation of camera swing momentum
        if self.animation == "swing" and self.animation_frame > 45:
            if self.direction == "right":
                CAMERA.x += 30
            else:
                CAMERA.x -= 30

        # Initiate swing when SPACE key is pressed
        if keys_pressed is not None and keys_pressed[pygame.K_SPACE]:
            if spiderman.swing_end is False:
                if CAMERA.y <= -80 or spiderman.is_swinging is True:
                    CAMERA.gravitational_vel = 0
                    spiderman.is_swinging = True
                    if spiderman.rope_length == 600:
                        spiderman.swing(CAMERA.temp_pos, 1.40)
                    elif spiderman.rope_length == 1000:
                        spiderman.swing(CAMERA.temp_pos, 1.75)

        # No key press logic during swing
        if self.animation_list[-1] == ("swing" or "land"):
            keys_pressed = None

        #  Set rope length according to the camera's - Y position
        if CAMERA.y > -200 and self.is_swinging is False:
            self.rope_length = 600
        elif CAMERA.y <= -200 and self.is_swinging is False:
            self.rope_length = 1000

        #  Landing logic
        if CAMERA.y < -300 and CAMERA.y > -400 and CAMERA.gravitational_vel > 50:
            self.animation = "land"
            self.animation_frame = 1

        # Conditions for player-border collision
        if self.x <= 100:
            self.border_collide_L = True
        elif self.x >= WIDTH - self.width - 200:
            self.border_collide_R = True

        # Code to switch player side
        if self.border_collide_L is False and self.direction == "right":
            pavement.movements(keys_pressed, 1)
            CAMERA.x += VEL * 5
            self.x -= VEL * 5
        elif self.border_collide_R is False and self.direction == "left":
            pavement.movements(keys_pressed, -1)
            CAMERA.x -= VEL * 5
            self.x += VEL * 5

    def draw_collison_bounds(self, show=False):
        """draws collision bounds around the character

        Args:
            show (bool, optional): collision bounds become visible during gameplay if True.
            Defaults to False.
        """
        active = None
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
            try:
                active = animation_cb_pairs[self.animation]
            except KeyError:
                None

        if active is not None:
            x_fac, y_fac, width_fac, height_fac = active[0], active[1], active[2], active[3]
            object_collision_bound = pygame.Rect(
                self.x + x_fac, self.y + y_fac, self.width + width_fac, self.height + height_fac)

        if show:
            try:
                return pygame.draw.rect(WIN, (255, 0, 0), object_collision_bound)
            except UnboundLocalError:
                None

    def swing(self, camera, depth_fac):
        """moves player on a curved swinging path

        Args:
            camera (list): fixed camera position
            depth_fac (int ): related to swing curvature
        """
        self.animation = "swing"

        #  Right direction swing
        if self.direction == "right":
            # Defining constants for a single swing
            swing_pivot = {'x': camera[0] +
                           (self.rope_length*depth_fac), 'y': camera[1] - self.rope_length}
            center = {'x': (swing_pivot['x']+camera[0])/2,
                      'y': (swing_pivot['y']+camera[1])/2}
            radius = math.sqrt((swing_pivot['x']-camera[0])**2
                               + (swing_pivot['y']-camera[1])**2)/2
            x_max = {'x': center["x"]+radius, 'y': center["y"]}

            if CAMERA.x >= x_max["x"]+300:
                self.swing_end = True

            # Moving player along the X axis
            if CAMERA.x < x_max['x']:
                CAMERA.x += 50
                if CAMERA.x >= x_max["x"]:
                    CAMERA.x = x_max["x"]
                # Moving player along Y axis according to eqation of circle
                CAMERA.y = center["y"] + \
                    math.sqrt(
                        abs(radius**2-(CAMERA.x-center["x"])**2))
            elif CAMERA.x >= x_max['x'] and CAMERA.x < x_max["x"]+300:
                CAMERA.x += 26
                CAMERA.y -= 25

            #  Drawing swinging rope
            if self.animation_frame > 5 and self.animation_frame < 42:
                pygame.draw.line(WIN, WHITE, (swing_pivot['x']-(CAMERA.x-400), swing_pivot['y']-(
                    CAMERA.y+400)), (self.x + 440, self.y + 350), 6)

        #  Left direction swing
        else:
            # Defining constants for a single swing
            swing_pivot = {'x': camera[0] -
                           (self.rope_length*depth_fac), 'y': camera[1] - self.rope_length}
            center = {'x': (swing_pivot['x']+camera[0])/2,
                      'y': (swing_pivot['y']+camera[1])/2}
            radius = math.sqrt((swing_pivot['x']-camera[0])**2
                               + (swing_pivot['y']-camera[1])**2)/2
            x_max = {'x': center["x"]-radius, 'y': center["y"]}

            if CAMERA.x <= x_max["x"]-300:
                self.swing_end = True

            # Moving player along the X axis
            if CAMERA.x > x_max['x']:
                CAMERA.x -= 50
                if CAMERA.x <= x_max["x"]:
                    CAMERA.x = x_max["x"]
                # Moving player along Y axis according to eqation of circle
                CAMERA.y = center["y"] + \
                    math.sqrt(
                        abs(radius**2-(CAMERA.x-center["x"])**2))

            elif CAMERA.x <= x_max['x'] and CAMERA.x > x_max["x"]-300:
                CAMERA.x -= 26
                CAMERA.y -= 25

            #  Drawing swinging rope
            if self.animation_frame > 5 and self.animation_frame < 42:
                pygame.draw.line(
                    WIN, WHITE, (swing_pivot['x']-(CAMERA.x-1200), swing_pivot['y']-(CAMERA.y)), (self.x+120, self.y+350), 5)


#  Defining drawable objects
CAMERA = Camera(0, 0)
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
        pavement.draw(4, 0, -CAMERA.y)
    elif spiderman.animation == "walk" and CAMERA.y >= -20:
        pavement.draw(2, 0, -CAMERA.y)
    elif spiderman.border_collide_L is False and spiderman.direction == "right":
        pavement.draw(4, 0, -CAMERA.y)
    elif spiderman.border_collide_R is False and spiderman.direction == "left":
        pavement.draw(4, 0, -CAMERA.y)
    else:
        pavement.draw(0, 0, -CAMERA.y)

    # Draws various buildings
    building1.draw(WIN, (CAMERA.x, CAMERA.y))
    building1.collision_bound((CAMERA.x, CAMERA.y), 120, 20, 2760, 2310)
    building2.draw(WIN, (CAMERA.x, CAMERA.y))
    building2.collision_bound((CAMERA.x, CAMERA.y), 186, 7, 1980, 2260)
    building3.draw(WIN, (CAMERA.x, CAMERA.y))
    building3.collision_bound((CAMERA.x, CAMERA.y), 180, 12, 2030, 1428)
    building4.draw(WIN, (CAMERA.x, CAMERA.y))
    building4.collision_bound((CAMERA.x, CAMERA.y), 343, 395, 4672, 3175)

    #  Draws spiderman character
    spiderman.draw_collison_bounds()
    spiderman.draw_player()
    spiderman.player_animations()
    spiderman.player_movements(keys_pressed, key_up)
    spiderman.player_settings(keys_pressed)


def main():

    clock = pygame.time.Clock()
    keys_used = [pygame.K_w, pygame.K_a,
                 pygame.K_s, pygame.K_d, pygame.K_SPACE, pygame.K_RIGHT]

    # GAME MAIN LOOP #
    while True:
        print(spiderman.jump)
        spiderman.animation_sequence(spiderman.animation)
        key_up = None  # Contains keys which are released
        clock.tick(FPS)
        WIN.fill(WHITE)
        CAMERA.temp_x = CAMERA.x
        keys_pressed = pygame.key.get_pressed()

        # takes all the keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:  # Button tapped
                if event.key == pygame.K_SPACE:
                    if CAMERA.y <= -80:
                        spiderman.animation_frame = 1
                    CAMERA.temp_pos = (CAMERA.x, CAMERA.y)

                if event.key == pygame.K_RIGHT:
                    if spiderman.animation == "cross_punch" or spiderman.animation == "punch_combo":
                        if spiderman.animation_frame > 17:
                            spiderman.animation_frame = 7
                            spiderman.animation = "cross_punch"
                            if spiderman.animation_list[-1] == "cross_punch":
                                spiderman.animation_frame = 1
                                spiderman.animation = "punch_combo"
                    else:
                        spiderman.animation_frame = 7
                        spiderman.animation = "cross_punch"
                        if spiderman.animation_list[-1] == "cross_punch":
                            spiderman.animation_frame = 1
                            spiderman.animation = "punch_combo"

                if event.key == pygame.K_LEFT:
                    if spiderman.animation == "hook_punch":
                        if spiderman.animation_frame > 13:
                            spiderman.animation_frame = 3
                            spiderman.animation = "hook_punch"
                    else:
                        spiderman.animation_frame = 3
                        spiderman.animation = "hook_punch"

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

            if event.type == pygame.KEYUP:  # Button released
                if event.key == pygame.K_w:
                    key_up = "w"
                if event.key == pygame.K_SPACE:
                    spiderman.is_swinging = False
                    spiderman.swing_end = False
                    CAMERA.gravitational_vel = 0

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
        CAMERA.set_boundary(-5500, 6000)

        # Implimentation of gravitaty
        CAMERA.set_gravity(4)

        # Animate pavement according to the camera movement
        pavement.movements(keys_pressed, CAMERA.check_movement())

        #  Update statement
        pygame.display.update()


# calling the main function
if __name__ == "__main__":
    main()
