import pygame
import os
from sys import exit

WIDTH, HEIGHT = 1600, 900
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Buildings")
WHITE = (255, 255, 255)
FPS = 60
indx = 0
font = pygame.font.Font(None, 50)


class Building():
    def __init__(self, name, offset_x, offset_y):
        self.name = name
        self.building = pygame.image.load(os.path.join(
            "assets/buildings", self.name)).convert_alpha()
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.x = offset_x
        self.y = offset_y

    def color_key(self, color):
        self.building.set_colorkey(color)

    def draw(self, WIN, camera_position):
        self.VEL = 20
        self.x = -camera_position[0]+self.offset_x
        self.y = -camera_position[1]+self.offset_y
        WIN.blit(self.building, (self.x, self.y))

    def movements(self, keys_pressed):
        if keys_pressed is None:
            return
        if keys_pressed[pygame.K_a]:
            self.x += self.VEL
            if keys_pressed[pygame.K_LSHIFT]:
                self.x += self.VEL
        elif keys_pressed[pygame.K_d]:
            self.x -= self.VEL
            if keys_pressed[pygame.K_LSHIFT]:
                self.x -= self.VEL

    def movements_updown(self, keys_pressed):
        if keys_pressed[pygame.K_w]:
            self.y += self.VEL
            if keys_pressed[pygame.K_LSHIFT]:
                self.y += self.VEL
        elif keys_pressed[pygame.K_s]:
            self.y -= self.VEL
            if keys_pressed[pygame.K_LSHIFT]:
                self.y -= self.VEL

    def collision_bound(self, camera_position, x_fac, y_fac, width_fac, height_fac, show=False):
        self.x = -camera_position[0]+self.offset_x
        self.y = -camera_position[1]+self.offset_y
        object_collision_bound = pygame.Rect(
            self.x+x_fac, self.y+y_fac, width_fac, height_fac)
        if show is True:
            pygame.draw.rect(WIN, (0, 255, 0), object_collision_bound)


def main():
    building1 = Building("4(1).png", -100, -1250)
    building2 = Building("5(1).png", 2000, -1800)
    building3 = Building("6.png", 5500, -1700)
    clock = pygame.time.Clock()

    while True:
        WIN.fill(WHITE)
        clock.tick(FPS)
        for event in pygame.event.get():
            keys_pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        building1.draw(WIN, [0, 0])
        building1.movements(keys_pressed)
        building1.movements_updown(keys_pressed)
        building2.draw(WIN, [0, 0])
        building2.movements(keys_pressed)
        building2.movements_updown(keys_pressed)
        building3.draw(WIN, [0, 0])
        building3.movements(keys_pressed)
        building3.movements_updown(keys_pressed)
        pygame.display.update()


if __name__ == "__main__":
    main()
