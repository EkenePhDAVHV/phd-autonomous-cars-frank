import os

import pickle

from AVHV_Main.Utilities.constants import *
from AVHV_Main.Agents.Car import Car
from AVHV_Main.Agents.CarSpawner import CarSpawner
from AVHV_Main.Environment import Environment
from AVHV_Main.LayoutList import cross_roads
from AVHV_Main.RoadSystem.RoadSystem import RoadSystem
from AVHV_Main.Simulator import Simulation
from AVHV_Main.tests.plot_velocity_graph import plot_velocity_graph

from AVHV_Main.tests.route_catalogue import *

from AVHV_Main.AVHV_TL.Car import Car as Car_TL
from AVHV_Main.AVHV_TL.Simulator import Simulation as Simulation_TL
from AVHV_Main.AVHV_TL.Environment import Environment as Environment_TL
from AVHV_Main.AVHV_TL.CarSpawner import CarSpawner as CarSpawner_TL
from AVHV_Main.AVHV_TL.RoadSystem import RoadSystem as RoadSystem_TL
from AVHV_Main.AVHV_TL.test.LayoutList import cross_roads as cross_roads_TL
from AVHV_Main.AVHV_TL.TrafficLight import TrafficLight as TrafficLight_TL

from AVHV_Main.AVHV_CAwSD4WI.Car import Car as Car_CAwSD4WI
from AVHV_Main.AVHV_CAwSD4WI.Simulator import Simulation as Simulation_CAwSD4WI
from AVHV_Main.AVHV_CAwSD4WI.Environment import Environment as \
    Environment_CAwSD4WI
from AVHV_Main.AVHV_CAwSD4WI.RoadSystem import RoadSystem as RoadSystem_CAwSD4WI
from AVHV_Main.AVHV_CAwSD4WI.CarSpawner import CarSpawner as CarSpawner_CAwSD4WI
from AVHV_Main.AVHV_CAwSD4WI.test.LayoutList import cross_roads as \
    cross_roads_CAwSD4WI


# get basename
basename = os.path.basename(__file__)

# get filename without extension
current_file_name = os.path.splitext(basename)[0]

output_path = "../output/experiment_results/"
file_path = "../output/experiment_results/AVHV_Reservation_Nodes/"
file_path_TL = "../output/experiment_results/AVHV_Traffic_Lights/"
file_path_CAwSD4WI = "../output/experiment_results/AVHV_CAwSD4WI/"

file_names = ["av", "hv"]

for _file_path in [file_path, file_path_TL, file_path_CAwSD4WI]:
    if not os.path.isdir(_file_path):
        os.mkdir(_file_path)

    for file_name in file_names:
        with open(_file_path + file_name + ".csv", "w", encoding="utf8") as f:
            f.write(
                "car_name,speed,safe_distance,reaction_time,time\n")


state_files = [os.path.dirname(
            os.path.realpath(__file__)) + "/" + "tl_result_values.pickle",
               os.path.dirname(
            os.path.realpath(__file__)) + "/" + "cawsd4wi_result_values.pickle",
                os.path.dirname(
            os.path.realpath(__file__)) + "/" + "rn_result_values.pickle"
               ]

occupancy_matrix_folder = "../output/occupancy_matrix/"
if not os.path.isdir(occupancy_matrix_folder):
    os.mkdir(occupancy_matrix_folder)

with open(occupancy_matrix_folder + "occupancy_matrix_results.csv", "w", encoding="utf8") as f:
    f.write("s_no, AV_Ratio, HV_Ratio, Occupancy_Time_secs")

layout_TL = cross_roads_TL()
layout_CAwSD4WI = cross_roads_CAwSD4WI()
layout = cross_roads()


def starting_node_TL(node):
    return layout_TL.get(RoadSystem_TL).node(node)


def starting_node_CAwSD4WI(node):
    return layout_CAwSD4WI.get(RoadSystem_CAwSD4WI).node(node)


def starting_node(node):
    return layout.get(RoadSystem).node(node)


