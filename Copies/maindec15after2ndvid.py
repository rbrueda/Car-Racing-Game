import pygame
import time
import math
import utils

GRASS = utils.scale_image(pygame.image.load("Assets/grass.jpg"), 2)
TRACK = utils.scale_image(pygame.image.load('Assets/track-border1.png'), 0.68)


TRACK_BORDER = utils.scale_image(pygame.image.load("Assets/track-border.png"), 0.68)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = utils.scale_image(pygame.image.load("Assets/finish.jpg"), 0.10)
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (100, 230)

PINK_CAR = utils.scale_image(pygame.image.load("Assets/car1.png"), 0.06)
BLUE_CAR = utils.scale_image(pygame.image.load("Assets/car2.png"), 0.03)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Le Jeu de Course!")

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
         #increase the velocity of the car based on the acceleration
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

# we put this in Abstract car class because this is both going to be for the computer and player my player
    def collide(self, mask, x=0, y=0): #***
        # mask meaning we are going to pass some other mask here, we will generate a mask for our own image
        #will have the x and y of the other mask? we obviously already have the x and y of the other car. We will determine if two masks are colliding in here
        car_mask = pygame.mask.from_surface(self.img)
        # whatever image we are using for this car
        offset = (int(self.x - x), int(self.y -y))
        # offset needs to be the integer values since we can get some floating values when subtracting
        #"self.x - x" means the starting position minus the x position of mask 
        poi = mask.overlap(car_mask, offset)
        # use the other mask as the calling mask which is going to dictate how we calculate the overlap 
        return poi

    def reset(self):
        # reset our car  positon so kind of preparing for the next level 
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0

class PlayerCar(AbstractCar):
    IMG = PINK_CAR
    START_POS = (140, 190)
    # starting position

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()
    #the class car does need to be able to reduce its speed the whole time and so its speed its going to be the same speed the entire time and so it make sense to have this class where its going to be used becasue its not going to be used by anything else that implements the abstact colour class

    def bounce(self):
        self.vel = -self.vel
        self.move()

def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win)
    pygame.display.update()

def move_player(player_car):
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


run = True
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]
player_car = PlayerCar(8, 8)

while run:
    clock.tick(FPS)

    draw(WIN, images, player_car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    move_player(player_car)

    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()

    finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POSITION)
    #with a "*" since what this does is split the tuple that is storing this position (x and y) into two individual coordinates and passes this to the function as TWO ARGUEMENTS
    if finish_poi_collide != None:
        # print(finish_poi_collide)
        if finish_poi_collide[1] == 0:
    # [1] -- means at index 1. index refers to a position within an ordered list 
            player_car.bounce()
            # just like when we hit the wall we are going to bounce meaning we are going to bounce ourselves up if we going backwards trying to hit the finish line
        else:
            player_car.reset()
            print("finish")



pygame.quit()