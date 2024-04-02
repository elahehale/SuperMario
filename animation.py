import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT, RLEACCEL,
)

# Set up the drawing window
world = "__G___L_"
actions = "10010202"
action = 0
round = 0
roud_len = len(world)
print(roud_len)
w = min(1500 / roud_len, 70)
SCREEN_WIDTH = w * (2 + roud_len)
SCREEN_HEIGHT = 450
color = (52, 195, 235)
roud = 0
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(color)
pygame.display.update()

tiles = []
mushrooms = []
lakipus = []
gumpas = []
for i in range(roud_len):
    imp = pygame.image.load("assets/tile.png").convert_alpha()
    ratio = imp.get_rect().width / imp.get_rect().height
    width = w
    height = width / ratio
    imp = pygame.transform.scale(imp, (width, height))
    tiles.append(imp)
    screen.blit(imp, (w + width * i, 450 - height))

player = pygame.image.load("assets/player.png").convert_alpha()
player_ratio = player.get_rect().width / player.get_rect().height
width = w
height = width / player_ratio
player = pygame.transform.scale(player, (width, height))
screen.blit(player, (w, 450 - tiles[0].get_rect().height - player.get_rect().height))
player.get_rect().x
player.get_rect().y
for i in range(roud_len):
    if world[i] == 'M':
        imp = pygame.image.load("assets/mushroom.png").convert_alpha()
        ratio = imp.get_rect().width / imp.get_rect().height
        width = w
        height = width / ratio
        imp = pygame.transform.scale(imp, (width, height))
        screen.blit(imp, (w + width * i, 450 - height - tiles[0].get_rect().height))
        mushrooms.append((imp, i))
for i in range(roud_len):
    if world[i] == 'G':
        imp = pygame.image.load("assets/gumpa.png").convert_alpha()
        ratio = imp.get_rect().width / imp.get_rect().height
        width = w
        height = width / ratio
        imp = pygame.transform.scale(imp, (width, height))
        screen.blit(imp, (w + width * i, 450 - height - tiles[0].get_rect().height))
        gumpas.append((imp, i))
for i in range(roud_len):
    if world[i] == 'L':
        imp = pygame.image.load("assets/lakipu.png").convert_alpha()
        ratio = imp.get_rect().width / imp.get_rect().height
        width = w
        height = width / ratio
        imp = pygame.transform.scale(imp, (width, height))
        screen.blit(imp, (w + width * i, 430 - 2 * w - imp.get_rect().height))
        lakipus.append((imp, i))

running = True
pygame.display.flip()
pygame.time.delay(500)

# Main loop
jumps = []
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    height = w / player_ratio
    player = pygame.transform.scale(player, (w, height))
    screen.fill(color)
    jump = 0
    print(actions[action])
    if actions[action] == '1':
        jump = w
        jumps.append(1)
    else:
        jumps.append(0)
    if actions[action] == '2':
        player = pygame.transform.scale(player, (w, w))
    action = action + 1
    pygame.time.delay(500)
    for i in range(len(tiles)):
        screen.blit(tiles[i], (w + w * i, 450 - tiles[0].get_rect().height))
    if action > 1 and jumps[action - 2] == 0:
        loose = next((index for index, pair in enumerate(mushrooms) if pair[1] == action - 1), -1)
        if loose > -1:
            mushrooms = mushrooms[:loose] + mushrooms[loose + 1:]
    for i in range(len(mushrooms)):
        screen.blit(mushrooms[i][0],
                    (w + w * mushrooms[i][1], 450 - mushrooms[i][0].get_rect().height - tiles[0].get_rect().height))

    for i in range(len(lakipus)):
        screen.blit(lakipus[i][0], (w + w * lakipus[i][1], 430 - 2 * w - lakipus[i][0].get_rect().height))
    if action > 2 and jumps[action - 3] == 1 and jumps[action - 2] == 0:
        loose = next((index for index, pair in enumerate(gumpas) if pair[1] == action - 1), -1)
        if loose > -1:
            gumpas = gumpas[:loose] + gumpas[loose + 1:]
    for i in range(len(gumpas)):
        screen.blit(gumpas[i][0],
                    (w + w * gumpas[i][1], 450 - gumpas[i][0].get_rect().height - tiles[0].get_rect().height))
    screen.blit(player, (action * w + w, 450 - tiles[0].get_rect().height - player.get_rect().height - jump))
    pygame.display.flip()
