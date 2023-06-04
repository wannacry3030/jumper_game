import pygame
from pygame.locals import *
import sys
import random
import time

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

vec = pygame.math.Vector2  # 2 for two dimensional

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("mago legal")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf_left = pygame.image.load("snowman_left.png")
        self.surf_right = pygame.image.load("snowman_right.png")
        self.surf = self.surf_right
        self.rect = self.surf.get_rect()

        self.pos = vec((10, 360))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = False
        self.score = 0
        self.direction = "right"

    def move(self):
        self.acc = vec(0, 0.5)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
            self.direction = "left"
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
            self.direction = "right"

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -15

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point:
                        hits[0].point = False
                        self.score += 1
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False

    def draw(self):
        if self.direction == "left":
            self.surf = self.surf_left
        elif self.direction == "right":
            self.surf = self.surf_right
        displaysurface.blit(self.surf, self.rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf_left = pygame.image.load("enemy_left.png")
        self.surf_right = pygame.image.load("enemy_right.png")
        self.surf = self.surf_right
        self.rect = self.surf.get_rect()

        self.pos = vec((random.randint(0, WIDTH), -100))
        self.vel = vec(0, 0)

    def move(self):
        self.vel.y = 5
        self.pos += self.vel
        if self.pos.y > HEIGHT:
            self.pos.y = random.randint(-100, -10)
            self.pos.x = random.randint(0, WIDTH)

        self.rect.midbottom = self.pos

    def draw(self):
        displaysurface.blit(self.surf, self.rect)


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.image.load("Coin.png")
        self.rect = self.image.get_rect()

        self.rect.topleft = pos

    def update(self):
        if self.rect.colliderect(P1.rect):
            P1.score += 5
            self.kill()


class Platform(pygame.sprite.Sprite):
    def __init__(self, width=0, height=18):
        super().__init__()

        if width == 0:
            width = random.randint(50, 120)

        self.image = pygame.image.load("platform.png")
        self.surf = pygame.transform.scale(self.image, (width, height))
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH-10),
                                               random.randint(0, HEIGHT-30)))

        self.point = True
        self.moving = True
        self.speed = random.randint(-1, 1)

        if self.speed == 0:
            self.moving = False

    def generate_coin(self):
        if self.speed == 0:
            coins.add(Coin((self.rect.centerx, self.rect.centery - 50)))

    def move(self):
        hits = self.rect.colliderect(P1.rect)
        if self.moving:
            self.rect.move_ip(self.speed, 0)
            if hits:
                P1.pos += (self.speed, 0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH


def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform, groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        return False


def plat_gen():
    while len(platforms) < 6:
        width = random.randrange(50, 100)
        p = Platform()
        c = True

        while c:
            p = Platform()
            p.rect.center = (random.randrange(0, WIDTH - width),
                             random.randrange(-50, 0))
            c = check(p, platforms)

        p.generate_coin()
        platforms.add(p)
        all_sprites.add(p)


all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
coins = pygame.sprite.Group()

PT1 = Platform(450, 80)

background = pygame.image.load("background.png")
PT1.rect = PT1.surf.get_rect(center=(WIDTH/2, HEIGHT - 10))
PT1.moving = False
PT1.point = False

P1 = Player()
E1 = Enemy()

all_sprites.add(PT1)
all_sprites.add(P1)
platforms.add(PT1)

for x in range(random.randint(4, 5)):
    c = True
    pl = Platform()
    while c:
        pl = Platform()
        c = check(pl, platforms)
    pl.generate_coin()
    platforms.add(pl)
    all_sprites.add(pl)

enemy_timer = pygame.time.get_ticks() + 5000  # Initial delay of 5 seconds

while True:
    P1.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()

    if pygame.time.get_ticks() >= enemy_timer:
        e = Enemy()
        all_sprites.add(e)
        enemy_timer += 5000

    for entity in all_sprites:
        displaysurface.blit(background, (0, 0))
        entity.move()
        displaysurface.blit(entity.surf, entity.rect)

    if P1.jumping:
        P1.surf = pygame.image.load("snowman_jump.png")
    else:
        if P1.direction == "left":
            P1.surf = pygame.image.load("snowman_left.png")
        elif P1.direction == "right":
            P1.surf = pygame.image.load("snowman_right.png")

    if P1.vel.y != 0:
        P1.jumping = True
    platforms.update()

    coins.update()
    coins.draw(displaysurface)

    if P1.score >= 20:
        pygame.mixer.music.pause()

        font = pygame.font.Font("freesansbold.ttf", 20)
        text = font.render("Você Ganhou", True, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (WIDTH // 2, HEIGHT // 2)
        displaysurface.blit(text, textRect)

        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    if pygame.sprite.spritecollideany(P1, E1):
        pygame.mixer.music.pause()

        P1.kill()
        font = pygame.font.Font("freesansbold.ttf", 20)
        text = font.render("Game Over", True, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (WIDTH // 2, HEIGHT // 2)
        displaysurface.blit(text, textRect)

        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    displaysurface.blit(P1.surf, P1.rect)

    pygame.display.update()
    FramePerSec.tick(FPS)
