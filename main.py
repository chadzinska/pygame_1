import pygame

clock = pygame.time.Clock()

from pygame.locals import *

pygame.init()

# define screen information
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
pygame.display.set_caption("My First Game!")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# load images
background_image = pygame.image.load("images/background.png")
dirt_image = pygame.image.load("images/dirt_placeholder.png")

fps = 60

# define size variables
tile_size = 50
# player_size = (height, width)

def draw_grid():
	for line in range(0, 20):
		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (SCREEN_WIDTH, line * tile_size))
		pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, SCREEN_HEIGHT))


class World():
    def __init__(self, data):
        self.tile_list = []

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_image, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1


    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
        

world_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
]

world = World(world_data)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.direction = 0
        # loop below loads in images for animation
        for i in range(1, 5):
            img_right = pygame.image.load(f"images/guy{i}.png").convert()
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.surf = self.images_right[self.index]
        self.surf.set_colorkey((255, 255, 255), RLEACCEL) # makes the background of the player image transparent. RLEACCEL flag optimises this on lower-performing hardware (https://www.pygame.org/docs/ref/surface.html)
        self.rect = self.surf.get_rect() 
        self.jumping = False
        self.jump_height = 60
        self.jump_count = 0
        self.jump_speed = 4

    def update(self, pressed_keys):
        walk_speed = 15
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
            self.counter += 1
            self.direction = 1
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(2, 0)
            self.counter += 1
            self.direction = 0

        if not pressed_keys[K_RIGHT] and not pressed_keys[K_LEFT]:
            self.index = 0
            self.counter = 0
            if self.direction == 0:
                self.surf = self.images_right[self.index]
            else:
                self.surf = self.images_left[self.index]
        
        if self.counter > walk_speed:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 0:
                    self.surf = self.images_right[self.index]
                else:
                    self.surf = self.images_left[self.index]

    def change_frames(counter, index, direction):
        # put the changing frames during animation logic here
        pass


        self.fall()

    def jump(self):
        if not self.jumping:
            self.jumping = True

    def fall(self):
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect):
                return
        if not self.jumping:
            self.rect.move_ip(0, 1)

player = Player()

all_sprites = pygame.sprite.Group()

# Game loop. The code from here on is mainly event handling.
running = True

while running:

    screen.blit(pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        if event.type == QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)

    screen.blit(player.surf, player.rect)

    world.draw()

    draw_grid()

    pygame.display.flip()