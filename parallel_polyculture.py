import __builtins__
import utils
import polyculture

tiles = 2048


def get_polyculture_func():
    def polyculture_func():
        global tiles
        arr = utils.init_arr(get_world_size(), -1)

        utils.move_to(random()*100%get_world_size(), random()*100%get_world_size())
        utils.get_plant_func(Grounds.Soil, Entities.Carrot)()
        plant_queue = []
        
        while tiles:
            arr, plant_queue = polyculture.polyculture(arr, plant_queue)
            tiles -= 1
    return polyculture_func


def non_blocking_join(drones, cnt):
    for i in range(len(drones)):
        if drones[i] == None:
            continue
        if has_finished(drones[i]):
            wait_for(drones[i])
            cnt, drones[i] = cnt-1, None
    return cnt


def parallel_polyculture(drone_cnt=4, n=2048):
    global tiles
    tiles = n
    polyculture_func = get_polyculture_func()

    drones = []
    for _ in range(drone_cnt):
        drones.append(spawn_drone(polyculture_func))
    polyculture_func()
    
    while drone_cnt:
        drone_cnt = non_blocking_join(drones, drone_cnt)
    
    return 0

if __name__ == '__main__':
    clear()
    parallel_polyculture()