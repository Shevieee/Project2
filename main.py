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
dead = 0
clckd = 0
pygame.display.set_caption("Platformer")
strt_menu = pygame.mixer.Sound("data/soundtrack/strt_mn.mp3")
strt_menu.set_volume(0.01)
strt_game = pygame.mixer.Sound("data/soundtrack/strt_gm.mp3")
strt_game.set_volume(0.05)
end_game = pygame.mixer.Sound("data/soundtrack/nd_gm.mp3")
end_game.set_volume(0.05)
jumped = pygame.mixer.Sound("data/soundtrack/jmp.mp3")
jumped.set_volume(0.8)
moneta = pygame.mixer.Sound("data/soundtrack/moneta.mp3")
moneta.set_volume(0.06)
door_cracking = pygame.mixer.Sound("data/soundtrack/door-cracking.mp3")
door_cracking.set_volume(0.8)


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
    fon = pygame.transform.scale(load_image('main/background.jpg'), (1000, 1000))
    screen.blit(fon, (0, 0))
    start_btn = pygame.transform.scale(load_image('main/start_btn.png'), (279, 126))
    screen.blit(start_btn, (150, 400))
    exit_btn = pygame.transform.scale(load_image('main/exit_btn.png'), (186, 72))
    screen.blit(exit_btn, (664, 423))
    while True:
        for event in pygame.event.get():
            strt_menu.play(-1)
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (664 <= x <= 850) and (423 <= y <= 495):
                    terminate()
                if (180 <= x <= 367) and (423 <= y <= 493):
                    strt_menu.stop()
                    return
        pygame.display.flip()
        clock.tick(60)


start_screen()
strt_game.play(-1)


def end_screen():
    global lvl, score
    end_text = ["Поздравляем! Вы прошли игру!",
                f"Ваш счёт: {score}"]
    fon = pygame.transform.scale(load_image('main/background.jpg'), (1000, 1000))
    screen.blit(fon, (0, 0))
    rest_btn = pygame.transform.scale(load_image("main/retry_btn.png"), (186, 70))
    screen.blit(rest_btn, (150, 425))
    exit_btn = pygame.transform.scale(load_image('main/exit_btn.png'), (186, 72))
    screen.blit(exit_btn, (664, 423))
    font = pygame.font.Font(None, 60)
    text_coord_y = 300
    text_coord_x = 180
    for line in end_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        end_rect = string_rendered.get_rect()
        end_rect.x = text_coord_x
        end_rect.y = text_coord_y
        screen.blit(string_rendered, end_rect)
        text_coord_y += 50
        text_coord_x += 195
    strt_menu.play(-1)
    strt_menu.set_volume(0.05)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (664 <= x <= 850) and (423 <= y <= 495):
                    with open("data/scores/score.txt", "w") as file:
                        file.write(f"Уровень за данную игру: {lvl - 1}\n")
                        file.write(f"Счёт за данную игру: {score}")
                        file.close()
                    terminate()
                if (150 <= x <= 336) and (425 <= y <= 495):
                    lvl = 1
                    strt_menu.stop()
                    score = 0
                    player, level_x, level_y, land_list, exit_dr, cactus = generate_level(load_level(f"lvls/lvl1.txt"))
                    strt_game.play(-1)
                    return player, level_x, level_y, land_list, exit_dr, cactus
        pygame.display.flip()
        clock.tick(60)


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
    "land": pygame.transform.scale(load_image('main/land.png'), (50, 50)),
    "grass": pygame.transform.scale(load_image('main/grass.png'), (50, 50)),
    "door": pygame.transform.scale(load_image('main/door.png'), (75, 125)),
    "cactus": pygame.transform.scale(load_image("main/cactus.png"), (50, 50))
}
player_image = pygame.transform.scale(load_image('player/player.png'), (65, 98))
coin_image = pygame.transform.scale(load_image('main/coin.png'), (50, 50))
restart_btn = pygame.transform.scale(load_image("main/retry_btn.png"), (150, 50))
dead_player = pygame.transform.scale(load_image("player/dead.png"), (100, 50))
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


