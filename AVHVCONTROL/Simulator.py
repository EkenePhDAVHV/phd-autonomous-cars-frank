#!/usr/bin/env python3
"""
    phd-autonomous-cars-frank
"""
# Operating System
import os, math
from platform import node
from random import random, randint
from time import time

import numpy as np
import matplotlib.pyplot as plt
from svgwrite import Drawing
from svgwrite.shapes import *
from copy import copy

# from test.Test2 import car
import copy as copy_module

os.chdir(os.path.dirname(__file__))
if not os.path.exists("drawings"):
    os.mkdir("drawings")

gravity = 9.81
uHf = 0.64
AVHV_total_cars = 100


class Vector2:
    def __init__(self, x=None, y=None):
        # Vector is a tuple
        if isinstance(x, Vector2):
            y = x.y
            x = x.x
        if isinstance(x, list):
            y = x[1]
            x = x[0]
        self.x = x if isinstance(x, int) or isinstance(x, float) else 0
        self.y = y if isinstance(y, int) or isinstance(y, float) else 0

    def copy(self):
        return copy(self)

    def get_value(self):
        return [self.x, self.y]

    def speed(self):
        #return math.sqrt(self.x ** 2 + self.y ** 2)
        return math.sqrt(self.velocity.x ** 2 + self.velocity.y ** 2)

    def reset_self(self):
        self.x = 0
        self.y = 0
        return self

    def draw(self, offset):
        if offset is None:
            offset = Vector2()
        return self.copy().add(Vector2([-offset.x, -offset.y]))

    def distance(self, point):
        return math.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)

    def magnitude(self):
        return self.distance(Vector2().reset_self())

    def redirect(self, angle):
        vector = self.copy()
        angle = math.radians(angle)
        magnitude = self.distance(Vector2([0, 0]))
        vector.x = magnitude * math.sin(angle)
        vector.y = magnitude * math.cos(angle)
        return vector

    def redirect_self(self, point):
        vector = self.redirect(point)
        self.x = vector.x
        self.y = vector.y
        return self

    def cap(self, bound):
        vector = self.copy()
        if vector.x > bound:
            vector.x = bound
        if vector.y > bound:
            vector.y = bound
        bound *= -1
        if vector.x < bound:
            vector.x = bound
        if vector.y < bound:
            vector.y = bound
        return vector

    def cap_self(self, bound):
        vector = self.cap(bound)
        self.x = vector.x
        self.y = vector.y
        return self

    def cap_magnitude(self, value):
        vector = self.copy()
        magnitude = math.sqrt(self.x * 2 + self.y * 2)
        if magnitude > value:
            vector.scale(value / magnitude)
        return vector

    def cap_magnitude_self(self, value):
        vector = self.cap_magnitude(value)
        self.x = vector.x
        self.y = vector.y
        return self

    def scale(self, scale):
        vector = self.copy()
        vector.x *= scale
        vector.y *= scale
        return vector

    def scale_self(self, scale_vector):
        vector = self.scale(scale_vector)
        self.x = vector.x
        self.y = vector.y
        return self

    def add(self, add_vector):
        vector = self.copy()
        vector.x += add_vector.x
        vector.y += add_vector.y
        return vector

    def add_self(self, add_vector):
        vector = self.add(add_vector)
        self.x = vector.x
        self.y = vector.y
        return self

    def add_self_velocity(self, add_vector):
        vector = self.add(add_vector)
        self.x = abs(vector.x)
        self.y = abs(vector.y)
        return self

    def direction(self, vector=None):
        # Return direction of this vector to the vector supplied, if no vector supplied, from origin to this vector.
        return math.atan2(vector.y - self.y, vector.x - self.x) if isinstance(vector, Vector2) else math.atan2(self.y,
                                                                                                               self.x)


class TrafficNode:
    def __init__(self, name, position=None, traffic_light=None, curve_radius=0, curve_center=[]):
        if position is None:
            position = [0, 0]

        self.pos = position
        self.id = name
        self.name = str(name)
        self.position = Vector2(position)
        self.traffic_light = traffic_light
        self.destination_nodes = []
        self.curve_radius = curve_radius
        self.curve_center = curve_center

    # the nodes concerned for test 4 = 2,4,6,7,8,12,14,16 and 18
    def check(self, node):
        if isinstance(node, TrafficNode):
            return self.position == node.position and self.name == node.name
        return False

    def get_info(self):
        output = str.format("{:7s} [{:3d}, {:3d}]", self.name, self.position.x, self.position.y)
        return output + str(self.destination_nodes)

    def connect(self, node, debug=False):
        if isinstance(node, TrafficNode):
            if not self.check(node) and not self.connected(node):
                self.destination_nodes.append(node)
                node.connect(self)
                if debug:
                    print("Connecting " + self.name + " to " + node.name)

    def connected(self, node):
        for destination_node in self.destination_nodes:
            if destination_node.check(node):
                return True
        return False

    def distance(self, pos):
      x = (self.pos[0] - pos[0])
      y = (self.pos[1] - pos[1])
      return math.sqrt(x*x+y*y)

class PedestrianNode(TrafficNode):
    def __init__(self, name, position=None, traffic_light=None):
        super(PedestrianNode, self).__init__(name=name, position=position, traffic_light=traffic_light)


