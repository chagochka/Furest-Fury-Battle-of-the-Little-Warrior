import pygame


class SkillTree:
    def __init__(self, player, window, font):
        self.player = player
        self.window = window
        self.font = font
        self.title = ""
        self.description = ["", "", "", ""]
        self.spell = {
            "Сапоги Гермеса": False,  # сделано
            "Светик-Сто-Смертник": False,  # сделано
            "Вдохновляющий стяг": False,  # сделано
            "Дуновение ветерка": False,
            "Тёмное братство": False,
            "Лечь костями": False,
            "Абаддон": False,
            "КДАБР": False,
            "Разбитое сердце": False,
            "Кровосися": False,
            "Геральт с гор": False,
            "Я есть грунт": False,
            "Сила майнкрфта": False,
            "Просвящённый": False,
            "Волчья истерика": False,
            "Удача Дрима": False,
            "Пудж": False,
            "Звездочёт": False,
            "Я терпила": False
        }
        self.points = 0
        self.all_points = 0
        self.error = ''
        self.descriptions = {
            "Сапоги Гермеса": ["За каждый пройденный", 'шаг добовляет', 'мало здоровья', ''],
            "Светик-Сто-Смертник": ["Добавление плоского", 'урона персонажу', '', ''],
            "Вдохновляющий стяг": ["Добавление процентного", 'урона для персонажа', '', ''],
            "Дуновение ветерка": ["Увеличивает радиус", 'атаки', '', ''],
            "Тёмное братство": ["Добавление критичесского", 'урона', '', ''],
            "Лечь костями": ["Добивает врага если", 'у него менее 10 %', '', ''],
            "Абаддон": ["Излишок востанавливаемого", 'наносится врагу', '', ''],
            "КДАБР": ["ускоряет перезарядку", 'атаки', '', ''],
            "Разбитое сердце": ["Увеличивает максимум", 'здоровья в 2 раза', '', ''],
            "Кровосися": ["Добавляет по 5%", 'здоровья от атаки', '', ''],
            "Геральт с гор": ["Позволяет получить", 'чеканную монету', '(нет)', ''],
            "Я есть грунт": ["(ням-ням)", 'Добавляет естественную', 'защиту - 5', ''],
            "Сила майнкрфта": ["Добавляет шипы 1", 'на персонажа', '', ''],
            "Просвящённый": ["Усиляет шипы до 3-го,", 'вампиризм шипам', 'в размере - 10%', ''],
            "Волчья истерика": ["Если здоровья меньше", '5%, увеличивает урон', 'в 2 раза', ''],
            "Удача Дрима": ["Ему не нужна удача", '', '', ''],
            "Пудж": ["Твой злейший враг", '', '', ''],
            "Звездочёт": ["Даёт шанс игроку", 'застанить существо', 'при его спавне', ""],
            "Я терпила": ["Если здоровье меньше", '10% от максимума,', 'увеличивает', 'защиту на 10']
        }
        self.spells = ["Сапоги Гермеса", "Светик-Сто-Смертник", "Вдохновляющий стяг", "Дуновение ветерка",
                       "Тёмное братство", "Лечь костями", "Абаддон", "КДАБР", "Кровосися", "Геральт с гор",
                       "Я есть грунт", "Сила майнкрфта", "Разбитое сердце", "Я терпила", "Просвящённый",
                       "Волчья истерика", "Удача Дрима", "Пудж", "Звездочёт"]

    def point(self, score):
        if score > 1000 + self.all_points * 1000:
            self.points += 1
            self.all_points += 1

    def new_text(self):
        # вывод названия перкa
        text_surf = self.font.render(str(self.title), False, (0, 0, 0))
        text_rect = text_surf.get_rect(bottomleft=(65, 310))
        self.window.blit(text_surf, text_rect)

        if self.error:
            text_surf = self.font.render(self.error, False, (0, 0, 0))
            text_rect = text_surf.get_rect(bottomleft=(460, 370))
            pygame.draw.rect(self.window, '#f7da9e', text_rect.inflate(20, 20))
            pygame.draw.rect(self.window, '#f7da9e', text_rect.inflate(20, 20), 3)
            self.window.blit(text_surf, text_rect)
        # ввывод изучена ли пасивкa
        if self.title != "":
            if self.spell[self.title]:
                text_surf = self.font.render("Изучено", False, (0, 0, 0))
            else:
                text_surf = self.font.render("Не изучено", False, (0, 0, 0))
            text_rect = text_surf.get_rect(bottomleft=(70, 270))
            pygame.draw.rect(self.window, '#f7da9e', text_rect.inflate(20, 20))
            pygame.draw.rect(self.window, '#f7da9e', text_rect.inflate(20, 20), 3)
            self.window.blit(text_surf, text_rect)
        # вывод описания пeрка
        for i in range(4):
            text_surf = self.font.render(str(self.description[i]), False, (0, 0, 0))
            text_rect = text_surf.get_rect(bottomleft=(65, 350 + i * 25))
            self.window.blit(text_surf, text_rect)
        # ввывод очков прокaчки
        text_surf = self.font.render(f"Очки улучшений: {str(self.points)}", False, (0, 0, 0))
        text_rect = text_surf.get_rect(bottomleft=(460, 320))
        pygame.draw.rect(self.window, '#f7da9e', text_rect.inflate(20, 20))
        pygame.draw.rect(self.window, '#f7da9e', text_rect.inflate(20, 20), 3)
        self.window.blit(text_surf, text_rect)

    def cursor_location(self, coor, clic):
        x, y = coor
        self.new_text()
        line = open('coords_skill_tree.txt').readlines()
        for i in line:
            x1, y1, x2, y2, num = i.split(".")
            x1, y1, x2, y2, num = int(x1), int(y1), int(x2), int(y2), int(num)
            if x1 < x < y1 and x2 < y < y2 and clic:
                self.title = self.spells[num]
                self.description = self.descriptions[self.spells[num]]
            if 225 < x < 345 and 445 < y < 470 and clic:
                self.contnue()

    def contnue(self):
        if self.title != "":
            if not self.spell[self.title] and self.points >= 1:
                self.error = ""
                self.spell[self.title] = True
                self.points -= 1
                if self.title == "Разбитое сердцe":
                    self.player.max_health = 2500
            elif not self.spell[self.title] and self.points == 0:
                self.error = "Недостаточно ОУ"
        else:
            self.error = "Умение не выбранно"
