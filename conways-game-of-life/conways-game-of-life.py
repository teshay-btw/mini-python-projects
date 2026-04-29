import random
import time
import os
import datetime
import sys


WIDTH = int(input("Enter the width of a field: \n> "))
HEIGHT = int(WIDTH / 3)

def create_field():
    field = []

    for i in range(HEIGHT):
        line = []
        for j in range(WIDTH):
            if random.randint(0,10) == 1:
                line.append("O")
            else:
                line.append(' ')
        field.append(line)
    return field

def draw_field(field,gen,elapsed_time,cells_count,fps):
    sys.stdout.write(f"\033[{HEIGHT}F")
    for i in range(HEIGHT):
        row = ''.join(field[i])
        sys.stdout.write('\r' + row + '                                         \n')
        sys.stdout.flush()
    print("-" * WIDTH)
    print(f"\rCONWAYS GAME OF LIFE --- Gen: {gen} | Cells: {cells_count} | Elapsed Time: {elapsed_time}s | Fps: {fps} | Created by: teshay            ",flush=True)

def find_cells_count(field,x,y):
    cells_count = 0 
    if y-1 > -1 and field[y-1][x] == "O":
        cells_count += 1
    if y+1 < HEIGHT and field[y+1][x] == "O":
        cells_count += 1
    if x-1 > -1 and field[y][x-1] == "O":
        cells_count += 1
    if x+1 < WIDTH and field[y][x+1] == "O":
        cells_count += 1
    if x-1 > -1 and y-1 > -1 and field[y-1][x-1] == "O":
        cells_count += 1
    if x+1 < WIDTH and y+1 < HEIGHT and field[y+1][x+1] == "O":
        cells_count += 1
    if x+1 < WIDTH and y-1 > -1 and field[y-1][x+1] == "O":
        cells_count += 1
    if x-1 > -1 and y+1 < HEIGHT and field[y+1][x-1] == "O":
        cells_count += 1
    return cells_count

def movement(field):
    for i in range(HEIGHT):
        for j in range(WIDTH):
            cells_count = find_cells_count(field,j,i)
            if (cells_count == 3) and (field[i][j] == " "):
                field[i][j] = "O"
            elif (cells_count < 2 or cells_count > 3) and (field[i][j] == "O"):
                field[i][j] = " "



field = create_field()
gen = 0
elapsed_time = 0
input("\t\t\tPress Enter to continue")

start = time.perf_counter()
while True:
    cells_count = 0
    gen+= 1
    sys.stdout.write(f"\033[{HEIGHT}F")
    elapsed_time = round(time.perf_counter() - start)+1

    for i in range(HEIGHT):
        for j in range(WIDTH):
            if field[i][j] == "O":
                cells_count+=1
    draw_field(field,gen,elapsed_time,cells_count, round(gen / elapsed_time,1))
    movement(field)
    sys.stdout.flush()
    time.sleep(0.05)