class RoadNode(TrafficNode):
    def __init__(self, name, position=None, traffic_light=None):
        super(RoadNode, self).__init__(name=name, position=position, traffic_light=traffic_light)


class _TrafficSystem:
    def __init__(self, nodes=None, edges=None, colors=None, stroke_width=10):
        self.draw_node = True
        self.stroke_width = stroke_width
        if nodes is None:
            nodes = []
        self.nodes = nodes
        if edges is not None:
            self.add_edges(edges)

        if colors is None:
            colors = {}

        if colors.get('node') is None:
            colors['node'] = 'blue'
        if colors.get('edge') is None:
            colors['edge'] = 'aqua'
        if colors.get('text') is None:
            colors['text'] = 'white'

        self.colors = colors

    def get_nodes(self):
        return self.nodes

    def node(self, name):
        if isinstance(name, TrafficNode):
            return name
        for node in self.nodes:
            if str(node.name) == str(name):
                return node
        return None

    def add_nodes(self, nodes=None):
        self.nodes += nodes
        return self

    def add_edges(self, edges=None):
        for node, destinations in edges.items():
            node = self.node(node)
            if isinstance(node, TrafficNode):
                for destination in destinations:
                    destination = self.node(destination)
                    if isinstance(destination, TrafficNode):
                        node.connect(destination)
        return self

    def print_system(self):
        print("\n\n\n\nNODE INFO")
        for n in self.nodes:
            print(n.get_info())

    def draw_edges(self, canvas, offset):
        for node in self.nodes:
            for con in node.destination_nodes:
                canvas.add(Line(
                    start=node.position.draw(offset).get_value(),
                    end=con.position.draw(offset).get_value(),
                    stroke=self.colors.get('edge'),
                    stroke_width=self.stroke_width
                ))

    def draw_nodes(self, canvas, offset):
        for node in self.nodes:
            if self.draw_node:
                canvas.add(
                    Circle(center=node.position.draw(offset=offset).get_value(), r=7, fill=self.colors.get('node')))

    def draw_text(self, canvas, offset):
        for node in self.nodes:
            canvas.add(canvas.text(
                node.name,
                insert=node.position.draw(offset=offset).add(Vector2([-7, 7])).get_value(),
                font_size=16,
                fill=self.colors.get('text')
            ))

    def draw(self, canvas, offset):
        self.draw_edges(canvas=canvas, offset=offset)
        self.draw_nodes(canvas=canvas, offset=offset)
        self.draw_text(canvas=canvas, offset=offset)


class PedestrianSystem(_TrafficSystem):
    def __init__(self, nodes, edges):
        colors = {
            'node': '#aa0000',
            'edge': '#330000',
            'text': 'white'
        }
        super(PedestrianSystem, self).__init__(nodes=nodes, edges=edges, colors=colors)


class RoadSystem(_TrafficSystem):
    edges = []
    nodes = []
    route = {}  # The routing table looks like:
    def __init__(self, nodes, edges):
        colors = {
            'node': '#0000aa',
            'edge': '#000033',
            'text': 'white'
        }
        self.edges = edges
        self.nodes = nodes
        # The routing table shall tell us what is the next node for the target node (if any)
        route = {}
        # Implement BFS to find the route
        changed = True
        # Preseed with initial route
        for x in nodes:
            route[x.id] = {}
        for e in edges:
            for x in edges[e]:
                route[e][x] = x
        # From node 1 to go to node 2 you go via node 2
        # {1: {2: 2},
        #  2: {3: 3, 4: 4, 18: 18} }
        # Next step: go over all edges
        # Results must be:
        # {1: {2:2, 3:2, 4:2, 18:2}}
        while (changed):
            changed = False
            oldRoute = copy_module.deepcopy(route)
            for r in oldRoute:
                for c in oldRoute[r]:
                    for n in oldRoute[c]:
                        if n not in route[r]:
                            route[r][n] = c
                            changed = True
        self.route = route
        super(RoadSystem, self).__init__(nodes=nodes, edges=edges, colors=colors)

    def getNextNode(self, nodeID, targetID):
        if not nodeID in self.route:
            return None
        tgt = self.route[nodeID][targetID]
        if tgt == None:
            return tgt
        return self.getNode(tgt)

    def getNode(self, id):
        for x in self.nodes:
            if x.id == id:
                return x
        return None

    def getAllNextNodes(self, node):
        return self.edges[node]


class RoadSystem1(_TrafficSystem):
    edges = []
    nodes = []
    route = {} # The routing table looks like:

    def __init__(self, nodes, edges):
        self.edges = edges
        self.nodes = nodes
        # The routing table shall tell us what is the next node for the target node (if any)
        route = {}
        # Implement BFS to find the route
        changed = True
        # Preseed with initial route
        for x in nodes:
            route[x.id] = {}
        for e in edges:
            for x in edges[e]:
                route[e][x] = x
        # From node 1 to go to node 2 you go via node 2
        # {1: {2: 2},
        #  2: {3: 3, 4: 4, 18: 18} }
        # Next step: go over all edges
        # Results must be:
        # {1: {2:2, 3:2, 4:2, 18:2}}
        while(changed):
            changed = False
            oldRoute = copy_module.deepcopy(route)
            for r in oldRoute:
                for c in oldRoute[r]:
                    for n in oldRoute[c]:
                        if n not in route[r]:
                            route[r][n] = c
                            changed = True
        self.route = route
        print(route)
        colors = {
          'node': '#0000aa',
          'edge': '#000033',
          'text': 'white'
        }
        super(RoadSystem1, self).__init__(nodes=nodes, edges=edges, colors=colors)

    def getNextNode(self, nodeID, targetID):
        if not nodeID in self.route:
            return None
        tgt = self.route[nodeID][targetID]
        if tgt == None:
            return tgt
        return self.getNode(tgt)

    def getNode(self, id):
        for x in self.nodes:
            if x.id == id:
                return x
        return None

    def getAllNextNodes(self, node):
        return self.edges[node]



