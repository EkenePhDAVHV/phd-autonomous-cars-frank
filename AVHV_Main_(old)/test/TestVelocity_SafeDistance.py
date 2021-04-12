# Imports
import unittest
import math

import numpy as np
import matplotlib.pyplot as plt

from AVHV_Main.RoadSystem import RoadSystem
# from AVHV_Main.constants import *
# from AVHV_Main.Vector2 import Vector2
from AVHV_Main.Environment import Environment
from AVHV_Main.test import LayoutList
from AVHV_Main.TrafficLight import TrafficLight
from AVHV_Main.Car import Car
from AVHV_Main.CarSpawner import CarSpawner
from AVHV_Main.Simulator import Simulation

from AVHV_Main.test.TestPhysics import PhysicsTest

# Instantiate the PhyicsTest Class and retrieve the position values returned from the testPhysics method
physicsTest = PhysicsTest()
position_vals = physicsTest.testPhysics()

layout = LayoutList.cross_roads()

# Create Simulation
simulation = Simulation(
    debugging=True,
    time_end=60.0,
    time_increment=.2,
    environment=Environment(
        name="Test collision",
        layout=layout
    ).add_objects([
        TrafficLight(name="Left Traffic Light   ", traffic_node=2, direction=0, timings=[4, 1], timer=0,
                     position=[-20, +40]),
        TrafficLight(name="Right Traffic Light ", traffic_node=4, direction=0, timings=[4, 1], timer=0,
                     position=[+20, +40]),
        TrafficLight(name="Top eTraffic Light   ", traffic_node=6, direction=0, timings=[4, 1], timer=5,
                     position=[+80, -112]),
        TrafficLight(name="Bottom Traffic Light", traffic_node=8, direction=0, timings=[4, 1], timer=5,
                     position=[-60, -10]),
        CarSpawner(name="Car 1", node=layout.get(RoadSystem).node(1), route=[1, 2, 4, 5], direction=0, car_ratio=5)
    ])
)

cars = []
for car in simulation.environment.environment_objects[Car]:
    cars.append(car)

# Get Times and Velocities
times = []
velocities = []

for car in cars:
    times.append(car.data['time'])
    velocities.append(car.data['velocity'])

# Extract Speeds
speeds = []
speeds = [[v.magnitude() for v in velocity] for velocity in velocities]

print(times)
print(speeds)

axes = zip(times, speeds)

# Plot
fig, ax = plt.subplots(figsize=(12, 6))
ax.set(xlabel='Time (s)', ylabel='Speed (m/s)', title='Car movement with Safe Distance Model for ' + str(len(cars)) +
                                                      ' cars (Safe Distance = ' + str(cars[0].safe_distance) + ')')

for _ in axes:
    time, speed = _
    ax.plot(time, speed)

plt.show()
