import __builtins__
import utils


def get_pattern_func(product, plant_func1, plant_func2=None, plant_func3=None):
    if product == Items.Wood:
        def plant_pattern_checkerboard():
            for x in range(get_world_size()):
                for y in range(get_world_size()):
                    if (x % 2) == (y % 2):
                        plant_func1()
                    else:
                        plant_func2()
                    move(North)
                move(East)

        pattern_func = plant_pattern_checkerboard

    else:
        def plant_pattern_uniform():
            for x in range(get_world_size()):
                for y in range(get_world_size()):
                    plant_func1()
                    move(North)
                move(East)
        pattern_func = plant_pattern_uniform
    return pattern_func


if __name__=='__main__':
    pass