class _EnvironmentObject:

    def __init__(self, name, position=None, velocity=None, acceleration=None, direction=None, size=10, mass=None,
                 color=None, speed=None, car_ratio=None):

        # Initialise Default Values
        if not isinstance(name, str):
            name = str(name)
        if not isinstance(direction, int) and not isinstance(direction, float):
            direction = 0
        if not isinstance(mass, int) and not isinstance(mass, float):
            mass = 1
        if not isinstance(color, str):
            color = "white"

        # Set Values
        self.name = name
        self.position = Vector2(position)
        self.velocity = Vector2(velocity)
        self.acceleration = Vector2(acceleration)
        self.direction = direction
        self.size = Vector2(size)
        self.mass = mass
        self.color = color
        self.speed = speed
        self.car_ratio = car_ratio
        self.total_cars_percent = 0

        self.last = None

        # Environment Object Values
        self.environment = None

        # Initialise Data Collector
        self.data = {}
        for metric in ['time', 'position', 'velocity', 'acceleration', 'speed']:
            self.data[metric] = []

    # Set Environment
    def set_environment(self, environment):
        self.environment = environment

    # Update of how the object should act
    def behaviour_update(self, t):
        def __init__(self, pos=[0, 0], mass=1020, max_acceleration=1, drag=1.0, max_deacceleration=1,
                     acceleration=[0, 0], velocity=[0, 0]):
            self.pos = pos  # in meterso it
            self.mass = mass  # kg
            self.max_acceleration = max_acceleration
            self.max_deacceleration = max_deacceleration
            self.acceleration = acceleration  # in m/s^2
            self.velocity = velocity  # in m/s
            self.drag = drag

        def get_speed(self):
            """Returns the absolute speed in m/s"""
            return math.sqrt(self.velocity[0] * self.velocity[0] + self.velocity[1] * self.velocity[1])

        def get_force(self):
            return math.sqrt(
                self.acceleration[0] * self.acceleration[0] + self.acceleration[1] * self.velocity[1]) * self.mass

        def __str__(self):
            return "pos: %s mass:%s maxAccl:%s maxDeaccl:%s Accl:%s Velocity:%s" % (
                self.pos, self.mass, self.max_acceleration, self.max_deacceleration, self.acceleration, self.velocity)

    # Update of how the object should move
    def physics_update(self, t):
        def __init__(self, friction=0.75, gravity=9.8):
            self.friction = friction
            self.gravity = gravity

        def update_acceleration(self, Car, delta_accl):
            Car.acceleration[0] = Car.acceleration[0] + delta_accl[0]
            Car.acceleration[1] = Car.acceleration[1] + delta_accl[1]

        def update_velocity(self, Car, delta_t):
            Car.velocity[0] = Car.velocity[0] + delta_t * Car.acceleration[0]
            Car.velocity[1] = Car.velocity[1] + delta_t * Car.acceleration[1]

        def update_pos(self, Car, delta_t):
            Car.pos[0] = Car.pos[0] + delta_t * Car.velocity[0]
            Car.pos[1] = Car.pos[1] + delta_t * Car.velocity[1]

        def max_speed_curve(self, curve_radius):
            return math.sqrt(self.gravity * self.friction * curve_radius)
        # TODO Fix Calculation of Drag
        # Adjust velocity by acceleration relative to how much time has passed
        self.velocity.add_self(self.acceleration.copy().scale(t))
        # Adjust position by velocity relative to how much time has passed
        self.position.add_self(self.velocity.copy().scale(t))

    class CurveMovement():
        def __init__(self, time, car, radius, curveCenter, startDegree, endDegree):
            self.curveCenter = curveCenter
            self.lengthCircle = 2 * math.pi * radius
            self.radius = radius
            self.startTime = time
            self.endDegree = endDegree
            self.actualDegree = startDegree
            self.startDegree = startDegree
            self.car = car

        def move(self, time):
            reachedEnd = False
            degree = 360 * self.car.get_speed() / self.lengthCircle
            if self.endDegree < self.startDegree:
                degree = - degree
            self.actualDegree = (time - self.startTime) * degree

            if self.endDegree >= self.startDegree:
                if (self.actualDegree >= self.endDegree):
                    reachedEnd = True
            else:
                degree = - degree
                if (self.actualDegree <= self.endDegree):
                    reachedEnd = True

            if reachedEnd:
                # compute amount of way driven
                timeAfterEndingCurve = (self.actualDegree - self.endDegree) / 360 * self.lengthCircle / self.car.get_speed()
                self.actualDegree = self.endDegree
                # use up timeAfterEndingCurve for moving straight ...
                absSpeed = self.car.get_speed()
                # self.car.velocity =

            alpha = self.actualDegree / 180 * math.pi
            # in this case it is a 270 - 360° turn
            self.car.pos[0] = self.curveCenter[0] + self.radius * math.sin(alpha)
            self.car.pos[1] = self.curveCenter[1] + self.radius * math.cos(alpha)

            if (self.actualDegree == self.endDegree):
                return [True, timeAfterEndingCurve]
            return [False]

    # Record Values
    def data_update(self, t):
        # Update the Data Collector with Values for Time and Position
        self.data['time'].append(copy(t))
        self.data['position'].append(self.position.copy())
        self.data['velocity'].append(self.velocity.copy())
        self.data['acceleration'].append(self.acceleration.copy())

    # Update the object in order
    def update(self, t, record=False):
        self.behaviour_update(t)
        self.physics_update(t)
        if record:
            self.data_update(t)

    # Get Object Information
    def get_info(self):
        # Return Position and Size as Default Information
        return (
                str.format("{:12s}", self.name) +
                self._format_components("Position", self.position) +
                self._format_components("Velocity", self.velocity) +
                self._format_components("Acceleration", self.acceleration)
        )

    def _format_components(self, name, vector):
        if not isinstance(vector, Vector2):
            vector = Vector2(vector)
        return str.format('{:<32s}', str.format(
            '{:12s} [{:.2f}, {:.2f}]',
            name,
            vector.x,
            vector.y
        ))

    def check_overlap(self, colliding):
        # Check if Objects are Colliding / Overlapping by Cropping infinite areas around the object away.
        # If the flow is not stopped by any check, then the objects are colliding
        """This method checks if this object and the other object overlaps, which could be a crash for cars and stuff"""
        # Crop the left side
        if colliding.position.x + colliding.size.x < self.position.x:
            return False
        # Crop the bottom side
        if colliding.position.y + colliding.size.x < self.position.y:
            return False
        # Crop the right side
        if self.position.x + self.size.x < colliding.position.x:
            return False
        # Crop the top side
        if self.position.y + self.size.y < colliding.position.y:
            return False
        return

    def draw(self, canvas, offset):
        if isinstance(canvas, type(Drawing())):
            canvas.add(Circle(
                center=self.position.draw(offset).get_value(),
                r=self.size.x,
                fill=self.color
            ))

    def draw_direction(self, canvas, offset):
        if isinstance(canvas, type(Drawing())):
            canvas.add(Line(
                start=self.position.draw(offset).get_value(),
                end=(self.position.x + math.sin(math.radians(self.direction)) * 600,
                     self.position.y + math.cos(math.radians(self.direction)) * 600),
                fill='red',
                stroke_width=200
            ))

    def apply_force(self, t, magnitude, direction=None):
        if direction is None:
            direction = self.direction
        acceleration_due_to_force = Vector2((magnitude / self.mass) * t).redirect(direction)
        # Apply force in a direction (changed from Degrees to Radians)
        self.acceleration = self.acceleration.add(acceleration_due_to_force)

    def calculate_friction(self, mu):
        mu = 2.7 # How did we arrive at this figure? It was earlier defined as something close to 0.7
        return mu * self.mass * self.gravity

    def air_resistance(self, t):
        # Apply a force in the opposite direction to travel.
        coefficient = 1 # I will put in the correct value for this later
        density = 1.1839  # Density of Air? I found to be approx. 1.2 at 25 degrees celsius
        air_resistance = (coefficient * density * self.drag_area * (self.get_speed() ** 2)) / 2
        return air_resistance


