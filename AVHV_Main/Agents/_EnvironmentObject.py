import math
from copy import copy

from svgwrite import Drawing
from svgwrite.shapes import *

from AVHV_Main.Utilities.Vector2 import Vector2
from AVHV_Main.Utilities.constants import *


class EnvironmentObject:

    def __init__(self, name, position=None, velocity=None, acceleration=None,
                 direction=None, size=10, mass=None, color=None,
                 car_ratio=None, should_accelerate=True):
        """Initialize Default Values"""

        if not isinstance(name, str):
            name = str(name)
        if not isinstance(direction, int) and not isinstance(direction, float):
            self.direction = 0
        if not isinstance(mass, int) and not isinstance(mass, float):
            mass = 1200
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

        self.car_ratio = car_ratio if car_ratio is not None else 0
        self.total_cars = round(self.car_ratio * AVHV_total_cars / 100)

        self.total_cars_percent = 100
        self.last = None
        self.turn_velocity_reached = False

        self.environment = None

        self.checked_polarity_x = False
        self.checked_polarity_y = False
        self.polarity_x = None
        self.polarity_y = None

        self.has_reached_destination = False
        self.has_recorded_last_values = False

        self.should_accelerate = should_accelerate
        self.is_decelerating = False

        self.has_set_initial_values = False
        self.angle = 0.0
        self.start_position_x = 0.0
        self.start_position_y = 0.0

        self.current_time = 0.0

        self.data = {}
        for metric in ('time', 'position', 'velocity', 'acceleration',
                       'speed', 'direction', 'nodes_left'):
            self.data[metric] = []

    def __str__(self):
        """Returns a string representation of the object when it is printed"""

        return f"Name: {self.name}\n" \
               f"Position: {self.position}\n" \
               f"Mass: {self.mass}\n" \
               f"Velocity: {self.velocity}"

    def set_environment(self, environment):
        """Sets environment"""

        self.environment = environment

    def behaviour_update(self, t):
        pass

    def physics_update(self, t):
        """Updates object's acceleration, velocity and position"""

        if self.velocity.magnitude() > max_velocity:
            pass
        else:
            if self.should_accelerate:
                self.velocity.add_self(self.acceleration.copy().scale(t))

        if not self.checked_polarity_x:
            if self.velocity.x < 0.0:
                self.polarity_x = "-"
            elif self.velocity.x > 0.0:
                self.polarity_x = "+"
            else:
                self.polarity_x = None

            if self.polarity_x is not None:
                self.checked_polarity_x = True

        if not self.checked_polarity_y:
            if self.velocity.y < 0.0:
                self.polarity_y = "-"
            elif self.velocity.y > 0.0:
                self.polarity_y = "+"
            else:
                self.polarity_y = None

            if self.polarity_y is not None:
                self.checked_polarity_y = True

        # if self.is_decelerating:
        #     if self.velocity.y < 0.0:
        #         self.velocity.y -= self.acceleration.y * t
        #     if self.velocity.x < 0.0:
        #         self.velocity.x -= self.acceleration.x * t
        #     if self.velocity.y > 0.0:
        #         self.velocity.y -= self.acceleration.y * t
        #     if self.velocity.x > 0.0:
        #         self.velocity.x -= self.acceleration.x * t

        self.velocity.add_self(self.acceleration.copy().scale(t))

        if self.checked_polarity_x:
            if self.velocity.x < 0.0 and self.polarity_x == "+":
                self.velocity.x = 0.0
            if self.velocity.x > 0.0 and self.polarity_x == "-":
                self.velocity.x = 0.0

        if self.checked_polarity_y:
            if self.velocity.y < 0.0 and self.polarity_y == "+":
                self.velocity.y = 0.0
            if self.velocity.y > 0.0 and self.polarity_y == "-":
                self.velocity.y = 0.0

        # self.velocity.cap_self(max_velocity)
        self.velocity.round_to_self(2)

        self.position.add_self(self.velocity.copy().scale(t))

    def update_records(self, t):
        """Update records."""

        self.data['time'].append(copy(t))
        self.data['position'].append(self.position.copy())
        self.data['velocity'].append(self.velocity.copy())
        self.data['acceleration'].append(self.acceleration.copy())
        self.data['direction'].append(self.direction)

    def data_update(self, t):
        """Records parameters of the object."""

        self.update_records(t)

    def update(self, t, record=True):
        """Updates the objects physics and behaviour"""

        self.behaviour_update(t)
        self.physics_update(t)
        self.current_time += t
        self.current_time = round(self.current_time, 1)

        if record:
            self.data_update(t)

    def get_speed(self):
        """Returns the absolute speed in m/s"""

        return math.sqrt(self.velocity.x ** 2 + self.velocity.y ** 2)

    def get_force(self):
        """Returns the force in N (F=ma)"""

        return self.mass * math.sqrt(self.acceleration.x ** 2 +
                                     self.acceleration.y ** 2)

    def get_info(self):
        """Returns information about the object"""

        return self.__str__()

    def is_colliding(self, colliding_object):
        """This method checks if this object and the other object
        overlaps/collide, which could mean a crash for cars and other
        environment objects."""

        # Check the left side
        if colliding_object.position.x + colliding_object.size.x < \
                self.position.x:
            return False

        # Check the bottom side
        if colliding_object.position.y + colliding_object.size.y < \
                self.position.y:
            return False

        # Check the right side
        if self.position.x + self.size.x < colliding_object.position.x:
            return False

        # Crop the top side
        if self.position.y + self.size.y < colliding_object.position.y:
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
                end=(self.position.x + math.sin(math.radians(self.direction))
                     * 600,
                     self.position.y + math.cos(math.radians(self.direction))
                     * 600),
                fill='red',
                stroke_width=200
            ))

    def apply_force(self, t, magnitude, is_around_curve=True, direction=None):
        """Applies force in a direction (changed from Degrees to Radians)"""

        # print(self.direction)

        if direction is None:
            direction = self.direction

        acceleration_due_to_force = Vector2(magnitude /
                                            self.mass).redirect_self(
            direction).round_to(2)

        center_of_rotation_x = -30 / 2
        center_of_rotation_y = 30 / 2
        radius = 50
        omega = 0.1  # Angular velocity

        # if is_around_curve:
        # if not self.has_set_initial_values:
        #     self.angle = math.radians(0)  # Starting angle
        #     self.position.x = self.position.x + radius * math.cos(self.angle)  # Starting position x
        #     self.position.y = self.position.y - radius * math.sin(self.angle)  # Starting position y
        #     self.has_set_initial_values = True
        # else:
        #     self.angle = self.angle + omega  # New angle, we add angular velocity
        #     self.position.x = (self.position.x + radius * omega * math.cos(self.angle + math.pi / 2)) / 10  # New x
        #     self.position.y = (self.position.y - radius * omega * math.sin(self.angle + math.pi / 2)) / 10  # New y
        #     print(self.acceleration.x, self.acceleration.y)
        # else:

        self.is_decelerating = False
        self.acceleration = acceleration_due_to_force.copy()

    def decelerate(self, t, magnitude=braking_force, limit=0, direction=None):
        """Applies deceleration force in a direction (changed from Degrees
        to Radians)"""

        if direction is None:
            direction = self.direction

        acceleration_due_to_force = Vector2(magnitude /
                                            self.mass).redirect_self(
            direction).round_to(2)

        if self.velocity.magnitude() > limit:
            acceleration_due_to_force.x = -acceleration_due_to_force.x
            acceleration_due_to_force.y = -acceleration_due_to_force.y

            self.is_decelerating = True
            self.acceleration = acceleration_due_to_force.copy()
