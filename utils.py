import __builtins__

def move_to_origin():
    for x in range(get_pos_x()):
        move(West)
    for y in range(get_pos_y()):
        move(South)


def move_to(x, y):
    # x: int
    # y: int
    delta_x = x - get_pos_x()
    delta_y = y - get_pos_y()

    if delta_x > 0:
        for x in range(delta_x):
            move(East)
    elif delta_x < 0:
        for x in range(-delta_x):
            move(West)

    if delta_y > 0:
        for y in range(delta_y):
            move(North)
    elif delta_y < 0:
        for y in range(-delta_y):
            move(South)


def check_harvest_till_plant(ground, crop, fert=False):
    # ground: Grounds
    # crop:   Entities
    if can_harvest():
        harvest()
        if get_ground_type() != ground:
            till()
        plant(crop)
    elif get_entity_type() == Entities.Dead_Pumpkin:
        plant(crop)
        if fert:
            use_item(Items.Fertilizer)
            harvest()
    elif not get_entity_type():
        plant(crop)


def water(threshhold=0.1):
    if get_water() < 0.1:
        use_item(Items.Water)


def init_arr(size, val=0):
    # size: int

    xrr = []
    yrr = []

    for y in range(size):
        yrr.append(val)
    for x in range(size):
        xrr.append(yrr)
    
    return xrr


if __name__=='__main__':
    pass