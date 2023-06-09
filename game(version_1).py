import pygame
import math
from sys import exit
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
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.jump = False  # checks if w key is pressed
        self.direction = "right"  # current direction of character
        self.border_collide_L = True
        self.border_collide_R = False
        self.animation_frame = 1
        self.animation = "idle"
        self.animation_list = [None, None, None, None, None]
        self.key_up = None
        # Key intensity increase at hold of space. Becomes zero at the top of jump
        self.key_intensity = 0
        self.max_key_intensity = 0
        self.space_up = False  # Jump key becomes True at release of space
        self.rope_length = 800
        self.start_swing = False
        self.swing_count = 0
        self.swing_pivot = [
            CAMERA_POSITION[0] + self.rope_length,
            CAMERA_POSITION[1] - self.rope_length,
        ]

        # defining player
        self.player = pygame.image.load(
            f"./assets/idle/{self.animation_frame}.png")
        self.width = self.player.get_size()[0]
        self.height = self.player.get_size()[1]

    def draw_player(self):
        """Draw the player sprite onto the screen"""
        if self.direction != "right":
            WIN.blit(
                pygame.transform.flip(
                    self.player, True, False), (self.x, self.y)
            )  # draws the character
        else:
            WIN.blit(self.player, (self.x, self.y))

    def player_animations(self):
        """Adds animations to the player"""
        if self.animation == "running_jump":
            max_frame = 30
            if self.animation_frame >= max_frame + 1:
                self.jump = False
                self.animation_frame = 1
            self.player = pygame.image.load(
                f"./assets/running_jump/{self.animation_frame}.png"
            ).convert_alpha()
            self.animation_frame += 1
        elif self.jump and self.animation != "running jump":
            try:
                max_frame = 21
                self.player = pygame.image.load(
                    f"./assets/standing_jump(full)/{self.animation_frame}.png"
                ).convert_alpha()
                self.animation_frame += 1
                if self.animation_frame >= max_frame:
                    self.jump = False
                    self.animation = "idle"
            except FileNotFoundError:
                self.animation_frame = 1

        elif self.animation == "idle":
            max_frame = 15
            if self.animation_frame >= max_frame + 1:
                self.animation_frame = 1
            self.player = pygame.image.load(
                f"./assets/idle/{self.animation_frame}.png"
            ).convert_alpha()
            self.animation_frame += 1

        elif self.animation == "sit":
            max_frame = 1
            self.player = pygame.image.load(
                "./assets/sit/sit.png").convert_alpha()
        elif self.animation == "walk":
            max_frame = 16
            if self.animation_frame >= max_frame + 1:
                self.animation_frame = 1
            self.player = pygame.image.load(
                f"./assets/walk/{self.animation_frame}.png"
            ).convert_alpha()
            self.animation_frame += 1
        elif self.animation == "run":
            max_frame = 16
            if self.animation_frame >= max_frame + 1:
                self.animation_frame = 1
            self.player = pygame.image.load(
                f"./assets/run/{self.animation_frame}.png"
            ).convert_alpha()
            self.animation_frame += 1
        elif self.animation == "swing_jump":
            max_frame = 20
            if self.animation_frame >= max_frame + 1:
                self.animation_frame = max_frame
            self.player = pygame.image.load(
                f"./assets/swing_jump/{self.animation_frame}.png"
            ).convert_alpha()
            self.animation_frame += 1
        elif self.animation == "swing":
            max_frame = 7
            if self.animation_frame >= max_frame + 1:
                self.animation_frame = 1
            self.player = pygame.image.load(
                f"./assets/swing/{self.animation_frame}.png"
            ).convert_alpha()
            self.animation_frame += 1
        elif self.animation == "swing_land":
            max_frame = 50
            if self.animation_frame >= max_frame + 1:
                self.animation_frame = max_frame
                self.animation = "idle"
            self.player = pygame.image.load(
                f"./assets/swing_land/{self.animation_frame}.png"
            ).convert_alpha()
            self.animation_frame += 1

    def animation_sequence(self, animation):
        if self.animation_list[4] != animation:
            for i in range(1, 5):
                if self.animation_list[i - 1] != self.animation_list[i]:
                    self.animation_list[i - 1] = self.animation_list[i]
            self.animation_list[4] = animation
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
            if self.animation != "swing_land":
                self.animation = "idle"  # No key pressed logic
            return

        if self.x <= 100:
            self.border_collide_L = True
        if keys_pressed[pygame.K_d] and self.x > 100 and not keys_pressed[pygame.K_a]:
            self.x -= VEL  # RIGHT
            self.direction = "right"
            self.border_collide_L = False
        elif keys_pressed[pygame.K_d] and not keys_pressed[pygame.K_a]:
            self.animation = "walk"
            CAMERA_POSITION[0] += VEL

        if self.x >= WIDTH - self.width - 200:
            self.border_collide_R = True
        if keys_pressed[pygame.K_a] and self.x < WIDTH - self.width - 200:
            self.x += VEL  # LEFT
            self.direction = "left"
            self.border_collide_R = False
        elif keys_pressed[pygame.K_a] and not keys_pressed[pygame.K_d]:
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

    def draw_collison_bounds(self):
        if self.jump:
            x_fac, y_fac, width_fac, height_fac = 200, 250, -380, -600
            object_collision_bound = pygame.Rect(
                self.x + x_fac,
                self.y + y_fac,
                self.width + width_fac,
                self.height + height_fac,
            )
        elif self.animation == "idle":
            x_fac, y_fac, width_fac, height_fac = 200, 350, -380, -560
            object_collision_bound = pygame.Rect(
                self.x + x_fac,
                self.y + y_fac,
                self.width + width_fac,
                self.height + height_fac,
            )
        elif self.animation == "walk":
            x_fac, y_fac, width_fac, height_fac = 200, 340, -380, -560
            object_collision_bound = pygame.Rect(
                self.x + x_fac,
                self.y + y_fac,
                self.width + width_fac,
                self.height + height_fac,
            )
        elif self.animation == "sit":
            x_fac, y_fac, width_fac, height_fac = 200, 470, -380, -680
            object_collision_bound = pygame.Rect(
                self.x + x_fac,
                self.y + y_fac,
                self.width + width_fac,
                self.height + height_fac,
            )
        elif self.animation == "run":
            x_fac, y_fac, width_fac, height_fac = 140, 360, -320, -580
            object_collision_bound = pygame.Rect(
                self.x + x_fac,
                self.y + y_fac,
                self.width + width_fac,
                self.height + height_fac,
            )
        if self.animation == "running_jump":
            x_fac, y_fac, width_fac, height_fac = 240, 200, -340, -600
            object_collision_bound = pygame.Rect(
                self.x + x_fac,
                self.y + y_fac,
                self.width + width_fac,
                self.height + height_fac,
            )

        try:
            return pygame.draw.rect(WIN, (255, 0, 0), object_collision_bound)
        except UnboundLocalError:
            None

    def swing(self, keys_pressed):

        # Setting the value of key intensity when space is pressed
        if self.space_up is True and self.key_intensity >= 0 and self.swing_count <= 1:
            CAMERA_POSITION[1] -= 40  # <--Speed of jumping straight upwards
            self.animation = "swing_jump"
        if keys_pressed is not None and keys_pressed[pygame.K_SPACE] and self.key_intensity <= 20 and self.swing_count <= 1:
            if self.animation_list[-1] == "idle":
                self.animation = "sit"
            self.key_intensity += 2  # <-- Key press intensity increases
            if self.max_key_intensity < self.key_intensity:
                self.max_key_intensity = self.key_intensity
        elif self.key_intensity > 0:
            self.key_intensity -= 1
        elif self.key_intensity <= 0:
            self.space_up = False

        # Adjust rope length according to jump height
        self.rope_length = self.max_key_intensity * 50

        # Start swinging at this point
        if self.direction == "right":

            if self.space_up is True and self.key_intensity <= 1 and self.swing_count <= 1:
                # Indicates that the player has reached the top position
                self.swing_pivot = [
                    CAMERA_POSITION[0] + self.rope_length, CAMERA_POSITION[1] - self.rope_length]
                self.start_swing = True

            if self.start_swing is True and self.swing_count <= 1:
                self.animation = "swing"
                if keys_pressed is None:
                    # Swings the player according to this equation
                    CAMERA_POSITION[1] = math.sqrt(2 * (self.rope_length**2) - (
                        self.swing_pivot[0] - CAMERA_POSITION[0]) ** 2) + self.swing_pivot[1]
                else:
                    self.y = 100

                if CAMERA_POSITION[0] < self.swing_pivot[0] + self.rope_length:
                    CAMERA_POSITION[0] += 40  # <--indicates speed of swing

                else:
                    self.start_swing = False
                    self.max_key_intensity = 0
                    self.animation = "swing_land"
                    self.swing_count = 0

        elif self.direction == "left":
            if self.space_up is True and self.key_intensity <= 1 and self.swing_count <= 1:
                self.swing_pivot = [
                    CAMERA_POSITION[0] - self.rope_length, CAMERA_POSITION[1] - self.rope_length]
                self.start_swing = True

            if self.start_swing is True and self.swing_count <= 1:
                self.animation = "swing"
                if keys_pressed is None:
                    CAMERA_POSITION[1] = math.sqrt(2 * (self.rope_length**2) - (
                        self.swing_pivot[0] - CAMERA_POSITION[0]) ** 2) + self.swing_pivot[1]

                else:
                    self.y = 100

                if CAMERA_POSITION[0] > self.swing_pivot[0] - self.rope_length:
                    CAMERA_POSITION[0] -= 40  # <--indicates speed of swing

                else:
                    self.start_swing = False
                    self.max_key_intensity = 0
                    self.animation = "swing_land"
                    self.swing_count = 0

        # Swing count logic
        if CAMERA_POSITION[1] > 0:
            self.swing_count = 0
        if keys_pressed is not None and self.swing_count >= 1 and keys_pressed[pygame.K_SPACE]:
            self.space_up = False
            self.key_intensity = 0
            self.start_swing = False
            CAMERA_POSITION[1] += 100
            return


