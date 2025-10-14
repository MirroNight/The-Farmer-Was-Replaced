import __builtins__
import utils, patterns

def plant_carrot(target=None):
    # target: Int (None = infinite)

    if target:
        while num_items(Items.Carrot) < target:
            patterns.plant_pattern_uniform(Grounds.Soil, Entities.Carrot)
    else:
        while True:
            patterns.plant_pattern_uniform(Grounds.Soil, Entities.Carrot)

if __name__=='__main__':
    utils.move_to_origin()
    plant_carrot()
