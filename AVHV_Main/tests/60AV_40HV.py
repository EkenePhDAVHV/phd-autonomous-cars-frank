# Imports
import math
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from AVHV_Main.RoadSystem.RoadSystem import RoadSystem
# from AVHV_Main.constants import *
from AVHV_Main.Environment import Environment
from AVHV_Main.Utilities.constants import drag_coefficient
from AVHV_Main import LayoutList
from AVHV_Main.Agents.CarSpawner import CarSpawner
from AVHV_Main.Agents.Car import Car

from AVHV_Main.Simulator import Simulation

from AVHV_Main.tests.TestPhysics import PhysicsTest, PhysicalObject
from AVHV_Main.tests.plot_velocity_graph import plot_velocity_graph

layout = LayoutList.cross_roads()

# get basename
basename = os.path.basename(__file__)

# get filename without extension
current_file_name = os.path.splitext(basename)[0]

file_path = "../output/AVHV_Reservation_Nodes/"

file_names = ["av", "hv"]

for _file_path in [file_path]:
    if not os.path.isdir(_file_path):
        os.mkdir(_file_path)

    for file_name in file_names:
        with open(_file_path + file_name + ".csv", "w", encoding="utf8") as f:
            f.write(
                "car_name,speed,safe_distance,reaction_time,stopping_time\n")

# Create Simulation
simulation = Simulation(
    debugging=True,
    time_end=500.0,
    time_increment=.1,
    environment=Environment(
        name="Test collision",
        layout=layout
    ).add_objects([
        # non-priority lane
        CarSpawner(name="GentleCar", node=layout.get(RoadSystem).node(11), route=[11, 12, 8, 9], direction=0,
                   car_ratio=8, file_path=file_path, file_names=file_names),
        CarSpawner(name="AggressiveCar", node=layout.get(RoadSystem).node(11), route=[11, 12, 8, 9], direction=0,
                   car_ratio=8, file_path=file_path, file_names=file_names),
        CarSpawner(name="GentleCar", node=layout.get(RoadSystem).node(11), route=[11, 12, 8, 9], direction=0,
                   car_ratio=4, file_path=file_path, file_names=file_names),
        CarSpawner(name="AggressiveCar", node=layout.get(RoadSystem).node(11), route=[11, 12, 8, 9], direction=0,
                   car_ratio=8, file_path=file_path, file_names=file_names),
        CarSpawner(name="GentleCar", node=layout.get(RoadSystem).node(11), route=[11, 12, 8, 9], direction=0,
                   car_ratio=5, file_path=file_path, file_names=file_names),
        CarSpawner(name="AggressiveCar", node=layout.get(RoadSystem).node(11), route=[11, 12, 8, 9], direction=0,
                   car_ratio=8, file_path=file_path, file_names=file_names),
        CarSpawner(name="GentleCar", node=layout.get(RoadSystem).node(11), route=[11, 12, 8, 9], direction=0,
                   car_ratio=9, file_path=file_path, file_names=file_names),

        # priority lane
        CarSpawner(name="GentleCar", node=layout.get(RoadSystem).node(7), route=[7, 6, 8, 9], direction=0,
                   car_ratio=8, file_path=file_path, file_names=file_names),
        CarSpawner(name="AggressiveCar", node=layout.get(RoadSystem).node(7), route=[7, 6, 8, 9], direction=0,
                   car_ratio=8, file_path=file_path, file_names=file_names),
        CarSpawner(name="GentleCar", node=layout.get(RoadSystem).node(7), route=[7, 6, 8, 9], direction=0,
                   car_ratio=13, file_path=file_path, file_names=file_names),
        CarSpawner(name="AggressiveCar", node=layout.get(RoadSystem).node(7), route=[7, 6, 8, 9], direction=0,
                   car_ratio=8, file_path=file_path, file_names=file_names),
        CarSpawner(name="GentleCar", node=layout.get(RoadSystem).node(7), route=[7, 6, 8, 9], direction=0,
                   car_ratio=13, file_path=file_path, file_names=file_names),

        # CarSpawner(name="GentleCar", node=layout.get(RoadSystem).node(7), route=[11, 12, 8, 9], direction=0,
        #            car_ratio=2, file_path=file_path, file_names=file_names),

        # CarSpawner(name="GentleCar", node=layout.get(RoadSystem).node(7), route=[7, 6, 8, 9], direction=0,
        #            car_ratio=1, file_path=file_path, file_names=file_names),
    ]),
    file_path=file_path,
    file_names=file_names,
)

# car = simulation.environment.environment_objects[Car][0]
#
# # Get All Attributes of the car per time
# time = car.data['time']
# position = car.data['position']
# starting_pos = position[0].get_value()
# velocity = car.data['velocity']
# acceleration = car.data['acceleration']
# nodes_left = car.data['nodes_left']
# mass = car.mass
#
# # Extract Speed
# speed = []
# for v in velocity:
#     if isinstance(v, Vector2):
#         speed.append(v.magnitude())
#
# accel = []
# for a in acceleration:
#     if isinstance(a, Vector2):
#         accel.append(a.magnitude())
#
# fig, ax = plt.subplots(figsize=(12, 6))
# fig.canvas.set_window_title('SpeedGraph_Straight_No_TrafficLights_NoBraking')
# ax.set(xlabel='Time (s)', ylabel='Speed (m/s)', title='Speed vs Time - Straight Movement without traffic stops')
# ax.plot(time, speed)
# ax.axis([0, simulation.time_end + 10, 0, car.velocity_max + 10])
# ax.margins(x=0.0, y=0.0, tight=False)
#
# plt.show()
#
# fig, ax = plt.subplots(figsize=(12, 6))
# fig.canvas.set_window_title('SpeedGraph_Straight_No_TrafficLights_NoBraking')
# ax.set(xlabel='Time (s)', ylabel='Speed (m/s)', title='Speed vs Time - Straight Movement without traffic stops')
# ax.plot(time, accel)
# ax.axis([0, simulation.time_end + 10, 0, car.acceleration_max + 10])
# ax.margins(x=0.0, y=0.0, tight=False)
#
# plt.show()

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
                                  easy_physics=car.easy_physics, nodes_left=n, no_braking=True, nth_time=i + 1)

cars = [car for car in simulation.environment.environment_objects[Car]]
plot_velocity_graph(cars, file_path=file_path,
                    current_file_name=current_file_name)
