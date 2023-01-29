print('Добро пожаловать в игру!')
print('Вводите координаты клетки через пробела')
print('Первый игрок - o, второй -  x')
print('_______________________________')

def pole():
    print(f" 0 1 2")
    for i in range(3):
        print(f"{i} {k[i][0]} {k[i][1]} {k[i][2]}")

def ask():
    while True:
        koo = input('Ведите координаты через пробел:').split()

        if len(koo) != 2:
            print('введите 2 кординаты')
            continue

        a, b = koo

        if not(a.isdigit()) or not(b.isdigit()):
            print('введены не числа')
            continue

        a, b = int(a), int(b)

        if 0 > a or a > 2 or 0 > b or b > 2:
            print(" Координаты вне диапазона! ")
            continue

        if k[a][b] != ' ':
            print('место уже занято')
            continue

        return a, b

def win():
    win_cord = (((0, 0), (0, 1), (0,2)),
         ((1, 0), (1, 1), (1, 2)),
         ((2, 0), (2, 1), (2, 2)),
         ((0,2), (1, 1), (2,0)),
         ((0, 0), (1,1), (2, 2)),
         ((0,0), (1,0), (2, 0)),
         ((0,1), (1,1), (2,1)),
          ((0,2), (1,2), (2,2)))
    for cord in win_cord:
        a = cord[0]
        b =cord[1]
        c =cord[2]
        if k[a[0]][a[1]] == k[b[0]][b[1]] == k [c[0]] [c[1]] != ' ':
            pole()
            print(f'выиграл {k[a[0]] [a[1]]}')
            return True
    return False

k = [ [' ', ' ', ' '] for i in range(3)]
c = 0
while True:
    pole()
    if c % 2 == 0:
        print('ходит 0')
    else:
        print("ходит X")
    a, b = ask()

    if c % 2 == 0:
        k[a][b] = '0'
    else:
        k[a][b] = 'X'
    c += 1
    if win():

        break
    if c == 9:
        print('ничья')
        break






