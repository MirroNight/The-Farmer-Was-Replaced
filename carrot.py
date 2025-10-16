import __builtins__
import utils, patterns


def restock_carrot():
    plant_func1 = utils.get_plant_func(Grounds.Soil, Entities.Carrot)
    plant_pattern = patterns.get_pattern_func(Items.Carrot, plant_func1)

    plant_pattern()


if __name__=='__main__':
    utils.move_to_origin()
    while(True):
        restock_carrot()
