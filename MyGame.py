import random

import pygame
from pygame import transform

from item import *


class Monster:
    """
    Класс монстра
    """

    def __init__(self):
        self.difficulty = ['low', 'medium', 'high', 'boss']
        self.monster_statistics = {
            'low': [20, (100, 150), 0.7],  # атака, хп монстра
            'medium': [50, (150, 200), 0.5],
            'high': [75, (200, 250), 0.3],
            'boss': [100, (250, 500), 0.3]
        }
        self.timer = 0
        self.scores = {
            'low': 50,
            'medium': 100,
            'high': 150,
            'boss': 200
        }

        self.x = random.randint(0, 1160)
        self.y = random.randint(0, 610)
        self.diff = random.choices(self.difficulty, weights=[4, 3, 2, 1], k=1)[0]
        self.atk = self.monster_statistics[self.diff][0]
        self.hp = random.randint(self.monster_statistics[self.diff][1][0], self.monster_statistics[self.diff][1][-1])
        self.speed = self.monster_statistics[self.diff][-1]
        self.right = True

    def is_life(self):
        """
        Проверка живой ли монстр, если нет то выпадает дроп
        :return: bool
        """
        if self.hp <= 0:
            item_type = random.choices([Weapon, Armor], weights=[1, 4])[0]
            rar = random.choices(Item.rarities, weights=[5, 4, 3, 2, 1])[0]
            if self.diff == 'boss':
                rar = 'legendary'
            if item_type == Weapon:
                items.append((Weapon(pygame.image.load(f'images/{rar}_sword.gif'), rar, 'sword'),
                              (self.x, self.y), cycle))
            else:
                armor_type = random.choice(['boots', 'trousers', 'helmet', 'breastplate'])

                items.append((Armor(pygame.image.load(f'images/{rar}_{armor_type}.gif'), rar, armor_type),
                              (self.x, self.y), cycle))
            player.score += self.scores[self.diff]
            return False
        return True

    def monster_move(self):
        """
        Движение монстра по карте (автоматически)
        :return: None
        """
        if self.hp > 0:
            if player.x != int(self.x):
                if player.x > self.x:
                    self.x += self.speed
                    self.right = True
                else:
                    self.x -= self.speed
                    self.right = False
            if player.y != int(self.y):
                if player.y > self.y:
                    self.y += self.speed
                else:
                    self.y -= self.speed

    def attack(self):
        """
        Атака по игроку (автоматически) + кд
        :return None
        """
        if player.attack_range() and self.hp > 0 >= self.timer and not player.immortality:
            player.damage_taken(self.atk)
            self.timer = 500


class Player:
    """
    Класс игрока
    """

    def __init__(self):
        self.health = 500
        self.attack = 50
        self.x = 580
        self.y = 305
        self.timer = 0
        self.score = 0
        self.right = True
        self.immortality = False
        self.inventory = {
            'sword': '',
            'helmet': '',
            'breastplate': '',
            'trousers': '',
            'boots': ''
        }
        self.items_inventory = [0, 0, 0]

    def damage_taken(self, damage):
        """
        Функция отнимает здоровье персонажа (броня блокирует процент урона максимум блокировки урона - 60%)
        :param damage: int
        :return: None
        """
        if not self.immortality:
            self.health -= damage / 100 * (  # ?
                    100 - (sum([armor.stat for armor in list(self.inventory.values())[1:] if armor])))
            # получение урона

    def damage_given(self):  # Нанесение урона мобу
        """
        Отнимает здоровье у монстра (начальный урон + дополнительный урон от меча)
        :return: None
        """
        if self.attack_range():
            if monsters.hp > 0 >= player.timer and self.health >= 0:  # ?
                if not self.immortality:
                    monsters.hp -= self.attack + (self.inventory['sword'].stat if self.inventory['sword'] else 0)
                else:
                    monsters.hp -= 500
                monsters.is_life()
                player.timer = 300

    def attack_range(self):  # радиус атаки
        """
        Возвращает True/False в зависимости от того насколько близко монстр находится к игроку (до 128 пикселей - True)
        :return: bool
        """
        return -128 <= self.x - monsters.x <= 128 and -128 <= self.y - monsters.y <= 128

    def move_left(self):  # Движение игрока по карте
        """
        Перемещает персонажа по оси Х влево
        :return: None
        """
        if self.x - 1 >= 0 and self.health > 0:
            self.x -= 1
            self.right = False

    def move_right(self):  # Движение игрока по карте
        """
        Перемещает персонажа по оси Х вправо
        :return: None
        """
        if self.x + 1 <= 1160 and self.health > 0:
            self.x += 1
            self.right = True

    def move_down(self):  # Движение игрока по карте
        """
        Перемещает персонажа по оси У вниз
        :return: None
        """
        if self.y + 1 <= 610 and self.health > 0:
            self.y += 1

    def move_up(self):  # Движение игрока по карте
        """
        Перемещает персонажа по оси У вверх
        :return: None
        """
        if self.health > 0:
            if self.y - 1 >= 0:
                self.y -= 1

    def move(self, key):
        pass  # ?

    def find_item(self, x, y):
        """
        Возвращает True/False в зависимости от того находится ли персонаж рядом с зельем
        (расстояние, для того чтобы подобрать предмет)
        :param x: int
        :param y: int
        :return: bool
        """
        return -64 <= self.x - x <= 64 and -64 <= self.y - y <= 64


