import pygame

clock = pygame.time.Clock()

from pygame.locals import *

pygame.init()

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
pygame.display.set_caption("My First Game!")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

fps = 60

class World():
    def __init__(self):
        

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/lil_guy.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL) # makes the background of the player image transparent. RLEACCEL flag optimises this on lower-performing hardware (https://www.pygame.org/docs/ref/surface.html)
        self.rect = self.surf.get_rect() 
        self.jumping = False
        self.jump_height = 60
        self.jump_count = 0
        self.jump_speed = 4

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.jump()
        if self.jumping:
            if self.jump_count < self.jump_height:
                self.rect.move_ip(0, -self.jump_speed)
                self.jump_count += self.jump_speed
            else:
                self.jumping = False
                self.jump_count = 0
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-2, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(2, 0)

    def jump(self):
        if not self.jumping:
            self.jumping = True

player = Player()

all_sprites = pygame.sprite.Group()

running = True

while running:
    for event in pygame.event.get():

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        if event.type == QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)

    screen.fill((0, 0, 0))
    screen.blit(player.surf, player.rect)

    pygame.display.flip()