import pygame
from pygame.locals import *
import sys
import random
import time
import pygame.mixer

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("assets/music.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

vec = pygame.math.Vector2  # 2 for two dimensional

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60
game_over = False

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("mago legal")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Carrega as imagens do personagem voltado para a esquerda e para a direita
        self.surf_left = pygame.image.load("assets/mage_left.png")
        self.surf_right = pygame.image.load("assets/mage_right.png")
        self.surf = self.surf_right  # Inicialmente, carrega a imagem voltada para a direita

        self.rect = self.surf.get_rect()  # Obtém o retângulo da imagem do personagem

        self.pos = vec((10, 360))  # Posição inicial do personagem
        self.vel = vec(0, 0)  # Velocidade inicial do personagem
        self.acc = vec(0, 0)  # Aceleração inicial do personagem
        self.jumping = False  # Variável para controlar se o personagem está pulando
        self.score = 0  # Pontuação do jogador
        self.direction = "right"  # Inicialmente, o personagem está voltado para a direita

    def move(self):
        self.acc = vec(0, 0.5)  # Define a aceleração vertical do personagem

        # Obtém o estado das teclas pressionadas
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            # Define a aceleração horizontal negativa quando a tecla "left" é pressionada
            self.acc.x = -ACC
            # Altera a direção para "left" quando a tecla "left" é pressionada
            self.direction = "left"

        if pressed_keys[K_RIGHT]:
            # Define a aceleração horizontal positiva quando a tecla "right" é pressionada
            self.acc.x = ACC
            # Altera a direção para "right" quando a tecla "right" é pressionada
            self.direction = "right"

        self.acc.x += self.vel.x * FRIC  # Aplica atrito à aceleração horizontal
        self.vel += self.acc  # Atualiza a velocidade com base na aceleração
        # Atualiza a posição com base na velocidade e aceleração
        self.pos += self.vel + 0.5 * self.acc

        # Limita a posição do personagem dentro dos limites da tela
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        # Atualiza a posição do retângulo da imagem do personagem
        self.rect.midbottom = self.pos

    def jump(self):
        # Verifica colisões entre o personagem e as plataformas
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True  # Define que o personagem está pulando
            self.vel.y = -15  # Define a velocidade vertical negativa para o pulo

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3  # Define uma velocidade vertical mínima durante o pulo

    def update(self):
        # Verifica colisões entre o personagem e as plataformas
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0:  # Verifica se o personagem está descendo
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point:
                        hits[0].point = False
                        self.score += 1  # Incrementa a pontuação quando o personagem passa por uma plataforma
                    # Reposiciona o personagem no topo da plataforma
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0  # Define a velocidade vertical como zero
                    self.jumping = False  # Define que o personagem não está mais pulando

    def draw(self):
        if self.direction == "left":
            self.surf = self.surf_left  # Usa a imagem voltada para a esquerda
        elif self.direction == "right":
            self.surf = self.surf_right  # Usa a imagem voltada para a direita
        # Desenha a imagem do personagem na tela
        displaysurface.blit(self.surf, self.rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, width=43, height=28):
        super().__init__()

        # Carrega as imagens do morcego virado para a esquerda e para a direita
        self.surf_left = pygame.image.load("assets/enemy_right.png")
        self.surf_right = pygame.image.load("assets/enemy_left.png")
        # Inicialmente, carrega a imagem do morcego virado para a esquerda
        self.surf = self.surf_left
        self.rect = self.surf.get_rect()  # Obtém o retângulo da imagem do morcego

        # Define a posição inicial do morcego no lado esquerdo ou direito da tela
        if random.choice([True, False]):
            self.rect.left = 0
            # Define a velocidade para a direita
            self.speed = random.randint(1, 3)
        else:
            self.rect.right = WIDTH
            # Define a velocidade para a esquerda
            self.speed = random.randint(-3, -1)

        # Define a posição vertical aleatória
        self.rect.centery = random.randint(0, HEIGHT - 30)

        self.point = True  # Variável para controlar se o morcego já pontuou
        self.moving = True  # Variável para controlar se o morcego está se movendo

    def move(self):
        # Verifica colisões entre o morcego e o jogador
        hits = self.rect.colliderect(P1.rect)
        if self.moving:
            # Move o morcego horizontalmente com base na velocidade
            self.rect.move_ip(self.speed, 0)
            if hits:
                global game_over
                game_over = True  # Define que o jogo acabou se houver colisão com o jogador
                P1.pos.x += self.speed  # Move o jogador horizontalmente na direção oposta ao morcego
            if self.speed > 0 and self.rect.left > WIDTH:
                self.kill()  # Remove o morcego se estiver fora da tela à direita
            if self.speed < 0 and self.rect.right < 0:
                self.kill()  # Remove o morcego se estiver fora da tela à esquerda

        self.update_image()  # Atualiza a imagem do morcego

    def update_image(self):
        if self.speed > 0:
            self.surf = self.surf_right  # Usa a imagem do morcego virado para a direita
        else:
            self.surf = self.surf_left  # Usa a imagem do morcego virado para a esquerda

        # Redimensiona a imagem do morcego para o tamanho do retângulo
        self.surf = pygame.transform.scale(
            self.surf, (self.rect.width, self.rect.height))


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.image.load(
            "assets/Coin.png")  # Carrega a imagem da moeda
        self.rect = self.image.get_rect()  # Obtém o retângulo da imagem

        self.rect.topleft = pos  # Define a posição inicial da moeda

    def update(self):
        # Verifica colisões entre a moeda e o jogador
        if self.rect.colliderect(P1.rect):
            P1.score += 5  # Incrementa a pontuação do jogador
            self.kill()  # Remove a moeda


class Platform(pygame.sprite.Sprite):
    def __init__(self, width=0, height=18):
        super().__init__()

        if width == 0:
            # Define uma largura aleatória se não for especificada
            width = random.randint(50, 120)

        # Carrega a imagem da plataforma
        self.image = pygame.image.load("assets/platform.png")
        # Redimensiona a imagem para a largura e altura desejadas
        self.surf = pygame.transform.scale(self.image, (width, height))
        # Obtém o retângulo da imagem e define a posição central aleatória
        self.rect = self.surf.get_rect(
            center=(random.randint(0, WIDTH-10), random.randint(0, HEIGHT-30)))

        self.point = True  # Variável para controlar se a plataforma já pontuou
        self.moving = True  # Variável para controlar se a plataforma está se movendo
        # Define a velocidade de movimento da plataforma
        self.speed = random.randint(-1, 1)

        if self.speed == 0:
            self.moving = False  # Se a velocidade for zero, a plataforma não se move

    def generateCoin(self):
        if self.speed == 0:
            # Gera uma moeda acima da plataforma se ela estiver parada
            coins.add(Coin((self.rect.centerx, self.rect.centery - 50)))

    def move(self):
        # Verifica colisões entre a plataforma e o jogador
        hits = self.rect.colliderect(P1.rect)
        if self.moving:
            # Move a plataforma horizontalmente com base na velocidade
            self.rect.move_ip(self.speed, 0)
            if hits:
                # Move o jogador horizontalmente junto com a plataforma em caso de colisão
                P1.pos += (self.speed, 0)
            if self.speed > 0 and self.rect.left > WIDTH:
                # Reposiciona a plataforma no lado esquerdo da tela se estiver fora da tela à direita
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                # Reposiciona a plataforma no lado direito da tela se estiver fora da tela à esquerda
                self.rect.left = WIDTH


def check(platform, groupies):
    # Verifica colisões entre a plataforma e o grupo de sprites
    if pygame.sprite.spritecollideany(platform, groupies):
        return True  # Retorna True se houver colisões
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top) < 40):
                return True  # Retorna True se houver sobreposição ou proximidade entre plataformas
        return False  # Retorna False se não houver colisões ou sobreposição