def draw_models():
    """
    Загружает модельки героя, монстра, и лежащего предмета
    :return: None
    """
    global monster_model_right, monster_model_left, player_model_right, player_model_left
    if bottle.is_created():
        window.blit(potion_model, bottle.cords)  # загружаем модельку выпавшего оружия на землю (не подобранное)

    window.blit(monster_model_right if monsters.right else monster_model_left, (monsters.x, monsters.y))
    window.blit(player_model_right if player.right else player_model_left, (player.x, player.y))
    # загружаем модельку игрока и монстра смотрящую в ту сторону куда направлено движение (право лево)


def items_draw():
    y = 64  # вывод снаряжения
    for item in player.inventory.values():
        if item:
            window.blit(item.image, (width - 64, y - 64))
            window.blit(font.render(str(item.stat), True, 'white'), (1280 - 80, y - 24))
        y += 64


def write_stats():
    """
    Выводит на экран игры все надписи (хп героя, хп монстра, кд, хил, результат)
    :return: None
    """
    Font = pygame.font.SysFont('timesnewroman', 30)  # отображает на экране хп и тд
    health = Font.render('Player: ' + (str(player.health).split('.')[0] + 'hp' if player.health > 0 else 'Dead'),
                         False, (0, 0, 0), (0, 150, 50))
    window.blit(health, (0, 0))

    heat = Font.render('Ready to heat: ' + str(player.timer <= 0), False, (0, 0, 0), (200, 100, 100))
    window.blit(heat, (0, 33))

    score = Font.render('Score: ' + str(player.score), False, (0, 0, 0), (200, 200, 0))
    window.blit(score, (580, 0))

    monster_hp = Font.render('Monster: ' + (str(monsters.hp) + 'hp' if monsters.hp > 0 else 'Dead'),
                             False, (0, 0, 0), (0, 150, 100))
    window.blit(monster_hp, (0, 685))