class Car(_EnvironmentObject):
    def __init__(self, name=None, position=None, velocity=None, acceleration=None, direction=None, size=10, mass=None,
                 route=None, color=None, power=1000, velocity_max=30, acceleration_max=30, easy_physics=True,
                 car_type=None):
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
        self.total_time = 0

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

    def get_speed(self):
        return self.velocity

    def draw(self, canvas, offset):
        if isinstance(canvas, type(Drawing())):
            color = 'blue'
            if len(self.route) > 0:
                color = 'grey' if self.traffic_light is None \
                    else 'yellow' if self.traffic_light.amber \
                    else 'green' if self.traffic_light.green \
                    else 'red' if self.traffic_light.red \
                    else 'blue'

            if self.environment.environment_objects is not None:
                if self.environment.environment_objects[CarSpawner] is not None:
                    for carSpawn in self.environment.environment_objects[CarSpawner]:
                        if carSpawn.name == 'GentleCar':
                            color = 'blue'
                        elif carSpawn.name == 'AggressiveCar':
                            color = 'red'
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
        super(Car, self).behaviour_update(t)
        self.next_node()
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

    def next_node(self):
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
                        self.acceleration.reset_self()
                        self.velocity.reset_self()
                        #self.velocity.redirect(self.direction)

        else:
            self.velocity.reset_self()
            self.acceleration.reset_self()

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
            self.apply_force(t, 5000)

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

        # Deleting Car once goal is reached
        def __del__(car):
            del car

