import os
import pickle

from AVHV_Main.Utilities.constants import *

# Get the random routes, cars and car spawners.
from AVHV_Main.experiments.route_chooser import *

from AVHV_Main.StatisticsReporter.Plotter import StandardPlotter, \
    OccupancyMatrixPlotter

# Modules for the Traffic Light experiment.
from AVHV_Main.AVHV_TL.Car import Car as Car_TL
from AVHV_Main.AVHV_TL.Simulator import Simulation as Simulation_TL
from AVHV_Main.AVHV_TL.Environment import Environment as Environment_TL
from AVHV_Main.AVHV_TL.CarSpawner import CarSpawner as CarSpawner_TL
from AVHV_Main.AVHV_TL.RoadSystem import RoadSystem as RoadSystem_TL
from AVHV_Main.AVHV_TL.test.LayoutList import cross_roads as cross_roads_TL
from AVHV_Main.AVHV_TL.TrafficLight import TrafficLight as TrafficLight_TL

# Modules for the Collision Avoidance with Safe Distance and 4 Way Intersection 
# experiment.
from AVHV_Main.AVHV_CAwSD4WI.Car import Car as Car_CAwSD4WI
from AVHV_Main.AVHV_CAwSD4WI.Simulator import Simulation as Simulation_CAwSD4WI
from AVHV_Main.AVHV_CAwSD4WI.Environment import Environment as \
    Environment_CAwSD4WI
from AVHV_Main.AVHV_CAwSD4WI.RoadSystem import RoadSystem as RoadSystem_CAwSD4WI
from AVHV_Main.AVHV_CAwSD4WI.CarSpawner import CarSpawner as CarSpawner_CAwSD4WI
from AVHV_Main.AVHV_CAwSD4WI.test.LayoutList import cross_roads as \
    cross_roads_CAwSD4WI

# Modules for the Reservation Node experiment.
from AVHV_Main.Agents.Car import Car
from AVHV_Main.Agents.CarSpawner import CarSpawner
from AVHV_Main.Environment import Environment
from AVHV_Main.LayoutList import cross_roads
from AVHV_Main.RoadSystem.RoadSystem import RoadSystem
from AVHV_Main.Simulator import Simulation
from AVHV_Main.experiments.plot_velocity_graph import plot_velocity_graph

cars_per_route_standard = choose_standard_experiments_routes()
cars_per_route_ratio_list = choose_ratioed_experiments_routes()

output_path = "../output/"
experiment_results_path = "../output/experiment_results/"
experiment_summary_path = "../output/experiment_results/experiment_summary/"
file_path = "../output/experiment_results/AVHV_Reservation_Nodes/"
file_path_TL = "../output/experiment_results/AVHV_Traffic_Lights/"
file_path_CAwSD4WI = "../output/experiment_results/AVHV_CAwSD4WI/"

file_names = ["av", "hv"]

for _file_path in [output_path, experiment_results_path,
                   experiment_summary_path]:
    if not os.path.isdir(_file_path):
        os.mkdir(_file_path)

for _file_path in [file_path, file_path_TL, file_path_CAwSD4WI]:
    if not os.path.isdir(_file_path):
        os.mkdir(_file_path)

    for file_name in file_names:
        with open(_file_path + file_name + ".csv", "w", encoding="utf8") as f:
            f.write(
                "car_name,speed,safe_distance,reaction_time,time\n")

state_files = [
    os.path.dirname(os.path.realpath(__file__)) + "/" +
    "tl_result_values.pickle",
    os.path.dirname(os.path.realpath(__file__)) + "/"
    + "cawsd4wi_result_values.pickle"
]

layout_TL = cross_roads_TL()
layout_CAwSD4WI = cross_roads_CAwSD4WI()
layout = cross_roads()


def starting_node_TL(node):
    return layout_TL.get(RoadSystem_TL).node(node)


def starting_node_CAwSD4WI(node):
    return layout_CAwSD4WI.get(RoadSystem_CAwSD4WI).node(node)


def starting_node(node):
    return layout.get(RoadSystem).node(node)


