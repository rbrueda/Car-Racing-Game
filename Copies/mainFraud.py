import pygame
import time 
import math 
import os
import utils

pygame.init() # Must initilize pygame in order for it to function

#def scale_image(img,factor): 
#    size = round(img.get_width() * factor), round(img.get_height() * factor)
    # new size - we need to round cuz we need integer values not decimals
#    return pygame.transform.scale(img, size)
## dont need this since this code in in utils

GRASS = utils.scale_image(pygame.image.load("Assets/grass.jpg"), 2)
TRACK = utils.scale_image(pygame.image.load('Assets/track-border1.png'), 0.68)


TRACK_BORDER = utils.scale_image(pygame.image.load("Assets/track-border.png"), 0.68)
FINISH = utils.scale_image(pygame.image.load("Assets/finish.jpg"), 0.10)

PINK_CAR = utils.scale_image(pygame.image.load("Assets/car1.png"), 0.08)
BLUE_CAR = utils.scale_image(pygame.image.load("Assets/car2.png"), 0.03)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((620, 600))
pygame.display.set_caption("Le Jeu de Course!")

FPS = 60

class AbstractCar: 
    # IMG = PINK_CAR
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left =False, right= False):
        if left:
            self.angle += self.rotation_vel
            # use +- to indicate the direction the angle is moving
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        utils.blit_rotate_center(win,self.IMG, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel= min(self.vel + self.acceleration, self.max_vel)
        #increase the velcity of the car based on the acceleration
        # if self.vel is already at maximum and we add self.acceleration, we don't want to go greater than maximum 
        self.move()

    def move_backward(self):
        self.vel= min(self.vel - self.acceleration, -self.max_vel)
        # "- self.max_vel/2" - it is negative because it is going in the negative direction and the max velocity is divided by 2 because the velocity moving forward CANNOT equal the velocity moving backward (must be half of it)
        #increase the velcity of the car based on the acceleration
        # if self.vel is already at maximum and we add self.acceleration, we don't want to go greater than maximum 
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) *self.vel

        self.y -= vertical
        self.x -= horizontal 
        # these are the x and y components for moving the car

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        # if this value is negative, we dont want the car to move backwards therefore the restriction is 0 
        self.move()


class Player_Car(AbstractCar):
    IMG = PINK_CAR
    START_POS = (140, 200)
    #starting positon

def draw(win, images,player_car):
    for img, pos in images:
        win.blit(img, pos)
    
    player_car.draw(win)
    pygame.display.update()

# def move_player(player_car):
        


def main():
    run = True
    clock = pygame.time.Clock() 
    images = [(GRASS, (0,0)), (TRACK, (0,0))]
    player_car = Player_Car(4, 4)


    while run:
        clock.tick(FPS)

        # WIN.blit(GRASS, (0, 0))
        # WIN.blit(TRACK, (0, 0))
        # WIN.blit(FINISH, (0,0))
        # # blit means place
        # WIN.blit(PINK_CAR, (0,0))
        # WIN.blit(BLUE_CAR, (20,0))

        draw(WIN,images,player_car)


        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # move_player(player_car)
        keys = pygame.key.get_pressed()
            # idicates the car is rotating when a certain key is pressed
        moved = False

        if keys[pygame.K_a]:
            player_car.rotate(left= True)
        if keys[pygame.K_d]:
                player_car.rotate(right=True)
        if keys[pygame.K_w]:
            moved = True
            # if we press the w key we dont want it to slow down (if we dont press it we want to)
            player_car.move_forward()
        if keys[pygame.K_s]:
            moved = True
            player_car.move_backward()

        if not moved:
            player_car.reduce_speed()


pygame.quit()

main()

if __name__ ==  "__main__":
    main()