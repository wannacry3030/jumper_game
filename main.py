import pygame
from pygame.locals import *
import sys
import random
import time
import pygame.mixer
import imageio

from player import Player
from enemy import Enemy
from coin import Coin
from platforma import Platform

# Código principal do jogo...
import pygame
from pygame.locals import *
import sys
import random
import time
import pygame.mixer

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)


HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60
game_over = False

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("mago legal")


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
        C = True

        while C:
            p = Platform()
            p.rect.center = (random.randrange(
                0, WIDTH - width), random.randrange(-50, 0))
            C = check(p, platforms)

        p.generateCoin()
        platforms.add(p)
        all_sprites.add(p)


all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
coins = pygame.sprite.Group()
enemies = pygame.sprite.Group()

PT1 = Platform(450, 80)

background = pygame.image.load("background.png")
PT1.rect = PT1.surf.get_rect(center=(WIDTH/2, HEIGHT - 10))
PT1.moving = False
PT1.point = False

P1 = Player()
E1 = Enemy()

all_sprites.add(PT1)
all_sprites.add(P1)
all_sprites.add(E1)
platforms.add(PT1)

for x in range(random.randint(4, 5)):
    C = True
    pl = Platform()
    while C:
        pl = Platform()
        C = check(pl, platforms)
    pl.generateCoin()
    platforms.add(pl)
    all_sprites.add(pl)

# Tempo inicial para o próximo spawn de inimigo
enemy_spawn_time = pygame.time.get_ticks() + random.randint(2000, 5000)
game_over = False

while not game_over:
    P1.update()
    E1.update()
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

    if pygame.sprite.spritecollideany(P1, enemies):
        game_over = True
        P1.vel.y = 0  # Adicione esta linha para parar o movimento vertical do jogador

    if P1.rect.top > HEIGHT:
        game_over = True

    if game_over:
        for entity in all_sprites:
            entity.kill()
        time.sleep(1)
        displaysurface.fill((255, 0, 0))
        pygame.display.update()
        time.sleep(1)
        pygame.quit()
        sys.exit()

    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()

        for coin in coins:
            coin.rect.y += abs(P1.vel.y)
            if coin.rect.top >= HEIGHT:
                coin.kill()

    if pygame.time.get_ticks() > enemy_spawn_time:
        enemy_spawn_time = pygame.time.get_ticks() + random.randint(2000, 5000)
        E = Enemy()
        all_sprites.add(E)
        enemies.add(E)  # Adicionar o objeto Enemy ao grupo de inimigos

    plat_gen()
    displaysurface.blit(background, (0, 0))
    f = pygame.font.SysFont("Verdana", 20)
    g = f.render(str(P1.score), True, (123, 255, 0))
    displaysurface.blit(g, (WIDTH/2, 10))

    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()

    for coin in coins:
        displaysurface.blit(coin.image, coin.rect)
        coin.update()

    P1.draw()

    pygame.display.update()
    FramePerSec.tick(FPS)
