import pygame
import random
import os

WIDTH = 852
HEIGHT = 480
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#set up assets
game_dir = os.path.dirname(__file__)
img_dir= os.path.join(game_dir, "img")

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Save the person")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')
def screen_text(surf, text, size, x,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_icon, (180,50))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT-150
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_d]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

class Para(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(para_img,(50,80))
        
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85/2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 6)
        # self.speedx = random.randrange(-2, 2)

    def update(self):
        # self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 4)

#load all game graphics
background = pygame.image.load(os.path.join(img_dir,"sea.jpg")).convert()
background_rect= background.get_rect()

player_icon = pygame.image.load(os.path.join(img_dir,"ship.png")).convert()
player_icon_rect= player_icon.get_rect()

para_img = pygame.image.load(os.path.join(img_dir,"para.gif")).convert()
para_img_rect= para_img.get_rect()

all_sprites = pygame.sprite.Group()
paras = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(3):
    m = Para()
    all_sprites.add(m)
    paras.add(m)

score = 0

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # check collision
    hits = pygame.sprite.spritecollide(player, paras, False, pygame.sprite.collide_circle)
    for hit in hits:
        score += 1
        m = Para()
        # all_sprites.add(m)
        paras.add(m)    # increase the score
        print("hi")
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    screen_text(screen, str(score), 25, WIDTH/2, 10)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
