import pygame
import time
import math
import utils

GRASS = utils.scale_image(pygame.image.load("Assets/grass.jpg"), 2)
TRACK = utils.scale_image(pygame.image.load('Assets/track-border1.png'), 0.68)


TRACK_BORDER = utils.scale_image(pygame.image.load("Assets/track-border.png"), 0.68)
FINISH = utils.scale_image(pygame.image.load("Assets/finish.jpg"), 0.10)

PINK_CAR = utils.scale_image(pygame.image.load("Assets/car1.png"), 0.08)
BLUE_CAR = utils.scale_image(pygame.image.load("Assets/car2.png"), 0.03)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

FPS = 60


class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
             # use +- to indicate the direction the angle is moving
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        utils.blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
         #increase the velcity of the car based on the acceleration
        # if self.vel is already at maximum and we add self.acceleration, we don't want to go greater than maximum 
        self.move()

    def move_backward(self):
        self.vel= min(self.vel - self.acceleration, -self.max_vel/2)
        # "- self.max_vel/2" - it is negative because it is going in the negative direction and the max velocity is divided by 2 because the velocity moving forward CANNOT equal the velocity moving backward (must be half of it)
        #increase the velcity of the car based on the acceleration
        # if self.vel is already at maximum and we add self.acceleration, we don't want to go greater than maximum 
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal
        # if this value is negative, we dont want bthe carf to mmove backwards therefore the restriction is 0

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()


class PlayerCar(AbstractCar):
    IMG = PINK_CAR
    START_POS = (140, 200)
    # starting position


def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win)
    pygame.display.update()


run = True
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0))]
player_car = PlayerCar(4, 4)

while run:
    clock.tick(FPS)

    draw(WIN, images, player_car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    keys = pygame.key.get_pressed()
    # indicates the car is rotating when a certain key is pressed
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
         # if we press the w key we dont want it to slow down (if we dont press it we want to)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()        
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()


    if not moved:
        player_car.reduce_speed()


pygame.quit()