import pygame
from config import *
import math
import random

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.facing ='down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(8, 0, 16, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.health = 100

        self.down_animations = [self.game.character_spritesheet.get_sprite(8, 0, 16, self.height), 
                            self.game.character_spritesheet.get_sprite(40, 0, 16, self.height),
                            self.game.character_spritesheet.get_sprite(72, 0, 16, self.height),
                            self.game.character_spritesheet.get_sprite(104, 0, 16, self.height)]

        self.up_animations = [self.game.character_spritesheet.get_sprite(136, 0, 16, self.height), 
                            self.game.character_spritesheet.get_sprite(168, 0, 16, self.height),
                            self.game.character_spritesheet.get_sprite(200, 0, 16, self.height),
                            self.game.character_spritesheet.get_sprite(232, 0, 16, self.height)]

        self.left_animations = [self.game.character_spritesheet.get_sprite(392, 0, 16, self.height), 
                            self.game.character_spritesheet.get_sprite(424, 0, 16, self.height),
                            self.game.character_spritesheet.get_sprite(456, 0, 16, self.height),
                            self.game.character_spritesheet.get_sprite(488, 0, 16, self.height)]

        self.right_animations = [self.game.character_spritesheet.get_sprite(264, 0, 16, self.height), 
                            self.game.character_spritesheet.get_sprite(296, 0, 16, self.height),
                            self.game.character_spritesheet.get_sprite(328, 0, 16, self.height),
                            self.game.character_spritesheet.get_sprite(360, 0, 16, self.height)]

    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()
        

        self.rect.x += self.x_change
        self.collide_blocks("x")
        self.rect.y += self.y_change
        self.collide_blocks("y")
        self.camera()

        self.x_change = 0
        self.y_change = 0
        
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            # for sprite in self.game.all_sprites:
            #     sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_d]:
            # for sprite in self.game.all_sprites:
            #     sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_w]:
            # for sprite in self.game.all_sprites:
            #     sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_s]:
            # for sprite in self.game.all_sprites:
            #     sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'
    
    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    overlap_x = self.rect.right - hits[0].rect.left
                    self.x_change = self.x_change - overlap_x
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    overlap_x = self.rect.left - hits[0].rect.right
                    self.x_change = self.x_change - overlap_x
                    self.rect.x = hits[0].rect.right

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    overlap_y = self.rect.bottom - hits[0].rect.top
                    self.y_change = self.y_change - overlap_y
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    overlap_y = self.rect.top - hits[0].rect.bottom
                    self.y_change = self.y_change - overlap_y
                    self.rect.y = hits[0].rect.bottom
        
    def camera(self):
        if self.x_change:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= self.x_change
        if self.y_change:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= self.y_change

    def animate(self):

        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(40, 0, 16, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 4:
                    self.animation_loop = 1
        
        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(168, 0, 16, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 4:
                    self.animation_loop = 1
        
        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(424, 0, 16, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(296, 0, 16, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 4:
                    self.animation_loop = 1
        
    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            print(self.health)
            self.health -=1
            if self.health == 0:
                self.kill()
                self.game.playing = False

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(["left", "right"])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(20, 30)

        self.image = self.game.enemy_spritesheet.get_sprite(40, 0, 16, self.height)

        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.health = 75

        # down_animations = [self.game.enemy_spritesheet.get_sprite(8, 0, 16, self.height), 
        #                     self.game.enemy_spritesheet.get_sprite(40, 0, 16, self.height),
        #                     self.game.enemy_spritesheet.get_sprite(72, 0, 16, self.height),
        #                     self.game.enemy_spritesheet.get_sprite(104, 0, 16, self.height)]

        # up_animations = [self.game.enemy_spritesheet.get_sprite(136, 0, 16, self.height), 
        #                     self.game.enemy_spritesheet.get_sprite(168, 0, 16, self.height),
        #                     self.game.enemy_spritesheet.get_sprite(200, 0, 16, self.height),
        #                     self.game.enemy_spritesheet.get_sprite(232, 0, 16, self.height)]

        self.left_animations = [self.game.enemy_spritesheet.get_sprite(392, 0, 16, self.height), 
                            self.game.enemy_spritesheet.get_sprite(424, 0, 16, self.height),
                            self.game.enemy_spritesheet.get_sprite(456, 0, 16, self.height),
                            self.game.enemy_spritesheet.get_sprite(488, 0, 16, self.height)]

        self.right_animations = [self.game.enemy_spritesheet.get_sprite(264, 0, 16, self.height), 
                            self.game.enemy_spritesheet.get_sprite(296, 0, 16, self.height),
                            self.game.enemy_spritesheet.get_sprite(328, 0, 16, self.height),
                            self.game.enemy_spritesheet.get_sprite(360, 0, 16, self.height)]

    def update(self):
        self.movement()
        self.animate()
        self.collide_attack()


        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0
    
    def movement(self):
        if self.facing == "left":
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = "right"
        
        if self.facing == "right":
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = "left"

    def animate(self):

        # if self.facing == "down":
        #     if self.y_change == 0:
        #         self.image = self.game.enemy_spritesheet.get_sprite(40, 0, 16, self.height)
        #     else:
        #         self.image = down_animations[math.floor(self.animation_loop)]
        #         self.animation_loop += 0.15
        #         if self.animation_loop >= 4:
        #             self.animation_loop = 1
        
        # if self.facing == "up":
        #     if self.y_change == 0:
        #         self.image = self.game.enemy_spritesheet.get_sprite(168, 0, 16, self.height)
        #     else:
        #         self.image = up_animations[math.floor(self.animation_loop)]
        #         self.animation_loop += 0.15
        #         if self.animation_loop >= 4:
        #             self.animation_loop = 1
        
        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(424, 0, 16, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(296, 0, 16, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 4:
                    self.animation_loop = 1

    def collide_attack(self):
        hits = pygame.sprite.spritecollide(self, self.game.attacks, False)
        if hits:
            print(f'enemy {self.health}')
            self.health -=1
            if self.health == 0:
                self.kill()

    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_spritesheet.get_sprite(0,0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups =self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_spritesheet.get_sprite(32, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Text_Box:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('arial.ttf', fontsize)

        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('arial.ttf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)


        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.animation_loop = 0

        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        self.down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        self.left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        self.up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]

    def update(self):
        self.animate()
        # self.collide()

    # def collide(self):
    #     hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

    
    def animate(self):
        direction = self.game.player.facing

        if direction == 'up':
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
        if direction == 'left':
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
        if direction == 'right':
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
        if direction == 'down':
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
        
