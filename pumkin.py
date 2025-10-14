import __builtins__
import utils, patterns


def plant_pumpkin(target=None, water=False,fert=False):
    # target: Int (None = infinite)

    if target:
        while num_items(Items.Pumpkin) < target:
            patterns.plant_pattern_uniform(Grounds.Soil, Entities.Pumpkin, water, fert)
    else:
        while True:
            patterns.plant_pattern_uniform(Grounds.Soil, Entities.Pumpkin, water, fert)

if __name__=='__main__':
    utils.move_to_origin()
    plant_pumpkin(None, True)
