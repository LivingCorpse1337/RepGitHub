from random import randint

class BoardExc(Exception):
    pass

class BoardOutException(BoardExc):
    def __str__(self):
        return "You are trying to shoot in nowhere!"

class BoardUsedException(BoardExc):
    def __str__(self):
        return "You already shot this sector!"

class BoardWrSExc(BoardExc):
    pass

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"

class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shoot(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hit=False, size=6):
        self.size = size
        self.hit = hit

        self.count = 0

        self.field = [["O"] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrSExc()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.frame(ship)

    def frame(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hit:
            res = res.replace("■", "O")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.frame(ship, verb=True)
                    print("Wrecked!")
                    return False
                else:
                    print("One more shot!")
                    return True

        self.field[d.x][d.y] = "."
        print("Missed!")
        return False

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardExc as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"AI's Turn!: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Players Turn:").split()

            if len(cords) != 2:
                print("Input 2 coordinates!")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print("Input numbers!")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hit = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrSExc:
                    pass
        board.begin()
        return board

    def greetings(self):
        print("---------------------------")
        print("  Welcome, young mariner,  ")
        print("        to the game       ")
        print("        Sea Battle    ")
        print("---------------------------")
        print(" Input example: x y ")
        print(" x - number of string  ")
        print(" y - number of column ")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Players deck:")
            print(self.us.board)
            print("-" * 20)
            print("AI's deck:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-" * 20)
                print("Players Turn!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("AI's Turn!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("PLAYER WINS!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("AI WINS!")
                break
            num += 1

    def start(self):
        self.greetings()
        self.loop()


g = Game()
g.start()





