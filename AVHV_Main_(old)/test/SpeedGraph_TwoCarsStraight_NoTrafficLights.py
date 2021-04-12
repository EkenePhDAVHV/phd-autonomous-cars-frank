# Imports
import unittest
import numpy as np
import matplotlib.pyplot as plt

from AVHV_Main.Vector2 import Vector2
from AVHV_Main.constants import *
from AVHV_Main.Environment import Environment
from AVHV_Main.test import LayoutList
from AVHV_Main.Car import Car
from AVHV_Main.Simulator import Simulation

from AVHV_Main.test.TestPhysics import *


# Create Simulation
simulation = Simulation(
    debugging=True,
    time_end=180.0,
    time_increment=.2,
    environment=Environment(
        name="Test collision",
        layout=LayoutList.cross_roads()
    ).add_objects([
        Car(name="Car 1", route=[1, 2, 4, 5], direction=0, easy_physics=True, velocity=0, velocity_max=max_velocity,
            acceleration=0, acceleration_max=max_acceleration, position=[0, 0]),
        Car(name="Car 2", route=[1, 2, 4, 5], direction=0, easy_physics=True, velocity=0, velocity_max=max_velocity + 10,
            acceleration=0, acceleration_max=max_acceleration, position=[0, 0], idle_time=10)
    ])
)

car = simulation.environment.environment_objects[Car][0]
car2 = simulation.environment.environment_objects[Car][1]

# car.draw(canvas, 3)


# Get Velocities
time = car.data['time']
velocity = car.data['velocity']

time2 = car2.data['time']
velocity2 = car2.data['velocity']

idle_time = car.idle_time

# Testing straight-curved-straight movement
# No output means assertion passed

# Get All Attributes of the car per time
time = car.data['time']
position = car.data['position']
velocity = car.data['velocity']
acceleration = car.data['acceleration']
nodes_left = car.data['nodes_left']
max_acceleration = car.max_acceleration
max_deceleration = car.max_deacceleration
mass = car.mass

time2 = car2.data['time']
position2 = car2.data['position']
velocity2 = car2.data['velocity']
acceleration2 = car2.data['acceleration']
nodes_left2 = car2.data['nodes_left']
max_acceleration2 = car2.max_acceleration
max_deceleration2 = car2.max_deacceleration
mass2 = car2.mass

# Extract Speed
speed = []
for v in velocity:
    if isinstance(v, Vector2):import unittest
import numpy as np
import matplotlib.pyplot as plt

from AVHV_Main.Vector2 import Vector2
from AVHV_Main.constants import *
from AVHV_Main.Environment import Environment
from AVHV_Main.test import LayoutList
from AVHV_Main.Car import Car
from AVHV_Main.Simulator import Simulation

from AVHV_Main.test.TestPhysics import *


# Create Simulation
simulation = Simulation(
    debugging=True,
    time_end=180.0,
    time_increment=.2,
    environment=Environment(
        name="Test collision",
        layout=LayoutList.cross_roads()
    ).add_objects([
        Car(name="Car 1", route=[1, 2, 4, 5], direction=0, easy_physics=True, velocity=0, velocity_max=max_velocity,
            acceleration=0, acceleration_max=max_acceleration, position=[0, 0]),
        Car(name="Car 2", route=[1, 2, 4, 5], direction=0, easy_physics=True, velocity=0, velocity_max=max_velocity + 10,
            acceleration=0, acceleration_max=max_acceleration, position=[0, 0], idle_time=10)
    ])
)

car = simulation.environment.environment_objects[Car][0]
car2 = simulation.environment.environment_objects[Car][1]

# car.draw(canvas, 3)


# Get Velocities
time = car.data['time']
velocity = car.data['velocity']

time2 = car2.data['time']
velocity2 = car2.data['velocity']

idle_time = car.idle_time

# Testing straight-curved-straight movement
# No output means assertion passed

# Get All Attributes of the car per time
time = car.data['time']
position = car.data['position']
velocity = car.data['velocity']
acceleration = car.data['acceleration']
nodes_left = car.data['nodes_left']
max_acceleration = car.max_acceleration
max_deceleration = car.max_deacceleration
mass = car.mass

