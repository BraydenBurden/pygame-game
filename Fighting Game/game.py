import pygame, sys
from sprites import *
from config import *
import random

class Game:
    def __init__(self):
        # new game starts
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.font = pygame.font.Font('arial.ttf', 32)

        self.character_spritesheet = Spritesheet('assets/character1.png')
        self.terrain_spritesheet = Spritesheet('assets/floor-sheet.png')
        self.enemy_spritesheet = Spritesheet('assets/enemy.png')
        self.attack_spritesheet = Spritesheet('assets/attack.png')
        self.intro_background = pygame.image.load('assets/intro-background.png')
        self.go_background = pygame.image.load('assets/game-over-background.png')
    
    def create_tilemap(self):
        for i, row in enumerate(tilemap2):
            for j, column in enumerate(row):
                if column != " ":
                    Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "E":
                    Enemy(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.create_tilemap()
        
    def events(self):
        # game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - TILE_SIZE)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + TILE_SIZE)
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x - TILE_SIZE, self.player.rect.y)
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x + TILE_SIZE, self.player.rect.y)

    def update(self):
        # game loop updates
        self.all_sprites.update()

    def draw(self):
        # game loop draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        # game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        go_text = Text_Box((WIN_WIDTH/2 - 140), (WIN_HEIGHT/6.7), 280, 50, WHITE, ORANGE, 'Game Over', 32)

        restart_button = Button((WIN_WIDTH/2 - 60), (WIN_HEIGHT/3.5), 120, 50, WHITE, ORANGE, 'Restart', 32)

        quit_button = Button((WIN_WIDTH/2 - 60), (WIN_HEIGHT/2.5), 120, 50, WHITE, ORANGE, 'Quit', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()
            if quit_button.is_pressed(mouse_pos, mouse_pressed):
                pygame.quit()
                sys.exit()

            self.screen.blit(self.go_background, (0,0))
            self.screen.blit(go_text.image ,go_text.rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.screen.blit(quit_button.image, quit_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        intro = True

        title = Text_Box((WIN_WIDTH/2 - 140), (WIN_HEIGHT/6.7), 280, 50, WHITE, ORANGE, 'Fighting Game', 32)

        play_button = Button((WIN_WIDTH/2 - 60), (WIN_HEIGHT/3.5), 120, 50, WHITE, ORANGE, 'Play', 32)

        quit_button = Button((WIN_WIDTH/2 - 60), (WIN_HEIGHT/2.5), 120, 50, WHITE, ORANGE, 'Quit', 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
            if quit_button.is_pressed(mouse_pos, mouse_pressed):
                pygame.quit()
                sys.exit()

            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title.image, title.rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(quit_button.image, quit_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()
pygame.quit()
sys.exit()