# Create Simulation
def run_simulation():

    if not os.path.exists(state_files[0]):

        car_spawner_objs = [
                CarSpawner_TL(name=item[0], node=starting_node_TL(item[1][0]),
                              route=item[1], direction=0, car_ratio=item[2],
                              file_path=file_path_TL,
                              file_names=["av", "hv"]) for
                item in cars_per_route]

        environment_TL = Environment_TL(
            name="Test collision",
            layout=layout_TL
        )

        environment_TL.add_objects(car_spawner_objs)
        environment_TL.add_objects([
                TrafficLight_TL(name="Top Traffic Light", traffic_node=18,
                                direction=0, timings=[50, 1], timer=50,
                                position=[+30, -50]),
                TrafficLight_TL(name="Left Traffic Light", traffic_node=12,
                                direction=270, timings=[50, 1], timer=100,
                                position=[-20, -50]),
                TrafficLight_TL(name="Right Traffic Light", traffic_node=4,
                                direction=90, timings=[50, 1], timer=100,
                                position=[+20, +50]),
                TrafficLight_TL(name="Bottom Traffic Light", traffic_node=6,
                                direction=180, timings=[50, 1], timer=50,
                                position=[-30, +50])
        ])

        simulation_TL = Simulation_TL(
            debugging=True,
            time_end=simulation_time,
            time_increment=sim_time_increment,
            environment=environment_TL,
            file_path=file_path_TL,
            file_names=file_names,
            active_routes=routes
        )

        cars_TL = [car for car in
                   simulation_TL.environment.environment_objects[Car_TL]]
        plot_velocity_graph(cars_TL, file_path=file_path_TL,
                            current_file_name=current_file_name)

        del cars_TL
        simulation_TL_experiment_values = simulation_TL.experiment_values

        with open(state_files[0], 'wb') as g:
            pickle.dump(simulation_TL.experiment_values, g)

        del simulation_TL
    else:
        with open(state_files[0], 'rb') as g:
            simulation_TL_experiment_values = pickle.load(g)

    if not os.path.exists(state_files[1]):

        simulation_CAwSD4WI = Simulation_CAwSD4WI(
            debugging=True,
            time_end=simulation_time,
            time_increment=sim_time_increment,
            environment=Environment_CAwSD4WI(
                name="Test collision",
                layout=layout_CAwSD4WI
            ).add_objects([
                CarSpawner_CAwSD4WI(name=item[0],
                                    node=starting_node_CAwSD4WI(item[1][0]),
                                    route=item[1], direction=0, car_ratio=item[2],
                                    file_path=file_path_CAwSD4WI,
                                    file_names=["av", "hv"]) for
                item in cars_per_route]
            ),
            file_path=file_path_CAwSD4WI,
            file_names=file_names,
            active_routes=routes
        )

        cars_CAwSD4WI = [car for car in
                         simulation_CAwSD4WI.environment.environment_objects[
                             Car_CAwSD4WI]]
        plot_velocity_graph(cars_CAwSD4WI, file_path=file_path_CAwSD4WI,
                            current_file_name=current_file_name)

        del cars_CAwSD4WI
        simulation_CAwSD4WI_experiment_values = \
            simulation_CAwSD4WI.experiment_values

        with open(state_files[1], 'wb') as g:
            pickle.dump(simulation_CAwSD4WI.experiment_values, g)

        del simulation_CAwSD4WI
    else:
        with open(state_files[1], 'rb') as g:
            simulation_CAwSD4WI_experiment_values = pickle.load(g)

    simulation = Simulation(
        debugging=False,
        time_end=simulation_time,
        time_increment=sim_time_increment,
        environment=Environment(
            name="Test collision",
            layout=layout
        ).add_objects([
            CarSpawner(name=item[0], node=starting_node(item[1][0]),
                       route=item[1], direction=0, car_ratio=item[2],
                       file_path=file_path,
                       file_names=["av", "hv"]) for
            item in cars_per_route]
            # CarSpawner(name="AggressiveCar", node=layout.get(RoadSystem).node(11),
            #            route=[7, 6, 2, 1], direction=0,
            #            car_ratio=4, file_path=file_path, file_names=file_names)]
        ),
        file_path=file_path,
        output_path=file_path,
        file_names=file_names,
        active_routes=routes,
        simulation_TL_values=simulation_TL_experiment_values,
        simulation_CAwSD4WI_values=simulation_CAwSD4WI_experiment_values,
        file_path_TL=file_path_TL,
        file_path_CAwSD4WI=file_path_CAwSD4WI
    )

    cars = [car for car in simulation.environment.environment_objects[Car]]
    plot_velocity_graph(cars, file_path=file_path,
                        current_file_name=current_file_name)

    del cars
    del simulation

    if os.path.exists(state_files[0]):
        os.remove(state_files[0])
    if os.path.exists(state_files[1]):
        os.remove(state_files[1])


run_simulation()

# first_ratio()