def plat_gen():
    while len(platforms) < 6:  # Gera novas plataformas até que haja 6 no total
        # Define uma largura aleatória para a plataforma
        width = random.randrange(50, 100)
        p = Platform()
        C = True

        while C:
            p = Platform()
            # Define uma posição aleatória para a plataforma
            p.rect.center = (random.randrange(
                0, WIDTH - width), random.randrange(-50, 0))
            # Verifica se há colisões ou sobreposição com outras plataformas
            C = check(p, platforms)

        p.generateCoin()  # Gera uma moeda acima da plataforma
        platforms.add(p)  # Adiciona a plataforma ao grupo de plataformas
        all_sprites.add(p)  # Adiciona a plataforma a todos os sprites


all_sprites = pygame.sprite.Group()  # Cria um grupo para todos os sprites
platforms = pygame.sprite.Group()  # Cria um grupo para as plataformas
coins = pygame.sprite.Group()  # Cria um grupo para as moedas
enemies = pygame.sprite.Group()  # Cria um grupo para os inimigos

# Cria uma plataforma específica (PT1) com largura e altura definidas
PT1 = Platform(450, 80)

background = pygame.image.load(
    "assets/background.png")  # Carrega a imagem de fundo

PT1.rect = PT1.surf.get_rect(
    center=(WIDTH/2, HEIGHT - 10))  # Define a posição da PT1
