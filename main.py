import os
import sys
import pygame

pygame.init()
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
lvl = 1
k = 0
score = 0

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


images = {
    "land": pygame.transform.scale(load_image('land.png'), (50, 50)),
    "grass": pygame.transform.scale(load_image('grass.png'), (50, 50)),
    "door": pygame.transform.scale(load_image('door.png'), (75, 125))
}
player_image = pygame.transform.scale(load_image('player.png'), (100, 100))
coin_image = pygame.transform.scale(load_image('coin.png'), (50, 50))
tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(coins_group, all_sprites)
        self.image = coin_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width, tile_height + 800)
        self.jmp = 0
        self.gravity = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.dx = 0
        self.k = 1


    def update(self):
        global player, level_x, level_y, land_list, exit_dr, k, lvl, score
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.jmp == 0:
            self.gravity = -12
            self.jmp = 1
        if not key[pygame.K_UP]:
            self.jmp = 0
        if key[pygame.K_RIGHT]:
            self.dx = 4
        if key[pygame.K_LEFT]:
            self.dx = -4

        self.gravity += 1
        if self.gravity > 8:
            self.gravity = 8
        self.rect.y += self.gravity

        for tile in land_list:
            if tile.colliderect(self.rect.x + self.dx, self.rect.y - 1, self.width, self.height):
                self.dx = 0
            if tile.colliderect(self.rect.x, self.rect.y + self.gravity, self.width, self.height):
                if self.gravity < 0:
                    self.rect.y += (tile.bottom - self.rect.top)
                    self.gravity = 0
                elif self.gravity >= 0:
                    self.rect.y += (tile.top - self.rect.bottom)
                    self.gravity = 0
        for move in exit_dr:
            if move.colliderect(self.rect.x, self.rect.y + self.gravity, self.width, self.height):
                all_sprites.empty()
                tiles_group.empty()
                player_group.empty()
                coins_group.empty()
                k = 1
                if k == 1:
                    lvl += 1
                    k = 0
                player, level_x, level_y, land_list, exit_dr = generate_level(load_level(f"lvl{lvl}.txt"))
        for coin in coins_group:
            if self.rect.colliderect(coin.rect):
                score += 10
                coin.kill()
        self.rect.x += self.dx
        if not key[pygame.K_LEFT] or not key[pygame.K_RIGHT]:
            self.dx = 0

        score_text = [f"СЧЁТ: {score}"]

        font = pygame.font.Font(None, 30)
        text_coord = 10
        for line in score_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            score_rect = string_rendered.get_rect()
            score_rect.top = text_coord
            score_rect.x = 10
            screen.blit(string_rendered, score_rect)


player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
coins_group = pygame.sprite.Group()



def generate_level(level):
    new_player, x, y = None, None, None
    land_list = []
    exit_dr = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                image = images["land"]
                rect = image.get_rect().move(
                    tile_width * x, tile_height * y)
                land_list.append(rect)
                Tile("land", x, y)
            elif level[y][x] == '@':
                Tile('grass', x, y)
                image = images["grass"]
                rect = image.get_rect().move(
                    tile_width * x, tile_height * y)
                land_list.append(rect)
            elif level[y][x] == '$':
                Tile('door', x - 0.5, y - 1.5)
                image = images["door"]
                rect = image.get_rect().move(tile_width * x, tile_height * y)
                exit_dr.append(rect)
            elif level[y][x] == "&":
                new_player = Player(x, y)
            elif level[y][x] == "%":
                Coin(x, y)

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y, land_list, exit_dr


player, level_x, level_y, land_list, exit_dr = generate_level(load_level('lvl1.txt'))

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
    player_group.draw(screen)
    exit_group.draw(screen)
    coins_group.draw(screen)
    all_sprites.update()
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
