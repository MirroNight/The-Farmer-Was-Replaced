import __builtins__
import utils

# start a new maze form (x,y) with size
# -> True/False
def new_maze(size=get_world_size(), x=None, y=None):
    if x!=None and y!=None:
        utils.move_to(x,y)
        plant(Entities.Bush)
    amount = size * 2**(num_unlocked(Unlocks.Mazes)-1)
    if num_items(Items.Weird_Substance) >= amount:
        use_item(Items.Weird_Substance, amount)
        return 0
    else:
        return 1

# map move direction to postition
# -> (x, y)
def get_next_node(x, y, direction):
    if direction == North:
        return (x, y+1)
    elif direction == South:
        return (x, y-1)
    elif direction == East:
        return (x+1, y)
    else:
        return (x-1, y)

# update neightboring
# -> {north: node, south: node, east: node, west: node}
def get_neighboring_nodes(x, y):
    next_node = {}
    for direction in [North, South, East, West]:
        if can_move(direction):
            next_node[direction] = get_next_node(x, y, direction)
        else:
            next_node[direction] = None
    return next_node

# get list of untraversed nodes
# -> [(x,y), ...]
def get_untraversed_neighboring_nodes(arr, maze_graph, x, y):
    # quick_print(x, y, maze_graph[(x,y)])
    viable_nodes = []
    for direction in [North, South, East, West]:
        pos = maze_graph[(x,y)][direction]
        if pos and (arr[pos[1]][pos[0]] == None):
            viable_nodes.append(pos)
    return viable_nodes

# move back to nearest untraversed node
# and return the next node's x and y
def backtrack(arr, maze_graph, node_stack, depth):
    arr[get_pos_y()][get_pos_x()] = depth
    # quick_print('backtracking ...')
    for _ in range(len(node_stack)):
        branchable, pos = node_stack.pop()
        utils.move_to(pos[0], pos[1])
        if branchable:
            break
    depth = arr[pos[1]][pos[0]]
    next_nodes = get_untraversed_neighboring_nodes(arr, maze_graph, pos[0], pos[1])
    # quick_print('end of backtrack ...')
    return arr, node_stack, next_nodes, depth


def get_stack_to_treasure(arr, child_node, stack_graph, stack):
    node = child_node
    stack.append(node)

    while stack_graph[node]:
        node = stack_graph[node]
        stack.append(node)
    return stack


def get_child_nodes(arr, stack_graph, parent_node, neighboring_nodes, depth, tpos):
    child_nodes, stack = [], []
    for child_node in neighboring_nodes:
        if child_node == tpos:
            arr[child_node[1]][child_node[0]] = depth
            stack_graph[child_node] = parent_node
            stack = get_stack_to_treasure(arr, child_node, stack_graph, stack)
            break
        else:
            arr[child_node[1]][child_node[0]] = depth
            stack_graph[child_node] = parent_node
            child_nodes.append(child_node)
    return stack, arr, stack_graph, child_nodes


def get_new_node_fronts(arr, maze_graph, node_fronts, stack_graph, depth, tpos):
    new_node_fronts, stack = [], []
    for parent_node in node_fronts:
        neighboring_nodes = get_untraversed_neighboring_nodes(
            arr, maze_graph, parent_node[0], parent_node[1]
            )
        stack, arr, stack_graph, child_nodes = get_child_nodes(
            arr, stack_graph, parent_node, neighboring_nodes, depth, tpos
            )
        new_node_fronts += child_nodes
        if stack:
            break
    return stack, arr, stack_graph, new_node_fronts, depth+1


# known map
def breadth_first_search(maze_graph, size):
    if get_entity_type() == Entities.Treasure:
        return maze_graph
    
    arr = utils.init_arr(size, None)
    tpos, x, y = measure(), get_pos_x(), get_pos_y()
    node_fronts = [(x, y)]
    stack_graph = {(x, y): None}
    arr[y][x], depth, stack = 0, 1, []

    while not stack:
        stack, arr, stack_graph, node_fronts, depth = get_new_node_fronts(
            arr, maze_graph, node_fronts, stack_graph, depth, tpos
            )
    while stack:
        x, y = stack.pop()
        utils.move_to(x, y)
        maze_graph[(x,y)] = get_neighboring_nodes(x, y)
    return maze_graph


# unknown map
def traverse_new_maze(arr, maze_graph, node_stack, depth, tpos):
    x, y = get_pos_x(), get_pos_y()
    maze_graph[(x,y)] = get_neighboring_nodes(x, y)
    next_nodes = get_untraversed_neighboring_nodes(arr, maze_graph, x, y)

    if not next_nodes:
        arr, node_stack, next_nodes, depth = backtrack(
            arr, maze_graph, node_stack, depth
            )
        x, y = get_pos_x(), get_pos_y()

    if len(next_nodes) == 1:
        node_stack.append((False, (x,y)))
    elif next_nodes == []:
        return arr, maze_graph, node_stack, None
    else:
        node_stack.append((True, (x,y)))

    arr[y][x] = depth
    utils.move_to(next_nodes[0][0], next_nodes[0][1])
    return arr, maze_graph, node_stack, depth+1            


def run_maze(x, y, size, times=10):
    if times > 300:
        times = 300
    
    new_maze(size, x, y)
    arr = utils.init_arr(size, None)
    
    maze_graph = {}
    # {node: {north: node, south: node, east: node, west: node}}
    # noe = (x,y) or (None, None)
    
    node_stack = []
    # [(bool, (x,y)), ...]
    # stack nodes that represent the past path

    depth, tpos = 0, None
    while depth != None:
        arr, maze_graph, node_stack, depth = traverse_new_maze(
            arr, maze_graph, node_stack, depth, tpos
            )

    maze_graph = breadth_first_search(maze_graph, size)

    for _ in range(times-1):
        if new_maze(size):
            break
        maze_graph = breadth_first_search(maze_graph, size)
    
    harvest()
    
    return 0


if __name__ == '__main__':
    run_maze(0, 0, 16, 300)
    pass
