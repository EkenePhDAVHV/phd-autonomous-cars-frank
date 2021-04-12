# Objects
class Vehicle:
    def __init__(self, length):
        self.length = length
        self.acceleration_forwards = 0
        self.speed = 0
        self.direction = 0

    def change_accelleration(delta):
        self.acceleration_forwards += delta

    def change_velocity(delta):
        self.speed += delta
        if self.speed < 0:
            self.speed = 0

    def update(time):
        change_velocity(self.acceleration * time)


class Intersection:
    def __init__(self, a, b):
        self.a = a
        self.b = b


# RX
def RX(vehicle, intersection, methodval):
    # Return Distance
    return_distance = vehicle.length + (2 * intersection.a)

    # Calculate Deltas
    delta = 0
    if methodval == 0:
        delta = 4
    if methodval == 1:
        delta = 1 / math.sqrt(2)
    if methodval == 2:
        delta = 3 / math.sqrt(2)
    if methodval == 3:
        delta = 2
    if methodval == 4:
        delta = 1 / math.sqrt(2)
    if methodval == 5:
        delta = 1 + math.sqrt(5)

    # Return Values
    return return_distance + delta * intersection.b


def Risk(i, j, t):  # Vehicles I and J, T = Time
    H = 1


vehicle = Vehicle(12)
intersection = Intersection(3, 4)
Rvals = ["R0", "R1", "R2", "R\'0", "R\'1", "R\'2"]
for i in range(0, 6):
    print(str.format("{:s} = {:f}", Rvals[i], RX(vehicle, intersection, i)))

