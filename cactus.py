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


def get_cactus_sorted_arr(arr):
    bins = [[], [], [], [], [],   [], [], [], [], [],]
    arr_sorted = utils.init_arr(get_world_size(), None)
    for y in range(get_world_size()):
        for x in range(get_world_size()):
            bins[arr[y][x]].append(arr[y][x])

    size_cnt = {}
    for size in range(10):
        size_cnt[size] = len(bins[size])

    x, y = get_world_size()-1, get_world_size()-1
    for size in range(9, -1, -1):
        while(bins[size]):
            arr_sorted[y][x] = bins[size].pop()
            x -= 1
            if x<0:
                x += get_world_size()
                y -= 1
    return arr_sorted, size_cnt


def mark_sorted(arr, size_cnt):
    size_large, xy_large = 9, (0,0)
    size_small, xy_small = 0, (get_world_size()-1, get_world_size()-1)
    end_large, end_small = (get_world_size()-1, get_world_size()-1), (0,0)

    # ignore the 0s from start
    for x in range(get_world_size()):
        for y in range(get_world_size()):
            if arr[y][x] == 0:
                arr[y][x] = None
                size_cnt[0] -= 1
                if y == get_world_size()-1:
                    end_small = (x+1, 0)
                else:
                    end_small = (x, y+1)
            else:
                break
        if arr[y][x] != 0:
            break

    # ignore the 9s from end
    for x in range(get_world_size()-1, -1, -1):
        for y in range(get_world_size()-1, -1, -1):
            if arr[y][x] == 9:
                arr[y][x] = None
                size_cnt[9] -= 1
                if y == 0:
                    end_large = (x-1, get_world_size()-1)
                else:
                    end_large = (x, y-1)
            else:
                break
        if arr[y][x] != 9:
            break

    return arr, size_cnt, size_large, xy_large, end_large, end_small, size_small, xy_small


def get_nearest(arr, size_cnt, size, last_pos, order):
    def out_of_bound(x):
        if (x >= get_world_size()) or (x < 0):
            return True
        return False

    # reset x/y_st when starting a new size
    if order == 'large':
        step = -1
    elif order == 'small':
        step = 1
    
    # size empty
    if not size_cnt[size]:
        if size_cnt[size] == 0:
            size_cnt.pop(size)
            if not size_cnt:
                return None, None, (0, 0)
        size += step
    
    st_x, st_y = last_pos
    size_cnt[size] -= 1
    
    while True:
        if size == None:
            pass
        elif arr[st_y][st_x] == size:
            return size_cnt, size, (st_x, st_y)
        st_y += 1*step
        if out_of_bound(st_y):
            st_y = (st_y + get_world_size()) % get_world_size()
            st_x += 1*step
        if out_of_bound(st_y):
            return False


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


def take_cactus_to_xy(arr, x0, y0, x, y, order):
    # x: int
    # y: int
    def move_n(arr, delta, direction_pair):
        if direction_pair == (East, West):
            x_multi, y_multi = 1, 0
        elif direction_pair == (North, South):
            x_multi, y_multi = 0, 1

        success = True
        while delta != 0:
            # quick_print('before: ', order, delta, old_pos, success)
            if delta > 0:
                if arr[get_pos_y()+1*y_multi][get_pos_x()+1*x_multi] == None:
                    success = False
                    break
                arr = swap_and_move(arr, direction_pair[0])
                delta -= 1
            elif delta < 0:
                if arr[get_pos_y()-1*y_multi][get_pos_x()-1*x_multi] == None:
                    success = False
                    break
                arr = swap_and_move(arr, direction_pair[1])
                delta += 1
            # quick_print('after:  ', order, delta, old_pos, success)
        return arr, delta, success
    
    if not (x0 == x and y0 == y):
        utils.move_to(x0, y0)
        delta_x, delta_y = x-x0, y-y0

        success = True
        while delta_x != 0 and success:
            arr, delta_x, success = move_n(arr, delta_x, (East, West))
        success = True
        while delta_y != 0 and success:
            arr, delta_y, success = move_n(arr, delta_y, (North, South))
        success = True
        while delta_x != 0 and success:
            arr, delta_x, success = move_n(arr, delta_x, (East, West))
        arr[get_pos_y()][get_pos_x()] = None
    else:
        arr[y][x] = None
    
    if order == 'large':
        if y == 0:
            old_pos = (x-1, get_world_size()-1)
        else:
            old_pos = (x, y-1)
    if order == 'small':
        if y == get_world_size()-1:
            old_pos = (x+1, 0)
        else:
            old_pos = (x, y+1)

    return arr, old_pos


def restock_cactus():
    arr = utils.init_arr(get_world_size(), -1)
    plant_cacuts = utils.get_plant_func(Grounds.Soil, Entities.Cactus, 0.0)
    plant_pattern = patterns.get_pattern_func(Items.Cactus, plant_cacuts)

    arr = plant_pattern(arr)
    # arr = map_size(arr)

    # utils.arr_display(arr, 'map')
    pass

    sorted_arr, size_cnt = get_cactus_sorted_arr(arr)
    # utils.arr_display(sorted_arr, 'sorted map')
    pass

    utils.move_to_origin()
    size_large, xy_large, end_large = 9, (0,0), (get_world_size()-1, get_world_size()-1)
    size_small, xy_small, end_small = 0, (get_world_size()-1, get_world_size()-1), (0,0)
    
    # arr, size_cnt, size_large, xy_large, end_large, end_small, size_small, xy_small = mark_sorted(arr, size_cnt)
    # utils.arr_display(arr, 'marked')


    while size_cnt:
        utils.arr_display(arr)
        quick_print(size_large, 'start_large: ', xy_large, '    end_large: ', end_large)
        quick_print(size_small, 'start_small: ', xy_small, '    end_small: ', end_small)

        size_cnt, size_large, xy_large = get_nearest(arr, size_cnt, size_large, end_large, 'large')
        if size_large == None:
            break
        arr, end_large = take_cactus_to_xy(arr, xy_large[0], xy_large[1], end_large[0], end_large[1], 'large')

        size_cnt, size_small, xy_small = get_nearest(arr, size_cnt, size_small, end_small, 'small')
        if size_small == None:
            break
        arr, end_small = take_cactus_to_xy(arr, xy_small[0], xy_small[1], end_small[0], end_small[1], 'small')

    utils.move_to_origin()
    harvest()
    return 0


if __name__ == '__main__':
    utils.move_to_origin()

    while True:
        restock_cactus()
