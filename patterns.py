import __builtins__
import utils

def plant_pattern_uniform(ground, crop, water=False, fert=False):
    # ground: Grounds
    # crop:   Entities
    # water:  Bool

    for x in range(get_world_size()):
        for y in range(get_world_size()):
            utils.check_harvest_till_plant(ground, crop, fert)
            if water:
                utils.water()
            move(East)
        move(North)


def plant_pattern_checkerboard(ground1, ground2,
                               crop1, crop2,
                               water1=False, water2=False,
                               fert1=False,  fert2=False):
    # ground1/2: Grounds
    # crop1/2:   Entities
    # water1/2:  Bool
    # fert1/2:   Bool

    for x in range(get_world_size()):
        for y in range(get_world_size()):
            if (x % 2) == (y % 2):
                utils.check_harvest_till_plant(ground1, crop1, fert1)
                if water1:
                    utils.water()
            else:
                utils.check_harvest_till_plant(ground2, crop2, fert2)
                if water2:
                    utils.water()
            move(East)
        move(North)

if __name__=='__main__':
    pass