class Aggressive_Car(Car):
    def __init__(self, name=None, route=None, direction=None, car_type='aggressive'):
        self.car_type = car_type
        self.route_old = route
        #car = Car(name=name, route=route, direction=direction)
        super(Aggressive_Car, self).__init__(name=name, route=route, direction=direction, car_type = car_type)
        #print(self.route)
        print('__init__', car_type)

    def behaviour_update1(self, t):
        super(Car, self).behaviour_update(t)
        print('next_node', self.next_node())
        self.next_node()
        self.direction
        self.turning(t)
        #color = color.red
        if len(self.route):
            if self.Traffic_light is None and self.Car is None and self.Car >0:
                self.apply_force(t, 4000)
            else:
                self.obey_traffic_light()


class Gentle_Car(Car):
    def __init__(self, name=None, route=None, direction=None, car_type='gentle'):
        self.car_type = car_type
        self.route = route
        super(Gentle_Car, self).__init__(name=name, route=self.route, direction=direction, car_type = car_type)
        print('__init__', car_type)

    def behaviour_update1(self, t):
        #color=color.green
        print('gentle car')
        if isinstance(self.Car, Aggressive_Car):
            self.next_node()
            if self.Aggressive_Car is None and self.Traffic_light is True:
                if self.safe_distance < 30:
                    self.direction = self.direction_to_next_node()
                    self.turning(t)
                    self.oby_traffic();
                    self.velocity.scale(0.9)
                    self.acceleration.re
        else:
            self.apply_force(t, 5000)

    '''def behaviour_update(self, t):
        print('beh', t)
        super(Car, self).behaviour_update(t)
        self.next_car()
        if len(self.car) > 0:
            self.turning(t)
            # Obey obstacle
            self.obey_obstacle(t)'''


class Pedestrian(_EnvironmentObject):
    def __init__(self, name, position=None, velocity=None, acceleration=None, direction=None, size=10, mass=None,
                 route=None, color=None):
        if not isinstance(color, str):
            color = "green"
        if not isinstance(mass, int) and not isinstance(mass, float):
            mass = 1200
        super(Pedestrian, self).__init__(name=name, position=position, velocity=velocity, acceleration=acceleration,
                                         direction=direction, size=size, mass=mass, color=color)
        if not isinstance(route, list):
            route = []
        self.route = route
        self.idle_time = 0
        self.pedestrian_light = None

    def draw(self, canvas, offset):
        if isinstance(canvas, type(Drawing())):
            color = 'yellow'
            if len(self.route) > 0:
                color = 'grey' if self.pedestrian_light is None \
                    else 'green' if self.pedestrian_light.green \
                    else 'red' if self.pedestrian_light.red \
                    else 'green'
            canvas.add(Circle(
                center=self.position.draw(offset).get_value(),
                r=self.size.x,
                fill=color
            ))
            super(pedestrian, self).draw_direction(canvas=canvas, offset=offset)


    def obey_pedestrian_light(self, t):
        # Test for traffic Light
        if self.pedestrian_light is None:
            if len(self.route) > 0:
                if isinstance(self.route[0], PedestrianNode):
                    if self.route[0].pedestrian_light is not None:
                        self.pedestrian_light = self.route[0].pedestrian_ligh


