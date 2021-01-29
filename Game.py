import os
import sys
import pygame

pygame.init()
clock = pygame.time.Clock()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
counter = 2
result = 0
deth = 0
level_result = 0
leveln = 'map2.txt'
player = None
s = pygame.mixer.Sound('data/sounds/Dum_Dee_Dum.wav')
ch = s.play(-1)
ch.set_volume(0.1)
STEP = 30
sc = pygame.display.set_mode((600, 600))
font = pygame.font.Font(None, 32)
label = "Уровень 1; Счет 0"
text = font.render(
    label, True, (255, 0, 0))
place = text.get_rect(
    center=(100, 20))
sc.blit(text, place)
pygame.display.update()


def generate_level(level):
    '''Генерация уровня'''
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '!':
                Tile('door', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '*':
                Tile('empty', x, y)
                Tile('apple', x, y)
            elif level[y][x] == '+':
                Tile('lava', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '$':
                Tile('empty', x, y)
                arr = Arrowup(x, y)
                arrow_group.add(arr)
            elif level[y][x] == '%':
                Tile('empty', x, y)
                arr = Arrowdown(x, y)
                arrow_group.add(arr)
            elif level[y][x] == '>':
                Tile('empty', x, y)
                arr = Arrowright(x, y)
                arrow_group.add(arr)
            elif level[y][x] == '<':
                Tile('empty', x, y)
                arr = Arrowleft(x, y)
                arrow_group.add(arr)

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y, arr


def load_image(name, colorkey=None):
    '''Загрузка картинки'''
    fullname = os.path.join('data/img/', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    ''' '''
    filename = "data/map/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'wall': load_image('wall.png'),
    'empty': load_image('parket.png'),
    'door': load_image('door.png'),
    'apple': load_image('apple.png'),
    'lava': load_image('lava.png')
}
arrow_image = load_image('str.png', -1)
player_image = load_image('dog.png', -1)
arrowg_image = load_image('strg.png', -1)
tile_width = tile_height = 30


class Arrowdown(pygame.sprite.Sprite):
    ''''''

    def __init__(self, pos_x, pos_y):
        super().__init__(arrow_group, all_sprites)
        self.image = arrow_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 10, tile_height * pos_y + 30)
        self.pos_x = pos_x
        self.pos_y = pos_y

    def get_pos(self):
        return self.pos_x, self.pos_y

    def update(self):
        ''''''
        self.rect.y += 2
        if "wall" in [x.get_tile_type() for x in
                      pygame.sprite.spritecollide(self, tiles_group, False)] or self.rect.y == height:
            self.rect = self.image.get_rect().move(
                tile_width * self.pos_x + 10, tile_height * self.pos_y)


class Arrowup(pygame.sprite.Sprite):
    ''''''

    def __init__(self, pos_x, pos_y):
        super().__init__(arrow_group, all_sprites)
        self.image = arrow_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 10, tile_height * pos_y + 30)
        self.pos_x = pos_x
        self.pos_y = pos_y

    def get_pos(self):
        return self.pos_x, self.pos_y

    def update(self):
        ''''''
        self.rect.y -= 2
        if "wall" in [x.get_tile_type() for x in
                      pygame.sprite.spritecollide(self, tiles_group, False)] or self.rect.y == 0:
            self.rect = self.image.get_rect().move(
                tile_width * self.pos_x + 10, tile_height * self.pos_y - 10)


class Arrowleft(pygame.sprite.Sprite):
    ''''''

    def __init__(self, pos_x, pos_y):
        super().__init__(arrow_group, all_sprites)
        self.image = arrowg_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 20, tile_height * pos_y + 10)
        self.pos_x = pos_x
        self.pos_y = pos_y

    def get_pos(self):
        return self.pos_x, self.pos_y

    def update(self):
        ''''''
        self.rect.x -= 2
        if "wall" in [x.get_tile_type() for x in
                      pygame.sprite.spritecollide(self, tiles_group, False)] or self.rect.x == 0:
            self.rect = self.image.get_rect().move(
                tile_width * self.pos_x + 20, tile_height * self.pos_y + 10)


class Arrowright(pygame.sprite.Sprite):
    ''''''

    def __init__(self, pos_x, pos_y):
        super().__init__(arrow_group, all_sprites)
        self.image = arrowg_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 30, tile_height * pos_y + 10)
        self.pos_x = pos_x
        self.pos_y = pos_y

    def get_pos(self):
        return self.pos_x, self.pos_y

    def update(self):
        ''''''
        self.rect.x += 2
        if "wall" in [x.get_tile_type() for x in
                      pygame.sprite.spritecollide(self, tiles_group, False)] or self.rect.x == width:
            self.rect = self.image.get_rect().move(
                tile_width * self.pos_x + 30, tile_height * self.pos_y + 10)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        self.pos_x = pos_x
        self.tile_type = tile_type
        self.pos_y = pos_y
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def get_tile_type(self):
        return self.tile_type

    def get_pos(self):
        return self.pos_x, self.pos_y

    def del_apple(self):
        self.image = tile_images['empty']
        self.tile_type = 'empty'


