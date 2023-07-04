
def print_tic_tac_toe():
    print(f"  | 0 | 1 | 2 |")
    print("--------------")
    print(f"0 | {tic_tac_toe_field [0][0]} | {tic_tac_toe_field [0][1]} | {tic_tac_toe_field [0][2]} |")
    print("--------------")
    print(f"1 | {tic_tac_toe_field [1][0]} | {tic_tac_toe_field [1][1]} | {tic_tac_toe_field [1][2]} |")
    print("--------------")
    print(f"2 | {tic_tac_toe_field [2][0]} | {tic_tac_toe_field [2][1]} | {tic_tac_toe_field [2][2]} |")

def hod():
    while True:
        coords = input("   Ваш ход:   ").split()

        if len(coords) != 2:
            print("Нужно ввести 2 числа")
            continue

        x, y = coords

        if not (x.isdigit()) or not (y.isdigit()):
             print("Нужно ввести числа")
             continue

        x, y = int(x), int(y)

        if 0 <= x <= 2 and 0 <= y <=2:
            if tic_tac_toe_field[x][y] == " ":
                return x, y
            else: print("Выберите другую клетку")
        else:
            print("Введите корректные данные")

def win_game():
    win_coords = [((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                ((0, 0), (1, 0), (2, 0)), ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)),
                ((0, 0), (1, 1), (2, 2)), ((0, 2), (1, 1), (2, 0))]
    for coord in win_coords:
        for c in coord:
            a = coord[0]
            b = coord[1]
            c = coord[2]
            if tic_tac_toe_field[a[0]][a[1]] == tic_tac_toe_field[b[0]][b[1]] == tic_tac_toe_field[c[0]][c[1]] != " ":
                print(f"Подеба {tic_tac_toe_field[c[0]][c[1]]}")
                return True
    return False

tic_tac_toe_field = [[" "] * 3 for i in range(3)]
num = 0
while True:
    num += 1
    print_tic_tac_toe()
    if num % 2 == 1:
        print("Крестик в БОЙ!")
    else:
        print("Нолик в БОЙ!")

    x, y = hod()

    if num % 2 == 1:
        tic_tac_toe_field[x][y] = "X"
    else:
        tic_tac_toe_field[x][y] = "O"

    if win_game():
        break

    if num == 9:
        print("ничья")
        break