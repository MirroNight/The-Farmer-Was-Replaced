import __builtins__
import utils


arr = utils.init_arr(get_world_size(), -1)  # will init to global 2D arr


def plant_cactus_x():
    global arr
    y = get_pos_y()
    plant_cactus = utils.get_plant_func(Grounds.Soil, Entities.Cactus)
    for x in range(get_world_size()):
        plant_cactus()
        arr[y][x] = measure()
        move(East)
    return arr


def swap_and_move(arr, direction):
    x, y = get_pos_x(), get_pos_y()
    swap(direction)
    move(direction)

    if direction == East:
        xi, yi = x+1, y
    elif direction == West:
        xi, yi = x-1, y
    elif direction == North:
        xi, yi = x, y+1
    elif direction == South:
        xi, yi = x, y-1

    arr[y][x], arr[yi][xi] = arr[yi][xi], arr[y][x]

    return arr


def bubble_sort_x():
    def push_larger_to_right(arr, x, y, ub):
        utils.move_to(x, y)
        ticks = 0
        while x < ub:
            if arr[y][x] > arr[y][x+1]:
                arr = swap_and_move(arr, East)
                ticks += 1
            else:
                move(East)
            x += 1
        if ticks == 0:
            ub = get_world_size()//2-1
        return arr, x-1, ub-1
    
    def push_smaller_to_left(arr, x, y, lb):
        utils.move_to(x, y)
        ticks = 0
        while x > lb:
            if arr[y][x] < arr[y][x-1]:
                arr = swap_and_move(arr, West)
                ticks += 1
            else:
                move(West)
            x -= 1
        if ticks == 0:
            lb = get_world_size()//2+1
        return arr, x+1, lb+1
    
    global arr
    x, y, lb, ub = 0, get_pos_y(), 0, get_world_size()-1
    while ub >= lb:
        arr, x, ub = push_larger_to_right(arr, x, y, ub)
        arr, x, lb = push_smaller_to_left(arr, x, y, lb)
    return arr


def bubble_sort_y():
    def push_larger_to_top(arr, x, y, ub):
        utils.move_to(x, y)
        ticks = 0
        while y < ub:
            if arr[y][x] > arr[y+1][x]:
                arr = swap_and_move(arr, North)
                ticks += 1
            else:
                move(North)
            y += 1
        if ticks == 0:
            ub = get_world_size()//2-1
        return arr, y-1, ub-1
    
    def push_smaller_to_bot(arr, x, y, lb):
        utils.move_to(x, y)
        ticks = 0
        while y > lb:
            if arr[y][x] < arr[y-1][x]:
                arr = swap_and_move(arr, South)
                ticks += 1
            else:
                move(South)
            y -= 1
        if ticks == 0:
            lb = get_world_size()//2+1
        return arr, y+1, lb+1
    
    global arr
    x, y, lb, ub = get_pos_x(), 0, 0, get_world_size()-1
    while ub >= lb:
        arr, y, ub = push_larger_to_top(arr, x, y, ub)
        arr, y, lb = push_smaller_to_bot(arr, x, y, lb)
    return arr


def non_blocking_join(ret_arr, drones, cnt):
    for i in range(len(drones)):
        if drones[i] == None:
            continue
        if has_finished(drones[i]):
            ret_arr[i], cnt = wait_for(drones[i]), cnt-1
            drones[i] = None
    return ret_arr, cnt


def parallel_restock_cactus():
    global arr
    arr = utils.init_arr(get_world_size(), -1)

    # plant
    drones = []
    for y in range(get_world_size()-1):
        utils.move_to(0, y)
        drones.append(spawn_drone(plant_cactus_x))
    move(North)
    arr = plant_cactus_x()

    # plant join
    cnt, ret_arr = len(drones), []
    for _ in range(cnt):
        ret_arr.append(None)
    while cnt:
        ret_arr, cnt = non_blocking_join(ret_arr, drones, cnt)
    for y in range(len(drones)):
        arr[y] = ret_arr[y][y]
    
    # sort_x
    drones = []
    for y in range(get_world_size()-1):
        utils.move_to(0, y)
        drones.append(spawn_drone(bubble_sort_x))
    move(North)
    arr = bubble_sort_x()

    # sort_x join
    cnt, ret_arr = len(drones), []
    for _ in range(cnt):
        ret_arr.append(None)
    while cnt:
        ret_arr, cnt = non_blocking_join(ret_arr, drones, cnt)
    for y in range(len(drones)):
        arr[y] = ret_arr[y][y]
    
    # sort_y
    drones = []
    for x in range(get_world_size()-1):
        utils.move_to(x, 0)
        drones.append(spawn_drone(bubble_sort_y))
    move(East)
    arr = bubble_sort_y()

    # sort_y join
    cnt, ret_arr = len(drones), []
    for _ in range(cnt):
        ret_arr.append(None)
    while cnt:
        ret_arr, cnt = non_blocking_join(ret_arr, drones, cnt)
    for x in range(len(drones)):
        for y in range(get_world_size()):
            arr[y][x] = ret_arr[x][y][x]

    harvest()

if __name__ == '__main__':
    parallel_restock_cactus()
