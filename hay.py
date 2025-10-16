import __builtins__
import utils, patterns


def make_grass_field():
    for x in range(get_world_size()):
        for y in range(get_world_size()):
            if can_harvest():
                harvest()
            if get_ground_type() != Grounds.Grassland:
                till()
            move(North)
        move(East)


def harvest_grass_field():
    for x in range(get_world_size()):
        for y in range(get_world_size()):
            harvest()
            move(North)
        move(East)


def restock_hey():
    make_grass_field()
    harvest_grass_field()


if __name__=='__main__':
    utils.move_to_origin()
    while True:
        restock_hey()
