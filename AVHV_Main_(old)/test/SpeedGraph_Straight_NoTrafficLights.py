# Imports
import unittest
import matplotlib.pyplot as plt

from AVHV_Main.Vector2 import Vector2
from AVHV_Main.constants import *
from AVHV_Main.Environment import Environment
from AVHV_Main.test import LayoutList
from AVHV_Main.Car import Car
from AVHV_Main.Simulator import Simulation

from AVHV_Main.test.TestPhysics import *

increment=.2,
    environment=Environment(
        name="Test collision",
        layout=LayoutList.cross_roads()
    ).add_objects([
        Car(name="Car 1", route=[1, 2, 4, 5], direction=0, easy_physics=True, velocity=0, velocity_max=max_velocity,
            acceleration=0, acceleration_max=max_acceleration, position=[0, 0]),
    ])
)

car = simulation.environment.environment_objects[Car][0]

# Get Velocities
time = car.data['time']
velocity = car.data['velocity']


# Testing straight-curved-straight movement
# No output means assertion passed
# physics_test1 = PhysicsTest('testMovement1')
# physics_test1.testMovement1()
#
# physics_test2 = PhysicsTest('testMovement2')
# physics_test2.testMovement2()
#
# physics_test3 = PhysicsTest('testMovement3')
# physics_test3.testMovement3()
#
# physics_test4 = PhysicsTest('testCurveRight')
# physics_test4.testCurveRight()
#
# physics_test5 = PhysicsTest('testRouting')
# physics_test5.testRouting()
#
# physics_test6 = PhysicsTest('testPhysics')
# physics_test6.testPhysics()


# Get All Attributes of the car per time
time = car.data['time']
position = car.data['position']
velocity = car.data['velocity']
acceleration = car.data['acceleration']
nodes_left = car.data['nodes_left']
mass = car.mass

# Extract Speed
speed = []
for v in velocity:
    if isinstance(v, Vector2):
        speed.append(v.magnitude())

#  Testing using TestPhysics
physical_object = PhysicalObject()

#  Assign static values to physical_object
physical_object.mass = mass
physical_object.drag = drag_coefficient


for i in range(0, len(car.data['time'])):
    physical_object.pos[0] = float("{0:.2f}".format(position[i].get_value()[0]))
    physical_object.pos[1] = float("{0:.2f}".format(position[i].get_value()[1]))

    physical_object.velocity[0] = float("{0:.9f}".format(velocity[i].get_value()[0]))
    physical_object.velocity[1] = float("{0:.9f}".format(velocity[i].get_value()[1]))

    physical_object.acceleration[0] = float("{0:.2f}".format(acceleration[i].get_value()[0]))
    physical_object.acceleration[1] = float("{0:.2f}".format(acceleration[i].get_value()[1]))

    print(f'Car Object: {physical_object}, '
          f'Speed: {physical_object.get_speed():.9f}m/s, '
          f'Force: {physical_object.get_force():.3f}N')


# Assertion tests for position and speed of the car per time.
for i in range(0, len(car.data['time'])):
    pos = position[i].get_value()
    accel = acceleration[i].get_value()
    s = speed[i]
    n = nodes_left[i]
    t = simulation.time_increment
    mass = car.mass
    physics_test = PhysicsTest('testMovement')
    # physics_test.testMovement(pos=pos, accel=accel, speed=s, t=t, easy_physics=car.easy_physics, nodes_left=n,
    #                           nth_time=i+1)


# Plot
fig, ax = plt.subplots(figsize=(12, 6))
ax.set(xlabel='Time (s)', ylabel='Speed (m/s)', title='Speed vs Time - Movement without traffic stops')
ax.plot(time, speed)
ax.axis([0, simulation.time_end + 20, 0, car.velocity_max + 10])
ax.margins(x=0.0, y=0.0, tight=False)

print(len(time))
print(len([v.x for v in velocity]))
print(len(speed))
# print(speed[92])

plt.show()
