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

# definindo o movimento direita e esquerda


def move(self):
    self.acc = vec(0, 0)

    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[K_LEFT]:
        self.acc.x = -ACC
    if pressed_keys[K_RIGHT]:
        self.acc.x = ACC

# DEFININDO O PROTAGONISTA


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128, 255, 40))
        self.rect = self.surf.get_rect()

        # implemento o movimento do protagonista
        self.pos = vec((10, 385))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

# DEFININDO AS PLATAFORMAS QUE SERAO UTILIZADAS DURANTE O JOGO


class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((WIDTH, 20))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center=(WIDTH/2, HEIGHT - 10))


PT1 = platform()
P1 = Player()


# CRIANDO O LOOP PRINCIPAL E RENDERIZANDO OS JOGADORES NA TELA
all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    displaysurface.fill((0, 0, 0))

    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)

        pygame.display.update()
        FramePerSec.tick(FPS)
