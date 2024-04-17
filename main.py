import pygame

clock = pygame.time.Clock()

from pygame.locals import * # Prevents us from having to add a "pygame." prefix to all keys

pygame.init()

# define screen information
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
pygame.display.set_caption("My First Game!")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# load terrain images
background_image = pygame.image.load("images/background.png")
dirt_image = pygame.image.load("images/dirt.png")
grass_image = pygame.image.load("images/grass.png")

# Sets the refresh rate for the screen. the "while running" loop iterates fps times per second
fps = 60

# define size variables
tile_size = 50
player_size = (45, 60)

# functions/classes that are helpful for game creation, not necessarily used in the actual game
def draw_grid():
	for line in range(0, 20):
		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (SCREEN_WIDTH, line * tile_size))
		pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, SCREEN_HEIGHT))


''' A debugger that can be optionally enabled to display any game information either
    on a button press, or at a specified interval, default being 4 times per second '''
class Debugger():
    def __init__(self, man_enabled, auto_enabled, auto_rate = 15):
        self.man_enabled = man_enabled
        self.auto_enabled = auto_enabled
        self.rate = auto_rate
        self.autocounter = 0

    def debug_manual(self):
        print("whatever you want to check")

    def debug_auto(self):
        if self.autocounter < self.rate:
                self.autocounter += 1
        else:
            print("whatever you want to check")
            self.autocounter = 0

    def update(self, pressed_keys):
        if self.auto_enabled == True:
            self.debug_auto()
        if pressed_keys[K_z] and self.man_enabled == True:
            self.debug_manual()
    
debugger = Debugger(True, False)


class World():
    def __init__(self, data):
        self.tile_list = [] # List containing all the terrain and its co-ordinates for the level

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
                    enemy = Enemy((col_count * tile_size + 8), (row_count * tile_size + 15))
                    all_sprites.add(enemy)
                col_count += 1
            row_count += 1


    def draw(self): # Draws each tile at its respective x/y co-ordinate
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
        

world_data = [ # A 16x9 grid representing the level terrain. Each tile has an instruction telling the game what kind of terrain it is
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
        self.animation_speed = 15
        self.index = 0
        self.walk_counter = 0
        self.direction = 1
        # loop below loads in images for animation
        for i in range(1, 4):
            img_right = pygame.image.load(f"images/guy{i}.png").convert()
            img_right = pygame.transform.scale(img_right, player_size) # Scale the image of the player to the size defined above
            img_left = pygame.transform.flip(img_right, True, False)
            img_right.set_colorkey((0, 0, 0), pygame.RLEACCEL) # makes the background of the player image transparent. RLEACCEL flag optimises this on lower-performing hardware (https://www.pygame.org/docs/ref/surface.html)
            img_left.set_colorkey((0, 0, 0), pygame.RLEACCEL)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.surf = self.images_right[self.index]
        self.rect = self.surf.get_rect() 
        # jumping/movement variables
        self.jump_velocity = 15
        self.yvelocity = 0
        self.walk_speed = 3
        # action variables
        self.jumping = False
        self.attacking = False # Don't mind this, going to come back to it to add a cooldown to attacking
        # where the player appears when the game starts based on the coordinates provided
        self.rect.x = x
        self.rect.y = y
        # physical attributes
        self.width = self.surf.get_width()
        self.height = self.surf.get_height()

    def update(self, pressed_keys):
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
            self.attack()

        if not pressed_keys[K_RIGHT] and not pressed_keys[K_LEFT] and not pressed_keys[K_UP]:
            # if not moving sets animation frame to 0
            self.index = 0
            self.walk_counter = 0
            self.change_frames()
        
        # makes animation run at self.animation_speed
        if self.walk_counter > self.animation_speed:
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

    def change_frames(self, index = None):
        """Changes current player based on whether turned left or right.
        Optional index argument, if none provided self.index is used"""
        if index == None:
            index = self.index
        if self.direction == 1:
            self.surf = self.images_right[index]
        else:
            self.surf = self.images_left[index]

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.yvelocity = -self.jump_velocity

    def attack(self): # https://www.w3schools.com/python/ref_func_isinstance.asp
        if not self.attacking:
            attack = Attack(player.rect.x, player.rect.y, player.direction)
            self.attacking = True


class Attack(pygame.sprite.Sprite):

    def __init__(self, x, y, direction):
        super(Attack, self).__init__()
        self.direction = direction
        all_sprites.add(self)
        self.timetolive = 30 # how long the attack will exist before disappearing
        self.timealive = 0
        # Make the attack face the same way as the player
        if self.direction == 1:
            self.image = pygame.image.load("images/attack.png").convert_alpha() #self.surf has to be self.image instead for draw function to work
            self.rect = self.image.get_rect()
            self.rect.x = x + 25 # Makes the attack go in front of the player, instead of overlapping
        else:
            self.image = pygame.transform.flip(pygame.image.load("images/attack.png").convert_alpha(), True, False)
            self.rect = self.image.get_rect()
            self.rect.x = x - 25
        self.image.set_colorkey((0,0,0,0), pygame.RLEACCEL)
        self.rect.y = y
    
    def update(self):
        self.timealive += 1
        if self.timealive < self.timetolive:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            all_sprites.remove(self)
            player.attacking = False # Spaghetti code here, accessing and changing an attribute of a different class, don't think it's too much of a problem since Player and Attack are so closely connected
    
    def collide(self):
        pass
        #pygame.sprite.spritecollide(self, all_sprites, True) # if the attack 

class StartMenu():
    def __init__(self):
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont('arial', 40)
        title = font.render('My Game', True, (255, 255, 255))
        start_button = font.render('Press space to start', True, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, SCREEN_HEIGHT/2 - title.get_height()/2))
        screen.blit(start_button, (SCREEN_WIDTH/2 - start_button.get_width()/2, SCREEN_HEIGHT/2 + start_button.get_height()/2))
        pygame.display.update()

class GameOverMenu():
    def __init__(self):
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont('arial', 40)
        title = font.render('Game Over', True, (255, 255, 255))
        start_button = font.render('Press r to restart, space to return to menu', True, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, SCREEN_HEIGHT/2 - title.get_height()/2))
        screen.blit(start_button, (SCREEN_WIDTH/2 - start_button.get_width()/2, SCREEN_HEIGHT/2 + start_button.get_height()/2))
        pygame.display.update()

player = Player(100, 200)

all_sprites = pygame.sprite.Group() # A container class to hold and manage multiple Sprite objects. https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Group

world = World(world_data)

game_state = 'start'
# Game loop. The code from here on is mainly event handling.
running = True

while running:

    if game_state == 'start':
        StartMenu()
        for event in pygame.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                
                if event.key == K_SPACE:
                    game_state = 'game'

            if event.type == QUIT:
                running = False

    if game_state == 'game-over':
        # there's currently no way for game state to be set to game over - once we add dying 
        # it will take you here
        GameOverMenu()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                
                if event.key == K_SPACE:
                    game_state = 'start'
                
                if event.key == K_r:
                    game_state = 'game'

            if event.type == QUIT:
                running = False

    if game_state == 'game':
        screen.blit(pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

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

        all_sprites.draw(screen)

        world.draw()

        draw_grid()
        debugger.update(pressed_keys)

        clock.tick(fps) # ensures that this loop is repeated fps times per second.

    pygame.display.flip()