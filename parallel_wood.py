import __builtins__
import utils


def plant_tree_x(cycles=10):
    y = get_pos_y()
    plant_tree = utils.get_plant_func(Grounds.Grassland, Entities.Tree, 0.7)
    plant_bush = utils.get_plant_func(Grounds.Grassland, Entities.Bush, 0.0)

    for _ in range(cycles):
        for x in range(get_world_size()):
            if (x+y)%2:
                plant_bush()
            else:
                plant_tree()
            move(East)
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


def parallel_restock_wood():
    # plant
    drones = []
    for y in range(get_world_size()-1):
        utils.move_to(0, y)
        drones.append(spawn_drone(plant_tree_x))
    move(North)
    plant_tree_x()

    # plant join
    cnt = len(drones)
    while cnt:
        cnt = non_blocking_join(drones, cnt)
    
    return 0

if __name__ == '__main__':
    parallel_restock_wood()