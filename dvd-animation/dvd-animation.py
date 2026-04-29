import random
import time
import sys
import cursor

WIDTH = 40
HEIGHT = 20

def create_field(char) -> list:
    screen = []
    spaces = ""

    for _ in range(len(char)):
        spaces += ' '

    for _ in range(HEIGHT):
        line = []
        for _ in range(WIDTH):
            line.append(spaces)
        screen.append(line.copy())

    return screen 

def print_screen(screen, char, x, y):
    for i, j in zip(x, y):
        screen[j][i] = char
    sys.stdout.write(f"\033[{HEIGHT}F")
    sys.stdout.write(f"Caught in a corner: {count}\n")

    sys.stdout.write(' ')
    sys.stdout.write(''.join('-' for _ in range(WIDTH * len(char))))
    sys.stdout.write('\n')


    for i in range(HEIGHT):
        sys.stdout.write('|')
        for j in range(WIDTH):
            sys.stdout.write(screen[i][j])
        sys.stdout.write('|')
        sys.stdout.write('\n')


    sys.stdout.write(' ')
    sys.stdout.write(''.join('-' for _ in range(WIDTH * len(char))))
    sys.stdout.write('\n')


def movement(screen,x,y,char,direction_x,direction_y,count,index):
    newx = x + direction_x[index]
    newy = y + direction_y[index]

    if newx < 0 and newy < 0:
        direction_x[index] = 1
        direction_y[index] = 1
        count += 1
    elif newx < 0 and newy == HEIGHT:
        direction_x[index] = 1
        direction_y[index] = -1
        count += 1
    elif newx == WIDTH and newy < 0:
        direction_x[index] = -1
        direction_y[index] = 1
        count += 1
    elif newx == WIDTH and newy == HEIGHT:
        direction_x[index] = -1
        direction_y[index] = -1
        count += 1
    elif newx < 0 or newx == WIDTH:
        direction_x[index] *= -1
    elif newy < 0 or newy == HEIGHT:
        direction_y[index] *= -1

    newx = x + direction_x[index]
    newy = y + direction_y[index]

    screen[newy][newx] = char
    screen[y][x] = ' ' * len(char)

    return [newx,newy,count]


direction_x = []
direction_y = []
x = []
y = []
count = 0
char_count = int(input("How many symbols? \n> "))
char = input("Type a symbol: \n> ")
screen = create_field(char) 
cursor.hide()

for i in range(char_count):
    direction_x.append(random.choice([1,-1]))
    direction_y.append(random.choice([1,-1]))
    x.append(random.randint(0,39))
    y.append(random.randint(0,19))

while True:

    sys.stdout.write(f"\033[{HEIGHT}F")
   
    
    print_screen(screen,char,x,y)
    
    for i in range(char_count):
        x[i],y[i],count = movement(screen, x[i], y[i],char, direction_x,direction_y,count,i)

    time.sleep(0.1)
    
