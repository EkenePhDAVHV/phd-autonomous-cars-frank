import math
from copy import copy

from svgwrite import Drawing
from svgwrite.shapes import *

import random

from AVHV_Main.AVHV_CAwSD4WI.CarSpawner import CarSpawner
from AVHV_Main.AVHV_CAwSD4WI.Vector2 import Vector2
from AVHV_Main.AVHV_CAwSD4WI.constants import *
from AVHV_Main.AVHV_CAwSD4WI.RoadNode import RoadNode
from AVHV_Main.AVHV_CAwSD4WI._EnvironmentObject import EnvironmentObject


class Car(EnvironmentObject):
    def __init__(self, name=None, position=None, velocity=None,
                 acceleration=None, direction=0, mass=None,
                 route=None, route_list=None, safe_distance=None,
                 reaction_time=None, color=None, file_path=None,
                 file_names=[None, None]):

        if not isinstance(color, str):
            color = "red"

        if not isinstance(mass, int) and not isinstance(mass, float):
            mass = 1200

        self.should_accelerate = True

        super().__init__(name=name, position=position, velocity=velocity,
                         acceleration=acceleration, direction=direction,
                         mass=mass, color=color,
                         should_accelerate=self.should_accelerate)

        if not isinstance(route, list):
            route = []

        if 'Aggressive' in self.name:
            self.deceleration_force = braking_force * 2
        else:
            self.deceleration_force = braking_force * 1.5

        self.route = route
        self.route_list = route_list

        self.position = position
        self.direction = direction
        self.first_node_in_route = None
        self.previous_node = None
        self.route_cache = []

        self.has_reached_destination = False

        # Car state
        self.car_started = False
        self.reset_acceleration = False
        self.has_decelerated = False

        self.safe_distance = safe_distance
        self.reaction_time = reaction_time

        self.safe_velocity = 0

        self.time_to_accelerate = 5

        self.should_brake_car = False
        self.should_bring_car_to_rest = False
        self.initial_velocity_before_rest = None
        self.initial_distance_before_rest = None
        self.is_reaching_destination = False

        self.file_path = file_path
        self.file_names = file_names

        self.all_routes_temp = None
        self.all_routes = None

        self.num_of_occupied_ways = 0

        self.brake_to_avoid_collision = False

    def set_environment(self, environment):
        super().set_environment(environment)

        self.all_routes_temp = [car_spawner.route for car_spawner in
                                self.environment.environment_objects[
                                    CarSpawner]]
        self.all_routes = []

        for route in self.all_routes_temp:
            if route not in self.all_routes:
                self.all_routes.append(route)

        self.num_of_occupied_ways = len(self.all_routes)

        if len(self.route) > 0:
            for _ in range(0, len(self.route)):
                self.route[_] = self.environment.road_system.node(self.route[_])

            if isinstance(self.route[0], RoadNode):
                self.position = self.route[0].position.copy()

                # Retrieve copy of first node before removing it from list
                self.first_node_in_route = self.route[0]
                self.previous_node = self.route[0]

                self.route = self.route[1:]

                for r in self.route:
                    if r not in self.route_cache:
                        self.route_cache.append(r)

        if self.first_node_in_route:
            self.position = self.first_node_in_route.position.copy()

    def draw(self, canvas, offset):
        if isinstance(canvas, type(Drawing())):

            if len(self.route) > 0:
                next_dir = math.degrees(self.previous_node.position.direction(
                    self.route[0].position))
            else:
                next_dir = math.degrees(
                    self.route_cache[-2].position.direction(
                        self.route_cache[-1].position))

            car_object = Circle(center=(self.position.draw(offset).x,
                                        self.position.draw(offset).y),
                                r=8,
                                stroke='red' if 'Aggressive' in self.name else 'blue',
                                stroke_width=2,
                                fill='#FF6644' if 'Aggressive' in self.name else '#7777FF',
                                )

            # car_object = Polygon(
            #     points=([[self.position.draw(offset).x - 2,
            #               self.position.draw(offset).y - 6],
            #              [self.position.draw(offset).x + 5,
            #               self.position.draw(offset).y],
            #              [self.position.draw(offset).x - 2,
            #               self.position.draw(offset).y + 6]]),
            #     stroke='red' if 'Aggressive' in self.name else 'blue',
            #     stroke_width=2,
            #     fill='#FF6644' if 'Aggressive' in self.name else '#7777FF',
            #     style="z-index: 500"
            # )
            #
            # car_object.rotate(next_dir, ((self.position.draw(offset).x
            #                               - 2 +
            #                               self.position.draw(offset).x + 3 +
            #                               self.position.draw(offset).x - 2) / 3,
            #                              (self.position.draw(offset).y - 6 +
            #                               self.position.draw(offset).y +
            #                               self.position.draw(
            #                                   offset).y + 6) / 3))

            canvas.add(car_object)

        super().draw_direction(canvas=canvas, offset=offset)

    def behaviour_update(self, t):
        super(Car, self).behaviour_update(t)

        self.next_node()

        if len(self.route) > 0:
            self.turning()

            # move car
            self.avoid_collision(t)
            self.move_car(t)

        cars = self.environment.environment_objects[Car]

        for car in cars:
            if car is not self and len(car.route) > 0 and \
                    not car.is_reaching_destination:
                if self.position.distance(car.position) <= 10:
                    if {self, car} not in self.environment.colliding_cars:
                        self.environment.colliding_cars.append({self, car})
                        self.environment.occurred_collisions += 1

            if self.should_brake_car and not self.should_accelerate:
                if self not in self.environment.cars_braked:
                    self.environment.cars_braked.append(self)
                    self.environment.collisions_prevented += 1
            elif not self.should_brake_car and self.should_accelerate:
                if self in self.environment.cars_braked:
                    self.environment.cars_braked.pop(
                        self.environment.cars_braked.index(self))

    def physics_update(self, t):
        """Updates Physics of the object."""

        super().physics_update(t)

        # if self.acceleration.magnitude() > 0.0:
        #     self.reaction_time = 0.1
        #     random_factor = 1.0
        #
        #     if 'Aggressive' in self.name:
        #         self.reaction_time = round(random.uniform(0.3, 0.75), 2)
        #
        #         random_factor = round(random.uniform(1.0, 3.0), 1)
        #
        #     self.safe_distance = round(self.velocity.magnitude() * \
        #                                random_factor * \
        #                                self.reaction_time + \
        #                                math.sqrt(
        #                                    math.pow(self.velocity.magnitude(),
        #                                             2) / \
        #                                    self.acceleration.magnitude()) +
        #                                self.reaction_time,
        #                                2)

    def reach_node(self):
        self.position = self.route[0].position.copy()

        # Increment car counter if car has reached its destination
        if len(self.route) == 1:
            if 'Gentle' in self.name:
                self.environment.passed_av_cars += 1
            elif 'Aggressive' in self.name:
                self.environment.passed_hv_cars += 1
            else:
                self.environment.passed_nl_cars += 1

        self.previous_node = self.route[0]
        self.route = self.route[1:]

    def next_node(self):
        """Schedules the next node in the route."""

        if len(self.route) > 0:
            if isinstance(self.route[0], RoadNode):

                velocity_magnitude = self.velocity.copy().magnitude()
                accel_magnitude = self.acceleration.copy().magnitude()

                next_dir = self.previous_node.position.direction(
                    self.route[0].position)

                self.velocity.x = velocity_magnitude * math.cos(next_dir)
                self.acceleration.x = accel_magnitude * math.cos(next_dir)

                self.velocity.y = velocity_magnitude * math.sin(next_dir)
                self.acceleration.y = accel_magnitude * math.sin(next_dir)

                if math.ceil(self.position.distance(
                        self.route[0].position)) == 1 or \
                        math.floor(self.position.distance(
                            self.route[0].position)) == 1 or \
                        round(self.position.distance(
                            self.route[0].position)) == 1:
                    self.reach_node()
                elif math.ceil(self.position.distance(
                        self.route[0].position)) == 2 or \
                        math.floor(self.position.distance(
                            self.route[0].position)) == 2 or \
                        round(self.position.distance(
                            self.route[0].position)) == 2:
                    self.reach_node()
        else:
            self.velocity.reset_self()
            self.acceleration.reset_self()

    def turning(self):
        if self.route[0] is not None:
            self.direction = math.degrees(math.atan2(
                self.route[0].position.y - self.previous_node.position.y,
                self.route[0].position.x - self.previous_node.position.x
            ))

    def dir_to_next_node(self):
        if len(self.route) > 0:
            return math.degrees(self.first_node_in_route.position.
                                direction(self.route[0].position))

    def get_info(self):
        return str.format("{:s}", super().get_info())

    def centripetal_velocity(self, magnitude, radius, mass):
        """Returns the centripetal velocity that the car will use to move
        around bends."""

        return Vector2(math.sqrt(magnitude * radius / mass)).redirect(
            self.direction)

    def do_avoid_collision(self, t, next_car, next_route_node,
                           next_car_route_node):
        """Prevents this car from hitting a car in front in it."""

        if next_route_node == next_car_route_node:
            car_to_node_distance = self.position.distance(
                next_car_route_node.position)

            next_car_to_node_distance = next_car.position.distance(
                next_car_route_node.position)

            # If the other car is closer to the next node
            if next_car_to_node_distance < car_to_node_distance:

                # Get the distance between the two cars
                distance_to_next_car = self.position.distance(next_car.position)

                if distance_to_next_car < self.safe_distance:
                    self.brake_to_avoid_collision = True
                    self.should_accelerate = False
                else:
                    self.brake_to_avoid_collision = False
                    self.should_accelerate = True

    def avoid_collision(self, t):
        """Preps the parameters for avoiding collisions."""

        index_of_self = self.environment.environment_objects[Car].index(self)

        if index_of_self > 0:
            for next_car in self.environment.environment_objects[Car]:
                if next_car is not self:
                    if self.time_to_accelerate > 0:
                        self.time_to_accelerate = self.time_to_accelerate - t
                    else:
                        if len(self.route) > 0:
                            next_route_node = self.route[0]

                        if len(next_car.route) > 0:
                            next_car_route_node = next_car.route[0]
                        else:
                            next_car_route_node = None

                        self.do_avoid_collision(t, next_car, next_route_node,
                                                next_car_route_node)

                        # Four way intersection

                        # One Vehicle One Direction Case
                        if self.num_of_occupied_ways == 1:
                            pass

                        if len(self.route) > 2 and len(next_car.route) > 2:
                            next_dir = math.degrees(
                                self.route[0].position.direction(
                                    self.route[1].position))

                            next_car_dir = math.degrees(
                                next_car.route[0].position.direction(
                                    next_car.route[1].position))

                            # print(next_dir)

                            if next_dir == 45.0 or next_dir == -45.0 \
                                    or next_dir == 135.0 or next_dir == \
                                    -135.0 and next_car_dir == 0.0 or \
                                    next_car_dir == 90.0 or next_car_dir == \
                                    -90.0 or next_car_dir == 180.0:
                                if self.route[0].id == 6 and self.route[1].id \
                                        == 2 or self.route[0].id == 18 and \
                                        self.route[1].id == 14 or \
                                        self.route[0].id == 12 and \
                                        self.route[1].id == 8 or \
                                        self.route[0].id == 4 and \
                                        self.route[1].id == 16:
                                    pass
                                else:
                                    if self.position.distance(self.route[
                                                                  0].position) \
                                            < 30:
                                        pass
                                        # self.should_brake_car = True
                                        # self.should_accelerate = False

                            cars_temp = [car for car in
                                         self.environment.environment_objects[
                                             Car] if \
                                         car.route_list == self.route_list and \
                                         len(car.route) > 0]

                            if len(cars_temp) > 0:
                                if cars_temp.index(self) == 0:
                                    pass
                                else:
                                    cars = cars_temp[:cars_temp.index(self)]

                                    if self.position.distance(
                                            cars[-1].position) < 40:
                                        self.should_brake_car = True
                                        self.should_accelerate = False
                                    else:
                                        self.should_brake_car = False
                                        self.should_accelerate = True

                        else:
                            self.should_brake_car = False
                            self.should_accelerate = True

    def move_car(self, t):
        """Moves car while checking for traffic control"""

        if len(self.route) == 1:
            if self.position.distance(self.route[0].position) > 27.5:
                pass
            else:
                self.should_brake_car = False
                self.should_bring_car_to_rest = True
                self.is_reaching_destination = True

                if self.initial_distance_before_rest is None:
                    self.initial_distance_before_rest = \
                        self.position.distance(self.route[0].position)

        if len(self.route) > 0:

            # Start car if it is at rest
            if not self.should_brake_car and not self.should_bring_car_to_rest:
                self.apply_force(t, moving_force)
            elif self.brake_to_avoid_collision:
                self.decelerate(t, self.deceleration_force, self.safe_velocity)
            elif self.should_bring_car_to_rest:
                self.decelerate(t, braking_force *
                                self.initial_distance_before_rest / 27.5)
            elif self.should_brake_car:
                self.acceleration.reset_self()
                self.velocity.reset_self()

                # self.decelerate(t, braking_force)

            if len(self.route) > 1:
                next_dir = math.degrees(self.route[0].position.direction(
                    self.route[1].position))

                # If the next 2 nodes don't form a straight line
                if next_dir != 0.0 and next_dir != 90.0 and next_dir != -90.0:
                    if self.position.distance(
                            self.route_cache[0].position) < 30.0:

                        if not self.has_decelerated:
                            deceleration_force = 2000
                            radius = self.route[0].position.distance(
                                self.route[1].position)
                            centripetal_speed = self.centripetal_velocity(
                                deceleration_force, radius,
                                self.mass).magnitude()

                            # self.should_brake_car = True
                            # self.decelerate(t, braking_force)

        if 'Gentle' in self.name:
            with open(self.file_path + str(self.file_names[0]) +
                      ".csv", "a", encoding="utf8") as f:
                self.write_metrics(f)
        elif 'Aggressive' in self.name:
            with open(self.file_path + str(self.file_names[1]) +
                      ".csv", "a", encoding="utf8") as f:
                self.write_metrics(f)
        else:
            with open(self.file_path + "all.csv", "a",
                      encoding="utf8") as f:
                self.write_metrics(f)

    def write_metrics(self, f):
        try:
            speed = round((self.safe_distance / self.velocity.magnitude()) *
                          2.237, 2)
        except ZeroDivisionError:
            speed = 0.0

        full_str = str(self.name + "," +
                       str(speed) + "," +
                       str(round(self.safe_distance, 2)) + "," +
                       str(round(self.reaction_time, 2)) + "," +
                       str(self.current_time) + "\n")
        f.write(full_str)
