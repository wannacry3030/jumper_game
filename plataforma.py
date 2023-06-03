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

    def move(self):
        self.acc = vec(0, 0.5)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        # equação que usa fricção pra diminuir a vel do P1
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # DEFININDO O PROTAGONISTA

    # criando "screen warping", atravessar de um lado para o outro da tela
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.vel.y = -15

    def update(self):
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if P1.vel.y > 0:
            if hits:
                self.pos.y = hits[0].rect.top + 1
                self.vel.y = 0

# DEFININDO AS PLATAFORMAS QUE SERAO UTILIZADAS DURANTE O JOGO


class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50, 100), 12))
        self.surf.fill((0, 255, 0))
        self.rect = self.surf.get_rect(
            center=(random.randint(0, WIDTH-10), random.randint(0, HEIGHT-30)))

    def move(self):
        pass


PT1 = platform()
P1 = Player()

PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255, 0, 0))
PT1.rect = PT1.surf.get_rect(center=(WIDTH/2, HEIGHT - 10))

# CRIANDO O LOOP PRINCIPAL E RENDERIZANDO OS JOGADORES NA TELA
all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

platforms = pygame.sprite.Group()
platforms.add(PT1)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()

        # checando a posição do P1 de acordo com a tela
        if P1.rect.top <= HEIGHT / 3:
            P1.pos.y += abs(P1.vel.y)
            for plat in platforms:
                plat.rect.y += abs(P1.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()

    displaysurface.fill((0, 0, 0))
    P1.update()

    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()

        pygame.display.update()
        FramePerSec.tick(FPS)

    for x in range(random.randint(5, 6)):
        pl = platform()
        platforms.add(pl)
        all_sprites.add(pl)
