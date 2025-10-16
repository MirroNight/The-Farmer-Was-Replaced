import __builtins__
import utils
import hay, wood, carrot, pumpkin


target_hay    = 1000
target_wood   = 1000
target_carrot = 1000
target_pumpkin= 1000


def fill():
    while (num_items(Items.Hay) < target_hay):
        hay.restock_hey()
    while (num_items(Items.Wood) < target_wood):
        wood.restock_wood()
    while (num_items(Items.Carrot) < target_carrot):
        pass
    while (num_items(Items.Pumpkin) < target_pumpkin):
        pass

if __name__=='__main__':
    utils.move_to_origin()
    # fill()
    crop_map = utils.init_arr(get_world_size())
    quick_print(len(crop_map), len(crop_map[0]))