class Player(pygame.sprite.Sprite):
    ''''''

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos_x = pos_x
        self.pos_y = pos_y

    def get_pos(self):
        return self.pos_x, self.pos_y

    def update(self, x, y):
        self.rect.x += x
        self.rect.y += y
        if pygame.sprite.spritecollide(self, tiles_group, False)[0].get_tile_type() == 'wall':
            if x > 0:
                self.rect.x -= x
            elif x < 0:
                self.rect.x += x
            elif y > 0:
                self.rect.y -= y
            elif y < 0:
                self.rect.y += y

def end_screen():
    ''''''
    intro_text = [
        "Поздравляем!",
        "Вы прошли игру.",
        "Задача игрока - собрать как можно больше яблок.",
        "Статистика игрока:",
        "Количество съеденых яблок - " + str(result),
        "Количество смертей - " + str(deth),
        "",
        "Спасибо за игру!",
        "Для того чтобы закончить игру нажмите пробел"
    ]

    fon = pygame.transform.scale(load_image('1.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    ''''''
    intro_text = [
        "Правила игры:",
        "В игре принимает участие один человек.",
        "Задача игрока - собрать как можно больше яблок.",
        "Чем быстрее вы это сделаете тем лучше.",
        "Игрок должен уклонятся от летящих дротиков.",
        "А также избегать различных ловушек.",
        "Значение кнопок:",
        "W - движение вверх",
        "S - движение вниз",
        "A - движение влево",
        "D - движение вправо",
        "",
        "Для того чтобы начать игру нажмите на пробел."
    ]

    fon = pygame.transform.scale(load_image('1.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


try:
    clock = pygame.time.Clock()
    start_screen()
    screen.fill(pygame.Color("white"))
    level = load_level(leveln)
    player, level_x, level_y, arr = generate_level(level)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    if player.rect.x - 30 >= 0:
                        player.rect.x -= 30
                        if pygame.sprite.spritecollide(player, tiles_group, False)[0].get_tile_type() == 'wall':
                            player.rect.x += 30
                if event.key == pygame.K_d:
                    if player.rect.x + 30 < width:
                        player.rect.x += 30
                        if pygame.sprite.spritecollide(player, tiles_group, False)[0].get_tile_type() == 'wall':
                            player.rect.x -= 30
                if event.key == pygame.K_w:
                    if player.rect.y - 30 >= 0:
                        player.rect.y -= 30
                        if pygame.sprite.spritecollide(player, tiles_group, False)[0].get_tile_type() == 'wall':
                            player.rect.y += 30
                if event.key == pygame.K_s:
                    if player.rect.y + 30 < height:
                        player.update(0, STEP)
        tiles_group.draw(screen)
        if pygame.sprite.spritecollide(player, tiles_group, False)[0].get_tile_type() == 'lava' or len(
                pygame.sprite.spritecollide(player, arrow_group, False)) > 0:
            player_group.draw(screen)
            pygame.display.flip()
            d = pygame.mixer.Sound('data/sounds/die.wav')
            die = d.play(0)
            die.set_volume(5)
            all_sprites = pygame.sprite.Group()
            tiles_group = pygame.sprite.Group()
            player_group = pygame.sprite.Group()
            arrow_group = pygame.sprite.Group()
            level = load_level(leveln)
            player, level_x, level_y, arr = generate_level(level)
            level_result = 0
            deth += 1
        elif len(pygame.sprite.spritecollide(player, tiles_group, False)) > 1 and \
                pygame.sprite.spritecollide(player, tiles_group, False)[1].get_tile_type() == 'apple':
            pygame.sprite.spritecollide(player, tiles_group, False)[1].del_apple()
            Tile('empty', player.get_pos()[0], player.get_pos()[1])
            level_result += 1
            a = pygame.mixer.Sound('data/sounds/apple.wav')
            app = a.play(0)
            app.set_volume(5)
            player_group.draw(screen)
        elif pygame.sprite.spritecollide(player, tiles_group, False)[0].get_tile_type() == 'door':
            newl = pygame.mixer.Sound('data/sounds/level-up.wav')
            newll = newl.play(0)
            counter += 1
            if counter <= 5:
                leveln = 'map' + str(counter) + '.txt'
                all_sprites = pygame.sprite.Group()
                tiles_group = pygame.sprite.Group()
                player_group = pygame.sprite.Group()
                arrow_group = pygame.sprite.Group()
                level = load_level(leveln)
                player, level_x, level_y, arr = generate_level(level)
                result += level_result
                level_result = 0
            else:
                running = False
        elif pygame.sprite.spritecollide(player, tiles_group, False)[0].get_tile_type() != 'wall':
            player_group.draw(screen)
        label = "Уровень " + str(counter - 1) + "; Счёт " + str(level_result + result)
        text = font.render(
            label, True, (255, 0, 0))
        clock.tick(FPS)
        arrow_group.update()
        arrow_group.draw(screen)
        sc.blit(text, place)
        pygame.time.delay(20)
        pygame.display.flip()
    end_screen()



except Exception as e:
    print(type(e).__name__, e.args)
    exit()

pygame.quit()
