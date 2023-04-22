import pygame
from pygame.locals import *
from sys import exit
from random import randint

width = 640
height = 480
default_rect_size = moving_step = 25
finished = False

def update(self, snake):
    def roll():
        rect = (randint(0, width-default_rect_size), randint(0, height-default_rect_size), self.width, self.height)
        for c in snake.length:
            if 'draw' in dir(c):
                    if not c.draw.colliderect(rect):
                        pass
                    else:
                        return None
        return rect
    
    rect = roll()
    while not rect:
        rect = roll()
    self.x = rect[0]
    self.y = rect[1]

def control(self):
    for i in range(1, len(self.length)):
        self.length[i].x = self.length[i-1].start_pos[0]
        self.length[i].y = self.length[i-1].start_pos[1]
    for i in range(0, len(self.length)):
        self.length[i].start_pos = (self.length[i].x, self.length[i].y)

class rect:
    def __init__(self, pos, color=(255, 0, 0)):
        self.start_pos = pos
        self.color = color
        self.x = pos[0]
        self.y = pos[1]
        self.width = default_rect_size
        self.height = default_rect_size

class snake:
    def __init__(self, length):
        self.direction = 'r'
        self.length = list()
        self._control = control

        self.length.append(
            rect((  randint(default_rect_size*length, width), randint(default_rect_size*length, height)  ), color=(255, 255, 0))
        )
        self.length.append(
            rect(( self.length[0].x-default_rect_size, self.length[0].y ))
        )

        for i in range(0, length):
            self.add()

    def add(self):
        x = y = None
        if self.length[len(self.length)-1].x == self.length[len(self.length)-2].x:
                x = self.length[len(self.length)-1].x
                if self.length[len(self.length)-2].y > self.length[len(self.length)-1].y:
                    y = self.length[len(self.length)-1].y - default_rect_size
                else:
                    y = self.length[len(self.length)-1].y + default_rect_size
        else:
                y = self.length[len(self.length)-1].y
                if self.length[len(self.length)-2].x > self.length[len(self.length)-1].x:
                    x = self.length[len(self.length)-1].x - default_rect_size
                else:
                    x = self.length[len(self.length)-1].x + default_rect_size
        self.length.append(rect( (x, y) ))

    def update(self, pos_x=None, pos_y=None):
        if pos_x:
            self.length[0].x += pos_x
        elif pos_y:
            self.length[0].y += pos_y

        if self.length[0].x  >=  width:
            self.length[0].x = 0
        elif self.length[0].x  <=  -default_rect_size:
            self.length[0].x = width-default_rect_size

        if self.length[0].y  >=  height:
            self.length[0].y = 0
        elif self.length[0].y  <=  -default_rect_size:
            self.length[0].y = height-default_rect_size
        
        self._control(self)


p1 = snake(6)
food = rect( pos=(randint(0, width-default_rect_size), randint(0, height-default_rect_size)), color=(0, 255, 0) )
food.update = update
pygame.init()
tela = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake game')
text = pygame.font.SysFont('arial', 40)
clock = pygame.time.Clock()



while True:
    clock.tick(15)
    tela.fill( (0,0,0) )
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    if pygame.key.get_pressed()[K_ESCAPE] or finished:
        pygame.quit()
        exit()


    food.draw = pygame.draw.circle(tela, food.color, (food.x, food.y), int(food.width/2))
    for c in p1.length:
        c.draw = pygame.draw.rect(tela, c.color, (c.x, c.y, c.width, c.height))

    if pygame.key.get_pressed()[K_a]:
        if not pygame.key.get_pressed()[K_d] and not pygame.key.get_pressed()[K_w] and not pygame.key.get_pressed()[K_s]:
                p1.direction = 'l' if p1.direction != 'r' else 'r'

    if pygame.key.get_pressed()[K_d]:
        if not pygame.key.get_pressed()[K_a] and not pygame.key.get_pressed()[K_w] and not pygame.key.get_pressed()[K_s]:
                p1.direction = 'r' if p1.direction != 'l' else 'l'

    if pygame.key.get_pressed()[K_w]:
        if not pygame.key.get_pressed()[K_s] and not pygame.key.get_pressed()[K_a] and not pygame.key.get_pressed()[K_d]:
                p1.direction = 'u' if p1.direction != 'd' else 'd'

    if pygame.key.get_pressed()[K_s]:
        if not pygame.key.get_pressed()[K_w] and not pygame.key.get_pressed()[K_a] and not pygame.key.get_pressed()[K_d]:
                p1.direction = 'd' if p1.direction != 'u' else 'u'

    if p1.direction == 'l':
        p1.update(  pos_x= moving_step*-1  )
    if p1.direction == 'r':
        p1.update(  pos_x=moving_step  )
    if p1.direction == 'u':
        p1.update(  pos_y= moving_step*-1  )
    if p1.direction == 'd':
        p1.update(  pos_y=moving_step  )

    if food.draw.colliderect(p1.length[0].draw):
        p1.add()
        food.update(food, p1)

    for i in range(1, len(p1.length)):
        if 'draw' in dir(p1.length[i]):
            if p1.length[0].draw.colliderect(p1.length[i].draw):
                finished = True
                ''

    pygame.display.update()