time2 = car2.data['time']
position2 = car2.data['position']
velocity2 = car2.data['velocity']
acceleration2 = car2.data['acceleration']
nodes_left2 = car2.data['nodes_left']
max_acceleration2 = car2.max_acceleration
max_deceleration2 = car2.max_deacceleration
mass2 = car2.mass



speed.append(v.magnitude())

speed2 = []
for v in velocity2:
    if isinstance(v, Vector2):
        speed2.append(v.magnitude())

#  Testing using TestPhysics
physical_object = PhysicalObject()

#  Assign static values to physical_object
physical_object.max_acceleration = max_acceleration
physical_object.max_deacceleration = max_deceleration
physical_object.mass = mass
physical_object.drag = drag_coefficient

#  Testing using TestPhysics
physical_object2 = PhysicalObject()

#  Assign static values to physical_object
physical_object2.max_acceleration = max_acceleration
physical_object2.max_deacceleration = max_deceleration
physical_object2.mass = mass
physical_object2.drag = drag_coefficient

# Iterate through all attributes per time for a car object and print property values
# for i in range(0, len(car.data['time'])):
#     physical_object.pos[0] = float("{0:.2f}".format(position[i].get_value()[0]))
#     physical_object.pos[1] = float("{0:.2f}".format(position[i].get_value()[1]))
#
#     physical_object.velocity[0] = float("{0:.2f}".format(velocity[i].get_value()[0]))
#     physical_object.velocity[1] = float("{0:.2f}".format(velocity[i].get_value()[1]))
#
#     physical_object.acceleration[0] = float("{0:.2f}".format(acceleration[i].get_value()[0]))
#     physical_object.acceleration[1] = float("{0:.2f}".format(acceleration[i].get_value()[1]))
#
#     print(f'Car Object: {physical_object}, '
#           f'Speed: {physical_object.get_speed():.3f}m/s, '
#           f'Force: {physical_object.get_force():.3f}N')
#
# for i in range(0, len(car2.data['time'])):
#     physical_object2.pos[0] = float("{0:.2f}".format(position2[i].get_value()[0]))
#     physical_object2.pos[1] = float("{0:.2f}".format(position2[i].get_value()[1]))
#
#     physical_object2.velocity[0] = float("{0:.2f}".format(velocity2[i].get_value()[0]))
#     physical_object2.velocity[1] = float("{0:.2f}".format(velocity2[i].get_value()[1]))
#
#     physical_object2.acceleration[0] = float("{0:.2f}".format(acceleration2[i].get_value()[0]))
#     physical_object2.acceleration[1] = float("{0:.2f}".format(acceleration2[i].get_value()[1]))
#
#     print(f'Car Object 2: {physical_object2}, '
#           f'Speed: {physical_object2.get_speed():.3f}m/s, '
#           f'Force: {physical_object2.get_force():.3f}N')


# Assertion tests for position and speed of the car per time.
# first car
for i in range(0, len(car.data['time'])):
    pos = position[i].get_value()
    accel = acceleration[i].get_value()
    s = speed[i]
    n = nodes_left[i]
    t = simulation.time_increment
    physics_test = PhysicsTest('testMovement')
    # physics_test.testMovement(pos=pos, accel=accel, speed=s, t=t, easy_physics=car.easy_physics, nodes_left=n,
    #                           nth_time=i)

# second car
for i in range(0, len(car2.data['time'])):
    pos = position2[i].get_value()
    accel = acceleration2[i].get_value()
    s = speed2[i]
    n = nodes_left2[i]
    t = simulation.time_increment
    physics_test2 = PhysicsTest('testMovement')
    # physics_test2.testMovement(pos=pos, accel=accel, speed=s, t=t, easy_physics=car2.easy_physics, nodes_left=n,
    #                            nth_time=i)

time = np.array(time)

idle_time = car2.idle_time

# Plot
fig, ax = plt.subplots(figsize=(12, 6))
ax.set(xlabel='Time (s)', ylabel='Speed (m/s)', title='2 Cars in a straight line with a delay for second car')
ax.plot(time, speed)
ax.plot(time + idle_time, speed2)
ax.axis([0, simulation.time_end + 20, 0, car2.velocity_max + 10])
ax.margins(x=0.0, y=0.0, tight=False)

print(time)
print([v.x for v in velocity])

plt.show()
