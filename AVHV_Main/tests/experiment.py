# Imports
import math

import numpy as np
import matplotlib.pyplot as plt

from AVHV_Main.RoadSystem import RoadSystem
# from AVHV_Main.constants import *
from AVHV_Main.Environment import Environment
from AVHV_Main.constants import drag_coefficient
from AVHV_Main.test import LayoutList
from AVHV_Main.CarSpawner import CarSpawner
from AVHV_Main.Car import Car

from AVHV_Main.Simulator import Simulation

from AVHV_Main.test.TestPhysics import PhysicsTest, PhysicalObject

layout = LayoutList.cross_roads()

# Create Simulation
simulation = Simulation(
    debugging=True,
    time_end=300.0,
    time_increment=.1,
    environment=Environment(
        name="Test collision",
        layout=layout
    ).add_objects([
        CarSpawner(name="GentleCar", node=layout.get(RoadSystem).node(11), route=[11, 12, 8, 9], direction=0,
                   car_ratio=500),
        CarSpawner(name="GentleCar", node=layout.get(RoadSystem).node(11), route=[7, 6, 8, 9], direction=0,
                   car_ratio=500),
    ])
)

cars = []
for car in simulation.environment.environment_objects[Car]:
    cars.append(car)

# Get All Attributes of all cars per time
time = []
velocity = []
position = []
starting_pos = []
acceleration = []
nodes_left = []
max_acceleration = []
max_deceleration = []
mass = []

for car in cars:
    time.append(car.data['time'])
    velocity.append(car.data['velocity'])
    position.append(car.data['position'])
    starting_pos.append(car.data['position'][0].get_value())
    acceleration.append(car.data['acceleration'])
    nodes_left.append(car.data['nodes_left'])
    max_acceleration.append(car.max_acceleration)
    max_deceleration.append(car.max_deacceleration)
    mass.append(car.mass)

# Extract Speeds
speed = []
speed = [[v.magnitude() for v in vel] for vel in velocity]


#  Testing using TestPhysics
physical_objects = []
for car in cars:
    physical_object = (PhysicalObject())

    #  Assign static values to physical_object
    physical_object.mass = mass[cars.index(car)]
    physical_object.drag = drag_coefficient

    # append to list
    physical_objects.append(physical_object)

# Assertion tests for position and speed of the car per time.
for car in cars:
    index = cars.index(car)  # get the index for the current car object
    for i in range(0, len(car.data['time'])):
        pos = position[index][i].get_value()
        accel = acceleration[index][i].get_value()
        s = speed[index][i]
        n = nodes_left[index][i]
        t = simulation.time_increment
        mass = car.mass
        physics_test = PhysicsTest('testMovement')
        physics_test.testMovement(starting_pos=starting_pos, pos=pos, accel=accel, speed=s, t=t,
                                  easy_physics=car.easy_physics, nodes_left=n, no_braking=True, nth_time=i+1)
