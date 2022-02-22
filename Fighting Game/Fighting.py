import pygame, sys
from pygame.locals import *


pygame.init()

FPS = 30
FramePerSec = pygame.time.Clock()

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (125,125,125)

WIDTH, HEIGHT = 400, 600

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAYSURF.fill(GREY)
pygame.display.set_caption("Fighting")

ENEMY_SPRITE = pygame.image.load("assets/Enemy-Sprite.png")
PLAYER_SPRITE = pygame.image.load("assets/Player-Sprite.png")
HITBOX = pygame.image.load("assets/Hit-Box32.png")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = PLAYER_SPRITE
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        self.attack_image = HITBOX
        self.attack_rect = self.attack_image.get_rect()
        self.attack_offset = self.attack_rect.height
        self.attack = "none"

    def update(self):
        self.attack = "none"
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_a]:
                self.rect.move_ip(-5,0)
        if self.rect.right > 0:
            if pressed_keys[K_d]:
                self.rect.move_ip(5,0)
        if self.rect.top > 0:
            if pressed_keys[K_w]:
                self.rect.move_ip(0,-5)
        if self.rect.bottom > 0:
            if pressed_keys[K_s]:
                self.rect.move_ip(0,5)
        if pressed_keys[K_f]:
            self.attack = "up"        

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.attack != "none":
            self.attack_rect.center = self.rect.center
            self.attack_rect.move_ip(0, -self.attack_offset)
            surface.blit(self.attack_image, self.attack_rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(self)
        self.image = ENEMY_SPRITE
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def update(self):
        


P1 = Player()

def main():
    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        P1.update()

        DISPLAYSURF.fill(GREY)
        P1.draw(DISPLAYSURF)

        pygame.display.update()
        FramePerSec.tick(FPS)

if __name__ == "__main__":
    main()