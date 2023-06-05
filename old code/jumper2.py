import sys
import pygame
import random
import time
pygame.init()
vec = pygame.math.Vector2

height = 900
width = 400
ACC = 0.5
FRIC = -0.12
FPS = 60
difficulty = 0
timer = 0

FramePerSecond = pygame.time.Clock()

displaySurface = pygame.display.set_mode((width, height))
pygame.display.set_caption("PlatformGame")


class Player(pygame.sprite.Sprite):
    def __init__(self, color=(255, 0, 0), nb=1):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.pos = vec(10, 850)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = False
        self.score = 0
        self.nb = nb

    def move(self):
        self.acc = vec(0, 0.5)
        pressed_keys = pygame.key.get_pressed()

        if self.nb == 1:
            if pressed_keys[pygame.K_LEFT]:
                self.acc.x = -ACC
            if pressed_keys[pygame.K_RIGHT]:
                self.acc.x = ACC
        if self.nb == 2:
            if pressed_keys[pygame.K_q]:
                self.acc.x = -ACC
            if pressed_keys[pygame.K_d]:
                self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > width:
            self.pos.x = 0
            self.score += 2
        if self.pos.x < 0:
            self.score += 2
            self.pos.x = width

        self.rect.midbottom = self.pos

    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            pygame.mixer.Sound("PlatformJump.mp3").play()
            self.jumping = True
            self.vel.y = -17

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0:
            if hits:
                if self.rect.y < hits[0].rect.bottom:
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False
                    if hits[0].point == True:
                        hits[0].point = False
                        self.score += 1


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((random.randint(50, 100), 20))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(
            center=(random.randint(0, width-10), random.randint(0, height-30)))
        self.moving = True
        self.speed = random.randint(-1, 1)
        self.point = True

    def move(self):
        if self.moving == True:
            self.rect.move_ip(self.speed, 0)
            if self.speed > 0 and self.rect.left > width - self.image.get_width():
                self.speed = self.speed * (-1)
            if self.speed < 0 and self.rect.right < self.image.get_width():
                self.speed = self.speed * (-1)


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
    while len(platforms) < 12:
        WIDTH = random.randrange(50, 100)
        p = Platform()
        C = True

        while C:
            p = Platform()
            p.rect.center = (random.randrange(
                0, width - WIDTH), random.randrange(-50, 0))
            C = check(p, platforms)

        platforms.add(p)
        all_sprites.add(p)


P1 = Player()
P2 = Player((255, 255, 255), 2)

PT1 = Platform()
PT1.image = pygame.Surface((width, 20))
PT1.image.fill((255, 0, 0))
PT1.rect = PT1.image.get_rect(center=(width/2, height - 10))
PT1.moving = False
PT1.point = False

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P2)
all_sprites.add(P1)

platforms = pygame.sprite.Group()
platforms.add(PT1)

for x in range(random.randint(10, 11)):
    C = True
    pl = Platform()
    while C:
        pl = Platform()
        C = check(pl, platforms)
    platforms.add(pl)
    all_sprites.add(pl)

while True:
    P1.update()
    P2.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                P1.jump()
            if event.key == pygame.K_z:
                P2.jump()
            if event.key == pygame.K_1:
                P2.kill()
                difficulty = 1
            if event.key == pygame.K_2:
                P2.kill()
                difficulty = 2
            if event.key == pygame.K_3:
                P2.kill()
                difficulty = 3
            if event.key == pygame.K_4:
                P2.kill()
                difficulty = 4
            if event.key == pygame.K_5:
                P2.kill()
                difficulty = 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                P1.cancel_jump()
            if event.key == pygame.K_z:
                P2.cancel_jump()

    if P1.pos.y < P2.pos.y:
        highestPlayer = P1
    else:
        highestPlayer = P2
    if difficulty == 0:
        if highestPlayer.pos.y <= height/3:
            P1.pos.y += abs(highestPlayer.vel.y)
            P2.pos.y += abs(highestPlayer.vel.y)
            for plat in platforms:
                plat.rect.y += abs(highestPlayer.vel.y)
                if plat.rect.top > height:
                    plat.kill()
    elif difficulty > 0:
        if timer >= FPS * 2:
            P1.pos.y += abs(difficulty)
            for plat in platforms:
                plat.rect.y += abs(difficulty)
                if plat.rect.top > height:
                    plat.kill()
        else:
            timer += 1

    plat_gen()
    displaySurface.fill((0, 0, 0))
    f = pygame.font.SysFont("Verdana", 20)
    g = f.render(str(P1.score), True, (123, 255, 0))
    displaySurface.blit(g, (width/2, 10))

    for entity in all_sprites:
        entity.move()
        displaySurface.blit(entity.image, entity.rect)

    if P1.rect.top > height or P2.rect.top > height:
        for entity in all_sprites:
            entity.kill()
        time.sleep(0.5)
        displaySurface.fill((255, 0, 0))
        pygame.display.update()
        time.sleep(0.5)
        pygame.quit()
        sys.exit()
    pygame.display.update()
    FramePerSecond.tick(FPS)
