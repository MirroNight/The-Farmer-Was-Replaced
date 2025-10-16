import __builtins__
import utils, patterns


def restock_wood():
    plant_func1 = utils.get_plant_func(Grounds.Soil, Entities.Tree)
    plant_func2 = utils.get_plant_func(Grounds.Soil, Entities.Bush)
    plant_pattern = patterns.get_pattern_func(Items.Wood, plant_func1, plant_func2)

    plant_pattern()


if __name__=='__main__':
    utils.move_to_origin()
    while True:
        restock_wood()
