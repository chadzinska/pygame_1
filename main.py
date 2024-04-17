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
dirt_image = pygame.image.load("images/dirt.png")
grass_image = pygame.image.load("images/grass.png")

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
                if tile == 1 or tile == 2:
                    if tile == 1:
                        img = pygame.transform.scale(dirt_image, (tile_size, tile_size))
                    elif tile == 2:
                        img = pygame.transform.scale(grass_image, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == 3:
                    enemy = Enemy((col_count * tile_size), (row_count * tile_size))
                    all_sprites.add(enemy)
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
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 2, 2],
    [1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 1, 1],
]

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Enemy, self).__init__()
        self.image = pygame.image.load("images/enemy1_r.png").convert_alpha() #self.surf has to be self.image instead for draw function to work
        self.image.set_colorkey((0,0,0,0), pygame.RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 5
    
    def take_damage(self, damage):
        self.health -= damage


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__()
        # animation variables
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.walk_counter = 0
        self.direction = 1
        # loop below loads in images for animation
        for i in range(1, 4):
            img_right = pygame.image.load(f"images/guy{i}.png").convert()
            img_left = pygame.transform.flip(img_right, True, False)
            img_right.set_colorkey((0, 0, 0), pygame.RLEACCEL) # makes the background of the player image transparent. RLEACCEL flag optimises this on lower-performing hardware (https://www.pygame.org/docs/ref/surface.html)
            img_left.set_colorkey((0, 0, 0), pygame.RLEACCEL)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.surf = self.images_right[self.index]
        self.rect = self.surf.get_rect() 
        # jumping/movement variables
        self.jumping = False
        self.jump_velocity = 15
        self.jump_count = 0
        self.yvelocity = 0
        self.walk_speed = 3
        # where the player appears when the game starts based on the coordinates provided
        self.rect.x = x
        self.rect.y = y
        # physical attributes
        self.width = self.surf.get_width()
        self.height = self.surf.get_height()
        self.topleft = (self.rect.x, self.rect.y)
        self.topright = ((self.rect.x + self.width), self.rect.y)
        self.bottomleft = (self.rect.x, (self.rect.y - self.height))
        self.bottomright = ((self.rect.x + self.width), (self.rect.y - self.height))

    def update(self, pressed_keys):
        animation_speed = 15
        dx = 0
        dy = 0

        if pressed_keys[K_UP]:
            self.jump()
            self.change_frames(2) # jumping animation, using same as peak walking for now might change

        if pressed_keys[K_LEFT]:
            dx -= self.walk_speed
            self.walk_counter += 1
            self.direction = -1

        if pressed_keys[K_RIGHT]:
            dx += self.walk_speed
            self.walk_counter += 1
            self.direction = 1

        if pressed_keys[K_SPACE]:
            attack = Attack(player.rect.x, player.rect.y)
            all_sprites.add(attack)

        if not pressed_keys[K_RIGHT] and not pressed_keys[K_LEFT] and not pressed_keys[K_UP]:
            # if not moving sets animation frame to 0
            self.index = 0
            self.walk_counter = 0
            self.change_frames()
        
        # makes animation run at animation_speed
        if self.walk_counter > animation_speed:
                self.walk_counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                self.change_frames()

        # gravity
        self.yvelocity += 1
        if self.yvelocity > 10:
            self.yvelocity = 10 # terminal velocity, you can't fall quicker than 10 pixels per frame
        dy += self.yvelocity

        # constantly updated variables for easy access to coordinates
        # not necessary at the moment but won't delete yet in case they end up being useful
        # self.topleft = (self.rect.x, self.rect.y)
        # self.topright = ((self.rect.x + self.width), self.rect.y)
        # self.bottomleft = (self.rect.x, (self.rect.y - self.height))
        # self.bottomright = ((self.rect.x + self.width), (self.rect.y - self.height))

        # collision detection with terrain
        for tile in world.tile_list:
            # check collision on x-axis ie. walking into a wall
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            # check collision on y-axis
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.yvelocity < 0: # checks whether you're on an upward trajectory ie. jumping into  block from above
                    dy = tile[1].bottom - self.rect.top
                    self.yvelocity = 0
                elif self.yvelocity >= 0: # this checks if you're standing on top of, or jumping down onto a block
                    dy = tile[1].top - self.rect.bottom
                    self.yvelocity = 0
                    self.jumping = False
                    ''' note to self for future 
                    use elif if you don't want the second condition to execute immediately after the first
                    '''

        self.rect.x += dx
        self.rect.y += dy

        print(self.rect.top)

    def change_frames(self, index = None):
        """Changes current player based on whether turned left or right.
        Optional index argument, if none provided self.index is used"""
        if index == None:
            index = self.index
        if self.direction == 1:
            self.surf = self.images_right[index]
        else:
            self.surf = self.images_left[index]

    def attack(self):
        pass

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.yvelocity = -self.jump_velocity


class Attack(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super(Attack, self).__init__()
        self.image = pygame.image.load("images/attack.png").convert_alpha() #self.surf has to be self.image instead for draw function to work
        self.image.set_colorkey((0,0,0,0), pygame.RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        self.collide()
        # wait some time
            # self.kill()
    
    def collide(self):
        pygame.sprite.spritecollide(self, all_sprites, True)



player = Player(100, 200)

all_sprites = pygame.sprite.Group() 

world = World(world_data)

# Game loop. The code from here on is mainly event handling.
running = True

while running:

    screen.blit(pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

    all_sprites.draw(screen)

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        if event.type == QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)

    all_sprites.update()

    screen.blit(player.surf, player.rect)

    world.draw()

    draw_grid()

    pygame.display.flip()