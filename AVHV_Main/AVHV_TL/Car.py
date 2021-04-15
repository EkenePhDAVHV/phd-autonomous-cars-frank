import math
from copy import copy
import random

from svgwrite import Drawing
from svgwrite.shapes import *

from AVHV_Main.AVHV_TL.Vector2 import Vector2
from AVHV_Main.AVHV_TL.constants import *

from AVHV_Main.AVHV_TL.RoadNode import RoadNode
from AVHV_Main.AVHV_TL.TrafficLight import TrafficLight
from AVHV_Main.AVHV_TL._EnvironmentObject import EnvironmentObject


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
                         mass=mass, color=color)

        if not isinstance(route, list):
            route = []

        self.route = route
        self.route_list = route_list

        self.position = position
        self.direction = direction
        self.first_node_in_route = None
        self.previous_node = None
        self.route_cache = []

        self.traffic_light = None

        self.turn_velocity_reached = False
        self.accelerate_again = False

        self.has_reached_destination = False

        # Car state
        self.car_started = False
        self.reset_acceleration = False
        self.has_decelerated = False

        self.safe_distance = safe_distance if safe_distance is not None else 10
        self.reaction_time = reaction_time if reaction_time is not None else 0.3

        self.should_brake_car = False
        self.should_bring_car_to_rest = False
        self.should_decelerate = False
        self.initial_velocity_before_rest = None
        self.initial_distance_before_rest = None
        self.is_reaching_destination = False

        self.file_path = file_path
        self.file_names = file_names

        self.turning_angle = 0
        self.total_time = 0
        self.traffic_light_nodes = []

        self.curve = None
        self.last = None
        self.last_node = None

        self.counter = 0

        self.has_traffic_lights = 0
        self.wait_time = 0

        self.velocity_to_slow_down = None

        self.decelerated = False
        self.car_started = False

        self.route_list = route_list
        self.previous_node = None

        self.time_to_accelerate = 5

    def set_environment(self, environment):
        super().set_environment(environment)

        try:
            for traffic_light in \
                    self.environment.environment_objects[TrafficLight]:
                for node in self.route:
                    if traffic_light.traffic_node.id == node:
                        self.traffic_light_nodes.append(
                            traffic_light.traffic_node.id)
        except KeyError:
            pass

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

            car_list = [car for car in self.environment.environment_objects[
                Car] if car.route_list == self.route_list]
            car_index = car_list.index(self)

            if len(car_list) > car_index + 1:
                next_car = car_list[car_index + 1]

                stroke_color = '#55AA55'

                if next_car.position.distance(self.position) < \
                        next_car.safe_distance:
                    stroke_color = 'red'

                if self.should_brake_car and not self.should_accelerate:
                    stroke_color = 'orange'

                stroke_width = 10

                line_objects = []

                if len(self.route) > 0 and len(next_car.route) and \
                        self.route[0] != next_car.route[0]:

                    line_objects.append(Polyline(
                        points=([[next_car.route[0].position.draw(offset).x,
                                  next_car.route[0].position.draw(offset).y],
                                 [next_car.position.draw(offset).x,
                                  next_car.position.draw(offset).y]]),
                        stroke=stroke_color,
                        stroke_width=stroke_width,
                    ))

                    line_objects.append(Polyline(
                        points=([[self.position.draw(offset).x,
                                  self.position.draw(offset).y],
                                 [self.previous_node.position.draw(offset).x,
                                  self.previous_node.position.draw(offset).y]]),
                        stroke=stroke_color,
                        stroke_width=stroke_width,
                    ))

                    line_objects.append(Polyline(
                        points=([[self.previous_node.position.draw(offset).x,
                                  self.previous_node.position.draw(offset).y],
                                 [next_car.route[0].position.draw(offset).x,
                                  next_car.route[0].position.draw(offset).y]]),
                        stroke=stroke_color,
                        stroke_width=stroke_width,
                    ))

                    if self.environment.environment_objects[Car].index(
                            self) != \
                            len(self.environment.environment_objects[Car]) - 1:
                        for line_object in line_objects:
                            # canvas.add(line_object)
                            pass
                else:
                    line_object = Polyline(
                        points=([[self.position.draw(offset).x,
                                  self.position.draw(offset).y],
                                 [next_car.position.draw(offset).x,
                                  next_car.position.draw(offset).y]]),
                        stroke=stroke_color,
                        stroke_width=stroke_width,
                    )

                    if self.environment.environment_objects[Car].index(
                            self) != \
                            len(self.environment.environment_objects[Car]) - 1:
                        # canvas.add(line_object)
                        pass

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
            self.obey_traffic_light(t)
            self.avoid_collisions(t)
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

        if self.acceleration.magnitude() > 0.0:
            self.reaction_time = 0.1
            random_factor = 1.0

            if 'Aggressive' in self.name:
                if self.get_speed() > 0.0:
                    self.reaction_time = self.safe_distance / self.get_speed()
                else:
                    self.reaction_time = 0.3

                random_factor = random.uniform(1.0, 3.0)

            self.safe_distance = round(self.velocity.magnitude() * \
                                       random_factor * \
                                       self.reaction_time + \
                                       math.sqrt(
                                           math.pow(self.velocity.magnitude(),
                                                    2) / \
                                           self.acceleration.magnitude()) +
                                       self.reaction_time,
                                       2)

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

    def obey_traffic_light(self, t):
        # Test for traffic Light
        if len(self.environment.environment_objects[TrafficLight]) > 0:
            if self.traffic_light is None:
                if len(self.route) > 0:
                    if isinstance(self.route[0], RoadNode):
                        if self.route[0].traffic_light is not None:
                            # print(self.route[0].id)
                            # angle = self.direction - self.route[
                            #     0].traffic_light.direction - 180
                            # while angle < 0:
                            #     angle += 360
                            # angle %= 360
                            # if angle < 30 or angle > 360 - 30:
                            self.traffic_light = self.route[0].traffic_light

        # Obey Traffic Light
        if isinstance(self.traffic_light, TrafficLight) and \
                self.position.distance(self.traffic_light.position) < 40:
            # Obey that light
            # If the traffic light is red, kill the velocity and acceleration
            if self.traffic_light.red and not self.traffic_light.amber and not self.traffic_light.green:
                self.should_brake_car = True
                self.should_accelerate = False
            # If the light is red and amber, apply a forward force.
            elif self.traffic_light.red and self.traffic_light.amber and not self.traffic_light.green:
                self.should_brake_car = False
                self.should_accelerate = True
            # If the light is green, accelerate forwards faster
            elif not self.traffic_light.red and not self.traffic_light.amber and self.traffic_light.green:
                self.should_brake_car = False
                self.should_decelerate = False
                self.should_accelerate = True
            # If the light is amber, prepare to break by applying a break force.
            elif self.traffic_light.amber:
                self.should_brake_car = False
                self.should_decelerate = True

    def avoid_collisions(self, t):

        if self.time_to_accelerate > 0:
            self.time_to_accelerate -= t
        else:
            cars_temp = [car for car in
                         self.environment.environment_objects[Car] if \
                         car.route_list == self.route_list and \
                         len(car.route) > 0 and not car.is_reaching_destination]

            if len(cars_temp) > 0:
                if self in cars_temp and cars_temp.index(self) == 0:
                    pass
                elif self in cars_temp and cars_temp.index(self) != 0:
                    cars = cars_temp[:cars_temp.index(self)]

                    if self.position.distance(cars[-1].position) < 40:
                        self.should_brake_car = True
                        self.should_accelerate = False
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
            elif self.should_bring_car_to_rest:
                self.decelerate(t, braking_force *
                                self.initial_distance_before_rest / 27.5)
            elif self.should_brake_car:
                self.acceleration.reset_self()
                self.velocity.reset_self()
            elif self.should_decelerate:
                self.decelerate(t, braking_force * 8)

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
                            # self.decelerate(t, deceleration_force,
                            #                 centripetal_speed)

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
