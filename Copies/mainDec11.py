import pygame
import time 
import math 
import os
import utils

pygame.init() # Must initilize pygame in order for it to have t

#def scale_image(img,factor): 
#    size = round(img.get_width() * factor), round(img.get_height() * factor)
    # new size - we need to round cuz we need integer values not decimals
#    return pygame.transform.scale(img, size)
## dont need this since this code in in utils

GRASS = utils.scale_image(pygame.image.load("Assets/grass.jpg"), 2)
TRACK = utils.scale_image(pygame.image.load('Assets/track-border1.png'), 0.68)


TRACK_BORDER = utils.scale_image(pygame.image.load("Assets/track-border.png"), 0.68)
FINISH = utils.scale_image(pygame.image.load("Assets/finish.jpg"), 0.10)

PINK_CAR = utils.scale_image(pygame.image.load("Assets/car1.png"), 0.12)
BLUE_CAR = utils.scale_image(pygame.image.load("Assets/car2.png"), 0.03)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((620, 600))
pygame.display.set_caption("Le Jeu de Course!")

FPS = 60

class AbstractCar: 
    IMG = PINK_CAR
    def __init__(self, max_vel, rotation_vel):
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS

    def rotate(self, left =False, right= False):
        if left:
            self.angle += self.rotation_vel
            # use +- to indicate the direction the angle is moving
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        utils.blit_rotate_center(win,self.IMG, (self.x, self.y), self.angle)

class Player_Car(AbstractCar):
    IMG = PINK_CAR
    START_POS = (140, 200)
    #starting positon

def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)
    
    player_car.draw(win)
    pygame.display.update()

player_car = Player_Car(4, 4)

def main():
    run = True
    clock = pygame.time.Clock()
    images = [(GRASS, (0,0)), (TRACK, (0,0))]

    while run:
        clock.tick(FPS)

        WIN.blit(GRASS, (0, 0))
        WIN.blit(TRACK, (0, 0))
        WIN.blit(FINISH, (0,0))
        # blit means place
        WIN.blit(PINK_CAR, (0,0))
        WIN.blit(BLUE_CAR, (20,0))

        draw(WIN,images,player_car)


        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                # print("Quitting..")
                break

            keys = pygame.key.get_pressed()
            # idicates the car is rotating when a certain key is pressed

            if keys[pygame.K_a]:
                player_car.rotate(Left= True)
            if keys[pygame.K_d]:
                player_car.rotate(right=True)

pygame.quit()

if __name__ ==  "__main__":
    main()