import pygame
import time
import math
import utils
pygame.font.init()

GRASS = utils.scale_image(pygame.image.load("Assets/grass.jpg"), 2)
TRACK = utils.scale_image(pygame.image.load('Assets/track-border1.png'), 0.68)


TRACK_BORDER = utils.scale_image(pygame.image.load("Assets/track-border.png"), 0.68)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = utils.scale_image(pygame.image.load("Assets/finish.jpg"), 0.10)
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (100, 230)

PINK_CAR = utils.scale_image(pygame.image.load("Assets/car1.png"), 0.06)
BLUE_CAR = utils.scale_image(pygame.image.load("Assets/car2.png"), 0.01499375)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Le Jeu de Course!")

MAIN_FONT = pygame.font.SysFont("Algerian", 25)

FPS = 60
PATH = [(137, 129), (100, 59), (45, 128), (53, 364), (262, 555), (305, 511), (325, 392), (379, 365), (447, 398), (463, 528), (556, 528), 
        (554, 308), (299, 240),  (528, 190), (558, 143), (541, 65), (228, 69), (209, 114), (206, 289), (144, 295)]
# PATH = [(175, 119), (110, 70), (56, 133), (70, 481), (318, 731), (404, 680), (418, 521), (507, 475), (600, 551), (613, 715), (736, 713),
#         (734, 399), (611, 357), (409, 343), (433, 257), (697, 258), (738, 123), (581, 71), (303, 78), (275, 377), (176, 388), (178, 260)]

class GameInfo:
    LEVELS = 10 

    def __init__(self, level=1):
        # indicating we are starting at level 1
        self.level = level
        self.started = False
        # indicating whether or not the level has started
        self.level_start_time = 0

    def next_level(self):
        self.level += 1
        self.started = False
        # this is because if we are going to the next level then we dont want ot start the next level yet we need to wait for the user to do that 

    def reset(self):
        # this will allow us to reset everything
        self.level = 1
        self.started = False
        self.level_start_time = 0 

    def game_finished(self):
        return self.level > self.LEVELS

    def start_level(self):
        self.started = True
        self.level_start_time = time.time()
        # want to keep track on when the level started so we can easily determine how many time has elapsed by checking the current time and subtracting from time.time()

    def get_level_time(self):
        if not self.started:
            return 0
        return round(time.time() - self.level_start_time)
        # time.time() is going to be after start time therefore it need to be time.time() - self.level_start_time

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0.6
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.05

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

class ComputerCar(AbstractCar):
    IMG = BLUE_CAR
    START_POS = (110, 190)

    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        # uses def __init__ function to initialize all the values needed
        self.path = path
        self.current_point = 0
        # need to know what point in my path i am currently at 
        self.vel = max_vel
        #dont need to worry about acceleration and will start at max velocity

    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0 , 0), point, 5)
            #circle is going to be red
            #  "point" means pass the point (going to be the centre of the circle)
            # "5" means the radius so 10 is the diameter

    def draw(self, win):
        super().draw(win)
        # self.draw_points(win)

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        # calculating the displacepent in x and y between the target point and in my current position
        # once that is done that allows to find the angle between my car and the point and then I can adjust the position or angle of my car accordingly towards that target point
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        
        if y_diff == 0:
            desired_radian_angle = math.pi / 2
            #this is used to avoid an "over 0" equation
            # if the y difference is 0 I have to manually set the angle because the equatuon made involves a division of the y difference and you can't have a division 0 error 
            #this will also give me the angle between my car and between my point
            #if there is not difference in y that means we are horizontal meaning we are either 90 degrees or 270 degrees 
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)
            #  will give the angle between my car and between the point

        if target_y > self.y:
            #it is lower down in the screen meaning we have to go down
            desired_radian_angle += math.pi
            # we have to make it so it is always an acute angle since it is the most efficient to get to that position
            # however, if the target that we are looking for is lower down on the screen than where the current car position is, the turn we need to make is more extreme than what the angle is (for example we are getting an angle of 25 degrees and to make it point down we have to ADD 180 degrees to it)

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        # we take whatever our current angle is and subtract it by whatever the desired angle is to get to and then based off whether if this number is positive or negative we are going to know if we have to move LEFT OR RIGHT
        # IF the difference in the angle is LARGER THAN 180 degrees we are taking an inefficient route to get to that angle 
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            # to ensure we are moving in the right direction to get to the angle that we want
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
            # doing this to not PASS THE ANGLE going the other direction 
            #  for eg if the angle is 3 degrees and the rotational velocity is 4 degrees, if i go 4 degrees to the right i will end up passing the angle that I want. And then you iwll be going one degree less than the degree that you want and therefore you will have to go back 1 degree the opposite way
            #  to avoid this from happening the min() is included so if the difference in the angle is less than the rotational velocity it will move by that amount
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))
            #  if difference in angle is less than 0 -- to move towards the point 

    def update_path_point(self):
        # allows us to move to the next point in our path 
        target = self.path[self.current_point]
        # check for collison with the points that we have, so whatever point in am on i am going to see if my car has collided with it and if it has collided with it then I am hit that point and go on with the next one 
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        # created a rectangle from my car
        # the purpose of creating this rectangle is that image alone is a rectangle but it doesn't know its location. So you make a rectangle using the x and y of the car (as the top left hand corner of the image) and get the width and height of the image so what you can use is a BUILT IN METHOD in python to determine if the point is colliding with the "rectangle"
        if rect.collidepoint(*target):
            # need "*" to get the x and y coordinate as SEPARATE ARGUMENTS to this function
            self.current_point += 1
            # if i am colliding with that point

    def move(self):
        if self.current_point < len(self.path):
        # we have a point to move to
        # this is going to ensure we will not get an index error to trying to move to a point that doesn't exist
            self.calculate_angle()
            # calculate the angle and shift the car in that direction
            self.update_path_point()
            super().move()
            # we are actually going to call manually the move method that we are overriding inside the car
        else:
            self.current_point = 0


    def next_level(self, level):
        self.reset() 
        self.vel = self.max_vel + (level - 1) * 0.2
        self.current_point = 0