class TrafficLight(_EnvironmentObject):

    def __init__(self, name=None, position=None, size=None, direction=None, traffic_node=None, timings=None,
                 timer=None, distance=None, throughput=None):
        if size is None:
            size = [20, 60]
        # Timings
        if timings is None:
            timings = [5, 1]
        if timer is None:
            timer = 0
        if distance is None:
            distance = 100
        self.cars = [4000]
        self.max_queue = 30
        if len(self.cars) > self.max_queue:
            self.max_queue = len(self.cars)
            # self.throughput = 100

        super(TrafficLight, self).__init__(name=name, position=position, size=size, direction=direction)
        self.traffic_node = traffic_node
        # Lights
        self.cycle = [
            [True, False, False],  # Green
            [False, True, False],  # Amber
            [False, False, True],  # Red
            [False, True, True]  # Red and Amber
        ]
        self.green, self.amber, self.red = self.cycle[0]
        self.phase = 0
        self.timings = timings
        self.timer = timer
        self.change(0)
        self.distance = distance

        self.count_cars = 0

    def set_environment(self, environment):
        super(TrafficLight, self).set_environment(environment=environment)
        if not isinstance(self.traffic_node, RoadNode):
            self.traffic_node = self.environment.road_system.node(self.traffic_node)
        if isinstance(self.traffic_node, RoadNode):
            self.traffic_node.traffic_light = self
            self.position = Vector2(
                [self.traffic_node.position.x + self.position.x, self.traffic_node.position.y + self.position.y])

    def set(self, phase=None):
        self.phase = (self.phase + 1 if phase is None else phase if isinstance(phase, int) else 0) % len(self.cycle)
        (self.green, self.amber, self.red) = self.cycle[self.phase % len(self.cycle)]

    def change(self, t):
        self.timer += t
        while self.timer >= self.timings[self.phase % len(self.timings)]:
            self.timer -= self.timings[self.phase % len(self.timings)]
            self.set()

    def behaviour_update(self, t):
        super(TrafficLight, self).behaviour_update(t)
        self.change(t)

    def car_queue_length(self):

        return len(self.cars)

    def traffic_light_decision(self, lane):
        self.lane = lane

    def lane_to_obey(self, car_queue_length, time):
        if self.car_queue_length() > 20 and self.car.idle_time < 10:
            pass  # Increment
        else:
            pass  # Do not increment
        self.count_cars += 1

    def get_info(self):
        return str.format(
            '{:s} {:10s} {:10s} {:10s} {:s} {:s}',
            super(TrafficLight, self).get_info(),
            'Red' if self.red else '',
            'Amber' if self.amber else '',
            'Green' if self.green else '',
            'Queue Length : ' + str(self.car_queue_length()),
            'Cars that pass :' + str(self.count_cars),
        )

    def draw(self, canvas, offset, rectangle=None, r=None):

        if (self.direction == 90 or self.direction == 270):
            canvas.add(Rect(
                insert=((self.position.draw(offset=offset).x - self.size.x / 2),
                        (self.position.draw(offset=offset).y - self.size.y / 2)),
                size=(self.size.x, self.size.y),
                fill="#222222"
            ))

            def draw_light(active_color, inactive_color, active, location):
                canvas.add(Circle(
                    fill=active_color if active else inactive_color,
                    center=location,
                    r=self.size.y * 0.4
                ))

            draw_light("#E6342F", "#350604", self.red,
                       (self.position.draw(offset=offset).x - self.size.x / 3, self.position.draw(offset=offset).y))
            draw_light("#E69C2F", "#422A05", self.amber,
                       (self.position.draw(offset=offset).x, self.position.draw(offset=offset).y))
            draw_light("#32AD51", "#0B4219", self.green,
                       (self.position.draw(offset=offset).x + self.size.x / 3, self.position.draw(offset=offset).y))
        else:
            canvas.add(Rect(
                insert=((self.position.draw(offset=offset).x - self.size.x / 2),
                        (self.position.draw(offset=offset).y - self.size.y / 2)),
                size=(self.size.x, self.size.y),
                fill="#222222"
            ))

            def draw_light(active_color, inactive_color, active, location):
                canvas.add(Circle(
                    fill=active_color if active else inactive_color,
                    center=location,
                    r=self.size.x * 0.4
                ))

            draw_light("#E6342F", "#350604", self.red, (
                self.position.draw(offset=offset).x, self.position.draw(offset=offset).y - self.size.y / 3))
            draw_light("#E69C2F", "#422A05", self.amber,
                       (self.position.draw(offset=offset).x, self.position.draw(offset=offset).y))
            draw_light("#32AD51", "#0B4219", self.green, (
                self.position.draw(offset=offset).x, self.position.draw(offset=offset).y + self.size.y / 3))
        super(TrafficLight, self).draw_direction(canvas=canvas, offset=offset)


class Intersection(_EnvironmentObject):

    def __init__(self, name=None, position=None, size=None, direction=None, lanes=None):
        super(Intersection, self).__init__(name=name, position=position, size=size, direction=direction)
        self.lanes = lanes



    def update(self, t):
        super(Intersection, self).update(t)


class Environment:

    def __init__(self, name, layout):
        self.name = name
        if not isinstance(layout, dict):
            layout = {layout.__class__: layout}
        if not layout.get(RoadSystem):
            layout[RoadSystem] = RoadSystem([], {})
        if not layout.get(PedestrianSystem):
            layout[PedestrianSystem] = PedestrianSystem([], {})
        self.layout = layout
        # Environment Objects
        self.environment_objects = {
            # Inanimate Objects
            Intersection: [],
            TrafficLight: [],
            CarSpawner: [],
            # Animate Objects
            Car: []
        }
        self.road_system = layout.get(RoadSystem)
        self.pedestrian_system = layout.get(PedestrianSystem)

    def draw(self, canvas, offset=None):
        if offset is None:
            offset = Vector2()
        for environment_object_type, environment_object_group in self.environment_objects.items():
            for environment_object in environment_object_group:
                environment_object.draw(canvas=canvas, offset=offset)

    def update(self, delta_time, record=False):
        output = ''
        # For each
        for environment_object_type, environment_object_group in self.environment_objects.items():
            for environment_object in environment_object_group:
                # Update
                environment_object.update(delta_time, record=record)
                # Increment Output
                output += "\n" + environment_object.get_info()
        # Record Values
        if record:
            self.record_values(delta_time)

        return output

    def add_objects(self, environment_objects):
        self.total_cars_percent = 0
        if not isinstance(environment_objects, list):
            environment_objects = [environment_objects]
        for environment_object in environment_objects:
            if environment_object.car_ratio is not None:
                if (environment_object.name == 'GentleCar'):
                    self.total_cars_percent += environment_object.car_ratio
                elif (environment_object.name == 'AggressiveCar'):
                    self.total_cars_percent += environment_object.car_ratio
            environment_object.total_cars_percent = self.total_cars_percent
            environment_object.set_environment(self)

            if not self.environment_objects.get(type(environment_object)):
                self.environment_objects[type(environment_object)] = []
            self.environment_objects[type(environment_object)].append(environment_object)
        return self

    def get_object(self, class_name, name):
        for environment_object in self.environment_objects[class_name]:
            if environment_object.name == name:
                return environment_object

    def record_values(self, t):
        for environment_object_type, environment_object_group in self.environment_objects.items():
            for environment_object in environment_object_group:
                environment_object.data_update(t)


