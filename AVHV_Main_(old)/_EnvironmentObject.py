import math
from copy import copy

from svgwrite import Drawing
from svgwrite.shapes import *

from AVHV_Main.constants import *
from AVHV_Main.Vector2 import Vector2


class EnvironmentObject:

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

        if acceleration is not None:
            if isinstance(acceleration, int):
                self.acceleration = [acceleration, 0]
            if isinstance(acceleration, float):
                self.acceleration = [acceleration, 0.0]
            else:
                self.acceleration = acceleration
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

        self.pos = position

        # Initialise Data Collector
        self.data = {}
        for metric in ['time', 'position', 'velocity', 'acceleration', 'speed', 'direction', 'nodes_left']:
            self.data[metric] = []

    # Set Environment
    def set_environment(self, environment):
        self.environment = environment

    # Update of how the object should act
    def behaviour_update(self, t):
        def __init__(pos=[0, 0], mass=1020, max_acceleration=1, drag=1.0, max_deacceleration=1,
                     acceleration=[0, 0],
                     velocity=[0, 0]):
            self.pos = pos  # in meterso it
            self.mass = mass  # kg
            self.max_acceleration = max_acceleration
            self.max_deacceleration = max_deacceleration
            self.acceleration = acceleration  # in m/s^2
            self.velocity = velocity  # in m/s
            self.drag = drag

    def get_speed(self):
        """Returns the absolute speed in m/s"""
        return math.sqrt(self.velocity.x * self.velocity.x + self.velocity.y * self.velocity.y)

    def get_force(self):
        return math.sqrt(
            self.acceleration[0] * self.acceleration[0] + self.acceleration[1] * self.acceleration[1]) * self.mass

    def __str__(self):
        props = []
        properties = ''

        try:
            props.append(self.name)
        except AttributeError:
            pass

        try:
            props.append(self.pos)
        except AttributeError:
            pass

        try:
            props.append(self.mass)
        except AttributeError:
            pass

        try:
            props.append(self.max_acceleration)
        except AttributeError:
            pass

        try:
            props.append(self.max_deacceleration)
        except AttributeError:
            pass

        try:
            props.append(self.velocity)
        except AttributeError:
            pass

            # return "pos: %s mass:%s maxAccl:%s maxDeaccl:%s Accl:%s Velocity:%s" % (
            #     self.pos, self.mass, self.max_acceleration, self.max_deacceleration, self.acceleration, self.velocity)
        for prop in props:
            properties += str(prop)
            properties += ' '

        return properties

    # Update of how the object should move
    def physics_update(self, t):
        def __init__(friction=0.75, grav_accel=grav_accel):
            self.friction = friction
            self.gravity = grav_accel

        def update_acceleration(car, delta_accl):
            car.acceleration[0] = car.acceleration[0] + delta_accl[0]
            car.acceleration[1] = car.acceleration[1] + delta_accl[1]

        def update_velocity(car, delta_t):
            car.velocity[0] = car.velocity[0] + delta_t * car.acceleration[0]
            car.velocity[1] = car.velocity[1] + delta_t * car.acceleration[1]

        def update_pos(car, delta_t):
            car.pos[0] = car.pos[0] + delta_t * car.velocity[0]
            car.pos[1] = car.pos[1] + delta_t * car.velocity[1]

        def max_speed_curve(curve_radius):
            return math.sqrt(self.gravity * self.friction * curve_radius)

        # TODO Fix Calculation of Drag
        # Adjust velocity by acceleration relative to how much time has passed
        self.velocity.add_self(self.acceleration.copy().scale(t))

        # so we don't have negative velocity
        if self.velocity.x < 0:
            self.velocity.x = 0
        if self.velocity.y < 0:
            self.velocity.y = 0

        # so we don't have exceed maximum velocity
        if self.velocity.magnitude() > self.velocity_max:
            self.velocity.cap(max_velocity)

        # Adjust position by velocity relative to how much time has passed
        self.position.add_self(self.velocity.copy().scale(t/4))

    class CurveMovement:
        def __init__(self, time, car, radius, curve_center, start_degree, end_degree):
            self.curve_center = curve_center
            self.length_circle = 2 * math.pi * radius

            self.radius = radius
            self.start_time = time
            self.end_degree = end_degree
            self.actual_degree = start_degree
            self.start_degree = start_degree
            self.car = car

        def move(self, time):
            reached_end = False
            degree = 360 * self.car.get_speed() / self.length_circle

            if self.end_degree < self.start_degree:
                degree = - degree
            self.actual_degree = (time - self.start_time) * degree

            if self.end_degree >= self.start_degree:
                if self.actual_degree >= self.end_degree:
                    reachedEnd = True
            else:
                degree = - degree
                if self.actual_degree <= self.end_degree:
                    reachedEnd = True

            if reached_end:
                # compute amount of way driven
                timeAfterEndingCurve = (self.actual_degree - self.end_degree) / 360 * self.length_circle / \
                                       self.car.get_speed()
                self.actual_degree = self.end_degree

                # use up timeAfterEndingCurve for moving straight ...
                absSpeed = self.car.get_speed()
                # self.car.velocity =

            alpha = self.actual_degree / 180 * math.pi
            # in this case it is a 270 - 360° turn
            self.car.pos[0] = self.curveCenter[0] + self.radius * math.sin(alpha)
            self.car.pos[1] = self.curveCenter[1] + self.radius * math.cos(alpha)

            if self.actual_degree == self.end_degree:
                return [True, timeAfterEndingCurve]
            return [False]

    # Record Values
    def data_update(self, t):
        # Update the Data Collector with Values for Time and Position
        self.data['time'].append(copy(t))
        self.data['position'].append(self.position.copy())
        self.data['velocity'].append(self.velocity.copy())
        self.data['acceleration'].append(self.acceleration.copy())
        self.data['direction'].append(self.direction)
        try:
            self.data['nodes_left'].append(len(self.route))
        except AttributeError:
            pass

    # Update the object in order
    def update(self, t, record=True):
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
        return True

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

    def apply_force(self, t, magnitude, decelerate=False, direction=None):
        if direction is None:
            direction = self.direction
        acceleration_due_to_force = Vector2((magnitude / self.mass) * t)
        # Apply force in a direction (changed from Degrees to Radians)

        if decelerate:  # if the car is decelerating
            acceleration_due_to_force.x = -acceleration_due_to_force.x
            acceleration_due_to_force.y = -acceleration_due_to_force.y

        # self.acceleration = self.acceleration.add(acceleration_due_to_force)
        self.acceleration = acceleration_due_to_force

    def calculate_friction(self, mu):
        mu = uHf  # Look in constants.py
        return mu * self.mass * grav_accel

    def air_resistance(self, t):
        # Apply a force in the opposite direction to travel.
        coefficient = drag_coefficient  # Look in constants.py
        density = air_density  # Look in constants.py
        air_resistance = (coefficient * density * self.drag_area * (self.get_speed() ** 2)) / 2
        return air_resistance
