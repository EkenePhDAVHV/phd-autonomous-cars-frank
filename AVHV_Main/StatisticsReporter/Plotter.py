import csv

import numpy as np

from AVHV_Main.Utilities.constants import *

from AVHV_Main.StatisticsReporter.traffic_plot import plot_traffic
from AVHV_Main.StatisticsReporter.occupancy_plot import plot_occupancy_matrix


def get_simulation_time_label(simul_time):
    if simul_time >= 60:
        simulation_time_label = str(round(simul_time / 60, 1)) + \
                                " min(s)"
    elif simul_time >= 3600:
        simulation_time_label = str(round(simul_time / 3600, 2
                                          )) + " hr(s)"
    else:
        simulation_time_label = str(simul_time) + " sec(s)"

    return simulation_time_label


class StandardPlotter:
    def __init__(self, all_results_path=None, file_path=None,
                 traffic_flow=[], car_densities=[], car_speeds=[],
                 num_of_passed_cars=[], safe_distances=[],
                 reaction_times=[], running_times=[], num_of_cars=[]):

        self.i = 0
        self.j = 100

        self.mean1 = None
        self.std1 = None
        self.mean2 = None
        self.std2 = None

        self.traffic_flow = traffic_flow
        self.car_densities = car_densities
        self.car_speeds = car_speeds
        self.safe_distances = safe_distances
        self.reaction_times = reaction_times

        self.num_of_passed_cars = num_of_passed_cars

        self.num_of_all_cars = num_of_cars[0]
        self.total_av = num_of_cars[1]
        self.total_hv = num_of_cars[2]

        time_graduation_1 = np.arange(0, running_times[0],
                                      sim_time_increment)
        time_graduation_2 = np.arange(0, running_times[1],
                                      sim_time_increment)
        time_graduation_3 = np.arange(0, running_times[2],
                                      sim_time_increment)

        self.time_graduation = [[round(time_step, 2) for time_step in
                                 time_graduation_1],
                                [round(time_step, 2) for time_step in
                                 time_graduation_2],
                                [round(time_step, 2) for time_step in
                                 time_graduation_3]]

        self.fields_1 = ['Density_(veh/hr)_TL',
                         'Density_(veh/hr)_CAwSD4WI',
                         'Density_(veh/hr)_RN',
                         'Time_(secs)']

        self.fields_2 = ['Speed_(km/hr)_TL',
                         'Speed_(km/hr)_CAwSD4WI',
                         'Speed_(km/hr)_RN',
                         'Time_(secs)'
                         ]

        self.all_results_path = all_results_path
        self.file_path = file_path

        self.simulation_time_label = get_simulation_time_label(simulation_time)

    @staticmethod
    def do_plot(self, all_fp):

        all_values_1 = zip(self.car_densities[0], self.car_densities[1],
                           self.car_densities[2], self.time_graduation[0])
        all_values_2 = zip(self.car_speeds[0], self.car_speeds[1],
                           self.car_speeds[2], self.time_graduation[0])

        key_variables_1 = list(all_values_1)
        key_variables_2 = list(all_values_2)

        with open(all_fp + 'all_densities.csv', 'w', newline='',
                  encoding='utf-8') as f:
            # using csv.writer method from CSV package
            write = csv.writer(f)

            write.writerow(self.fields_1)
            write.writerows(key_variables_1)

        with open(all_fp + 'all_speeds.csv', 'w', newline='',
                  encoding='utf-8') as f:
            # using csv.writer method from CSV package
            write = csv.writer(f)

            write.writerow(self.fields_2)
            write.writerows(key_variables_2)

        plot_traffic(self, self.traffic_flow, self.car_densities,
                     'Traffic Flow vs Density',
                     'Traffic Flow (vehicle / hr)',
                     'Density (vehicle / mile)',
                     all_fp, 'flow-density', 'Flow', 'Density')

        plot_traffic(self, self.car_speeds, self.car_densities,
                     'Speed vs Density',
                     'Speed (miles / hr)',
                     'Density (vehicle / mile)',
                     all_fp, 'speed-density', 'Speed', 'Density')

        plot_traffic(self, self.traffic_flow, self.car_speeds,
                     'Traffic Flow vs Speed',
                     'Traffic flow (vehicle / hr)',
                     'Speed (miles / hr)',
                     all_fp, 'flow-speed', 'Flow', 'Speed')

        plot_traffic(self, self.time_graduation, self.safe_distances,
                     'Safe Distance over Time',
                     'Time (secs)',
                     'Safe Distance (m)',
                     all_fp, 'safe_distance', 'Safe Dist.',
                     x_val_only_in_table=True)

        plot_traffic(self, self.time_graduation, self.reaction_times,
                     'Reaction Time over Time',
                     'Time (secs)',
                     'Reaction Time (secs)',
                     all_fp, 'reaction_time', 'React. Time',
                     x_val_only_in_table=True)

    def plot(self):
        try:
            self.do_plot(self, self.all_results_path)
        except FileNotFoundError as e:
            print(e)


class OccupancyMatrixPlotter:
    def __init__(self, all_results_path=None, num_of_cars=[]):

        self.all_results_path = all_results_path

        self.num_of_all_cars = num_of_cars[0]
        self.total_av = num_of_cars[1]
        self.total_hv = num_of_cars[2]

        self.simulation_time_label = get_simulation_time_label(simulation_time)

    @staticmethod
    def do_plot(self, all_fp):

        occupancy_times = [[], [], []]
        ratio_codes = []

        with open(all_fp + 'occupancy_matrix_results.csv', 'r') as f:

            # using csv.writer method from CSV package
            reader = csv.reader(f)

            for index, line in enumerate(reader):
                if index > 0:
                    occupancy_times[0].append(float(line[3]))
                    occupancy_times[1].append(float(line[4]))
                    occupancy_times[2].append(float(line[5]))
                    ratio_codes.append(int(line[0]))

        plot_occupancy_matrix(self, ratio_codes, occupancy_times,
                              'Occupancy Time Matrix',
                              'Ratio Code',
                              'Occupancy Time (secs)',
                              all_fp, 'occupancy_time_matrix')

    def plot(self):
        try:
            self.do_plot(self, self.all_results_path)
        except FileNotFoundError as e:
            print(e)