# Run the standard experiments.
def run_standard_experiments():
    if not os.path.exists(state_files[0]):

        car_spawner_objs = [
            CarSpawner_TL(name=item[0], node=starting_node_TL(item[1][0]),
                          route=item[1], velocity=10, direction=0,
                          car_ratio=item[2], file_path=file_path_TL,
                          file_names=["av", "hv"]) for
            item in cars_per_route_standard]

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
        plot_velocity_graph(cars_TL, file_path=file_path_TL)

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
                                    route=item[1], velocity=10, direction=0,
                                    car_ratio=item[2],
                                    file_path=file_path_CAwSD4WI,
                                    file_names=["av", "hv"]) for
                item in cars_per_route_standard]
            ),
            file_path=file_path_CAwSD4WI,
            file_names=file_names,
            active_routes=routes
        )

        cars_CAwSD4WI = [car for car in
                         simulation_CAwSD4WI.environment.environment_objects[
                             Car_CAwSD4WI]]
        plot_velocity_graph(cars_CAwSD4WI, file_path=file_path_CAwSD4WI)

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
                       route=item[1], velocity=10, direction=0, car_ratio=item[2],
                       file_path=file_path, file_names=["av", "hv"]) for
            item in cars_per_route_standard]
        ),
        file_path=file_path,
        experiment_results_path=experiment_results_path,
        active_routes=routes,
        simulation_TL_values=simulation_TL_experiment_values,
        simulation_CAwSD4WI_values=simulation_CAwSD4WI_experiment_values,
        file_path_TL=file_path_TL,
        file_path_CAwSD4WI=file_path_CAwSD4WI
    )

    simulation_experiment_values = simulation.experiment_values

    cars = [car for car in simulation.environment.environment_objects[Car]]
    try:
        plot_velocity_graph(cars, file_path=file_path)
    except Exception as e:
        print(e)

    standard_plotter = StandardPlotter(
        experiment_results_path,
        file_path,
        [simulation_TL_experiment_values[8],
         simulation_CAwSD4WI_experiment_values[8],
         simulation_experiment_values[8]],
        [simulation_TL_experiment_values[9],
         simulation_CAwSD4WI_experiment_values[9],
         simulation_experiment_values[9]
         ],
        [simulation_TL_experiment_values[10],
         simulation_CAwSD4WI_experiment_values[10],
         simulation_experiment_values[10]
         ],
        [simulation_TL_experiment_values[11],
         simulation_CAwSD4WI_experiment_values[11],
         simulation_experiment_values[11]
         ],
        [simulation_TL_experiment_values[12],
         simulation_CAwSD4WI_experiment_values[12],
         simulation_experiment_values[12]
         ],
        [simulation_TL_experiment_values[13],
         simulation_CAwSD4WI_experiment_values[13],
         simulation_experiment_values[13]
         ],
        [simulation_TL_experiment_values[14],
         simulation_CAwSD4WI_experiment_values[14],
         simulation_experiment_values[14]],
        [simulation.num_of_all_cars,
         simulation.num_av,
         simulation.num_hv]
    )

    standard_plotter.plot()

    del cars
    del simulation_TL_experiment_values
    del simulation_CAwSD4WI_experiment_values
    del simulation

    if os.path.exists(state_files[0]):
        os.remove(state_files[0])
    if os.path.exists(state_files[1]):
        os.remove(state_files[1])


# Run the standard experiments with ratios.
def run_ratio_experiments():
    with open(experiment_results_path + "occupancy_matrix_results.csv", "w",
              encoding="utf8") as h:
        h.write("s_no, AV_Ratio, HV_Ratio, TL_Occupancy_Time_secs, "
                "CAwSD4WI_Occupancy_Time_secs, RN_Occupancy_Time_secs\n")

    # Set ratios for incrementing and decrementing before writing to file.
    AV_ratio = 100
    HV_ratio = 0

    for cars_per_route in cars_per_route_ratio_list:
        car_spawner_objs = [
            CarSpawner_TL(name=item[0], node=starting_node_TL(item[1][0]),
                          route=item[1], velocity=10, direction=0,
                          car_ratio=item[2], file_path=file_path_TL,
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
            time_end=ratio_simulation_time,
            time_increment=ratio_sim_time_increment,
            environment=environment_TL,
            active_routes=routes,
            is_running_ratio=True,
            _ratio=(AV_ratio, HV_ratio)
        )

        simulation_CAwSD4WI = Simulation_CAwSD4WI(
            debugging=True,
            time_end=ratio_simulation_time,
            time_increment=ratio_sim_time_increment,
            environment=Environment_CAwSD4WI(
                name="Test collision",
                layout=layout_CAwSD4WI
            ).add_objects([
                CarSpawner_CAwSD4WI(name=item[0],
                                    node=starting_node_CAwSD4WI(item[1][0]),
                                    route=item[1], velocity=10, direction=0,
                                    car_ratio=item[2],
                                    file_path=file_path_CAwSD4WI,
                                    file_names=["av", "hv"]) for
                item in cars_per_route]
            ),
            active_routes=routes,
            is_running_ratio=True,
            _ratio=(AV_ratio, HV_ratio)
        )

        simulation = Simulation(
            debugging=False,
            time_end=ratio_simulation_time,
            time_increment=ratio_sim_time_increment,
            environment=Environment(
                name="Test collision",
                layout=layout
            ).add_objects([
                CarSpawner(name=item[0], node=starting_node(item[1][0]),
                           route=item[1], velocity=10, direction=0,
                           car_ratio=item[2], file_path=file_path,
                           file_names=["av", "hv"]) for
                item in cars_per_route]
            ),
            active_routes=routes,
            is_running_ratio=True,
            file_path_TL=file_path_TL,
            file_path_CAwSD4WI=file_path_CAwSD4WI,
            _ratio=(AV_ratio, HV_ratio)
        )

        with open(experiment_results_path + "occupancy_matrix_results.csv", "a",
                  encoding="utf8") as h:
            h.write(
                str(cars_per_route_ratio_list.index(cars_per_route) + 1) + "," +
                str(AV_ratio) + "," +
                str(HV_ratio) + "," +
                str(round(simulation_TL.completion_time, 2)) + "," +
                str(round(simulation_CAwSD4WI.completion_time, 2)) + "," +
                str(round(simulation.completion_time, 2)) + "\n")

            AV_ratio -= 5
            HV_ratio += 5

    occupancy_matrix_plotter = OccupancyMatrixPlotter(
        experiment_results_path,
        [simulation.num_of_all_cars,
         simulation.num_av,
         simulation.num_hv])
    occupancy_matrix_plotter.plot()
