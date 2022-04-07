import pygame, sys
from sprites import *
from config import *
import random

class Game:
    def __init__(self):
        # new game starts
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.attack = pygame.mixer.Sound("sounds/attack.wav")
        self.dead = pygame.mixer.Sound("sounds/dead.wav")
        self.drink_potion = pygame.mixer.Sound("sounds/drink.wav")
        

        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.font = pygame.font.Font('arial.ttf', 32)
        self.font_small = pygame.font.Font('arial.ttf', 16)

        self.character_spritesheet = Spritesheet('assets/character1.png')
        self.terrain_spritesheet = Spritesheet('assets/floor-sheet.png')
        self.enemy_spritesheet = Spritesheet('assets/enemy.png')
        self.attack_spritesheet = Spritesheet('assets/attack.png')
        self.intro_background = pygame.image.load('assets/intro-background.png')
        self.go_background = pygame.image.load('assets/game-over-background.png')
        self.potion_img = pygame.image.load('assets/potion.png')
    
    def create_tilemap(self):
        for i, row in enumerate(tilemap1):
            for j, column in enumerate(row):
                if column != " ":
                    Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "E":
                    self.enemy = Enemy(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)
                if column == "H":
                    Potion(self, j, i)

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.player = pygame.sprite.LayeredUpdates()
        self.potions = pygame.sprite.LayeredUpdates()

        self.create_tilemap()
        
    def events(self):
        # game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pygame.mixer.Sound.set_volume(self.attack, 0.2)
                    pygame.mixer.Sound.play(self.attack)
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
        keys = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        w_key = Rect_Bar((WIN_WIDTH/2 - 40), (WIN_HEIGHT - 80), 20, 20, WHITE, BLACK, 'W', 8)
        if keys[pygame.K_w]:
            w_key = Rect_Bar((WIN_WIDTH/2 - 40), (WIN_HEIGHT - 80), 20, 20, BLACK, WHITE, 'W', 8)

        a_key = Rect_Bar((WIN_WIDTH/2 - 61), (WIN_HEIGHT - 58), 20, 20, WHITE, BLACK, 'A', 8)
        if keys[pygame.K_a]:
            a_key = Rect_Bar((WIN_WIDTH/2 - 61), (WIN_HEIGHT - 58), 20, 20, BLACK, WHITE, 'A', 8)

        s_key = Rect_Bar((WIN_WIDTH/2 - 40), (WIN_HEIGHT - 58), 20, 20, WHITE, BLACK, 'S', 8)
        if keys[pygame.K_s]:
            s_key = Rect_Bar((WIN_WIDTH/2 - 40), (WIN_HEIGHT - 58), 20, 20, BLACK, WHITE, 'S', 8)

        d_key = Rect_Bar((WIN_WIDTH/2 - 19), (WIN_HEIGHT - 58), 20, 20, WHITE, BLACK, 'D', 8)
        if keys[pygame.K_d]:
            d_key = Rect_Bar((WIN_WIDTH/2 - 19), (WIN_HEIGHT - 58), 20, 20, BLACK, WHITE, 'D', 8)

        HuD = Rect_Bar((WIN_WIDTH - WIN_WIDTH), (WIN_HEIGHT - 100), WIN_WIDTH, 200, WHITE, GREY, '', 16)
        health_bar_outline = Rect_Bar((WIN_WIDTH/64 -5), (WIN_HEIGHT/1.2 + 30), 210, 40, WHITE, BLACK, '', 16)
        HEALTH_BAR = Rect_Bar((WIN_WIDTH/64), (WIN_HEIGHT/1.2 + 35), (self.player.health * 2), 30, WHITE, RED, '', 16)
        health_text = Rect_Bar((WIN_WIDTH/64), (WIN_HEIGHT/1.2 + 35), 200, 30, WHITE, TRANSPARENT, f'{self.player.health} / 100', 16)

        movement_text = self.font_small.render("WASD to move player", True, BLACK)

        mouse_click_text = self.font_small.render("Left click to attack", True, BLACK)
        mouse_img = pygame.image.load('assets/mouse.png')
        if mouse_pressed == (True, False, False):
            mouse_img = pygame.image.load('assets/mouse_clicked.png')

        self.screen.blit(HuD.image, HuD.rect)

        self.screen.blit(health_bar_outline.image, health_bar_outline.rect)
        self.screen.blit(HEALTH_BAR.image, HEALTH_BAR.rect)
        self.screen.blit(health_text.image, health_text.rect, special_flags=pygame.BLEND_MAX)

        self.screen.blit(w_key.image, w_key.rect)
        self.screen.blit(a_key.image, a_key.rect)
        self.screen.blit(s_key.image, s_key.rect)
        self.screen.blit(d_key.image, d_key.rect)
        self.screen.blit(movement_text, (((WIN_WIDTH/2) - (movement_text.get_width() * 1.5)), (WIN_HEIGHT - 69)))

        self.screen.blit(mouse_img, (WIN_WIDTH/2 +20, WIN_HEIGHT - 80))
        self.screen.blit(mouse_click_text, (WIN_WIDTH/2 + 56, WIN_HEIGHT - 69))

        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        # game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        go_text = Text_Box((WIN_WIDTH/2 - 140), (WIN_HEIGHT/6.7), 280, 50, WHITE, BLACK, 'Game Over', 32)

        restart_button = Button((WIN_WIDTH/2 - 60), (WIN_HEIGHT/3.5), 120, 50, WHITE, BLACK, 'Restart', 32)

        quit_button = Button((WIN_WIDTH/2 - 60), (WIN_HEIGHT/2.5), 120, 50, WHITE, BLACK, 'Quit', 32)

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

        title = Text_Box((WIN_WIDTH/2 - 240), (WIN_HEIGHT - 680), 480, 80, WHITE, BLACK, 'Fighting Game', 64)

        play_button = Button((WIN_WIDTH/2 - 60), (WIN_HEIGHT/2 - 64), 120, 50, WHITE, BLACK, 'Play', 32)

        menu_button = Button((WIN_WIDTH/2 - 60), (WIN_HEIGHT/2), 120, 50, WHITE, BLACK, 'Menu', 32)

        quit_button = Button((WIN_WIDTH/2 - 60), (WIN_HEIGHT/2 + 64), 120, 50, WHITE, BLACK, 'Quit', 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
            if menu_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
                self.menu()
            if quit_button.is_pressed(mouse_pos, mouse_pressed):
                pygame.quit()
                sys.exit()

            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title.image, title.rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(menu_button.image, menu_button.rect)
            self.screen.blit(quit_button.image, quit_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def menu(self):
        menu = True

        title = Text_Box((WIN_WIDTH/2 - 240), (WIN_HEIGHT - 680), 480, 80, WHITE, BLACK, 'Fighting Game', 64)

        back_button = Button((WIN_WIDTH - 1200), (WIN_HEIGHT - 64), 120, 50, WHITE, BLACK, 'Back', 32)

        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if back_button.is_pressed(mouse_pos, mouse_pressed):
                menu = False
                self.intro_screen()

            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title.image, title.rect)
            self.screen.blit(back_button.image, back_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()
    
    def inventory(self):
        inv = True

        inv_title = Text_Box((WIN_WIDTH/2 - 240), (WIN_HEIGHT - 680), 480, 80, WHITE, BLACK, 'Inventory', 64)
        exit_instruction = self.font.render("Press ESC key to exit inventory", True, BLACK)

        while inv:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    inv = False
                    self.running = False
                key_pressed = pygame.key.get_pressed()
                if key_pressed[pygame.K_ESCAPE]:
                    inv = False

            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(inv_title.image, inv_title.rect)
            self.screen.blit(exit_instruction, ((WIN_WIDTH/64), (WIN_HEIGHT/1.2 + 35)))
            self.clock.tick(FPS)
            pygame.display.update()

pygame.mixer.init()
pygame.mixer.music.load("sounds/background_music.wav")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)
g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()
pygame.quit()
sys.exit()