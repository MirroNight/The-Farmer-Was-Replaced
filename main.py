import __builtins__
import utils
import parallel_energy, snake_solver
import parallel_hay, parallel_wood, parallel_carrot
import parallel_cactus, parallel_maze_solver, parallel_pumpkin


target_amount = {
    Items.Hay:           1000000000,
    Items.Wood:         10000000000,
    Items.Carrot:        1000000000,
    Items.Cactus:        1000000000,
    Items.Gold:           100000000,
    Items.Power:             500000,
    Items.Pumpkin:        100000000,
    Items.Bone:            10000000,
    Items.Weird_Substance: 10000000,
}


prerequisite = {
    Items.Hay:             [],
    Items.Wood:            [],
    Items.Carrot:          [Items.Hay, Items.Wood],
    Items.Cactus:          [Items.Pumpkin],
    Items.Gold:            [Items.Weird_Substance],
    Items.Power:           [Items.Carrot],
    Items.Pumpkin:         [Items.Carrot],
    Items.Bone:            [Items.Cactus],
    Items.Weird_Substance: [Items.Carrot, Items.Fertilizer],
}


next_item = {
Items.Hay:             Items.Wood,
Items.Wood:            Items.Carrot,
Items.Carrot:          Items.Cactus,
Items.Cactus:          Items.Gold,
Items.Gold:            Items.Pumpkin,
Items.Pumpkin:         Items.Bone,
Items.Bone:            Items.Weird_Substance,
Items.Weird_Substance: None,
}


function_map = {
Items.Hay:             parallel_hay.parallel_restock_hay,
Items.Wood:            parallel_wood.parallel_restock_wood,
Items.Carrot:          parallel_carrot.parallel_restock_carrot,
Items.Cactus:          parallel_cactus.parallel_restock_cactus,
Items.Gold:            parallel_maze_solver.parallel_maze_solver,
Items.Power:           parallel_energy.parallel_restock_energy,
Items.Pumpkin:         parallel_pumpkin.parallel_restock_pumpkin,
Items.Bone:            snake_solver.solve_snake,
Items.Weird_Substance: parallel_pumpkin.parallel_restock_pumpkin,
}


def check_prerequisite(item):
    if num_items(item) > target_amount[item]:
        item = next_item[item]
        if item == None:
            return 0

    # check energy situation
    if num_items(Items.Power) < target_amount[Items.Power]:
        # not enough power
        carrot_needed = (target_amount[Items.Power] - num_items(Items.Power))//5
        if num_items(Items.Carrot) > carrot_needed:
            # enough carrot
            item = Items.Power
        elif num_items(Items.Hay) < carrot_needed:
            # not enough hay for carrot
            item = Items.Hay
        elif num_items(Items.Wood) < carrot_needed:
            # not enough wood for carrot
            item = Items.Wood
        else:
            # enough hay & wood for carrot
            item = Items.Carrot
    else:
        for requirement in prerequisite[item]:
            if num_items(requirement) < target_amount[requirement]:
                item = requirement
    return item


def restock_everything(item):
    item = check_prerequisite(item)
    if item == 0:
        return 0
    elif item == Items.Bone:
        clear()
        arr = utils.init_arr()
        arr = snake_solver.get_hamilton_path(arr)
        arr = snake_solver.solve_snake(arr)
    elif item == Items.Weird_Substance:
        function_map[Items.Weird_Substance](True)
    else:
        function_map[item]()
    return item


if __name__=='__main__':
    utils.move_to_origin()
    item = Items.Hay
    while item:
        item = restock_everything(item)
