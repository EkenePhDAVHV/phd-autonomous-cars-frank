# Imports
import os

from AVHV_Main import LayoutList
from AVHV_Main.Agents.Car import Car
from AVHV_Main.Environment import Environment
from AVHV_Main.Simulator import Simulation

from AVHV_Main.tests.plot_velocity_graph import plot_velocity_graph

# get basename
basename = os.path.basename(__file__)

# get filename without extension
current_file_name = os.path.splitext(basename)[0]

file_path = "../output/AVHV_Reservation_Nodes/"

# Create Simulation
simulation = Simulation(
    debugging=False,
    time_end=50.0,
    time_increment=0.1,
    environment=Environment(
        name="Test collision",
        layout=LayoutList.cross_roads()
    ).add_objects([
        Car(name="Car 1", route=[1, 2, 6, 7], direction=0, velocity=0,
            acceleration=0, position=[0, 0], file_path=file_path)
    ]),
    file_path=file_path,
)

cars = [car for car in simulation.environment.environment_objects[Car]]
plot_velocity_graph(cars, file_path=file_path,
                    current_file_name=current_file_name)
