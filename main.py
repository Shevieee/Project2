import os
import sys
import pygame

pygame.init()
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["", "",
                  ""]

    fon = pygame.transform.scale(load_image('background.jpg'), (1000, 1000))
    screen.blit(fon, (0, 0))
    start_btn = pygame.transform.scale(load_image('start_btn.png'), (279, 126))
    screen.blit(start_btn, (150, 400))
    exit_btn = pygame.transform.scale(load_image('exit_btn.png'), (186, 72))
    screen.blit(exit_btn, (664, 423))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (664 <= x <= 850) and (423 <= y <= 495):
                    terminate()
                if (180 <= x <= 367) and (423 <= y <= 493):
                    return
        pygame.display.flip()
        clock.tick(60)


start_screen()


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


level = load_level("lvl1.txt")
images = {
    "grass": pygame.transform.scale(load_image('grass.png'), (50, 50)),
    "land": pygame.transform.scale(load_image('land.png'), (50, 50)),
    "door": pygame.transform.scale(load_image('door.png'), (75, 125))
}

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('land', x, y)
            elif level[y][x] == '@':
                Tile('grass', x, y)
            elif level[y][x] == '$':
                Tile('door', x - 0.5, y - 1.5)
    # вернем игрока, а также размер поля в клетках
    return x, y


level_x, level_y = generate_level(load_level('lvl1.txt'))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(pygame.Color("white"))
    fon = pygame.transform.scale(load_image('background.jpg'), (1000, 1000))
    screen.blit(fon, (0, 0))
    all_sprites.draw(screen)
    tiles_group.draw(screen)
    all_sprites.update()
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
