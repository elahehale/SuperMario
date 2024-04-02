import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

class Game:
    def __init__(self, world, actions):
        self.world = world
        self.actions = actions
        self.action = 0
        self.round = 0
        self.round_len = len(world)
        self.w = min(1500 / self.round_len, 70)
        self.SCREEN_WIDTH = self.w * (2 + self.round_len)
        self.SCREEN_HEIGHT = 450
        self.color = (52, 195, 235)
        self.round = 0
        self.jumps = []

        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.tiles = []
        self.mushrooms = []
        self.lakipus = []
        self.gumpas = []
        self.player = pygame.image.load("assets/player.png").convert_alpha()
        self.player_ratio = self.player.get_rect().width / self.player.get_rect().height

    def load_images(self):
        for i in range(self.round_len):
            imp = pygame.image.load("assets/tile.png").convert_alpha()
            ratio = imp.get_rect().width / imp.get_rect().height
            width = self.w
            height = width / ratio
            imp = pygame.transform.scale(imp, (width, height))
            self.tiles.append(imp)
            self.screen.blit(imp, (self.w + width * i, 450 - height))

        for i in range(self.round_len):
            if self.world[i] == 'M':
                imp = pygame.image.load("assets/mushroom.png").convert_alpha()
                ratio = imp.get_rect().width / imp.get_rect().height
                width = self.w
                height = width / ratio
                imp = pygame.transform.scale(imp, (width, height))
                self.screen.blit(imp, (self.w + width * i, 450 - height - self.tiles[0].get_rect().height))
                self.mushrooms.append((imp, i))

        for i in range(self.round_len):
            if self.world[i] == 'G':
                imp = pygame.image.load("assets/gumpa.png").convert_alpha()
                ratio = imp.get_rect().width / imp.get_rect().height
                width = self.w
                height = width / ratio
                imp = pygame.transform.scale(imp, (width, height))
                self.screen.blit(imp, (self.w + width * i, 450 - height - self.tiles[0].get_rect().height))
                self.gumpas.append((imp, i))

        for i in range(self.round_len):
            if self.world[i] == 'L':
                imp = pygame.image.load("assets/lakipu.png").convert_alpha()
                ratio = imp.get_rect().width / imp.get_rect().height
                width = self.w
                height = width / ratio
                imp = pygame.transform.scale(imp, (width, height))
                self.screen.blit(imp, (self.w + width * i, 430 - 2 * self.w - imp.get_rect().height))
                self.lakipus.append((imp, i))
        player = pygame.image.load("assets/player.png").convert_alpha()
        player_ratio = player.get_rect().width / player.get_rect().height
        width = self.w
        height = width / player_ratio
        player = pygame.transform.scale(player, (width, height))
        self.screen.blit(player, (self.w, 450 - self.tiles[0].get_rect().height - player.get_rect().height))
        player.get_rect().x
        player.get_rect().y
    def update_screen(self):
        self.screen.fill(self.color)
        height = self.w / self.player_ratio
        player = pygame.transform.scale(self.player, (self.w, height))

        jump = 0
        if self.actions[self.action] == '1':
            jump = self.w
            self.jumps.append(1)
        else:
            self.jumps.append(0)

        if self.actions[self.action] == '2':
            player = pygame.transform.scale(player, (self.w, self.w))

        self.action += 1
        pygame.time.delay(500)

        for i in range(len(self.tiles)):
            self.screen.blit(self.tiles[i], (self.w + self.w * i, 450 - self.tiles[0].get_rect().height))

        if self.action > 1 and self.jumps[self.action - 2] == 0:
            loose = next((index for index, pair in enumerate(self.mushrooms) if pair[1] == self.action - 1), -1)
            if loose > -1:
                self.mushrooms = self.mushrooms[:loose] + self.mushrooms[loose + 1:]

        for i in range(len(self.mushrooms)):
            self.screen.blit(self.mushrooms[i][0],
                             (self.w + self.w * self.mushrooms[i][1], 450 - self.mushrooms[i][0].get_rect().height - self.tiles[0].get_rect().height))

        for i in range(len(self.lakipus)):
            self.screen.blit(self.lakipus[i][0], (self.w + self.w * self.lakipus[i][1], 430 - 2 * self.w - self.lakipus[i][0].get_rect().height))

        if self.action > 2 and self.jumps[self.action - 3] == 1 and self.jumps[self.action - 2] == 0:
            loose = next((index for index, pair in enumerate(self.gumpas) if pair[1] == self.action - 1), -1)
            if loose > -1:
                self.gumpas = self.gumpas[:loose] + self.gumpas[loose + 1:]

        for i in range(len(self.gumpas)):
            self.screen.blit(self.gumpas[i][0],
                             (self.w + self.w * self.gumpas[i][1], 450 - self.gumpas[i][0].get_rect().height - self.tiles[0].get_rect().height))

        self.screen.blit(player, (self.action * self.w + self.w, 450 - self.tiles[0].get_rect().height - player.get_rect().height - jump))
        pygame.display.flip()

    def run(self):
        running = True
        self.screen.fill(self.color)
        self.load_images()
        pygame.display.flip()
        pygame.time.delay(500)

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                elif event.type == QUIT:
                    running = False

            self.update_screen()

        pygame.quit()

# # Example usage
# world = "__G___L_"
# actions = "10010202"
# game = Game(world, actions)
# game.run()
