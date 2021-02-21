import pygame
from settings import *


pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running, self.status = True, 'begin'
        self.cell_width, self.cell_height = map_width // cols, map_height // rows
        self.walls, self.coins, self.enemies, self.enem_pos, self.player_pos = [], [], [], [], None
        self.load()
        self.player = Player(self, vec(self.p_pos))
        self.create_enemies()

    def run(self):
        while self.running:
            if self.status == 'begin':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.status == 'playing':
                self.plaing_events()
                self.playing_update()
                self.playing_draw()
            elif self.status == 'loss':
                self.loss_events()
                self.loss_update()
                self.loss_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    def write_text(self, text, screen, pos, size, colour, font, centered=False):
        font = pygame.font.SysFont(font, size)
        text1 = font.render(text, False, colour)
        text_size = text1.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_szie[1] // 2
        screen.blit(text1, pos)

    def load(self):
        pass

    def create_enemies(self):
        pass

    def start_events(self):
        pass

    def start_update(self):
        pass

    def start_draw(self):
        pass

    def playing_events(self):
        pass

    def playing_update(self):
        pass

    def playing_draw(self):
        pass

    def end_events(self):
        pass

    def end_update(self):
        pass

    def end_draw(self):
        pass





