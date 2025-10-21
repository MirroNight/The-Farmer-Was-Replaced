import __builtins__
import utils
import maze_solver


def parallel_maze_solver(size=8):
    drones = []
    for i in range(get_world_size()//size):
        for j in range(get_world_size()//size):
            utils.move_to(i*size+size//2, j*size+size//2)
            drones.append(spawn_drone(maze_solver.run_maze))
    return 0


if __name__ == '__main__':
    parallel_maze_solver()