class StatisticsReporter:
    def __init__(self, environment):
        # History
        self.history = {}
        # Records
        self.history.update({'time': []})
        self.history.update({'collisions': []})
        self.history.update({'intersections': []})
        self.environment = environment

    def record(self, t):
        # Time
        self.history['time'].append(t)
        # Values
        self.record_car_collisions()
        self.record_cars_in_intersections()

    def record_car_collisions(self):
        collisions = []
        for car_a in self.environment.environment_objects[Car]:
            for car_b in self.environment.environment_objects[Car]:
                if car_a is not car_b:
                    if car_a.check_overlap(car_b):
                        collisions.append([car_a, car_b])
        self.history['collisions'].append(collisions)

    def record_cars_in_intersections(self):
        intersections = []
        for car in self.environment.environment_objects[Car]:
            for intersection in self.environment.environment_objects[Intersection]:
                if intersection.check_overlap(car):
                    intersections.append([intersection, car])
        self.history['intersections'].append(intersections)

    def frequency_dumper(self, metric):
        count = []
        for _ in metric:
            count.append(len(_))
        return count

    def calculate_car_collisions(self):
        return np.divide(self.frequency_dumper(self.history['collisions']), 2)

    def calculate_cars_in_intersection(self):
        return self.frequency_dumper(self.history['intersections'])

    def get_data_with_filter(self, set_name, name_filter):
        result = []
        intersection_collisions = self.history[set_name]
        for tick in intersection_collisions:
            tick_result = []
            for collision in tick:
                if collision[0].name == name_filter:
                    tick_result.append(collision)
            result.append(tick_result)
        return result

    def plot_graph_of_collisions(self):
        plt.plot(self.calculate_car_collisions())
        plt.show()

    def plot_graph_of_collisions_vs_intersection(self, intersection_name):
        collisions = []
        # For Each Frame
        for tick in range(0, len(self.history['time'])):
            # Register the Intersection and Collision Snapshot
            intersection_snapshot = self.history['intersections'][tick]
            collisions_snapshot = self.history['collisions'][tick]
            # For Every Intersection Record
            collisions_in_tick = []
            for intersection_record in intersection_snapshot:
                # Data
                intersection = intersection_record[0]
                car = intersection_record[1]
                # Check Intersection is Useful
                if intersection.name == intersection_name:
                    # Check if the Car in the Intersection was involved in any collisions
                    collision = None
                    for collision_record in collisions_snapshot:
                        # Data
                        car_a = collision_record[0]
                        car_b = collision_record[1]
                        # Check if it collided
                        if car_a.name == car.name or car_b.name == car.name:
                            collision = collision_record
                    if collision is not None:
                        collisions_in_tick.append(collision)
            collisions.append(collisions_in_tick)

        count_collisions = self.frequency_dumper(collisions)
        count_cars_in_intersection = self.frequency_dumper(
            self.get_data_with_filter('intersections', intersection_name))

        # Plot
        plt.scatter(count_cars_in_intersection, count_collisions)

    def result(self):
        # Plot
        intersection_names = ["First Intersection", "Second Intersection"]
        title = "Collisions in"
        for intersection_name in intersection_names:
            title += " " + intersection_name + ","
            self.plot_graph_of_intersection_vs_collisions(intersection_name)
            plt.show()

        title = title[:-1]
        plt.title(title)
        plt.xlabel('No of collisions')
        plt.ylabel('No of cars in Intersection')
        plt.savefig(self.environment.name + "_collisions.pdf")


class FileHandler:

    def __init__(self, directory='output'):
        # Init Data
        self.directory = self.fix_directory(directory)
        self.files = []

        # Create Directory
        if not os.path.isdir(directory):
            os.mkdir(directory)
        self.update_files()

    @staticmethod
    def fix_directory(directory):
        if not directory.endswith('/'):
            directory += '/'
        return directory

    def update_files(self):
        self.files = os.listdir(self.directory)

    def list_files(self, display=False):
        self.update_files()
        if display:
            for file in self.files:
                print(file)
        return self.files

    def write_file(self, filename='', file_contents='', sub_directory=''):
        file = open(self.directory + self.fix_directory(sub_directory) + filename, 'w')
        file.write(file_contents)

    def remove_files(self, files, display=False):
        self.update_files()
        if files is None:
            files = self.files
        for file in files:
            if display:
                print('Menus ' + file)
            os.remove(file)
        self.update_files()


class CarSpawner(_EnvironmentObject):  # new car arrivals to grow the queue length
    def __init__(self, name, node, direction, route=None, safe_distance=None, car_ratio=None, easy_physics=True):
        self.route = route
        if safe_distance is None:
            safe_distance = 30
        self.node = node
        self.car_ratio = car_ratio
        super(CarSpawner, self).__init__(name=name, position=self.node.position, direction=direction, car_ratio=car_ratio)
        self.cars = []
        self.safe_distance = safe_distance
        self.easy_physics = easy_physics
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
                    count_carspwan = len(self.environment.environment_objects[CarSpawner]) - 1
                    total_cars_percent = self.environment.environment_objects[CarSpawner][count_carspwan].total_cars_percent
                    if total_cars_percent == 100:
                        cars_running = round((AVHV_total_cars * self.car_ratio) / 100)
                    else:
                        try:
                            cars_num = (self.car_ratio / total_cars_percent) * 100
                            cars_running = round((AVHV_total_cars * cars_num) / 100)
                        except TypeError as e:
                            print(str(e))
                        except:
                            print('error')
                except:
                    pass

                if (cars_running is not None and  len(self.cars) < cars_running):
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

    def spawn_another_car(self, route):
        if route is not None:
            route = route
            if len(route) > 0:
                for _ in range(0, len(route)):
                    route[_] = self.environment.road_system.node(route[_])
                if isinstance(route[0], RoadNode):
                    self.position = route[0].position.copy()
                    self.last = route[0]
                    #self.route = route[1:]
            if self.last:
                pass
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
        self.cars.append(Car(
            name=self.name + " : " + str(len(self.cars) + 1),
            position=self.node.position,
            route=route
        ))
        self.environment.add_objects(self.cars[-1])


