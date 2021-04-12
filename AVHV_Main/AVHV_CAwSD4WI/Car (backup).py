import math
from copy import copy

from svgwrite import Drawing
from svgwrite.shapes import *

import random

from AVHV_Main.Vector2 import Vector2
from AVHV_Main.constants import *
from AVHV_Main.RoadNode import RoadNode
from AVHV_Main.TrafficLight import TrafficLight
from AVHV_Main._EnvironmentObject import EnvironmentObject


class Car(EnvironmentObject):
    def __init__(self, name=None, position=None, velocity=None, acceleration=None, direction=None, size=(4.5, 2),
                 mass=None,
                 route=None, color=None, power=1000, velocity_max=max_velocity, acceleration_max=max_acceleration,
                 easy_physics=True, car_type=None, idle_time=0, m_force=moving_force, b_force=braking_force,
                 car_in_front=None, safe_distance=None, no_braking=False, deceleration_force=None, reaction_time=None,
                 file_path=None, file_name=None, file_name2=None):
        if not isinstance(color, str):
            color = "red"
        if not isinstance(mass, int) and not isinstance(mass, float):
            mass = 1200
        if not isinstance(power, int) and not isinstance(power, float):
            power = 1000
        super(Car, self).__init__(name=name, position=position, velocity=velocity, acceleration=acceleration,
                                  direction=direction, size=size, mass=mass, color=color)
        if not isinstance(route, list):
            route = []
        self.route = route

        # self.start_velocity = velocity
        # self.velocity = Vector2(10)

        self.position = position
        self.power = power
        self.turning_angle = 0
        self.traffic_light = None
        self.easy_physics = easy_physics
        self.velocity_max = velocity_max
        self.acceleration_max = acceleration_max
        self.max_acceleration = 1
        self.max_deacceleration = 1
        self.total_time = 0
        self.traffic_light_nodes = []
        self.moving_force = m_force
        self.braking_force = b_force
        self.no_braking = no_braking

        self.idle_time = idle_time
        self.idle_t = copy(self.idle_time)

        self.time_to_accelerate_from_zero_velocity = 5

        self.position = position
        self.direction = direction
        self.curve = None
        self.last = None
        self.last_node = None

        self.file_path = file_path
        self.file_name = file_name
        self.file_name2 = file_name2

        self.counter = 0

        self.car_in_front = car_in_front

        if safe_distance is not None:
            self.safe_distance = 0
        else:
            self.safe_distance = 0  # placeholder value

        if deceleration_force is not None:
            self.deceleration_force = deceleration_force
        else:
            self.deceleration_force = 50000

        self.reaction_time = reaction_time

        self.has_traffic_lights = 0
        self.wait_time = 0

        self.velocity_to_slow_down = None
        self.route_cache = []

        self.turn_velocity_reached = False
        self.accelerate_again = False

        self.decelerated = False
        self.car_started = False

        self.decel_to_avoid_collision = False

        self.is_done = False
        self.reached_destination = False

        self.column_names_written = False

        self.initial_values_set = False

    def set_environment(self, environment):
        # if not self.initial_values_set:
        #     self.acceleration.x = 0.0
        #     self.acceleration.y = 0.0
        #     self.initial_values_set = True

        super(Car, self).set_environment(environment)

        try:
            for traffic_light in self.environment.environment_objects[TrafficLight]:
                for node in self.route:
                    if traffic_light.traffic_node.id == node:
                        self.traffic_light_nodes.append(traffic_light.traffic_node.id)
        except KeyError:
            pass

        if len(self.route) > 0:
            for _ in range(0, len(self.route)):
                self.route[_] = self.environment.road_system.node(self.route[_])

            if isinstance(self.route[0], RoadNode):
                self.position = self.route[0].position.copy()

                self.last_node = self.route[0]
                self.last = self.route[0]
                self.route = self.route[1:]

                for i in self.route:
                    self.route_cache.append(i)

        if self.last:
            pass
            self.position = self.last.position.copy()

    def draw(self, canvas, offset):
        if isinstance(canvas, type(Drawing())):
            color = 'blue'
            if len(self.route) > 0:
                color = 'grey' if self.traffic_light is None \
                    else 'yellow' if self.traffic_light.amber \
                    else 'green' if self.traffic_light.green \
                    else 'red' if self.traffic_light.red \
                    else 'blue'

            canvas.add(Rect(
                insert=(self.position.draw(offset).x - 5, self.position.draw(offset).y - 5),
                size=(10, 10),
                rx=2,
                ry=2,
                fill='red' if 'Aggressive' in self.name else 'blue' if 'Gentle' in self.name else color
            ))
            super(Car, self).draw_direction(canvas=canvas, offset=offset)

    def get_centripetal_force(self):
        return (self.mass * math.sqrt(self.velocity.x ** 2 + self.velocity.y ** 2)) / self.get_radius_of_turn()

    def get_radius_of_turn(self):
        return (self.length / 2) * math.tan(math.pi / 4 - self.turning_angle)

    def turn(self, turning_angle_adjustment):
        self.turning_angle -= turning_angle_adjustment

    def reset_turn(self):
        self.turning_angle = 0

    def behaviour_update(self, t):
        if self.idle_t > 0:
            self.idle_t -= t
            return False

        super(Car, self).behaviour_update(t)

        self.next_node(t)

        if len(self.route) > 0:
            self.turning(t)

            # Obey Traffic Lights
            self.obey_traffic_light(t)

    def physics_update(self, t):
        super(Car, self).physics_update(t)
        if self.easy_physics:
            self.acceleration.cap_self(self.acceleration_max)
            self.velocity.cap_self(self.velocity_max)
            # if self.velocity.magnitude() >= max_velocity:
            #     self.velocity.y = max_velocity * math.sin(self.direction)
            # if self.velocity.magnitude() > self.velocity_max:
            #     # if self.velocity.y > self.velocity.x:
            #     self.velocity.x = math.sqrt((math.pow(self.velocity.x, 2) / (
            #                 math.pow(self.velocity.x, 2) + math.pow(self.velocity.y, 2))) * math.pow(self.velocity_max, 2))
            #     # if self.velocity.x > self.velocity.y:
            #     self.velocity.y = math.sqrt((math.pow(self.velocity.y, 2) / (
            #                 math.pow(self.velocity.x, 2) + math.pow(self.velocity.y, 2))) * math.pow(self.velocity_max, 2))

    def next_node(self, t):
        if len(self.route) > 0:

            self.direction = self.direction_to_next_node()
            # print('current node:', self.route[0].id)
            if isinstance(self.route[0], RoadNode):
                if self.position.distance(self.route[0].position) < 2:
                    self.position = self.route[0].position.copy()
                    # if this car has reached its destination
                    if len(self.route) == 1:
                        if "Gentle" in self.name:
                            self.environment.passed_av_cars += 1
                        elif "Aggressive" in self.name:
                            self.environment.passed_hv_cars += 1
                        else:
                            self.environment.passed_nl_cars += 1

                    if isinstance(self.traffic_light, TrafficLight):
                        self.traffic_light.count_cars += 1
                        for car in range(0, len(self.traffic_light.cars)):
                            if self.traffic_light.cars[car] is self:
                                try:
                                    self.traffic_light.cars.remove(car)
                                except ValueError:
                                    pass

                    vel_mag = self.velocity.copy().magnitude()
                    accel_mag = self.acceleration.copy().magnitude()

                    if len(self.route) > 1:
                        next_direction = self.route[0].position.direction(self.route[1].position)
                        self.velocity.x = vel_mag * math.cos(next_direction)
                        self.velocity.y = vel_mag * math.sin(next_direction)
                        # self.acceleration.x = accel_mag * math.cos(next_direction)
                        # self.acceleration.y = accel_mag * math.sin(next_direction)
                        if not self.accelerate_again:
                            self.acceleration.reset_self()
                    else:
                        direction = self.last_node.position.direction(self.route[0].position)
                        self.velocity.x = vel_mag * math.cos(direction)
                        self.velocity.y = vel_mag * math.sin(direction)

                    self.last_node = self.route[0]

                    self.route = self.route[1:]

                    if len(self.route) > 0 and isinstance(self.route[0], RoadNode):
                        self.traffic_light = self.route[0].traffic_light
                        if isinstance(self.traffic_light, TrafficLight):
                            self.traffic_light.cars.append(self)
                    if self.easy_physics:
                        pass
        else:
            self.velocity.reset_self()
            self.acceleration.reset_self()
            self.reached_destination = True
            # break

    def obey_traffic_light(self, t):
        # Test for traffic Light
        if len(self.environment.environment_objects[TrafficLight]) > 0:
            if self.traffic_light is None:
                if len(self.route) > 0:
                    if isinstance(self.route[0], RoadNode):
                        if self.route[0].traffic_light is not None:
                            angle = self.direction - self.route[0].traffic_light.direction - 180
                            while angle < 0:
                                angle += 360
                            angle %= 360
                            if angle < 30 or angle > 360 - 30:
                                self.traffic_light = self.route[0].traffic_light
        # Obey Traffic Light
        if isinstance(self.traffic_light, TrafficLight):
            # Obey that light
            # If the traffic light is red, kill the velocity and acceleration
            if self.traffic_light.red and not self.traffic_light.amber and not self.traffic_light.green:
                # self.apply_force(t, -100000)
                self.velocity.scale(0.1)
                self.acceleration.reset_self()
            # If the light is red and amber, apply a forward force.
            elif self.traffic_light.red and self.traffic_light.amber and not self.traffic_light.green:
                self.apply_force(t, 10000)
            # If the light is green, accelerate forwards faster
            elif not self.traffic_light.red and not self.traffic_light.amber and self.traffic_light.green:
                self.apply_force(t, 50000)
            # If the light is amber, prepare to break by applying a break force.
            elif self.traffic_light.amber:
                self.velocity.scale(0.9)
                self.acceleration.reset_self()
        else:
            if len(self.route) > 0:
                # start car if it is at rest
                if not self.car_started:
                    self.apply_force(t, self.moving_force)
                    # self.velocity = Vector2(self.start_velocity)
                    # self.start_max_velocity(t, self.moving_force, self.start_velocity)
                    self.car_started = not self.car_started

                # if there are at least 2 nodes left in the route
                if len(self.route) > 1:
                    next_direction = math.degrees(self.route[0].position.direction(self.route[1].position))

                    # if the next 2 nodes aren't a straight route
                    if next_direction != 0.0 and next_direction != -0.0 and next_direction != 90.0 \
                            and next_direction != -90.0:
                        if self.position.distance(self.route_cache[0].position) < 30.0:
                            if not self.decelerated:
                                decel_force = 2000
                                radius = self.route[0].position.distance(self.route[1].position) / 2
                                centripetal_speed = self.centripetal_velocity(decel_force, radius,
                                                                              self.mass).magnitude()
                                self.decelerate_car(t, decel_force, centripetal_speed)
                    elif next_direction == 0.0 or next_direction == 0.0 or next_direction == 90.0 \
                            or next_direction == -90.0:
                        if self.position.distance(self.route[0].position) < 10.0:
                            self.accelerate_again = True
                            self.apply_force(t, self.moving_force)

                    self.collision_avoidance(t)

                elif len(self.route) > 0:
                    # if there is just 1 node left in the route
                    if self.position.distance(self.route[0].position) > 20:
                        self.apply_force(t, self.moving_force)
                    else:
                        if self.no_braking:
                            pass
                        else:
                            self.apply_force(t, self.braking_force, decelerate=True)
                else:
                    pass

    def collision_avoidance(self, t):
        # collision avoidance
        # to prevent cars from bumping into each other

        # only check for the minimum distance from the second to the last car
        index_of_this_car = self.environment.environment_objects[Car].index(self)
        if index_of_this_car > 0:

            # perform this check against every other car
            for next_car in self.environment.environment_objects[Car]:
                if next_car is not self:

                    # double check to be sure that it is a car object
                    if isinstance(next_car, Car):
                        # give this car some time to accelerate
                        if self.time_to_accelerate_from_zero_velocity > 0:
                            self.time_to_accelerate_from_zero_velocity = self.time_to_accelerate_from_zero_velocity - t
                            pass
                        else:
                            # perform this check across the next 2 nodes due to length of routes
                            nrn = self.route[0]  # get the next route node
                            nrn2 = self.route[1]  # get the second next node

                            # check that car has not reached destination
                            if len(next_car.route) > 0:
                                ncrn = next_car.route[0]
                            else:
                                ncrn = None

                            if len(next_car.route) > 1:
                                ncrn2 = next_car.route[1]
                            elif len(next_car.route) > 0:
                                ncrn2 = ncrn

                            # make sure the next route node or the second next route node for this car is
                            # the same as for the other car we are checking safe distance against

                            # if the next car hasn't reached its destination
                            # The decision making process starts here
                            if len(next_car.route) > 0:
                                if nrn == ncrn:
                                    dcn = self.position.distance(ncrn.position)
                                    dncn = next_car.position.distance(ncrn.position)

                                    # If the other car is ahead of this car / closer to the next route node
                                    if dcn > dncn:
                                        # I considered the distance to the car in front here
                                        # get the distance between the two cars
                                        distance_to_next_car = self.position.distance(next_car.position)

                                        # assign reaction time depending on car type
                                        # if reaction_time

                                        # ---- Equation (3) is applied here ---------------------- #

                                        if self.acceleration.magnitude() > 0.0:  # prevent division by zero error
                                            self.safe_distance = self.velocity.magnitude() * self.reaction_time + \
                                                                 (math.pow(self.velocity.magnitude(), 2) / \
                                                                  self.acceleration.magnitude() * 2)

                                        # self.safe_distance = self.velocity.magnitude() * (60 * 60) / 1000 * 0.621371

                                        # If the distance between cars is close to below safe distance, slow down
                                        if distance_to_next_car < self.safe_distance:
                                            if 'Aggressive' in self.name:
                                                # random value e.g 0.134235 is generated
                                                # e.g 0.5 + (0.1 - 0.5) <= 1.0
                                                self.deceleration_force = 7500 + 500 * (0.5 + random.uniform(0.0,
                                                                                                             0.5))
                                            else:
                                                self.deceleration_force = 7500

                                            # ---- Equation (5) is applied here ---------------------- #

                                            vel_safe = (self.deceleration_force / self.mass) * self.reaction_time + \
                                                       math.sqrt((math.pow(self.deceleration_force / self.mass, 2) *
                                                                  math.pow(self.reaction_time, 2))
                                                                 + 2 * self.safe_distance)

                                            # decelerate to safe velocity
                                            # self.decelerate_car(t, self.deceleration_force, vel_safe + 4)

                                            # if self.acceleration.magnitude() > 0.0:  # prevent division by zero error
                                            self.safe_distance = self.velocity.magnitude() * self.reaction_time + \
                                                                 math.pow(self.velocity.magnitude(), 2) / \
                                                                 (self.deceleration_force / self.mass) * 2

                                            # if not self.column_names_written:
                                            #     with open(self.file_path + "all_ratios.csv", "w",
                                            #               encoding="utf8") as g:
                                            #         g.write("car_name,speed,deceleration_force,safe_distance,"
                                            #                 "stopping_time\n")
                                            #     self.column_names_written = not self.column_names_written

                                            if self.velocity.magnitude() > 0.0:  # Avoid division by zero error
                                                if 'Gentle' in self.name:
                                                    with open(self.file_path + str(self.file_name) + ".csv", "a",
                                                              encoding="utf8") as h:
                                                        full_str = str(self.name + "," +
                                                                       str(round(self.velocity.magnitude(), 2)) + "," +
                                                                       str(self.deceleration_force) + "," +
                                                                       str(round(self.safe_distance, 2)) + "," +
                                                                       str(round(self.reaction_time, 2)) + "," +
                                                                       str(round(
                                                                           self.safe_distance / self.velocity.magnitude(),
                                                                           2)) + "\n")
                                                        h.write(full_str)
                                                elif 'Aggressive' in self.name:
                                                    with open(self.file_path + str(self.file_name2) + ".csv", "a",
                                                              encoding="utf8") as h:
                                                        full_str = str(self.name + "," +
                                                                       str(round(self.velocity.magnitude(), 2)) + "," +
                                                                       str(self.deceleration_force) + "," +
                                                                       str(round(self.safe_distance, 2)) + "," +
                                                                       str(round(self.reaction_time, 2)) + "," +
                                                                       str(round(
                                                                           self.safe_distance / self.velocity.magnitude(),
                                                                           2)) + "\n")
                                                        h.write(full_str)
                                                else:
                                                    with open(self.file_path + "all.csv", "a",
                                                              encoding="utf8") as h:
                                                        full_str = str(self.name + "," +
                                                                       str(round(self.velocity.magnitude(), 2)) + "," +
                                                                       str(self.deceleration_force) + "," +
                                                                       str(round(self.safe_distance, 2)) + "," +
                                                                       str(round(self.reaction_time, 2)) + "," +
                                                                       str(round(
                                                                           self.safe_distance / self.velocity.magnitude(),
                                                                           2)) + "\n")
                                                        h.write(full_str)

    def turning(self, t):
        if self.route[0] is not None:
            self.direction = math.degrees(math.atan2(
                self.route[0].position.y - self.position.y,
                self.route[0].position.x - self.position.x
            ))

    def direction_to_next_node(self):
        return math.degrees(self.last.position.direction(self.route[0].position)) \
            if len(self.route) > 0 and isinstance(self.route[0], RoadNode) \
            else 0

    def get_info(self):
        return str.format("{:s}", super(Car, self).get_info())

    def curve(self, mass, radius, final_velocity, uHf, gravity):
        self.curve = mass * final_velocity ** 2 / radius
        print(self.curve)
        print('curve')
        print(final_velocity < math.sqrt(uHf * gravity))

    def centripetal_velocity(self, magnitude, radius, mass):
        # return the centripetal velocity that this car will use to negotiate curves
        return Vector2(math.sqrt((magnitude * radius) / mass)).redirect(self.direction)
