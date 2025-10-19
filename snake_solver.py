import __builtins__
import utils


def get_hamilton_path(arr):
    index, max_index = 0, get_world_size()**2
    for x in range(get_world_size()):
        arr[0][x], index = index, index+1
    
    for y in range(1, get_world_size()):
        for x in range(
                get_world_size()**(y%2) + (-1)*(y%2),
                get_world_size()**((y+1)%2) + (-1)*(y%2),
                (-1)**(y%2)
                ):
            arr[y][x], index = index, index+1
    
        # quivilant to:
        # if y%2:
        #     for x in range(get_world_size()-1, 0, -1):
        #         pass
        # else:
        #     for x in range(1, get_world_size(), 1):
        #         pass

    for y in range(get_world_size()-1, 0, -1):
        arr[y][0], index = index, index+1
    return arr


def snake_move_prime(_x, _y):
    if _x == 0:
        if _y == 0:
            move(East)
        else:
            move(South)
    elif _x == 1 and _y == get_world_size()-1:
        move(West)
    elif _y%2:
        if _x > 1:
            move(West)
        else:
            move(North)
    else:
        if _x < get_world_size()-1:
            move(East)
        else:
            move(North)

## TODO: add tail check
def snake_move_dest(arr, _x, _y, x, y, tail_length):
    apple     = arr[y][x]
    val_north = arr[(_y+1)%get_world_size()][_x]
    val_east  = arr[_y][(_x+1)%get_world_size()]
    val_west  = arr[_y][_x-1]
    tail_end  = (arr[_y][_x] - tail_length + get_world_size()**2) % get_world_size()**2

    if _x == 0 and _y == 0: # at (0,0): East, West
        move(East)
    elif _x == 0 and _y != 0: # at x=0: South
        move(South)
    else:
        if _y%2: # y%2 == 1: North, West
            if _x == 1 and _y != get_world_size()-1:
                move(North)
            elif (apple - val_north) >= 0: # apple is >= north
                if (val_north < tail_end) or (not move(North)):
                    move(West)
            # apple is < north
            elif (apple - val_west) < 0: # apple is < west
                if (val_north < tail_end) or (not move(North)):
                    move(West)
            else:
                move(West)
        else: # y%2 == 0: North, East
            if _x == get_world_size()-1 and _y != get_world_size()-1:
                move(North)
            elif (apple - val_north) >= 0: # apple is >= north
                if (val_north < tail_end) or (not move(North)):
                    move(East)
            # apple is < north
            elif (apple - val_east) < 0: # apple is < east
                if (val_north < tail_end) or (not move(North)):
                    move(East)
            else:
                move(East)


def snake_move(arr, x, y, tail_length):
    _x, _y = get_pos_x(), get_pos_y()
    if (x==None) and (y==None):
        snake_move_prime(_x, _y)
    else:
        snake_move_dest(arr, _x, _y, x, y, tail_length)
    return get_entity_type() == Entities.Apple


def get_apple(arr, x, y, tail_length):
    is_apple = False
    while not is_apple:
        is_apple = snake_move(arr, x, y, tail_length)
    tail_length = tail_length+1
    x, y = measure()
    return arr, x, y, tail_length 


def solve_snake(arr):
    # arr is hamilton path
    change_hat(Hats.Dinosaur_Hat)
    x, y, tail_length = None, None, 1
    while tail_length < (get_world_size()**2 - 1):
        arr, x, y, tail_length = get_apple(arr, x, y, tail_length)
    change_hat(Hats.Brown_Hat)
    return arr


if __name__ == '__main__':
    clear()
    arr = utils.init_arr()
    arr = get_hamilton_path(arr)
    # utils.arr_display(arr, 'hamilton path')
    arr = solve_snake(arr)
