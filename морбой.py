from random import randint

class BoardExeption(Exception):
    pass

class BoardOutExeption(BoardExeption):
    def __str__(self):
        return "Вы стреляете за доску"

class BoardUsedExeption(BoardExeption):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

class BoardWrongShipExeption(BoardExeption):
    pass

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"

class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow #нос корабля
        self.l = l
        self.o = o #задает ориентацию корабля
        # 0 - вертикальный 1 -горизонтальный
        self.lives = l
    @property
    def dots(self): #метод возвращает список объектов класса Dot наших точек в формате
        ship_dots = [] #список всех точек корабля
        for i in range(self.l): #значения от 0 до длины корабля-1
            cur_x = self.bow.x #(self.bow)-self  self.x - 1 точка корабля
            cur_y = self.bow.y #берем нос корабля
            # и начинаем от него шагать на i
            # клеток (в зависимости от длины корабля)

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

    def shooten(self, shot):
        return shot in self.dots() #здесь нам как раз пригодился метод __eq__


class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0 #количество побежденных кораблей

        self.field = [["O"] * size for _ in range(size)]

        self.busy = [] #занятые точки
        self.ships = [] #корабли на доске

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.busy: #каждая точка корабля не выходит за границы и не занята уже другим
                raise BoardWrongShipExeption()
        for d in ship.dots:#для кажой точки корабля:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False): #метод,
        near = [
            (-1, -1), (-1, 0), (-1, 1),#все точки вокруг той, в которой мы находимся (0, 0) - сама точка
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots: #берем каждую точку корабля (ship_dots.append(Dot(cur_x, cur_y)))  т
            #ТО ЕСТЬ каждый элемент d это объект класса Dot = Dot(cur_x, cur_y)
            for dx, dy in near: #берем первую итераци. например (-1, 1) то етсть
                #для точек -1 и 1  переменная кур равна ОПЯТЬ ЖЕ ОБЪЕКТУ класса Dot с точками( изн.х+смещение, изн.у + смещ)
                cur = Dot(d.x + dx, d.y + dy) # по очереди сюда попадают все точки, которые соседствуют с кораблем
                if not (self.out(cur)) and cur not in self.busy:
                    if verb: #ограничение, чтобы ставить точки только тогда, когда мы убили полностью корабль
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def __str__(self):#доска выводится просто с print(b), если b = Board()
        res = "" #записываем сюда всю нашу доску
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field): #проходимся по строкам доски
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))  #проверяет находится ли точка
        # за пределами доски d.x и d.y - координаты рандомной точки д

    def shot(self, d):#метод, который делает выстрел
        if self.out(d):
            raise BoardOutException()#проверка выходв зв границу и занятости

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d) #добавляем в список занятых

        for ship in self.ships: #self.ships = [] корабли на доске ship кортеж из тосек одного корабля
            if ship.shooten(d): #если рандомная точка в одном из кораблей   def shooten(self, shot):self=ship
                # return shot in self.dots() #здесь нам как раз пригодился метод __eq__
                # return d in ship.dots()
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1 #счетник уничтоженных
                    self.contour(ship, verb=True) #обводка по контуру, чтобы не мочь стрелять в точки рядом с кораблем
                    print("Корабль уничтожен!")
                    return False #переход хода
                else:
                    print("Корабль ранен!")
                    return True #повтор хода

        self.field[d.x][d.y] = "." # ежели никто не поражен
        print("Мимо!")
        return False #переход хода

    def begin(self):
        self.busy = [] #обнуляем, чтобы хранить там точки куда игрок стрелял, до этого хранили там точки с кораблями


class Player:
    def __init__(self, board, enemy): #две доски
        self.board = board
        self.enemy = enemy

    def ask(self): #метод для потомков класса
        raise NotImplementedError()

    def move(self):#в бесконечном цикле выполняем выстрел
        while True:
            try:
                target = self.ask() #просим дать координаты выстрела
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self): #случайный ход компа
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1) #т.к size = 6 и все координаты у нас поползди вверх
            # на одну из-за нумерации с 0


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board() #создание двух досок
        co = self.random_board()
        co.hid = True #скрытие кораблей компа

        self.ai = AI(co, pl) #создание двух игроков
        self.us = User(pl, co)

    def random_board(self):#гарантированная генерация рандомной доски
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self): #попытки расставить наши корабли
        lens = [3, 2, 2, 1, 1, 1, 1] #нужные длины
        board = Board(size=self.size) #создание доски
        attempts = 0
        for l in lens: #для каждой длины мы
            # в бесконечном цикле будем делать попытки его потсавить
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipExeption:
                    pass
        board.begin() #подготовка доски к игре
        return board

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move() #вызываем метод, отвечающий за ход.
                # если нужно повторить он тебе сам НЕ повторит,
                #рипит это  булевая штука то, нужно ли повторить наш ход
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat: #если повторить ход нужно, то чтобы по четности ходы не сбились уменьшаем и
                # ты снова ходишь, что и требовалось допустить
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()

