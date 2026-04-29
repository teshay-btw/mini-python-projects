import random
import time
import sys

from wcwidth import wcwidth
WIDTH = 134
HEIGHT = 30

multi_fish1 = [
    "          \\",
    "    '''''''\\''",
    "\\ /'          \\",
    ">=        [  ' >",
    "/ \\         / /",
    "    '''''''/''",
    "          /",
]
multi_fish2 = [
    " \\;,  ,;\\\\\\,,",
    "  \\\\\\;;:::::::°",
    "  ///;;::::::::<",
    " /;'   '/////''"
]

multi_fish3 = [
    "   ,,\,",
    ">='  {°>",
    "   ''/'"
]

multi_fish1_rev = [
    "/",
    "''/'''''''",
    "/          \\ /",
    "< '  ]          =<",
    "   \\   \\         / \\",
    "''\\''''''''",
    "       \\"
]


multi_fish2_rev = [
    ",,///;,  ,;/ ",
    "°:::::::;;///  ",
    ">::::::::;;\\\\\\  ",
    "''\\\\\\\''   ';\\ "
]

fish_type1 = "<==-<"
fish_type2 = "-_-_^=<" 
fish_type3 = "<//<"
fish_type4 = "}-[[[*>" 
fish_type6 = ">><>>°>" 
fish_type7 = "~~°>" 
fish_type5 = "<°[[<" 

fish_type8 = ">]]°>"
fish_type9 = ">-==>"
fish_type10 = "-_-_^=>" 
fish_type11 = ">\\\>"

fish_list_right = [
    fish_type1,
    fish_type2,
    fish_type3,
    fish_type5
]
fish_list_left = [
    fish_type4,
    fish_type6,
    fish_type7,
    fish_type8,
    fish_type9,
    fish_type10,
    fish_type11
]

multi_fish_left = [
    multi_fish1,
    multi_fish2,
    multi_fish3
]
multi_fish_right = [
    #multi_fish1_rev
    multi_fish2_rev
]

