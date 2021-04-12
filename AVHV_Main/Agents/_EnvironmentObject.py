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

        if self.is_decelerating:
            self.velocity.add_self(self.acceleration.copy().scale(t))

        self.velocity.cap_self(max_velocity)
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

    def apply_force(self, t, magnitude, direction=None):
        """Applies force in a direction (changed from Degrees to Radians)"""

        if direction is None:
            direction = self.direction

        acceleration_due_to_force = Vector2(magnitude /
                                            self.mass).redirect_self(
            direction).round_to(2)

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