def draw(win, images, player_car, computer_car, game_info):
    for img, pos in images:
        win.blit(img, pos)

    level_text = MAIN_FONT.render(f"Level{game_info.level}", 1, (255, 255, 255))
    win.blit(level_text, (10, HEIGHT - level_text.get_height() - 70))
    # this is for displaying this text on the screen
    
    time_text = MAIN_FONT.render(f"Time: {game_info.get_level_time()}s", 1, (255, 255, 255))
    win.blit(time_text, (10, HEIGHT - time_text.get_height() - 40))
    #  there is -40 because we are going to have 30 px off set whidch is something we may need to modify 

    vel_text = MAIN_FONT.render(f"Vel: {round(player_car.vel, 1)}px/s", 1, (255, 255, 255))
    win.blit(vel_text, (10, HEIGHT - vel_text.get_height() - 10)) 

    player_car.draw(win)
    computer_car.draw(win)
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

def handle_collision(player_car, computer_car, game_info):
    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()

    computer_finish_poi_collide = computer_car.collide(FINISH_MASK, *FINISH_POSITION)
    if computer_finish_poi_collide != None:
        utils.blit_text_center(WIN, MAIN_FONT, "Tu as perdu!","")
        pygame.time.wait(2000)
        game_info.reset()
        player_car.reset()
        computer_car.reset()

    player_finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POSITION)
    #with a "*" since what this does is split the tuple that is storing this position (x and y) into two individual coordinates and passes this to the function as TWO ARGUEMENTS
    if player_finish_poi_collide != None:
        # print(finish_poi_collide)
        if player_finish_poi_collide[1] == 0:
    # [1] -- means at index 1. index refers to a position within an ordered list 
            player_car.bounce()
            # just like when we hit the wall we are going to bounce meaning we are going to bounce ourselves up if we going backwards trying to hit the finish line
        else:
            game_info.next_level()
            player_car.reset()
            computer_car.next_level(game_info.level)
            # allows the car to move on to a new vel to the next level

run = True
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]
player_car = PlayerCar(8, 8)
computer_car = ComputerCar(2, 5, PATH)
#  "(_,_)" means max velocity and max rotational velocity
game_info = GameInfo()

# pygame.time.wait(10000)

count = 0
while run:
    clock.tick(FPS)

    draw(WIN, images, player_car, computer_car, game_info)

    while count < 10000:
        utils.blit_text_center(WIN, MAIN_FONT, "Appuyez sur n'importe quelle touche ", f"pour démarrer le niveau {game_info.level}!")
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

            if event.type == pygame.KEYDOWN:
                game_info.start_level() 
        count += 1
    


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    # if event.type == pygame.MOUSEBUTTONDOWN:
    #     pos = pygame.mouse.get_pos()
    #     computer_car.path.append(pos)
    #  wont need this since my path has already been set 


    move_player(player_car)
    computer_car.move()

    handle_collision(player_car, computer_car, game_info)

    if game_info.game_finished():
        utils.blit_text_center(WIN, MAIN_FONT, "Vous avez gagné le jeu!","")
        pygame.time.wait(5000)
        game_info.reset()
        player_car.reset()
        computer_car.reset()


print(computer_car.path)
pygame.quit()