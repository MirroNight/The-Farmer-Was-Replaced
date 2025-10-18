import __builtins__
import utils, patterns


plant_map = {
    Entities.Grass:  0,
    Entities.Bush:   1,
    Entities.Tree:   2,
    Entities.Carrot: 3,
}

plant_grass  = utils.get_plant_func(Grounds.Grassland, Entities.Grass,  0.0, False, True)
plant_Bush   = utils.get_plant_func(Grounds.Grassland, Entities.Bush,   0.0, False, True)
plant_tree   = utils.get_plant_func(Grounds.Grassland, Entities.Tree,   0.0, False, True)
plant_carrot = utils.get_plant_func(Grounds.Soil,      Entities.Carrot, 0.0, False, True)

plant_func_list = [
    plant_grass,
    plant_Bush,
    plant_tree,
    plant_carrot,
]


def get_next_location(arr, pos, plant_queue):
    # not planted
    if arr[pos[0]][pos[1]] < 0:
        return arr, pos, plant_queue
    
    # harvest first in queue
    elif len(plant_queue) > get_world_size() * (get_world_size()//2):
        while len(plant_queue) > get_world_size()//3:
            queue_pos = plant_queue.pop(0)
            utils.move_to(queue_pos[0], queue_pos[1])
            while not can_harvest():
                pass
            harvest()
            if get_ground_type() != Grounds.Grassland:
                till()
            arr[queue_pos[0]][queue_pos[1]] = -1
        return arr, queue_pos, plant_queue
    
    # find somewhere else
    else:
        for x in range(get_world_size()):
            for y in range(get_world_size()):
                if arr[x][y] < 0:
                    return arr, (x,y), plant_queue


def polyculture(arr, plant_queue):
    # arr init to -1
    # plnat_queue is empty list
    crop_next, pos_next = get_companion()

    # decide next position
    arr, pos_next, plant_queue = get_next_location(arr, pos_next, plant_queue)
    utils.move_to(pos_next[0], pos_next[1])
    # plant
    plant_func_list[plant_map[crop_next]]()
    # add to queue
    plant_queue.append((pos_next[0], pos_next[1]))
    # update arr
    arr[pos_next[0]][pos_next[1]] = plant_map[crop_next]

    return arr, plant_queue


if __name__=='__main__':
    arr = utils.init_arr(get_world_size(), -1)

    utils.move_to(0,0)
    utils.get_plant_func(Grounds.Soil, Entities.Carrot)()
    plant_queue = []
    
    while True:
        arr, plant_queue = polyculture(arr, plant_queue)