def main():
    spiderman = Player(100, 100)
    clock = pygame.time.Clock()
    keys_used = [pygame.K_w, pygame.K_a,
                 pygame.K_s, pygame.K_d, pygame.K_SPACE]
    gravity = 0
    pavement = Pavement()
    building1 = Building("5(1).png", 0, -1680)
    building2 = Building("6(1).png", 2800, -1620)
    building3 = Building("7(1).png", 5000, -800)
    building4 = Building("8(8).png", -5500, -2920)

    # GAME MAIN LOOP #
    while True:
        print(spiderman.key_intensity)
        spiderman.animation_sequence(spiderman.animation)
        key_up = None
        clock.tick(FPS)
        WIN.fill(WHITE)
        temp_cam_pos = CAMERA_POSITION[0]
        keys_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():  # takes all the keyboard and mouse events
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:  # UP released
                if event.key == pygame.K_w:
                    key_up = "w"
                if event.key == pygame.K_SPACE:
                    spiderman.space_up = True
                    spiderman.swing_count += 1

        for i in keys_used:
            if pygame.key.get_pressed()[i] is False:
                keys_pressed = None
            else:
                keys_pressed = pygame.key.get_pressed()
                break

        # Implimentation of camera boundaries
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
            gravity += 0.5  # <-- This number indicates the intensity of force
        if CAMERA_POSITION[1] >= 0:
            gravity = 0

        # Draws pavement and adjust speed according to player's action
        if (spiderman.start_swing is True or spiderman.animation == "run" or spiderman.animation == "running_jump"):
            pavement.draw(4, 0, -CAMERA_POSITION[1])
        else:
            pavement.draw(2, 0, -CAMERA_POSITION[1])

        building1.draw(WIN, CAMERA_POSITION)
        building2.draw(WIN, CAMERA_POSITION)
        building3.draw(WIN, CAMERA_POSITION)
        building4.draw(WIN, CAMERA_POSITION)

        # spiderman.draw_collison_bounds()
        spiderman.draw_player()
        spiderman.player_animations()
        spiderman.player_movements(keys_pressed, key_up)
        spiderman.swing(keys_pressed)

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
