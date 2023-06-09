import os
from sys import exit
import pygame

WIDTH, HEIGHT = 1600, 900
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sidewalk")
WHITE = (255, 255, 255)
FPS = 90
indx = 0
font = pygame.font.Font(None, 50)


class Pavement():
    def __init__(self):
        self.VEL = 20
        self.min_frame = 1
        self.max_frame = 213
        self.direction = "right"
        self.animation_frame = 1

    def draw(self, speed, offset_x, offset_y):
        if self.direction == "right":
            if self.animation_frame >= self.max_frame-2:
                self.animation_frame = self.min_frame
            elif self.animation_frame <= self.max_frame:
                self.animation_frame += speed
        elif self.direction == "left":
            if self.animation_frame <= self.min_frame+2:
                self.animation_frame = self.max_frame
            elif self.animation_frame >= self.min_frame:
                self.animation_frame -= speed

        self.pavement = pygame.image.load(os.path.join(
            "assets/sidewalk(reduced)", f"{self.animation_frame}.jpg")).convert()
        WIN.blit(self.pavement, (offset_x, offset_y))

    def movements(self, keys_pressed, cam_direction):
        if keys_pressed is None:
            self.direction = None
        elif keys_pressed[pygame.K_a] and not keys_pressed[pygame.K_d]:
            self.direction = "left"
        elif keys_pressed[pygame.K_d] and not keys_pressed[pygame.K_a]:
            self.direction = "right"
        else:
            self.direction = None

        if cam_direction == -1:
            self.direction = "left"
        elif cam_direction == +1:
            self.direction = "right"

    def collision_bound(self, x_fac, y_fac, width_fac, height_fac):
        pygame.draw.rect(WIN, (255, 0, 0), pygame.Rect(
            self.x+x_fac, self.y+y_fac, width_fac, height_fac))


def main():
    pavement = Pavement()
    clock = pygame.time.Clock()

    while 1:
        print(clock.get_fps())
        WIN.fill(WHITE)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        keys_pressed = pygame.key.get_pressed()
        pavement.draw(1, 0, -180)
        pavement.movements(keys_pressed, 0)
        pygame.display.update()


if __name__ == "__main__":
    main()
