import pygame
from pygame.locals import *

vec = pygame.math.Vector2  # 2 for two dimensional


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf_left = pygame.image.load("snowman_left.png")
        self.surf_right = pygame.image.load("snowman_right.png")
        self.surf = self.surf_right  # Inicialmente, carrega a imagem voltada para a direita
        self.rect = self.surf.get_rect()

        self.pos = vec((10, 360))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = False
        self.score = 0
        self.direction = "right"  # Inicialmente, o personagem está voltado para a direita

    def move(self):
        self.acc = vec(0, 0.5)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
            # Altera a direção para "left" quando a tecla "left" é pressionada
            self.direction = "left"
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
            # Altera a direção para "right" quando a tecla "right" é pressionada
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