class Cactuss(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(cactus_group, all_sprites)
        self.image = coin_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        global dead
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width, tile_height + 800)
        self.jmp = 0
        self.gravity = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.dx = 0
        self.k = 1
        self.go = 0
        self.frame = 0
        self.direction = 'r'
        self.in_jump = 0
        self.pr = 0
        self.ply1 = 0
        self.ply2 = 0
        self.jmp_count = 0
        dead = 0

    def update(self):
        global player, level_x, level_y, land_list, exit_dr, k, dead, clckd, lvl, score, cactus
        key = pygame.key.get_pressed()
        self.pr = 0
        if key[pygame.K_UP] and self.jmp == 0 and self.pr == 0 and self.jmp_count < 2:
            self.jmp_count += 1
            self.gravity = -16
            self.jmp = 1
            self.in_jump = 1
            self.pr = 1
            jumped.play()

        if not key[pygame.K_UP]:
            self.jmp = 0
        if key[pygame.K_RIGHT]:
            self.dx = 4
            self.go = 1
            self.direction = 'r'
        if key[pygame.K_LEFT]:
            self.dx = -4
            self.go = 1
            self.direction = 'l'

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
                    self.in_jump = 0
                    self.jmp_count = 0
        for move in exit_dr:
            if move.colliderect(self.rect.x, self.rect.y, self.width, self.height):
                door_cracking.play()
                all_sprites.empty()
                tiles_group.empty()
                player_group.empty()
                coins_group.empty()
                k = 1
                if k == 1:
                    lvl += 1
                    k = 0
                if lvl > 8:
                    strt_game.stop()
                    player, level_x, level_y, land_list, exit_dr, cactus = end_screen()
                else:
                    player, level_x, level_y, land_list, exit_dr, cactus = (
                        generate_level(load_level(f"lvls/lvl{lvl}.txt")))
        for coin in coins_group:
            if self.rect.colliderect(coin.rect):
                score += 10
                moneta.play()
                coin.kill()
        for cact in cactus:
            if cact.colliderect(self.rect.x, self.rect.y, self.width, self.height):
                if self.direction == 'r' and dead != -1:
                    self.image = dead_player
                elif dead != -1:
                    self.image = pygame.transform.scale(load_image("player/dead_left.png"), (100, 50))
                self.jmp = -1
                self.dx = 0
                dead = -1
                strt_game.stop()
                if self.ply1 == 0:
                    end_game.play(-1)
                    self.ply1 = 1
                screen.blit(restart_btn, (400, 500))
        self.rect.x += self.dx
        if not key[pygame.K_LEFT] or not key[pygame.K_RIGHT]:
            self.dx = 0
        if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
            self.go = 0
        if not self.in_jump and dead != -1:
            if self.go == 1:
                self.frame += 0.3
                if self.frame > 6:
                    self.frame -= 6
                if self.direction == 'r':
                    animation_images = ["player/player_run_right_1.png", "player/player_run_right_2.png",
                                        "player/player_run_right_3.png", "player/player_run_right_4.png",
                                        "player/player_run_right_5.png", "player/player_run_right_6.png"]
                    self.image = pygame.transform.scale(load_image(animation_images[int(self.frame)]), (75, 98))
                else:
                    animation_images = ["player/player_run_left_1.png", "player/player_run_left_2.png",
                                        "player/player_run_left_3.png", "player/player_run_left_4.png",
                                        "player/player_run_left_5.png", "player/player_run_left_6.png"]
                    self.image = pygame.transform.scale(load_image(animation_images[int(self.frame)]), (75, 98))
            else:
                if self.direction == 'r':
                    self.image = player_image
                else:
                    self.image = pygame.transform.scale(load_image("player/player_left.png"), (65, 98))
        elif dead != -1:
            if self.direction == 'r':
                self.image = pygame.transform.scale(load_image("player/player_jump_right.png"), (65, 98))
            else:
                self.image = pygame.transform.scale(load_image("player/player_jump_left.png"), (65, 98))

        score_text = [f"СЧЁТ: {score}"]
        lvl_text = [f"УРОВЕНЬ: {lvl}"]

        font = pygame.font.Font(None, 30)
        text_coord = 10
        for line in score_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            score_rect = string_rendered.get_rect()
            score_rect.top = text_coord
            score_rect.x = 51
            score_rect.y = 91
            screen.blit(string_rendered, score_rect)
        for line2 in lvl_text:
            string_rendered = font.render(line2, 1, pygame.Color('black'))
            score_rect = string_rendered.get_rect()
            score_rect.top = text_coord
            score_rect.x = 51
            score_rect.y = 51
            screen.blit(string_rendered, score_rect)
        if clckd == 1:
            end_game.stop()
            if self.ply2 == 0:
                strt_game.play(-1)
                self.ply2 = 1
                self.ply1 = 0
                clckd = 0
        if dead == -1:
            self.jmp = -1
            self.gravity = 0


player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
coins_group = pygame.sprite.Group()
cactus_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    land_list = []
    exit_dr = []
    cactus = []
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
            elif level[y][x] == "*":
                Tile("cactus", x, y)
                image = images["cactus"]
                rect = image.get_rect().move(tile_width * x, tile_height * y)
                cactus.append(rect)

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y, land_list, exit_dr, cactus


player, level_x, level_y, land_list, exit_dr, cactus = generate_level(load_level('lvls/lvl1.txt'))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and dead == -1:
            x, y = event.pos
            if (401 <= x <= 549) and (500 <= y <= 550):
                all_sprites.empty()
                tiles_group.empty()
                player_group.empty()
                coins_group.empty()
                clckd = 1
                score = 0
                player, level_x, level_y, land_list, exit_dr, cactus = generate_level(load_level(f"lvls/lvl{lvl}.txt"))
    screen.fill(pygame.Color("white"))
    fon = pygame.transform.scale(load_image('main/background.jpg'), (1000, 1000))
    screen.blit(fon, (0, 0))
    all_sprites.draw(screen)
    tiles_group.draw(screen)
    player_group.draw(screen)
    exit_group.draw(screen)
    coins_group.draw(screen)
    all_sprites.update()
    clock.tick(60)
    pygame.display.flip()

with open("data/scores/score.txt", "w") as file:
    file.write(f"Уровень за данную игру: {lvl}\n")
    file.write(f"Счёт за данную игру: {score}")
    file.close()

pygame.quit()
