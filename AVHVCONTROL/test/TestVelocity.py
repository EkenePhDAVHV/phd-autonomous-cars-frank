# Imports
import numpy as np

import unittest

import matplotlib.pyplot as plt
from AVHVCONTROL.Simulator import Simulation, Environment, Car, TrafficLight, Vector2
from AVHVCONTROL.test import LayoutList

from AVHVCONTROL.test.TestPhysics import PhyicsTest

# Instantiate the PhyicsTest Class and retrieve the position values returned from the testPhysics method
physicsTest = PhyicsTest()
position_vals = physicsTest.testPhysics()

# Create Simulation
simulation = Simulation(
    debugging=True,
    time_end=20.0,
    time_increment=.1,
    environment=Environment(
        name="Test collision",
        layout=LayoutList.cross_roads()
    ).add_objects([
        TrafficLight(name="Left Traffic Light   ", traffic_node=2, direction=0, timings=[4, 1], timer=0),
        TrafficLight(name="Right Traffic Light ", traffic_node=4, direction=0, timings=[4, 1], timer=0,
                     position=[+20, +40]),
        TrafficLight(name="Top eTraffic Light   ", traffic_node=6, direction=0, timings=[4, 1], timer=5,
                     position=[+80, -112]),
        TrafficLight(name="Bottom Traffic Light", traffic_node=8, direction=0, timings=[4, 1], timer=5,
                     position=[-60, -10]),
        Car(name="Car 1", route=[1, 2, 4, 5], direction=180, easy_physics=True, velocity=0, velocity_max=20,
            acceleration=0, acceleration_max=4, position=[0, 0]),
    ])
)

car = simulation.environment.environment_objects[Car][0]

# car.draw(canvas, 3)


# Get Velocities
time = car.data['time']
velocity = car.data['velocity']

# New Graph
plt.close()

# Graph Info
plt.title("Speed vs Time - First Car")
plt.ylabel('Speed (m/s)')
plt.xlabel('Time (s)')

# Extract Speed
speed = []
for v in velocity:
    if isinstance(v, Vector2):
        speed.append(v.magnitude())

# Plot
# plt.figure()
plt.plot(time, speed)

print(time)
print([v.x for v in velocity])


# Then graph
plt.show()