BLACK   = "\033[30m"
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
BLUE    = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[36m"
WHITE   = "\033[37m"

RESET   = "\033[0m" 

def fill_field(field  ):
    for i in range(HEIGHT):
        line = []
        for j in range(WIDTH):
            line.append(" ")
        field.append(line)
    for i in range(WIDTH-1):
        field[HEIGHT-1][i] = "░"

        if random.randint(1,10) == 1:
            field[HEIGHT-2][i] = random.choice(["●", "○", "◉", "Ͻ", "Ͼ"])

def draw_field(field,elapsed_time, fps):
    sys.stdout.write(f"\033[{HEIGHT}F")
    for i in range(HEIGHT):
        row = ''.join(field[i][17:117])
        row_colored = ""
        for ch in row:
            if ch in "<>-_^\\/=[]~*}{":
                row_colored += BLUE + ch
            elif ch == "░":
                row_colored += YELLOW + ch
            elif ch in "()":
                row_colored += GREEN + ch
            elif ch in ":;,'":
                row_colored += YELLOW + ch    
            else:
                row_colored += RESET + ch
        row_colored += RESET  # сброс цвета один раз в конце

        sys.stdout.write('\r' + row_colored + ' ' * 40 + '\n')
        sys.stdout.flush()
        #sys.stdout.write('\r' + row + '                                         \n')
    print("-" * (WIDTH-34))
    print(f"\rFISH TANK ---  Elapsed Time: {elapsed_time}s | Fps: {fps} | Created by: teshay            ",flush=True)

def air_movement(field,air_coords):
    for x,y in list(air_coords.items()):
        random_x_increase = random.randint(-1,1)
        for i in y:
            if field[i][x] not in "()":
                
                if (i - 1 >= 0) and (x + random_x_increase >=0 and x+ random_x_increase < WIDTH):
                    if field[i-1][x+random_x_increase] not in "()":
                        if field[i][x] in ["O", "o","."]:
                            field[i-1][x+random_x_increase] = field[i][x]
                        else:
                            field[i-1][x+random_x_increase] = random.choice(["O","o","."])
                    air_coords[x+random_x_increase] = air_coords.get(x+random_x_increase, []) + [i-1]
                
                field[i][x] = " "
            if field[i][x] == " ":
                air_coords[x].remove(i)
        if not air_coords[x]:
            air_coords.pop(x)

def generate_air(field,air_coords):
    if random.randint(1,5) == 1:
        for i in range(random.randint(1,2)):
            x = random.randint(17,WIDTH-17)
            y = random.randint(HEIGHT-3,HEIGHT-2)
            air_coords[x] = air_coords.get(x, []) + [y]
            if field[y][x] not in "()":
                match random.randint(1,3):
                    case 1:
                        field[y][x] = "O"
                    case 2:
                        field[y][x] = "o"
                    case 3:
                        field[y][x] = "."

def generate_seaweed(field,seaweed_coords):
    for i in range(random.randint(5,10)):
        y = HEIGHT-2
        x = random.randint(20,WIDTH-18)
        if field[y][x-2] in "()" or field[y][x+2] in "()" or field[y][x-1] in "()" or field[y][x+1] in "()" : continue
        seaweed_coords[x] = y
        
        if random.randint(1,2) == 1:
            field[y][x] = "("
        else:
            field[y][x] = ")"
 
        for j in range(random.randint(2,10)):
            if field[y][x] == "(":
                field[y-1][x+1] = ")"
            elif field[y][x] == ")":
                field[y-1][x-1] = "("
            elif field[y+1][x+1] == ")":
                field[y][x] = "("
            elif field[y+1][x-1] == "(":
                field[y][x] = ")"
            elif field[y+1][x] == ")":
                field[y][x-1] = "("
            elif field[y+1][x] == "(":
                field[y][x+1] = ")"
            y -= 1

def seaweed_movement(field,seaweed_coords,skip):
    if skip == 1:
        for x,y in list(seaweed_coords.items()):
            j = y
            while (field[j][x] == ")") or (field[j][x] == "(") or (field[j][x+1] == ")") or (x-1 >= 0 and field[j][x-1] == "("):
                if field[j][x-1] == "(":
                    field[j][x] = ")"
                    field[j][x-1] = " "  
                elif field[j][x] == ")":
                    field[j][x-1] = "("
                    field[j][x] = " "
                elif field[j][x] == "(":
                    field[j][x+1] = ")"
                    field[j][x] = " "
                elif field[j][x+1] == ")":
                    field[j][x] = "("
                    field[j][x+1] = " "
                j-=1  
        
def generate_fish(field,fish_list):
    
    key = random.randint(0,1000)
    if key in fish_list.keys():
        return
    if random.randint(1,2) == 1:
        fish = random.choice(fish_list_left)
        way = "l"
        x = 0
    else:
        fish = random.choice(fish_list_right)
        x = WIDTH-1
        way = "r"
    speed = random.randint(1,2)


    if random.randint(1,5) == 1:
        y = random.randint(1,HEIGHT-10)
        
        if way == "l":
            fish = random.choice(multi_fish_left)
            fish_list[key] = [x,y,way,fish,0,speed,0,True]
            temp_x = 0
            temp_y = 0
            for i in range(y,y+len(fish)):
                temp_x = 0
                for j in range(x,x+len(fish[temp_y])):
                    field[i][j] = fish[temp_y][temp_x]
                    temp_x +=1
                temp_y += 1
        elif way == "r":
            fish = random.choice(multi_fish_right)
            fish_list[key] = [x,y,way,fish,0,speed,0,True]
            temp_x = 0
            temp_y = 0
            for i in range(y,y+len(fish)):
                temp_x = len(fish[temp_y])
                for j in range(x,x-len(fish[temp_y]),-1):
                    temp_x -=1
                    field[i][j] = fish[temp_y][temp_x]
                    
                temp_y += 1
            

    else:
        
        y = random.randint(1,HEIGHT-4)   
        
        fish_list[key] = [x,y,way,fish,len(fish),speed,0,False]

        if way == "l":
            for i in range(len(fish)):
                field[y][x] = fish[i]
                x+=1
        else:
            for i in reversed(range(len(fish))):
                field[y][x] = fish[i]
                x-=1


def fish_movement_logic(way,x,y,fish,fish_length,id):

    if random.randint(1,5) == 1:
        random_y = random.randint(-1,1)
    else:
        random_y = 0
    if y + random_y >= HEIGHT-2 or y + random_y < 0:
        random_y = 0
    if way == "l":
        for i in reversed(range(fish_length)):
            if x+i < WIDTH:
                fish_list[id][0] = x+1
                fish_list[id][1] = y + random_y
                if field[y+random_y][x+i] not in "()":
                    field[y+random_y][x+i] = fish[i]

                if random_y !=0:
                    for j in range(x-1,x+fish_length):

                        if j >= 0 and field[y][j] not in "()░":
                            field[y][j] = " "
                elif random_y == 0:
                    if x-1 >= 0 and field[y][x-1] not in "()":
                       field[y][x-1] = " "
            else:
                fish_list.pop(id)
                break
    elif way == "r":
        for i in range(fish_length):
            if x-i >= 0:
                fish_list[id][0] = x-1
                fish_list[id][1] = y + random_y
                if field[y+random_y][x-i] not in "()":
                    field[y+random_y][x-i] = fish[i]
                
                if random_y !=0:
                    for j in range(x+1,x-fish_length,-1):
                        if 0 <= j < WIDTH and field[y][j] not in "()░":
                            field[y][j] = " "
                elif random_y == 0:
                    if x+1 < WIDTH and field[y][x+1] not in "()":
                       field[y][x+1] = " "

            else:
                fish_list.pop(id)
                break

def fish_movement(fish_list):

    for id,data in list(fish_list.items()):
        if data[7] == False:
            x,y,way,fish,fish_length,speed,speed_counter,*_ = data

            if speed_counter == 100: fish_list[id][6] = 0
            if speed == 2:
                if speed_counter % 2 == 0:
                    fish_movement_logic(way,x,y,fish,fish_length,id)
            else:
                fish_movement_logic(way,x,y,fish,fish_length,id)
            
            if id in fish_list.keys(): fish_list[id][6] += 1

def multi_fish_movement(field,fish_list):
    for id, data in list(fish_list.items()):
        if data[7] == True:
            x,y,way,fish,*_ = data
            temp_y = 0
            if way == "l":
                
                for i in range(y,y+len(fish)):
                    temp_x = 0
                    j = x
                    if field[i][j-1] not in "()oO.":
                        field[i][j-1] = " "
                    for j in range(x,x+len(fish[temp_y])):
                        if i + 1 < HEIGHT and j < WIDTH:
                            if field[i+1][j] not in "()oO.":
                                field[i+1][j] = fish[temp_y][temp_x]
                        else:
                            fish_list.pop(id)
                        temp_x +=1

                    
                    temp_y += 1
                if id in fish_list.keys():
                    fish_list[id][0] += 1

            elif way == "r":
                for i in range(y,y+len(fish)):
                    temp_x = len(fish[temp_y])
                    j = x
                    if j+1 < WIDTH and field[i][j+1] not in "()oO.":
                        field[i][j+1] = " "
                    for j in range(x,x-len(fish[temp_y]),-1):
                        temp_x -=1
                        if j-1 >= 0:
                            if field[i][j-1] not in "()oO.":
                                field[i][j-1] = fish[temp_y][temp_x]
                        else:
                            fish_list.pop(id)
                        

                    
                    temp_y += 1
                if id in fish_list.keys():
                    fish_list[id][0] -= 1               

input("Make sure ur console size is large enough \nPress Enter...")
air_coords = {}
seaweed_coords = {}
particle_coords = {}
field = []
fill_field(field)
generate_seaweed(field,seaweed_coords)
start = time.perf_counter()
k = 0
fish_list = {}

while True:
    sys.stdout.write(f"\033[{HEIGHT}F")
    elapsed_time = round(time.perf_counter() - start)+1
    
    # Рисуем поле
    draw_field(field,elapsed_time,round(k / elapsed_time,1))
    ###

    # Симуляция воздуха
    generate_air(field,air_coords)
    air_movement(field,air_coords)
    ###

    seaweed_movement(field,seaweed_coords,(k % 2 == 0))

    if k % 10 == 0:
        generate_fish(field,fish_list)
    fish_movement(fish_list)
    multi_fish_movement(field,fish_list)
    k += 1
    sys.stdout.flush()
    time.sleep(0.2)
