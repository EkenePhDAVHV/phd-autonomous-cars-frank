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

total_num = total_num_of_cars
types_of_spawners = ['GentleCar', 'AggressiveCar']
cars_per_route = []

while total_num > 0:
    num_of_cars_for_route = random.randint(2, 4)
    type_of_spawner = random.choice(types_of_spawners)
    route = random.choice(routes)

    if total_num < num_of_cars_for_route:
        cars_per_route.append((type_of_spawner, route, total_num))
        total_num -= total_num
    else:
        cars_per_route.append((type_of_spawner, route, num_of_cars_for_route))
        total_num -= num_of_cars_for_route