PT1.moving = False  # Define PT1 como não se movendo
PT1.point = False  # Define PT1 como não pontuando

P1 = Player()  # Cria um jogador (P1)
E1 = Enemy()  # Cria um inimigo (E1)

all_sprites.add(PT1)  # Adiciona PT1 a todos os sprites
all_sprites.add(P1)  # Adiciona P1 a todos os sprites
all_sprites.add(E1)  # Adiciona E1 a todos os sprites
platforms.add(PT1)  # Adiciona PT1 ao grupo de plataformas

for x in range(random.randint(4, 5)):  # Gera um número aleatório de plataformas adicionais
    C = True
    pl = Platform()
    while C:
        pl = Platform()
        # Verifica colisões ou sobreposições com outras plataformas
        C = check(pl, platforms)
    pl.generateCoin()  # Gera uma moeda acima da plataforma
    platforms.add(pl)  # Adiciona a plataforma ao grupo de plataformas
    all_sprites.add(pl)  # Adiciona a plataforma a todos os sprites

# Define o tempo para o próximo spawn de inimigo
enemy_spawn_time = pygame.time.get_ticks() + random.randint(3000, 6000)
game_over = False

while not game_over:
    P1.update()  # Atualiza o jogador
    E1.update()  # Atualiza o inimigo
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

    # Verifica colisões entre o jogador e os inimigos
    if pygame.sprite.spritecollideany(P1, enemies):
        game_over = True
        P1.vel.y = 0  # Para o movimento vertical do jogador

    if P1.rect.top > HEIGHT:  # Verifica se o jogador caiu abaixo da tela
        game_over = True

    if game_over:  # Se o jogo acabou
        for entity in all_sprites:
            entity.kill()  # Remove todos os sprites
        time.sleep(1)
        # Preenche a tela com uma cor vermelha
        displaysurface.fill((255, 0, 0))
        pygame.display.update()
        time.sleep(1)
        pygame.quit()
        sys.exit()

    if P1.rect.top <= HEIGHT / 3:  # Move o jogador e as plataformas para cima
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()  # Remove as plataformas que estão fora da tela

        for coin in coins:
            coin.rect.y += abs(P1.vel.y)
            if coin.rect.top >= HEIGHT:
                coin.kill()  # Remove as moedas que estão fora da tela

    if pygame.time.get_ticks() > enemy_spawn_time:  # Verifica se é hora de gerar um novo inimigo
        enemy_spawn_time = pygame.time.get_ticks() + random.randint(3000, 6000)
        E = Enemy()
        all_sprites.add(E)
        enemies.add(E)  # Adiciona o inimigo ao grupo de inimigos

    plat_gen()  # Gera novas plataformas se necessário
    displaysurface.blit(background, (0, 0))  # Desenha o fundo na tela
    f = pygame.font.SysFont("Verdana", 20)  # Define a fonte do texto
    # Renderiza o texto do score
    g = f.render(str(P1.score), True, (123, 255, 0))
    displaysurface.blit(g, (WIDTH/2, 10))  # Desenha o score na tela

    for entity in all_sprites:
        # Desenha os sprites na tela
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()  # Move os sprites

    for coin in coins:
        displaysurface.blit(coin.image, coin.rect)  # Desenha as moedas na tela
        coin.update()  # Atualiza as moedas

    P1.draw()  # Desenha o jogador na tela

    pygame.display.update()  # Atualiza a tela
    FramePerSec.tick(FPS)  # Controla a taxa de quadros por segundo
