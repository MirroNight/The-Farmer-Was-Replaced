import __builtins__
import utils
import maze_solver


def non_blocking_join(drones, cnt):
    for i in range(len(drones)):
        if drones[i] == None:
            continue
        if has_finished(drones[i]):
            wait_for(drones[i])
            drones[i] = None
            cnt -= 1
    return cnt


def parallel_maze_solver(size=8):
    drones = []
    for i in range(get_world_size()//size):
        for j in range(get_world_size()//size):
            utils.move_to(i*size+size//2, j*size+size//2)
            drones.append(spawn_drone(maze_solver.run_maze))
    
    cnt = len(drones)
    while cnt:
        cnt = non_blocking_join(drones, cnt)
    return 0


if __name__ == '__main__':
    parallel_maze_solver()
