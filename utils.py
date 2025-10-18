import __builtins__


crop_ground_map = {
    Entities.Grass:  None,
    Entities.Bush:   None,
    Entities.Tree:   None,
    Entities.Carrot: Grounds.Soil,
}


def move_to_origin():
    move_to(0, 0)


def move_to(x, y):
    # x: int
    # y: int
    x0, y0 = get_pos_x(), get_pos_y()
    
    def move_n(direction, n):
        for i in range(n):
            move(direction)
    
    def move_wrap(a, b, d1, d2):
        if abs(b-a) < get_world_size()/2:
            if b-a > 0:
                move_n(d1, b-a)
            else:
                move_n(d2, a-b)
        else:
            if get_world_size()-b+a < get_world_size()/2:
                move_n(d2, get_world_size()-b+a)
            else:
                move_n(d1, get_world_size()-a+b)

    move_wrap(x0, x, East, West)
    move_wrap(y0, y, North, South)


def enum(iterable, func):
    for i in range(len(iterable)):
        func(i, iterable[i])


def arr_display(arr, title=None):
    quick_print('')
    if title:
        quick_print(title)
    for i in range(get_world_size()):
        quick_print(i, arr[i])


def enum_display(iterable, title=None):
    quick_print('')
    if title:
        quick_print(title)

    def enum_func(i, e):
        quick_print(i, e)
    
    enum(iterable, enum_func)


def get_plant_func(ground, crop, water_level_threshold=0.5, wait=False, fert=False):

    def check_harvest_till_plant():
        # ground: Grounds
        # crop:   Entities

        if wait and (not can_harvest()) :
            pass

        if can_harvest():
            harvest()
            if get_ground_type() != ground:
                till()
            plant(crop)
        elif ((not get_entity_type()) 
             or
             (get_entity_type() == Entities.Dead_Pumpkin)):
            plant(crop)

        if get_water() < water_level_threshold:
            use_item(Items.Water)

    return check_harvest_till_plant


def init_arr(size=get_world_size(), val=0):
    xrr = []
    for x in range(size):
        yrr = []
        for y in range(size):
            yrr.append(val)
        xrr.append(yrr)
    
    return xrr


def map_cond(arr, cond, val=1):
    for x in range(get_world_size()):
        for y in range(get_world_size()):
            if cond(x, y):
                arr[x][y] = val
    
    return arr


def arr_fill(arr, x, y, size, val=0):
    for xi in range(size):
        for yi in range(size):
            arr[x+xi][y+yi] = val
    
    return arr


def sum_kernel(arr, x, y, size, cond):
    ret = 0
    for xi in range(x, x+size):
        for yi in range(y, y+size):
            if cond(arr, xi, yi):
                ret += 1
    
    return ret


def rank_list_add(rank_list, key, val, sp_cond=None, sp_func=None):
    if sp_cond(key, val):
        return sp_func(key, val)
    if not len(rank_list):
        rank_list.append((key, val))
        return
    
    def enum_func(i, e):
        if key > e[0]:
                rank_list.insert(i, (key, val))
        else:
            if i == len(rank_list)-1:
                rank_list.append((key, val))

    enum(rank_list, enum_func)


def arr_sum_kernel(arr, size, cond):
    def is_zero(key, val):
        return key == 0

    def skip(key, val):
        pass

    arr_kernel_sum = init_arr(get_world_size())
    rank_list = []
    for x in range(get_world_size()-size+1):
        for y in range(get_world_size()-size+1):
            tmp = sum_kernel(arr, x, y, size, cond)
            arr_kernel_sum[x][y] = tmp

            rank_list_add(rank_list, tmp, (x, y), is_zero, skip)

    return arr_kernel_sum, rank_list


if __name__=='__main__':
    move_to(0,0)
    move_to(8,0)
    
    pass
