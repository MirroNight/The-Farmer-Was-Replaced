import __builtins__
import utils
import hay, wood, carrot, pumkin


target_hay    = 1000
target_wood   = 1000
target_carrot = 1000
target_pumpkin= 1000


def fill():
    while (num_items(Items.Hay) < target_hay):
        hay.plant_hay(target_hay)

    while (num_items(Items.Wood) < target_wood):
        wood.plant_bush(target_wood)

    while (num_items(Items.Carrot) < target_carrot):
        carrot.plant_carrot(target_carrot)
    
    while (num_items(Items.Pumpkin) < target_pumpkin):
        pumkin.plant_carrot(target_pumpkin)


if __name__=='__main__':
    utils.move_to_origin()
    # fill()
    crop_map = utils.init_arr(get_world_size())
    quick_print(len(crop_map), len(crop_map[0]))