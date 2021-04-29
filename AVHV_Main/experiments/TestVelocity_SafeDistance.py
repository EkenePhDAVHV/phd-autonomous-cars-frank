# Imports
import os

from AVHV_Main import LayoutList
from AVHV_Main.Agents.Car import Car
from AVHV_Main.Agents.CarSpawner import CarSpawner
from AVHV_Main.Environment import Environment
from AVHV_Main.RoadSystem.RoadSystem import RoadSystem
from AVHV_Main.Simulator import Simulation

# get basename
from AVHV_Main.tests.plot_velocity_graph import plot_velocity_graph

basename = os.path.basename(__file__)

# get filename without extension
current_file_name = os.path.splitext(basename)[0]

file_path = "../output/experiment_results/"

layout = LayoutList.cross_roads()

# Create Simulation
simulation = Simulation(
    debugging=False,
    time_end=60.0,
    time_increment=.2,
    environment=Environment(
        name="Test collision",
        layout=layout
    ).add_objects([
        CarSpawner(name="Car 1", node=layout.get(RoadSystem).node(1),
                   route=[1, 2, 4, 5], direction=0, car_ratio=5,
                   file_path=file_path)
    ]),
    file_path=file_path
)

cars = [car for car in simulation.environment.environment_objects[Car]]
plot_velocity_graph(cars, file_path=file_path,
                    current_file_name=current_file_name)
