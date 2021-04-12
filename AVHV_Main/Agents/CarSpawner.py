import random
from random import randint

from copy import copy

from AVHV_Main.Node.RoadNode import RoadNode
from AVHV_Main.Agents._EnvironmentObject import EnvironmentObject
from AVHV_Main.Agents.Car import Car


class CarSpawner(EnvironmentObject):
    def __init__(self, name, node, direction, route=None, velocity=None,
                 car_ratio=None, capacity_type="full", file_path=None,
                 file_names=None):

        self.node = copy(node)
        self.route = route.copy()
        self.route_list = route.copy()

        self.velocity = velocity

        self.cars = []
        self.last = None
        self.last_car = None

        self.file_path = file_path
        self.file_names = file_names

        self.capacity_type = capacity_type.lower()
        self.finished_spawning = False

        super().__init__(name=name, position=self.node.position,
                         direction=direction, car_ratio=car_ratio)

        if 'Aggressive' in name:
            self.safe_distance = 20
            self.reaction_time = 0.3
        else:
            self.safe_distance = 20
            self.reaction_time = random.uniform(0.1, 0.3)

        if self.capacity_type == "full":
            # Full traffic
            if 'Aggressive' in name:
                self.spawning_distance = randint(20, 25)
            else:
                self.spawning_distance = randint(20, 25)
            # Half traffic
        else:
            self.spawning_distance = self.safe_distance + randint(5, 10)

    def begin_behaviour_update(self, t):
        super().behaviour_update(t)

        # If no cars have been spawned
        if len(self.cars) == 0:
            self.spawn_another_car(self.route)
        else:
            # Get the last spawned car
            last_car = self.cars[-1]

            if self.total_cars is not None and len(self.cars) < self.total_cars:
                # Spawns a new car if the last spawned car is at least the
                # spawning distance away from the spawner.

                if isinstance(last_car, Car):
                    distance_to_last_car = \
                        self.position.distance(last_car.position)

                    if distance_to_last_car >= self.spawning_distance:
                        self.spawn_another_car(self.route)
            else:
                self.finished_spawning = True

    def behaviour_update(self, t):
        environment_objects = self.environment.environment_objects.copy()
        spawner_objects = environment_objects[CarSpawner]

        prev_spawner_same_route = [cs for cs in spawner_objects if
                                   cs.route_list[0] == self.route_list[0] and
                                   spawner_objects.index(cs) <
                                   spawner_objects.index(self)]

        if len(prev_spawner_same_route) > 0:
            if all(s.finished_spawning for s in prev_spawner_same_route):
                distance_to_last_car = self.position.distance(
                    prev_spawner_same_route[-1].cars[-1].position)
                if distance_to_last_car >= self.spawning_distance:
                    self.begin_behaviour_update(t)
        else:
            self.begin_behaviour_update(t)

    def spawn_another_car(self, route):
        if route is not None:
            route = route
            if len(route) > 0:
                for _ in range(0, len(route)):
                    route[_] = self.environment.road_system.node(route[_])
                if isinstance(route[0], RoadNode):
                    self.position = route[0].position.copy()
                    self.last = route[0]
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
                        destination = destinations[randint(0,
                                                           len(destinations)
                                                           - 1)]
                        if isinstance(destination, RoadNode):
                            for node in route:
                                if node == destination:
                                    visited = True
                                    destinations.remove(node)
                                if not visited:
                                    route.append(destination)
                    if visited:
                        break

        self.cars.append(Car(
            name=self.name + str(len([car for car in
                                      self.environment.environment_objects[
                                          Car] if self.name in car.name]) + 1),
            position=self.node.position,
            route=route,
            route_list=self.route_list,
            safe_distance=self.safe_distance,
            velocity=self.velocity,
            reaction_time=self.reaction_time,
            file_path=self.file_path,
            file_names=self.file_names
        ))

        self.environment.add_objects(self.cars[-1])
