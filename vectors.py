
class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def multiply_x_and_y(self):
        return self.x * self.y

    def addition(self, x, y):
        return x + y


position = Vector2(2,3)
print(position.x)
print(position.y)
print(position.x * position.y)
print(position.x * position.y)
print(position.multiply_x_and_y())
print(position.addition(5,6))