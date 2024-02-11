import random


class Item:
    """
    Класс предмет
    """
    rarities = ['common', 'uncommon', 'rare', 'mythical', 'legendary']

    def __init__(self, image, rarity, item_type):

        self.image = image
        self.rarity = rarity
        self.type = item_type

    def blit_image(self, window, pos):
        window.blit(self.image, pos)


class Weapon(Item):
    stats = ((100, 120), (120, 150), (150, 170), (170, 200), (200, 250))

    def __init__(self, image, rarity, item_type):
        super().__init__(image, rarity, item_type)
        self.image = image
        self.rarity = rarity
        self.type = item_type
        stats_index = self.rarities.index(self.rarity)
        self.stat = random.randint(self.stats[stats_index][0], self.stats[stats_index][1])


class Armor(Item):
    stats = {
        'boots': [(3, 5), (5, 8), (8, 10), (10, 13), (13, 15)],
        'trousers': [(3, 5), (5, 8), (8, 10), (10, 13), (13, 15)],
        'breastplate': [(3, 5), (5, 8), (8, 10), (10, 13), (13, 15)],
        'helmet': [(3, 5), (5, 8), (8, 10), (10, 13), (13, 15)],
    }

    def __init__(self, image, rarity, item_type):
        super().__init__(image, rarity, item_type)
        self.image = image
        self.rarity = rarity
        self.type = item_type
        stats_index = self.rarities.index(self.rarity)
        self.stat = random.randint(self.stats[self.type][stats_index][0], self.stats[self.type][stats_index][1])


class HealingBottle(Item):
    """Класс зелья здоровья"""

    def __init__(self, image, rarity, item_type):
        super().__init__(image, rarity, item_type)
        self.stat = 100

    def heal(self, player):
        if player.health + self.stat < 1000:
            if player.health + self.stat > player.max_health:
                player.max_health += player.health + self.stat - player.max_health
            player.health += self.stat
