# goals - Get twenty points by eating green blocks
# rules - Dont let green block hit the white wall on the right
# feedback - red blocks subract points, green blocks add points
# freedom - move with w, a, s, and d

# import libraries and modules
# from platform import platform
from turtle import end_fill
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint

vec = pg.math.Vector2

# game settings 
WIDTH = 800
HEIGHT = 400
FPS = 30

# player settings
PLAYER_GRAV = 0.8
PLAYER_FRIC = 0.1
SCORE = 0

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# drawing text, sets the font
def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

def colorbyte():
    return random.randint(0,255)

# sprites...
# creating player class
class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((25, 25))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        # self.pos.y = 
        # self.pos.x = 
        self.vel = vec(0,0)
        self.acc = vec(0,0)
# the freedom or movement of the player
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.pos.y -= 10
        if keys[pg.K_a]:
            self.pos.x -= 10
        if keys[pg.K_s]:
            self.pos.y += 10
        if keys[pg.K_d]:
            self.pos.x += 10
        # if keys[pg.K_SPACE]:
        #     self.vel.y -= 5
# inbounds sets the boundaries on the screen 
    def inbounds(self):
        # left side of the screen
        if self.rect.x < 0:
            self.pos.x = 0
            self.rect.x = 0
        # right side
        if self.rect.right > WIDTH:
            self.pos.x = WIDTH - self.rect.width
            self.rect.x = WIDTH - self.rect.width
        # top
        if self.rect.y < 0:
            self.pos.y = 0
            self.rect.y = 0
        # bottom
        if self.rect.bottom > HEIGHT:
            self.pos.y = HEIGHT - self.rect.height
            self.rect.y = HEIGHT - self.rect.height
        # defing the updates for the player
    def update(self):

        self.controls()
        # friction
        # self.acc.x += self.vel.x * -0.1
        # self.acc.y += self.vel.y * -0.1
        self.vel += self.acc
        self.pos += self.vel + 1 * self.acc
        # self.rect.x += self.xvel
        # self.rect.y += self.yvel
        self.rect.topleft = self.pos
        self.inbounds()

# creating class for mobs or green blocks
class Mob(Sprite):
    # defining the properties in the parameter
    def __init__(self, x, y, w, h, color):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.color = color
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.rect.x = x
        self.rect.y = y
        self.vel = vec(0,0)
        self.pos = vec(0,0)
    def update(self):
        # movement of the mob
        self.rect.x += 2
        
# creating enemy class or the red blocks
class Enemy(Sprite):
    # properties in the parameter
    def __init__(self, x, y, w, h, color):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.color = color
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.rect.x += 2
        
# creating class for the wall
class Wall(Sprite):
    def __init__(self, x, y, w, h, color):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.color = color
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        pass
        

# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")
clock = pg.time.Clock()
  


# instantiate classes
player = Player()
wall = Wall(750, 0, 100, 400, (WHITE))

# create groups
all_sprites = pg.sprite.Group()
all_plats = pg.sprite.Group()
mobs = pg.sprite.Group()
enemys = pg.sprite.Group()
all_walls = pg.sprite.Group()

# a range for enemys to spawn and the rate they spawn
for i in range (1000):
    # e = Enemy(randint(-500, 0), randint(0,HEIGHT), 25, 25, (255, 0, 0))
    for j in range(5):
        # random spawns in the x and y
        e = Enemy(randint(-(i + 1) * 100, -(i * 100)), randint(j * 100,(j + 1) * 100), 25, 25, (255, 0, 0))
        # adds the variable e to enemy sprites
        all_sprites.add(e)
        enemys.add(e)
# a range for mobs to spawn and the rate they spawn
for i in range(500):
    # m = Mob(randint(-500, 0), randint(0,HEIGHT), 25, 25, (0, 255, 0))
    for j in range(4):
        # random spawns in x and y
        m = Mob(randint(-(i + 1) * 100, -(i * 100)), randint(j * 100,(j + 1) * 100), 25, 25, (0, 255, 0))
        # adds the variable m to mobs sprites
        all_sprites.add(m)
        mobs.add(m)
    

# add player to all sprites group
all_sprites.add(player, wall)


# gameended = False

# glob variable for the beginning screen
gamestarted = False

# Game loop starts HERE
running = True
while running:
    # keep the loop running using clock
    clock.tick(FPS)    

    # using pygames collide function to add or subtract points
    enemyhits = pg.sprite.spritecollide(player ,enemys, True)
    if enemyhits:
        SCORE -= 1
    mobhits = pg.sprite.spritecollide(player, mobs, True)
    if mobhits:   
        SCORE += 1

    # ends the game if these if statements are true
    mobhitswall = pg.sprite.spritecollide(wall, mobs, True)
    if mobhitswall:
        # gameended = True
        break
    if SCORE == 30:
        # gameended = True
        break

    
    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            # if event.key == pg.K_SPACE:
                gamestarted = True
                # gameended = True

    # drawing the screen and text in that screen for the start of the game      
    if not gamestarted:
        screen.fill(WHITE)
        draw_text("PRESS SPACE TO START", 25, (BLACK), WIDTH/2, HEIGHT/2)
        draw_text("DONT LET THE GREEN BLOCKS HIT THE END", 25, (BLACK), WIDTH/2, 150)
        draw_text("SEE HOW FAST YOU CAN GET TO 20 POINTS", 25, (BLACK), WIDTH/2, 100)
        pg.display.update()
        continue
    
    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.jump()



    ############ Update ##############
    # update all sprites
    all_sprites.update()

    ############ Draw ################
    # draw the background screen
    screen.fill(BLACK)
    # draw text
    draw_text("POINTS: " + str(SCORE), 22, WHITE, WIDTH / 2, HEIGHT / 24)
    # draw all sprites
    all_sprites.draw(screen)

    # buffer - after drawing everything, flip display
    pg.display.flip()
    # if SCORE == 20:
    #     end_fill
    #     gameended = True
        
    # if gameended:
    #     screen.fill(WHITE)
    #     draw_text("THANKS FOR PLAYING", 25, (BLACK), WIDTH/2, HEIGHT/2)
    #     pg.display.update()
pg.quit()
