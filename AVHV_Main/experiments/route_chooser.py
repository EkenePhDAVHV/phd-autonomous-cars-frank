import random

route_group_1 = [[11, 12, 14, 15], [11, 12, 8, 9], [11, 12, 16, 17]]
route_group_2 = [[5, 4, 2, 1], [5, 4, 16, 17], [5, 4, 8, 9]]
route_group_3 = [[7, 6, 8, 9], [7, 6, 2, 1], [7, 6, 14, 15]]
route_group_4 = [[19, 18, 16, 17], [19, 18, 14, 15], [19, 18, 2, 1]]

routes = [random.choice(route_group_1), random.choice(route_group_2),
          random.choice(route_group_3), random.choice(route_group_4)]

num_of_cars = [random.randint(50, 75), random.randint(50, 75),
               random.randint(50, 75), random.randint(50, 75)]

total_num_of_cars = random.randint(200, 300)


def choose_standard_experiments_routes():
    # Choose random numbers for car spawners to spawn and choose random
    # routes for the car spawners.

    total_num = total_num_of_cars
    types_of_spawners = ['GentleCarSpawner', 'AggressiveCarSpawner']
    cars_per_route = []

    while total_num > 0:
        num_of_cars_for_route = random.randint(2, 4)
        type_of_spawner = random.choice(types_of_spawners)
        route = random.choice(routes)

        if total_num < num_of_cars_for_route:
            cars_per_route.append((type_of_spawner, route, total_num))
            total_num -= total_num
        else:
            cars_per_route.append(
                (type_of_spawner, route, num_of_cars_for_route))
            total_num -= num_of_cars_for_route

    return cars_per_route


def choose_ratioed_experiments_routes():
    # Define a ratio list to store the ratios for the AV and HV.
    ratio_list = []
    cars_per_route = []
    cars_per_route_ratio_list = []

    types_of_spawners = ['GentleCar', 'AggressiveCar']

    # Start from a 100:0 ratio for AV and HV respectively and loop down to
    # a 0:100 ratio with decrements of 5.

    for _ratio in range(100, -5, -5):
        AV_ratio = _ratio
        HV_ratio = 100 - AV_ratio

        # Divide by 100 to get the simplest fractions.
        AV_ratio = AV_ratio / 100
        HV_ratio = HV_ratio / 100

        # Append to the ratio list.
        ratio_list.append((round(AV_ratio * total_num_of_cars),
                           round(HV_ratio * total_num_of_cars)))

    for _ratio in ratio_list:
        for x in _ratio:
            total_num = x

            while total_num > 0:
                num_of_cars_for_route = random.randint(2, 4)
                type_of_spawner = (types_of_spawners[_ratio.index(x)])
                route = random.choice(routes)

                if total_num < num_of_cars_for_route:
                    cars_per_route.append((type_of_spawner, route, total_num))
                    total_num -= total_num
                else:
                    cars_per_route.append(
                        (type_of_spawner, route, num_of_cars_for_route))
                    total_num -= num_of_cars_for_route

        random.shuffle(cars_per_route)
        cars_per_route_ratio_list.append(cars_per_route)
        cars_per_route = []

    random.shuffle(cars_per_route_ratio_list)
    return cars_per_route_ratio_list
