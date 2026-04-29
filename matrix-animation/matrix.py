import random
import time
import os
import datetime
import sys
import string
from colour import Color
import cursor
from wcwidth import wcwidth
import threading

WIDTH = 100
HEIGHT = 30

def create_field():
    field = []
    for i in range(HEIGHT):
        line = []
        for j in range(WIDTH):
            line.append(' ')
        field.append(line)
    return field

def colored(text, color):
    r = int(color.red * 255)
    g = int(color.green * 255)
    b = int(color.blue * 255)
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

def draw_field(field,elapsed_time,fps,coords,colors):
    sys.stdout.write(f"\033[{HEIGHT}F")
    stop = False
    for i in range(20):
        for j in range(WIDTH):
            stop = False
            for l in range(9):
                if i+l in coords.get(j,[]):
                    print(colored(field[i][j],colors[l]),end="")
                    stop = True
                    break
            if stop == False: 
                print(colored(field[i][j],colors[8]),end="")
            sys.stdout.flush()
        sys.stdout.write('\n')
    print("-" * WIDTH)
    print(f"\rMATRIX --- Elapsed Time: {elapsed_time}s | Fps: {fps} | Created by: teshay            ",flush=True)

def random_symbol(symbols):
    return random.choice(symbols)

def generate_col(field,coords:dict,symbols):
    for i in range(WIDTH):
        if random.randint(1,30) == 1:
            field[0][i] = random_symbol(symbols)
            coords[i] = coords.get(i, []) + [0]

def movement(field,coords):
    for x, y in list(coords.items()):
        for i in y:
            if i + 1 < HEIGHT:
                field[i+1][x] = random_symbol(symbols)
                coords[x][coords[x].index(i)] = i+1 
    
field = create_field()
cursor.hide()
while True:
    letters = input("ASCII letter, chinese, or 0/1 (1,2,3): \n> ")
    if letters == "1":
        symbols = list(string.ascii_letters + string.digits)
    elif letters == "2":
        symbols = [chr(i) for i in range(0xFF61, 0xFF9F+1)]
    else:
        symbols = [0,1]
    color = input("Choose color: \n> ")
    colors = list(Color(color).range_to(Color("black"), 10))

    elapsed_time = 0
    print("Press Enter during the animation to stop.")
    input("Press Enter to continue...")
    k = 0
    coords = {}
    start = time.perf_counter()
    generate_col(field,coords,symbols)
    user_input = None

    def wait_input():
        global user_input
        user_input = input()
        user_input = "1"


    threading.Thread(target=wait_input, daemon=True).start()

    while True:
        sys.stdout.write(f"\033[{HEIGHT}F")
        k += 1
        elapsed_time = round(time.perf_counter() - start)+1
        coords = {x:y for x,y in coords.items() if y != HEIGHT-1}
        generate_col(field,coords,symbols)

        draw_field(field,elapsed_time,round(k / elapsed_time,1),coords,colors)
        sys.stdout.flush()
        movement(field,coords)

        if user_input:
            os.system("cls")
            break
