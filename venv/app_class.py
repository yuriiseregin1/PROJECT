import pygame
import sys
import copy
from settings import *
from player_class import *
from enemy_class import *
import sqlite3


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('PACMAN')
        self.running = True
        self.state = 'start'
        self.cell_width = MAZE_WIDTH // COLS
        self.cell_height = MAZE_HEIGHT // ROWS
        self.walls = []
        self.coins = []
        self.enemies = []
        self.e_pos = []
        self.p_pos = None
        self.player_info()
        self.load()
        self.player = Player(self, vec(self.p_pos))
        self.make_enemies()
        with open('settings.txt', 'r') as f:
            self.settings = f.read()
        if self.settings.split()[1] == 'True':
            pygame.mixer.music.load('music.mp3')
            pygame.mixer.music.play()
        pygame.display.set_icon(pygame.image.load('logo.png'))

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
                self.write_record()
                self.check_win()
            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            elif self.state == 'win':
                self.win_events()
                self.win_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2
        screen.blit(text, pos)

    def load(self):
        self.background = pygame.image.load('map1.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx, yidx))
                    elif char == "C":
                        self.coins.append(vec(xidx, yidx))
                    elif char == "P":
                        self.p_pos = [xidx, yidx]
                    elif char in ["2", "3", "4", "5"]:
                        self.e_pos.append([xidx, yidx])
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (xidx*self.cell_width, yidx*self.cell_height,
                                                                  self.cell_width, self.cell_height))

    def check_win(self):
        if str(self.player.current_score) == '287':
            self.state = 'win'
            self.player_record = '287'
            self.player.current_score = '287'

    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, vec(pos), idx))

    def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.background, GREY, (x*self.cell_width, 0),
                             (x*self.cell_width, HEIGHT))
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x*self.cell_height),
                             (WIDTH, x*self.cell_height))

    def reset(self):
        if int(self.player_record) < int(self.player.current_score):
            self.player_record = str(self.player.current_score)
        self.new_output_rec()
        self.player.lives = 3
        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        self.coins = []
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx, yidx))
        self.state = "playing"

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('НАЖМИТЕ ПРОБЕЛ', self.screen, [WIDTH // 2, HEIGHT // 2 - 50], 16, (170, 132, 58), 'arial black', centered=True)
        self.draw_text(str('НАИБОЛЬШЕЕ: ' + self.player_record), self.screen, [4, 0], 16, (255, 255, 255), 'arial black')
        self.draw_text(self.player_name, self.screen, [WIDTH // 2, 15], 16, (170, 132, 58), 'arial black', centered=True)
        pygame.display.update()

    def player_info(self):
        with open('player_info.txt', 'r') as f:
            res = str(f.read())
            self.player_name = res.split()[0]
            self.player_record = res.split()[1]

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))

    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        self.draw_coins()
        self.draw_text('ТЕКУЩИЙ РЕЗУЛЬТАТ: {}'.format(self.player.current_score),
                       self.screen, [60, 0], 18, WHITE, START_FONT)
        self.draw_text(str('НАИБОЛЬШЕЕ: ' + self.player_record), self.screen, [WIDTH//2+60, 0], 18, WHITE, START_FONT)
        self.player.draw()

        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()

    def new_output_rec(self):
        self.draw_text(str('НАИБОЛЬШЕЕ: ' + self.player_record), self.screen, [WIDTH // 2 + 60, 0], 18, WHITE,
                       START_FONT)
        pygame.display.flip()

    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = "game over"
        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0

    def write_record(self):
        if int(self.player.current_score) > int(self.player_record):
            con = sqlite3.connect("base.bd")
            cur = con.cursor()
            cur.execute("""UPDATE players 
                        SET record = (?)
                        WHERE name = (?)""", (self.player.current_score, self.player_name))
            con.commit()

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (124, 123, 7),
                               (int(coin.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2,
                                int(coin.y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_BUFFER//2), 5)

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_update(self):
        pass

    def game_over_draw(self):
        self.screen.fill(BLACK)
        quit_text = "ДЛЯ ВЫХОДА НАЖМИТЕ ESC"
        again_text = "НАЖМИТЕ ПРОБЕЛ ДЛЯ ПЕРЕЗАПУСКА"
        self.draw_text("ИГРА ОКОНЧЕНА", self.screen, [WIDTH//2, 100],  52, RED, "arial", centered=True)
        self.draw_text(again_text, self.screen, [
                       WIDTH//2, HEIGHT//2],  36, (190, 190, 190), "arial", centered=True)
        self.draw_text(quit_text, self.screen, [
                       WIDTH//2, HEIGHT//1.5],  36, (190, 190, 190), "arial", centered=True)
        pygame.display.update()

    def win_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def win_draw(self):
        self.screen.fill(BLACK)
        quit_text = "ДЛЯ ВЫХОДА НАЖМИТЕ ESC"
        again_text = "НАЖМИТЕ ПРОБЕЛ ДЛЯ ПЕРЕЗАПУСКА"
        self.draw_text("ПОБЕДА", self.screen, [WIDTH // 2, 100], 52, (255, 255, 0), "arial", centered=True)
        self.draw_text(again_text, self.screen, [
            WIDTH // 2, HEIGHT // 2], 36, (190, 190, 190), "arial", centered=True)
        self.draw_text(quit_text, self.screen, [
            WIDTH // 2, HEIGHT // 1.5], 36, (190, 190, 190), "arial", centered=True)
        pygame.display.update()


pygame.init()
vec = pygame.math.Vector2