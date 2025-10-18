import __builtins__
import utils
import patterns


def map_petals_cnt(arr):
    for y in range(get_world_size()):
        for x in range(get_world_size()):
            utils.move_to(x,y)
            arr[y][x] = measure()
    return arr


def bin_petals_cnt(arr):
    bins = {7:[], 8:[], 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[],}
    for y in range(get_world_size()):
        for x in range(get_world_size()):
            bins[arr[y][x]].append((x,y))
    return bins


def harvest_next(bins, petals_cnt):
    if not bins[petals_cnt]:
        bins.pop(petals_cnt)
        petals_cnt -= 1
        if petals_cnt == 6:
            bins = None
            return None, None
        
    x, y = bins[petals_cnt].pop(0)
    # quick_print(x, y, petals_cnt)
    utils.move_to(x, y)
    while not can_harvest():
        pass
    harvest()
    return bins, petals_cnt


def restock_power(arr):
    petals_cnt = 15
    plant_sunflower = utils.get_plant_func(Grounds.Soil, Entities.Sunflower)
    arr = patterns.get_pattern_func(Items.Power, plant_sunflower)(arr)
    bins = bin_petals_cnt(arr)

    while petals_cnt:
        bins, petals_cnt = harvest_next(bins, petals_cnt)
    return arr


if __name__ == '__main__':
    utils.move_to_origin()

    arr = utils.init_arr()
    while True:
        arr = restock_power(arr)
