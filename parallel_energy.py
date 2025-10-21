import __builtins__
import utils


arr, petals_cnt = [], 15


def plant_sunflower_x():
    y = get_pos_y()
    plant_sunflower = utils.get_plant_func(Grounds.Soil, Entities.Sunflower, 0.5)

    size_list = []
    for x in range(get_world_size()):
        plant_sunflower()
        size_list.append(measure())
        move(East)
    return size_list


def harvest_by_petals_cnt_x():
    global arr
    global petals_cnt
    y = get_pos_y()
    for x in range(get_world_size()):
        if arr[y][x] == petals_cnt:
            utils.move_to(x, y)
            while not can_harvest():
                pass
            harvest()
    return arr[y]


def non_blocking_join(arr, drones, cnt):
    for i in range(len(drones)):
        if drones[i] == None:
            continue
        if has_finished(drones[i]):
            arr[i] = wait_for(drones[i])
            drones[i] = None
            cnt -= 1
    return arr, cnt


def parallel_restock_energy():
    # plant
    global arr
    global petals_cnt
    arr, drones, petals_cnt = utils.init_arr(get_world_size()), [], 15
    for y in range(get_world_size()-1):
        utils.move_to(0, y)
        drones.append(spawn_drone(plant_sunflower_x))
    move(North)
    arr[get_pos_y()] = plant_sunflower_x()

    # plant join
    cnt = len(drones)
    while cnt:
        arr, cnt = non_blocking_join(arr, drones, cnt)
    
    # harvest by size
    while petals_cnt >= 7:
        # harvest
        drones = []
        for y in range(get_world_size()-1):
            utils.move_to(0, y)
            drones.append(spawn_drone(harvest_by_petals_cnt_x))
        move(North)
        harvest_by_petals_cnt_x()

        # harvest join
        cnt = len(drones)
        while cnt:
            arr, cnt = non_blocking_join(arr, drones, cnt)
        petals_cnt -= 1
    return 0


if __name__ == '__main__':
    parallel_restock_energy()
