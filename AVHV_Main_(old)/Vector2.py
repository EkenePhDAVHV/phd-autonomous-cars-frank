import math
from copy import copy


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
        return math.sqrt(self.x ** 2 + self.y ** 2)

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
        return self.distance(Vector2([0, 0]))

    def redirect(self, angle):
        vector = self.copy()
        angle = math.radians(angle)
        magnitude = self.distance(Vector2([0, 0]))
        vector.x = magnitude * math.sin(angle)
        vector.y = magnitude * math.cos(angle)
        return vector

    def redirect_self(self, angle):
        vector = self.redirect(angle)
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
