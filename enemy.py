import pygame
import random
from pygame.locals import *

HEIGHT = 450
WIDTH = 400


class Enemy(pygame.sprite.Sprite):
    def __init__(self, width=43, height=28):
        super().__init__()

        self.original_image = pygame.image.load("batleft.gif")
        self.surf = pygame.transform.scale(
            self.original_image, (width, height))
        self.rect = self.surf.get_rect()

        # Set the initial x position on either the left or right side of the screen
        if random.choice([True, False]):
            self.rect.left = 0
            self.speed = random.randint(1, 3)
        else:
            self.rect.right = WIDTH
            self.speed = random.randint(-3, -1)

        self.rect.centery = random.randint(0, HEIGHT - 30)

        self.point = True
        self.moving = True

    def move(self):
        hits = self.rect.colliderect(P1.rect)
        if self.moving:
            self.rect.move_ip(self.speed, 0)
            if hits:
                global game_over
                game_over = True
                P1.pos.x += self.speed
            if self.speed > 0 and self.rect.left > WIDTH:
                self.kill()
            if self.speed < 0 and self.rect.right < 0:
                self.kill()

    def update_image(self):
        # Scale the image using the original dimensions
        self.surf = pygame.transform.scale(
            self.original_image, (self.rect.width, self.rect.height))
