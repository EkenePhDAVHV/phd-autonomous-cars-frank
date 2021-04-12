from random import randint

from AVHV_Main.Car import Car
from AVHV_Main.RoadNode import RoadNode
from AVHV_Main._EnvironmentObject import EnvironmentObject
from AVHV_Main.constants import AVHV_total_cars


class CarSpawner(EnvironmentObject):  # new car arrivals to grow the queue length
    def __init__(self, name, node, direction, route=None, safe_distance=None, car_ratio=None):
        self.route = route
        if safe_distance is None:
            safe_distance = 30
        self.node = node
        self.car_ratio = car_ratio
        super(CarSpawner, self).__init__(name=name, position=self.node.position, direction=direction,
                                         car_ratio=car_ratio)
        self.cars = []
        self.safe_distance = safe_distance

        self.position = node.position
        self.last = None

        self.last_car = None

        self.cars_running = 0

        try:
            pass
        except:
            print('test')
            pass

    def behaviour_update(self, t):
        super(CarSpawner, self).behaviour_update(t)

        # If no cars have been spawned
        if len(self.cars) <= 0:
            # Spawn a new car
            self.spawn_another_car(self.route)
        else:
            # Otherwise, get the last car that was spawned
            last_car = self.cars[-1]

            # Check that the car is actually a car (this should always be the case)
            if self.car_ratio is not None:
                try:
                    count_carspawn = len(self.environment.environment_objects[CarSpawner]) - 1
                    total_cars_percent = self.environment.environment_objects[CarSpawner][count_carspawn].total_cars_percent
                    if total_cars_percent == 100:
                        self.cars_running = round((AVHV_total_cars * self.car_ratio) / 100)
                    else:
                        total_cars_percent = self.environment.environment_objects[CarSpawner][
                            count_carspawn].total_cars_percent
                        try:
                            cars_num = (self.car_ratio / total_cars_percent) * 100
                            print("We got here")
                            print(cars_num)
                            self.cars_running = round((AVHV_total_cars * cars_num) / 100)
                        except TypeError as e:
                            print(str(e))
                        # except:
                        #     print('error')
                except:
                    pass

                if self.cars_running is not None and len(self.cars) < self.cars_running:
                    if isinstance(last_car, Car):
                        # Set the distance to the car as the distance between the spawner and the car
                        distance_to_last_car = self.position.distance(last_car.position)
                        # If the distance to the car is greater than the minimum safe distance, it's safe to spawn a car
                        if distance_to_last_car >= self.safe_distance:
                            # Spawn another car
                            self.spawn_another_car(self.route)
            else:
                if isinstance(last_car, Car):
                    # Set the distance to the car as the distance between the spawner and the car
                    distance_to_last_car = self.position.distance(last_car.position)
                    # If the distance to the car is greater than the minimum safe distance, it's safe to spawn a car
                    if distance_to_last_car >= self.safe_distance:
                        # Spawn another car
                        self.spawn_another_car(self.route)

        # Keep the minimum distance between cars
        # for car in self.cars:
        #     if self.cars.index(car) < len(self.cars) - 1:
        #         if isinstance(car, Car):
        #             distance_to_next_car = car.position.distance(self.cars[self.cars.index(car) + 1].position)
        #
        #             if distance_to_next_car >= self.safe_distance:
        #                 print('We got here')
        #                 print('Carcar.velocity.get_value())
        #                 pass
        #             else:
        #                 # print('Slow down!')
        #                 car.velocity.scale(0.1)
        #                 print(car.velocity.get_value())
        #                 car.acceleration.reset_self()

    def spawn_another_car(self, route):
        if route is not None:
            route = route
            if len(route) > 0:
                for _ in range(0, len(route)):
                    route[_] = self.environment.road_system.node(route[_])
                if isinstance(route[0], RoadNode):
                    self.position = route[0].position.copy()
                    self.last = route[0]
                    # self.route = route[1:]
            if self.last:
                self.position = self.last.position.copy()
        else:
            route = [self.node]
            for i in range(0, 4):
                last = route[-1]
                if isinstance(last, RoadNode):
                    destinations = last.destination_nodes.copy()
                    visited = True
                    while visited and len(destinations) > 0:
                        visited = False
                        destination = destinations[randint(0, len(destinations) - 1)]
                        if isinstance(destination, RoadNode):
                            for node in route:
                                if node == destination:
                                    visited = True
                                    destinations.remove(node)
                            if not visited:
                                route.append(destination)
                    if visited:
                        break

        # print(len(self.cars))

        self.cars.append(Car(
            name=self.name + " : " + str(len(self.cars) + 1),
            position=self.node.position,
            route=route,
            safe_distance=self.safe_distance
        ))

        if len(self.cars) > 1:
            # print(type(self.cars[-1]))
            last_car = self.cars[len(self.cars) - 1]
            self.cars[-1].car_in_front = self.cars[-2]

        self.environment.add_objects(self.cars[-1])