class Simulation:

    def __init__(self, environment, time_end=10, time_increment=0.1, debugging=False):
        # Environment
        self.environment = environment
        # Timing Control
        self.__end_time = time_end
        self.__time_increment = time_increment
        self.__debug_counter = 0
        self.__current_time = 0
        # Statistics
        self.debugging = debugging
        self.__reporter = None
        # Drawings
        self.__frame = None
        self.__scene = Drawing()
        self.__min_bound = Vector2([0, 0])
        self.__max_bound = Vector2([0, 0])
        # File Path
        self.__drawing_directory = "drawings/"
        self.__drawing_prefix = "svgwriter_frame_"
        # Start
        self.__start_simulation()

    def __calculate_blank(self):
        if isinstance(self.environment, Environment):
            layout_nodes = self.environment.road_system.nodes + self.environment.pedestrian_system.nodes
            if len(layout_nodes) > 0:
                self.__min_bound = layout_nodes[0].position.copy()
                self.__max_bound = layout_nodes[0].position.copy()
            else:
                self.__min_bound = Vector2(-600, -600)
                self.__max_bound = Vector2(600, 600)
            for node in layout_nodes:
                # Min X
                if node.position.x < self.__min_bound.x:
                    self.__min_bound.x = node.position.x
                # Min Y
                if node.position.y < self.__min_bound.y:
                    self.__min_bound.y = node.position.y
                # Max X
                if node.position.x > self.__max_bound.x:
                    self.__max_bound.x = node.position.x
                # Max Y
                if node.position.y > self.__max_bound.y:
                    self.__max_bound.y = node.position.y
        border = 100
        self.__min_bound.x -= border
        self.__min_bound.y -= border
        self.__max_bound.x += border
        self.__max_bound.y += border

        self.__scene = Drawing(
            "blank.svg",
            size=[
                abs(self.__max_bound.x - self.__min_bound.x),
                abs(self.__max_bound.y - self.__min_bound.y)
            ]
        )
        self.__scene.add(Polygon(
            [
                # Bottom Left
                [0, 0],
                # Top Left
                [0, abs(self.__max_bound.y - self.__min_bound.y)],
                # Top Right
                [abs(self.__max_bound.x - self.__min_bound.x), abs(self.__max_bound.y - self.__min_bound.y)],
                # Bottom Right
                [abs(self.__max_bound.x - self.__min_bound.x), 0],
            ],
            fill='white'
        ))

    def __calculate_layout(self):
        self.__calculate_blank()
        for layout_type, layout in self.environment.layout.items():
            layout.draw_edges(canvas=self.__scene, offset=self.__min_bound)
        for layout_type, layout in self.environment.layout.items():
            layout.draw_nodes(canvas=self.__scene, offset=self.__min_bound)
        for layout_type, layout in self.environment.layout.items():
            layout.draw_text(canvas=self.__scene, offset=self.__min_bound)

    def __draw_current(self, timestep):
        # New Canvas
        self.__frame = self.__scene.copy()
        self.__frame.filename = str.format(
            "{:s}{:s}{:.2f}{:s}",
            self.__drawing_directory, self.__drawing_prefix, timestep, ".svg"
        )
        # Draw Elements and Save
        self.environment.draw(canvas=self.__frame, offset=self.__min_bound)
        self.__frame.save()

    def __start_simulation(self):
        self.__calculate_layout()
        if isinstance(self.environment, Environment):
            self.__reporter = StatisticsReporter(self.environment)
            self.__debug_counter = 0
            self.__current_time = 0
            # Drawing Prep
            for frame in os.listdir(self.__drawing_directory):
                os.remove(self.__drawing_directory + frame)
            self.__draw_current(self.__current_time)
            # Canvas and Line
            while self.__current_time < self.__end_time:
                # Calculate Time Change
                debug = self.environment.update(delta_time=self.__time_increment, record=False)
                debug = str.format("\nTick : {:3.3f}\t", self.__current_time) + debug
                # Check if Debug should be run
                if self.__debug_counter <= self.__current_time:
                    self.__debug_counter += self.__time_increment
                    # Data RecordingpendingCars
                    self.environment.record_values(self.__current_time)
                    self.__reporter.record(self.__debug_counter)
                    if self.debugging:
                        pass
                        #print(debug)
                    # Finish Data Reporting
                # Increment at end
                self.__current_time = self.__current_time + self.__time_increment
                self.__draw_current(self.__current_time)


if __name__ == '__main__':
    print("Ekene's Simulation, please create a Simulation and add and Environment")