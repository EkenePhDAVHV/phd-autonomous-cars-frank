import math

from svgwrite import Drawing
from svgwrite.shapes import *

from AVHV_Main.constants import *

from AVHV_Main.RoadNode import RoadNode
from AVHV_Main.TrafficLight import TrafficLight
from AVHV_Main._EnvironmentObject import EnvironmentObject


class Car(EnvironmentObject):
    def __init__(self, name=None, position=None, velocity=None, acceleration=None, direction=None, size=10, mass=None,
                 route=None, color=None, power=1000, velocity_max=30, acceleration_max=30,\
                 easy_physics=True, car_type=None, idle_time=0, car_in_front=None, safe_distance=None, no_braking=False):
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

        self.power = power

        self.turning_angle = 0
        self.idle_time = 0
        self.traffic_light = None
        self.easy_physics = easy_physics
        self.velocity_max = velocity_max
        self.acceleration_max = acceleration_max
        self.max_acceleration = 1
        self.max_deacceleration = 1
        self.total_time = 0
        self.traffic_light_nodes = []
        self.no_braking = no_braking

        self.turning_angle = 0
        self.traffic_light = None
        self.easy_physics = easy_physics
        self.velocity_max = velocity_max
        self.acceleration_max = acceleration_max
        self.max_acceleration = 1
        self.max_deacceleration = 1
        self.total_time = 0

        self.idle_time = idle_time
        self.idle_t = idle_time

        self.position = position
        self.direction = direction
        self.curve = None
        self.last = None

        self.counter = 0

        self.car_in_front = car_in_front
        self.safe_distance = safe_distance

        self.has_traffic_lights = 0
        self.wait_time = 0

    def set_environment(self, environment):
        super(Car, self).set_environment(environment)
        if len(self.route) > 0:
            for _ in range(0, len(self.route)):
                self.route[_] = self.environment.road_system.node(self.route[_])

            if isinstance(self.route[0], RoadNode):
                self.position = self.route[0].position.copy()
                self.last = self.route[0]
                self.route = self.route[1:]
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

            # if self.environment.environment_objects is not None:
            #     if self.environment.environment_objects[CarSpawner] is not None:
            #         for carSpawn in self.environment.environment_objects[CarSpawner]:
            #             if carSpawn.name == 'GentleCar':
            #                 color = 'blue'
            #             elif carSpawn.name == 'AggressiveCar':
            #                 color = 'red'
            canvas.add(Circle(
                center=self.position.draw(offset).get_value(),
                r=self.size.x,
                fill=color
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

            # print(self, self.car_in_front)
        self.wait_time = t

        super(Car, self).behaviour_update(t)
        self.next_node(t)
        #print(self.route)  # <---- Here
        if len(self.route) > 0:
            self.turning(t)
            # Obey Traffic Lights
            self.obey_traffic_light(t)


            # car waiting timeeuioiro[ioeioio
            # if isinstance(self.traffic_light, TrafficLight):
            #   if t in range and not moving:
            #       if self.traffic_light.position.distance(self.position) < self.traffic_light.distance \
            #          and self.get_speed() < 1:
            #          self.idle_time += t

            # car friction controlling the curve
            # def curve(mu, magnitude, )

            #   self.apply_force(t, magnitude=5000)  # Direction = self.direction
            # if self.acceleration.direction():
            #  Direction = self.direction
            # friction = mu * magntude * gravity
            # return friction

    def physics_update(self, t):
        super(Car, self).physics_update(t)
        if self.easy_physics:
            self.acceleration.cap_self(self.acceleration_max)
            self.velocity.cap_self(self.velocity_max)

    def next_node(self, t):
        if len(self.route) > 0:
            if isinstance(self.route[0], RoadNode):
                if self.position.distance(self.route[0].position) < 10:

                    if isinstance(self.traffic_light, TrafficLight):
                        self.traffic_light.count_cars += 1
                        for car in range(0, len(self.traffic_light.cars)):
                            if self.traffic_light.cars[car] is self:
                                try:
                                    self.traffic_light.cars.remove(car)
                                except ValueError:
                                    pass
                    self.route = self.route[1:]
                    self.direction = self.direction_to_next_node()

                    #test curve data
                    #print('velocity')
                    #print('gravity')
                    #radius = self.get_radius_of_turn()
                    #print(radius)
                    #mass = 1
                    #curve_data = self.curve(self, self.mass, radius, self.velocity, uHf, gravity)
                    self.idle_time = 0
                    if len(self.route) > 0 and isinstance(self.route[0], RoadNode):
                        self.traffic_light = self.route[0].traffic_light
                        if isinstance(self.traffic_light, TrafficLight):
                            self.traffic_light.cars.append(self)
                    if self.easy_physics:
                        pass
                        # self.acceleration.reset_self()
                        # self.velocity.reset_self()
                        # self.velocity.redirect(self.direction)

        else:
            pass
            # self.apply_force(t, braking_force, decelerate=True)

    def obey_traffic_light(self, t):
        # Test for traffic Light
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
            print('current node:', self.route[0].id)
            print('distance:', self.position.distance(self.route[0].position), self.position.get_value(),
                  self.route[0].position.get_value())
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
            if self.no_braking:
                self.apply_force(t, moving_force)
            else:
                if len(self.route) > 1:
                    self.apply_force(t, moving_force)
                else:
                    self.apply_force(t, braking_force, decelerate=True)
            # self.apply_force(t, 5000)

    def turning(self, t):
        if self.route[0] is not None:
            self.direction = math.degrees(math.atan2(
                self.route[0].position.x - self.position.x,
                self.route[0].position.y - self.position.y
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
        return final_velocity < math.sqrt(uHf * gravity)
