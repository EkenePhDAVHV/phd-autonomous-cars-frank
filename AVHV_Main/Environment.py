import math

from AVHV_Main.Agents.Car import Car
from AVHV_Main.Agents.CarSpawner import CarSpawner
from AVHV_Main.Agents.Intersection import Intersection
from AVHV_Main.RoadSystem.PedestrianSystem import PedestrianSystem
from AVHV_Main.RoadSystem.ReservationSystem import ReservationSystem
from AVHV_Main.RoadSystem.RoadSystem import RoadSystem
from AVHV_Main.Utilities.Vector2 import Vector2


class Environment:
    def __init__(self, name, layout):
        self.all_route_lists = []

        self.active_reservation_nodes = {}
        self.route_list_catalogue = {
            301: [],
            302: [],
            303: [],
            304: [],
            305: [],
            306: [],
            307: [],
            308: [],
            309: [],
            310: [],
            311: [],
            312: []
        }

        self.total_car_percent = 100
        self.name = name

        if not isinstance(layout, dict):
            layout = {layout.__class__: layout}

        if not layout.get(RoadSystem):
            layout[RoadSystem] = RoadSystem([], {})

        if not layout.get(PedestrianSystem):
            layout[PedestrianSystem] = PedestrianSystem([], {})

        if not layout.get(ReservationSystem):
            layout[ReservationSystem] = ReservationSystem([], {})

        self.layout = layout

        # Environment Objects
        self.environment_objects = {
            # Inanimate Objects
            Intersection: [],
            CarSpawner: [],

            # Animate Objects
            Car: []
        }

        self.road_system = layout.get(RoadSystem)
        self.pedestrian_system = layout.get(PedestrianSystem)
        self.reservation_system = layout.get(ReservationSystem)

        self.cars = []

        self.passed_av_cars = 0
        self.passed_hv_cars = 0
        self.passed_nl_cars = 0

        self.cars_braked = []
        self.colliding_cars = []

        self.collisions_prevented = 0
        self.occurred_collisions = 0

        self.reservation_node_catalogue = {
            301: [[12, 14], [6, 8], [18, 2]],
            302: [[12, 14], [4, 8], [18, 16]],
            303: [[4, 2], [6, 14], [12, 16]],
            304: [[4, 2], [6, 8], [18, 16]],
            305: [[12, 8], [6, 8], [4, 8]],
            306: [[18, 16], [18, 2], [14, 15]],
            307: [[6, 8], [6, 2], [6, 14]],
            308: [[18, 16], [4, 16], [12, 16]],
            309: [[12, 14], [4, 8], [18, 2]],
            310: [[6, 8], [12, 14], [4, 2], [12, 16], [18, 2]],
            311: [[18, 16], [12, 14], [4, 2], [6, 14], [4, 8]],
            312: [[4, 2], [12, 16], [6, 14]],
        }

    def add_objects(self, environment_objects):
        """Adds objects to this environment object."""

        if not isinstance(environment_objects, list):
            environment_objects = [environment_objects]

        for environment_object in environment_objects:
            if environment_object.total_cars is not None:
                self.total_car_percent += environment_object.total_cars

            environment_object.total_car_percent = self.total_car_percent
            environment_object.set_environment(self)

            if not self.environment_objects.get(type(environment_object)):
                self.environment_objects[type(environment_object)] = []

            self.environment_objects[type(environment_object)].append(
                environment_object)

        self.get_all_unique_nodes()

        return self

    def draw(self, canvas, offset=None):
        if offset is None:
            offset = Vector2()

        for environment_object_type, environment_object_group in \
                self.environment_objects.items():
            for environment_object in environment_object_group:
                environment_object.draw(canvas=canvas, offset=offset)

    def update(self, delta_time, record=False):
        """Updates records of every object in the environment object."""

        output = ''

        self.prevent_collisions()

        # For each
        for environment_object_type, environment_object_group in \
                self.environment_objects.items():
            for environment_object in environment_object_group:
                environment_object.update(delta_time, record=record)
                output = "\n" + environment_object.get_info()

        # Record Values
        if record:
            self.record_values(delta_time)

        return output

    def record_values(self, t):
        for environment_object_type, environment_object_group in \
                self.environment_objects.items():
            for environment_object in environment_object_group:
                environment_object.data_update(t)

    @staticmethod
    def sort_list(sub_li):
        length = len(sub_li)
        for i in range(0, length):
            for j in range(0, length - i - 1):
                if sub_li[j][0] >= sub_li[j + 1][0]:
                    tempo = sub_li[j]
                    sub_li[j] = sub_li[j + 1]
                    sub_li[j + 1] = tempo
        return sub_li

    def get_all_unique_nodes(self):
        """Extracts all unique route nodes in use and check reservation nodes
        against them."""

        all_route_lists_temp = [cs.route_list for cs in
                                self.environment_objects[CarSpawner]]

        for route_list in all_route_lists_temp:
            if route_list not in self.all_route_lists:
                self.all_route_lists.append(route_list)

        for item in self.all_route_lists:

            for _id, route_lists in self.reservation_node_catalogue.items():

                if any(route_list[0] in item and route_list[1] in item for
                       route_list in route_lists):
                    if self.active_reservation_nodes.get(_id) is None:
                        self.active_reservation_nodes[_id] = \
                            [n for n in self.reservation_system.nodes if n.id
                             == _id][0]
                    if item not in self.route_list_catalogue[_id]:
                        self.route_list_catalogue[_id].append(item)
                    continue

        # for item in self.all_route_lists:
        #     for _id, route_list in self.reservation_node_catalogue_b.items():
        #         if route_list[0] in item:
        #             if self.active_reservation_nodes.get(_id) is None:
        #                 self.active_reservation_nodes[_id] = \
        #                     [n for n in self.reservation_system.nodes if n.id
        #                      == _id][0]
        #             if item not in self.route_list_catalogue[_id]:
        #                 self.route_list_catalogue[_id].append(item)
        #             continue

        # self.reservation_node_catalogue. \
        #     update(self.reservation_node_catalogue_a)

        # self.reservation_node_catalogue. \
        #     update(self.reservation_node_catalogue_b)

    def prevent_collisions(self):
        """Prevents collisions of cars based on applicable reservation nodes
        of cars and distances between cars."""

        self.cars = [car for car in self.environment_objects[Car]]

        times_to_reserved_nodes = {}

        #  Because the reservation nodes in use have been packed into a Python
        #  dictionary, each key-value pair is the id of a reservation node - a
        #  number and the reservation node object itself.

        for _id, reserved_node in self.active_reservation_nodes.items():

            # Go through every car in the simulation.

            for car in self.cars:

                # We need to see if the car will come across that node by
                # checking the car’s route list.

                if car.route_list in self.route_list_catalogue.get(
                        _id):
                    if car.velocity.magnitude() > 0.0:
                        times_to_reserved_nodes.update(
                            {car.name: car.position.distance(
                                reserved_node.position) /
                                       car.velocity.magnitude()}
                        )

            # Make sure the dictionary of distances is not empty before
            # proceeding.

            for car in self.cars:
                distances_to_other_cars = [car.position.distance(
                    other_car.position) for other_car in
                    self.cars[:self.cars.index(car)] if
                    len(other_car.route) >= 1 and not
                    other_car.is_reaching_destination]

                if len(distances_to_other_cars) > 0 and min(
                        distances_to_other_cars) <= car.safe_distance:
                    car.should_brake_car = True
                    car.should_accelerate = False
                    car.distance_from_other_car = \
                        min(distances_to_other_cars)
                else:
                    car.should_brake_car = False
                    car.should_accelerate = True

            if len(times_to_reserved_nodes) == 0:
                pass
            else:
                for car in self.cars:
                    if car.name != min(times_to_reserved_nodes,
                                       key=times_to_reserved_nodes.get):
                        distances_to_other_cars = [car.position.distance(
                            other_car.position) for other_car in
                            self.cars[:self.cars.index(car)] if
                            len(other_car.route) >= 1 and not
                            other_car.is_reaching_destination]

                        if len(distances_to_other_cars) > 0 and min(
                                distances_to_other_cars) <= car.safe_distance:
                            car.should_brake_car = True
                            car.should_accelerate = False
                            car.distance_from_other_car = \
                                min(distances_to_other_cars)
                        else:
                            car.should_brake_car = False
                            car.should_accelerate = True

            times_to_reserved_nodes = {}
