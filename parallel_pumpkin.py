import __builtins__
import utils

fert = False
arr = utils.init_arr(get_world_size(), -1)  # will init to global 2D arr


def replant_pumpkin_x(checklist, y):
    global fert
    done_list = []
    for x in checklist:
        utils.move_to(x,y)
        if not (get_entity_type() == Entities.Pumpkin and can_harvest()):
            plant(Entities.Pumpkin)
            if fert:
                use_item(Items.Fertilizer)
        else:
            done_list.append(x)
    for x in done_list:
        checklist.remove(x)
    return checklist


def plant_pumpkin_x():
    global fert
    y = get_pos_y()
    checklist = []
    plant_pupmpkin = utils.get_plant_func(Grounds.Soil, Entities.Pumpkin, 0.0)
    for x in range(get_world_size()):
        if can_harvest():
            harvest()
        if get_ground_type() != Grounds.Soil:
            till()
        plant_pupmpkin()
        if fert:
            use_item(Items.Fertilizer)
        checklist.append(x)
        move(East)

    while checklist:
        checklist = replant_pumpkin_x(checklist, y)

    return 0


def non_blocking_join(drones, cnt):
    for i in range(len(drones)):
        if drones[i] == None:
            continue
        if has_finished(drones[i]):
            wait_for(drones[i])
            drones[i] = None
            cnt -= 1
    return cnt


def parallel_restock_pumpkin(use_fert=False):
    # plant
    global fert
    fert, drones = use_fert, []
    for y in range(get_world_size()-1):
        utils.move_to(0, y)
        drones.append(spawn_drone(plant_pumpkin_x))
    move(North)
    plant_pumpkin_x()

    # plant join
    cnt = len(drones)
    while cnt:
        cnt = non_blocking_join(drones, cnt)

    harvest()
    return 0

if __name__ == '__main__':
    parallel_restock_pumpkin(True)
