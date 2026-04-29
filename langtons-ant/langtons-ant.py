import random
import time
import sys


WIDTH = int(input("Enter the width of a field: \n> "))

HEIGHT = int(WIDTH / 3)

def create_field(x,y):
    field = []

    for i in range(HEIGHT):
        line = []
        for j in range(WIDTH):
                line.append(' ')
        field.append(line)
    return field

def draw_field(field,gen,elapsed_time,fps,x,y):
    sys.stdout.write(f"\033[{HEIGHT}F")

    for i in range(HEIGHT):
        row = list(field[i])  # copy

        if i == y:
            row[x] = "X"

        print("".join(row))
    print("-" * WIDTH)
    print(f"\rLANGTONS ANT --- Step: {gen} | Elapsed Time: {elapsed_time}s | Fps: {fps} | Created by: teshay            ",flush=True)

def choose_direction(x,y):
    direction = random.randint(1,4) # 1 - right, 2 - left, 3 - up, 4 - down

    if x == WIDTH -1 and y == HEIGHT-1:
        direction = random.choice([3,2])
    elif x == WIDTH-1 and y == 0:
        direction = random.choice([4,2])
    elif x == 0 and y == HEIGHT -1:
        direction = random.choice([3,1])
    elif x == 0 and y == 0:
        direction = random.choice([1,4])
    elif x == WIDTH - 1:
        direction = random.randint(2,4)
    elif x == 0:
        direction = random.choice([1,3,4])
    elif y == HEIGHT - 1:
        direction = random.choice([1,2,3])
    elif y == 0:
        direction = random.choice([1,2,4])

    match direction:
        case 1:
            x += 1
        case 2:
            x -= 1
        case 3:
            y -= 1
        case 4:
            y += 1

    return [x,y]


def movement(field,x,y):
    
    newx,newy = choose_direction(x,y)
    if field[newy][newx] == " ":
        field[newy][newx] = "O"
    elif field[newy][newx] == "O":
        field[newy][newx] = " "

    return [newx,newy]




x = random.randint(0,WIDTH)
y = random.randint(0,HEIGHT)
field = create_field(x,y)
gen = 0
elapsed_time = 0
input("\t\t\tPress Enter to continue")

start = time.perf_counter()
while True:
    gen+= 1
    sys.stdout.write(f"\033[{HEIGHT}F")
    elapsed_time = round(time.perf_counter() - start)+1

    
    x,y = movement(field,x,y)
    draw_field(field,gen,elapsed_time, round(gen / elapsed_time,1),x,y)
   
    sys.stdout.flush()
    time.sleep(0.1)
