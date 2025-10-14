import __builtins__
import utils, patterns


def make_grass_field():
    for x in range(get_world_size()):
        for y in range(get_world_size()):
            if can_harvest():
                harvest()
            if get_ground_type() != Grounds.Grassland:
                till()
            move(East)
        move(North)


def harvest_grass_field():
    for x in range(get_world_size()):
        for y in range(get_world_size()):
            harvest()
            move(East)
        move(North)


def plant_hay(target=None):
    # target: Int (None = infinite)

    make_grass_field()

    if target:
        while num_items(Items.Hay) < target:
            harvest_grass_field()
    else:
        while True:
            harvest_grass_field()
        

if __name__=='__main__':
    utils.move_to_origin()
    plant_hay()
