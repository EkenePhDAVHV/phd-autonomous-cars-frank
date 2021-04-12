# Imports
import os

import matplotlib.pyplot as plt
import numpy as np

from AVHV_Main import LayoutList
from AVHV_Main.Agents.Car import Car
from AVHV_Main.Agents.CarSpawner import CarSpawner
from AVHV_Main.Environment import Environment
from AVHV_Main.RoadSystem.RoadSystem import RoadSystem
from AVHV_Main.Simulator import Simulation
from AVHV_Main.Utilities.constants import drag_coefficient
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
    time_end=150.0,
    time_increment=.1,
    environment=Environment(
        name="Test collision",
        layout=layout
    ).add_objects([
        # non-priority lane
        CarSpawner(name="GentleCar", node=layout.get(RoadSystem).node(11),
                   route=[11, 12, 8, 9], direction=0,
                   car_ratio=15, file_path=file_path, file_names=file_names),
        CarSpawner(name="AggressiveCar", node=layout.get(RoadSystem).node(11),
                   route=[11, 12, 8, 9], direction=0,
                   car_ratio=1, file_path=file_path, file_names=file_names),
        CarSpawner(name="GentleCar", node=layout.get(RoadSystem).node(11),
                   route=[11, 12, 8, 9], direction=0,
                   car_ratio=10, file_path=file_path, file_names=file_names),
        CarSpawner(name="AggressiveCar", node=layout.get(RoadSystem).node(11),
                   route=[11, 12, 8, 9], direction=0,
                   car_ratio=1, file_path=file_path, file_names=file_names),
        CarSpawner(name="GentleCar", node=layout.get(RoadSystem).node(11),
                   route=[11, 12, 8, 9], direction=0,
                   car_ratio=10, file_path=file_path, file_names=file_names),
        CarSpawner(name="AggressiveCar", node=layout.get(RoadSystem).node(11),
                   route=[11, 12, 8, 9], direction=0,
                   car_ratio=1, file_path=file_path, file_names=file_names),
        CarSpawner(name="GentleCar", node=layout.get(RoadSystem).node(11),
                   route=[11, 12, 8, 9], direction=0,
                   car_ratio=12, file_path=file_path, file_names=file_names),

        # priority lane
        CarSpawner(name="GentleCar", node=layout.get(RoadSystem).node(7),
                   route=[7, 6, 8, 9], direction=0,
                   car_ratio=15, file_path=file_path, file_names=file_names),
        CarSpawner(name="AggressiveCar", node=layout.get(RoadSystem).node(7),
                   route=[7, 6, 8, 9], direction=0,
                   car_ratio=1, file_path=file_path, file_names=file_names),
        CarSpawner(name="GentleCar", node=layout.get(RoadSystem).node(7),
                   route=[7, 6, 8, 9], direction=0,
                   car_ratio=20, file_path=file_path, file_names=file_names),
        CarSpawner(name="AggressiveCar", node=layout.get(RoadSystem).node(7),
                   route=[7, 6, 8, 9], direction=0,
                   car_ratio=1, file_path=file_path, file_names=file_names),
        CarSpawner(name="GentleCar", node=layout.get(RoadSystem).node(7),
                   route=[7, 6, 8, 9], direction=0,
                   car_ratio=13, file_path=file_path, file_names=file_names),
    ]),
    file_path=file_path,
    file_names=file_names
)

cars = [car for car in simulation.environment.environment_objects[Car]]
plot_velocity_graph(cars, file_path=file_path,
                    current_file_name=current_file_name)
