import pygame
from pygame.locals import *

pygame.init()
vec = pygame.math.Vector2  # 2 é usado pra 2 dimensoes - 2D

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60


FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

# criando as classes do player e das plataformas


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128, 255, 40))
        self.rect = self.surf.get_rect(center=(10, 420))


class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((WIDTH, 20))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center=(WIDTH/2, HEIGHT - 10))


PT1 = platform()
P1 = Player()

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    displaysurface.fill((0, 0, 0))  # a superfície com a cor de fundo

    displaysurface.blit(PT1.surf, PT1.rect)
    displaysurface.blit(P1.surf, P1.rect)

    pygame.display.update()
    FramePerSec.tick(FPS)