def inventory_draw():
    """
    Рисует ячейки инвентаря и их содержимое
    :return: None
    """
    font = pygame.font.SysFont(None, 40)

    window.blit(inventory_cell, (width // 2 - 96, height - 64))
    window.blit(inventory_cell, (width // 2 - 32, height - 64))
    window.blit(inventory_cell, (width // 2 + 32, height - 64))
    if player.items_inventory[0]:
        window.blit(potion_inventory, (width // 2 - 96, height - 64))
        window.blit(font.render(str(player.items_inventory[0]), True, (200, 200, 200)),
                    (width // 2 - 96 + 48, height - 64 + 32))
    if player.items_inventory[1]:
        window.blit(potion_inventory, (width // 2 - 32, height - 64))
        window.blit(font.render(str(player.items_inventory[1]), True, (200, 200, 200)),
                    (width // 2 - 32 + 48, height - 64 + 32))
    if player.items_inventory[2]:
        window.blit(potion_inventory, (width // 2 + 32, height - 64))
        window.blit(font.render(str(player.items_inventory[2]), True, (200, 200, 200)),
                    (width // 2 + 32 + 48, height - 64 + 32))


width, height = 1280, 720

player = Player()
monsters = Monster()
bottle = HealingBottle()

pygame.init()
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('fight!')

player_model_right = pygame.image.load('images/ninja.gif')
player_model_left = transform.flip(player_model_right, True, False)  # герой смотрящий влево

monster_textures = {
    'low': pygame.image.load('images/slither.gif'),
    'medium': pygame.image.load('images/spider.gif'),
    'high': pygame.image.load('images/knight.gif'),
    'boss': pygame.image.load('images/boss.gif')
}

monster_model_right = monster_textures[monsters.diff]
monster_model_left = transform.flip(monster_model_right, True, False)  # монстр смотрящий влево
background = pygame.image.load('images/background.jpg')
menu = pygame.image.load('images/game_menu.jpg')
potion_model = pygame.image.load('images/potion.gif')
potion_inventory = pygame.image.load('images/potion_in_inventory.gif')
inventory_cell = pygame.image.load('images/inventory.gif')

inGame = False
items = []
run = True
cycle = 0
font = pygame.font.SysFont(None, 25)
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    key = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed(5)
    clock = pygame.time.Clock()

    if inGame:
        pygame.mouse.set_visible(False)

        if key[pygame.K_d] and player.x < 1160:  # движение героя
            player.move_right()
        if key[pygame.K_s] and player.y < 610:
            player.move_down()
        if key[pygame.K_a] and player.x >= 0:
            player.move_left()
        if key[pygame.K_w] and player.y >= 0:
            player.move_up()
        if key[pygame.K_e] or mouse[0]:
            player.damage_given()
        if key[pygame.K_t]:
            print(monsters.timer)
        if key[pygame.K_j]:
            player.immortality = True

        monsters.monster_move()
        monsters.attack()
        monsters.timer -= 1
        player.timer -= 1
        bottle.timer -= 1

        if monsters.hp <= 0 and monsters.timer <= 0:
            bottle.drop(monsters.x, monsters.y)  # нужно сделать геттер
            print('kill')
            del monsters
            monsters = Monster()
            monster = monster_textures[monsters.diff]

        if key[pygame.K_m]:
            print('Cords= ' + str((player.x, player.y)), str((monsters.x, monsters.y)))
            print('Hp= ' + str(player.health), str(monsters.hp))
            print('monster info:', monsters.diff)

        if key[pygame.K_i]:
            print(player.items_inventory)
            # print(items[0])

        if key[pygame.K_ESCAPE]:
            inGame = False

        if key[pygame.K_f]:  # на f поднимать предмет (64 пикселя)
            try:
                if player.find_item(*bottle.cords):
                    player.find_heal(bottle.heal)
                    bottle = HealingBottle()  # пересоздаем ботл чтобы нельзя было собрать больше одного раза
                    print('drop')
            except TypeError:  # Пока что не тестил без try. Просто чтобы не крашило
                pass
            except AttributeError:
                pass

        if key[pygame.K_1]:
            if bottle.can_use() and player.items_inventory[0] and player.health > 0:
                player.health += 50
                player.items_inventory[0] -= 1
                bottle.use_heal()

        if key[pygame.K_2]:
            if bottle.can_use() and player.items_inventory[1] and player.health > 0:
                player.health += 75
                player.items_inventory[1] -= 1
                bottle.use_heal()

        if key[pygame.K_3]:
            if bottle.can_use() and player.items_inventory[2] and player.health > 0:
                player.health += 100
                player.items_inventory[2] -= 1
                bottle.use_heal()

        window.blit(background, (0, 0))  # фон, монстр, игрок

        for dropped_item, pos, drop_cycle in items:

            dropped_item.blit_image(window, pos)

            if cycle - drop_cycle == 1000:
                items.pop(items.index((dropped_item, pos, drop_cycle)))  # удаление предметов с земли

            if key[pygame.K_f]:
                if player.find_item(pos[0], pos[1]) and \
                        (not player.inventory[dropped_item.type] or
                         dropped_item.stat > player.inventory[dropped_item.type].stat):
                    player.inventory[dropped_item.type] = dropped_item
                    items.pop(items.index((dropped_item, pos, drop_cycle)))  # ?

        window.blit(monster_model_right if monsters.right else monster_model_left, (monsters.x, monsters.y))
        window.blit(player_model_right if player.right else player_model_left, (player.x, player.y))
        # загружаем модельку игрока и монстра смотрящую в ту сторону куда направлено движение (право лево)

        items_draw()

        inventory_draw()

        write_stats()

        clock.tick(300)
    else:
        pygame.mouse.set_visible(True)
        window.blit(menu, (0, 0))  # меню игры, кнопки и тд

        if pygame.mouse.get_pressed()[0] and 760 >= pygame.mouse.get_pos()[0] >= 510 and \
                300 >= pygame.mouse.get_pos()[1] >= 240:
            inGame = True
        if pygame.mouse.get_pressed()[0] and 760 >= pygame.mouse.get_pos()[0] >= 510 and \
                480 >= pygame.mouse.get_pos()[1] >= 400:
            break

    cycle += 1
    pygame.display.update()

pygame.quit()

"""не загружается другая картинка моба"""
