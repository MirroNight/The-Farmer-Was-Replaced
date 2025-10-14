import __builtins__
import utils, patterns

def plant_bush(target=None):
    # target: Int (None = infinite)

    if target:
        while num_items(Items.Wood) < target:
            patterns.plant_pattern_checkerboard(Grounds.Soil,  Grounds.Soil,
                                                Entities.Tree, Entities.Bush,
                                                True)
    else:
        while True:
            patterns.plant_pattern_checkerboard(Grounds.Soil,  Grounds.Soil,
                                                Entities.Tree, Entities.Bush)

if __name__=='__main__':
    utils.move_to_origin()
    plant_bush()
