import __builtins__
import utils
import patterns


def map_size(arr):
    for y in range(get_world_size()):
        for x in range(0, get_world_size(), 3):
            utils.move_to(x,y)
            arr[y][x-1] = measure(West)
            arr[y][x] = measure()
            arr[y][(x+1)%get_world_size()] = measure(East)
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


def bubble_sort_x(arr, y):
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
    
    x, lb, ub = 0, 0, get_world_size()-1
    while ub >= lb:
        arr, x, ub = push_larger_to_right(arr, x, y, ub)
        arr, x, lb = push_smaller_to_left(arr, x, y, lb)

    return arr


def bubble_sort_y(arr, x):
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
    
    y, lb, ub = 0, 0, get_world_size()-1
    while ub >= lb:
        arr, y, ub = push_larger_to_top(arr, x, y, ub)
        arr, y, lb = push_smaller_to_bot(arr, x, y, lb)

    return arr


def restock_cactus():
    arr = utils.init_arr(get_world_size(), -1)
    plant_cacuts = utils.get_plant_func(Grounds.Soil, Entities.Cactus, 0.0)
    plant_pattern = patterns.get_pattern_func(Items.Cactus, plant_cacuts)

    arr = plant_pattern(arr)
    # arr = map_size(arr)

    utils.arr_display(arr, 'map')
    pass

    utils.move_to_origin()
    
    for y in range(get_world_size()):
        arr = bubble_sort_x(arr, y)
    for x in range(get_world_size()):
        arr = bubble_sort_y(arr, x)

    utils.move_to_origin()
    harvest()
    return 0


if __name__ == '__main__':
    utils.move_to_origin()

    while True:
        restock_cactus()
