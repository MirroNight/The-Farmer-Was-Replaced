import __builtins__
import utils, patterns

def check_and_harvest_pumpkin(arr, x, y, size, xi=0, yi=0, mv=True):
    # utils.arr_disply(arr, 'check')
    if arr[x][y] > size**2:
        if mv:
            utils.move_to(x+xi, y+yi)
        if can_harvest():
            harvest()
            plant(Entities.Pumpkin)
            # utils.arr_disply(arr, '0 before')
            arr = utils.arr_fill(arr, x, y, size, 0)
            # utils.arr_disply(arr, '0 after')
    return arr


def subregions_pumpkin(arr, x, y, size=6):
    # quick_print('----- -----')
    # quick_print('sub cord', x, y, size)
    # utils.arr_disply(arr, 'sub before')
    
    if arr[x][y] <= 0:
        utils.move_to(x, y)
        if can_harvest():
            arr[x][y] *= -1
            arr[x][y] += 2
            sub_ori = 1
        elif not (get_entity_type() == Entities.Pumpkin):
            plant(Entities.Pumpkin)
            sub_ori = -1
        else:
            sub_ori = -1
    else:
        arr = check_and_harvest_pumpkin(arr, x, y, size)
        if arr[x][y] < 0:
            sub_ori = -1
        else:
            sub_ori = 1
    # quick_print(sub_ori)

    for xi in range(size):
        for yi in range(size):
            if (not xi) and (not yi):
                continue

            if arr[x+xi][y+yi] == 1:
                continue
            else:
                utils.move_to(x+xi, y+yi)

            if can_harvest():
                arr[x+xi][y+yi] = 1
                arr[x][y] += 1*sub_ori
                arr = check_and_harvest_pumpkin(arr, x, y, size, xi, yi, False)
            elif get_entity_type() == Entities.Pumpkin:
                continue
            else:
                plant(Entities.Pumpkin)
                arr[x+xi][y+yi] = 0
    
    return arr


def remainder_pumpkin(arr, size):
    remainder1 = get_world_size() % size
    remainder2 = get_world_size() % remainder1
    start = get_world_size() - remainder1

    if remainder2:
        # bottom right 2nd remainder
        for xi in range(start, get_world_size(), remainder2):
            for _ in range(0, get_world_size(), remainder2):
                arr = subregions_pumpkin(arr, xi, 0, remainder2, size)
        
        # bottom left 1st remainder
        for y in range(remainder2, get_world_size(), remainder1):
            arr = subregions_pumpkin(arr, start, y, remainder1, size)

        # top left 2nd remainder
        for yi in range(start, get_world_size(), remainder2):
            for _ in range(0, get_world_size(), remainder2):
                arr = subregions_pumpkin(arr, 0, yi, remainder2, size)
        
        # top left 1st remainder
        for x in range(remainder2, get_world_size(), remainder1):
            arr = subregions_pumpkin(arr, x, start, remainder1, size)
    
    return arr


def main_pumpkin(arr, size):
    # arr holds bitmap of live pumpkins

    # utils.arr_disply(arr, 'main before')

    for x in range(get_world_size() // size):
        for y in range(get_world_size() // size):
            arr = subregions_pumpkin(arr, x*size, y*size, size)

    if get_world_size() % size:
        arr = remainder_pumpkin(arr, size)

    # utils.arr_disply(arr, 'main after')

    return arr


def restock_pumpkin(arr, init=False, size=get_world_size()):
    plant_func1 = utils.get_plant_func(Grounds.Soil, Entities.Pumpkin)
    plant_pattern = patterns.get_pattern_func(Items.Pumpkin, plant_func1)
    
    if init:
        plant_pattern()
    else:
        arr = main_pumpkin(arr, size)
    return arr


if __name__=='__main__':
    # set_world_size(10)
    utils.move_to_origin()
    
    arr = restock_pumpkin(utils.init_arr(get_world_size()))
    while True:
        arr = restock_pumpkin(arr)
