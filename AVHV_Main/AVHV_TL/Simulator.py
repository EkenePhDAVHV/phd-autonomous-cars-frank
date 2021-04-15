#!/usr/bin/env python3
"""
    phd-autonomous-cars-frank
"""

# Operating System
import os
import sys

import pickle

from svgwrite import Drawing
from svgwrite.shapes import *

from AVHV_Main.Logger.Tqdm import Tqdm

from AVHV_Main.Utilities.checkpoint import load_checkpoint, save_checkpoint

from AVHV_Main.AVHV_TL.CarSpawner import CarSpawner
from AVHV_Main.AVHV_TL.Car import Car
from AVHV_Main.AVHV_TL.Environment import Environment
from AVHV_Main.AVHV_TL.StatisticsReporter import StatisticsReporter
from AVHV_Main.AVHV_TL.Vector2 import Vector2

os.chdir(os.path.dirname(__file__))
if not os.path.exists("drawings"):
    os.mkdir("drawings")


class Simulation:
    def __init__(self, environment, time_end=10, time_increment=0.1,
                 debugging=False, active_routes=[None, None, None, None],
                 file_path=None, file_names=[None, None],
                 current_file_name=None):

        # Environment
        self.environment = environment

        # Timing Control
        self.end_time = time_end
        self.__time_increment = time_increment
        self.__debug_counter = 0
        self.current_time = 0
        self.__running_time = 0

        # Statistics
        self.debugging = debugging
        self.__reporter = None

        self.file_path = file_path
        self.file_names = file_names
        self.current_file_name = current_file_name

        # Drawings
        self.__frame = None
        self.__scene = Drawing()
        self.__min_bound = Vector2([0, 0])
        self.__max_bound = Vector2([0, 0])

        # File Path
        self.__drawing_directory = "../AVHV_TL/drawings/"
        self.__drawing_prefix = "svgwriter_frame_"

        state_file = os.path.dirname(
                    os.path.realpath(__file__)) + "/" + "state.pickle"

        backup_file = os.path.dirname(
            os.path.realpath(__file__)) + "/" + "state.pickle.bak"

        if not os.path.exists(os.path.dirname(
                os.path.realpath(__file__)) + "/" + "state.pickle"):

            self.active_routes = active_routes

            # Car counter
            self.num_of_all_cars = 0
            self.num_av = 0
            self.num_hv = 0
            self.num_no_label = 0
            self.num_of_all_cars = 0
            self.num_unique_routes = 0

            self.environment_objects = self.environment.environment_objects.copy()

            spawner_objects = self.environment_objects[CarSpawner]
            self.car_objects = self.environment_objects[Car]

            self.av_list = [cs for cs in spawner_objects if 'Gentle' in cs.name]
            self.hv_list = [cs for cs in spawner_objects if
                            'Aggressive' in cs.name]
            self.no_label_list = [cs for cs in spawner_objects if
                                  'Gentle' not in
                                  cs.name and 'Aggressive' not in cs.name]

            self.av_total_safe_distance = 0.0
            self.hv_total_safe_distance = 0.0
            self.no_label_total_safe_distance = 0.0

            self.av_averages_safe_distance = 0.0
            self.hv_averages_safe_distance = 0.0
            self.no_label_averages_safe_distance = 0.0

            self.av_average_safe_distance = 0.0
            self.hv_average_safe_distance = 0.0
            self.no_label_average_safe_distance = 0.0

            self.car_density = []
            self.traffic_flow = []
            self.car_speed = []
            self.safe_distances = []
            self.reaction_times = []

            self.total_braked_cars = 0.0
            self.average_braked_cars_per_min = 0.0

            self.throughput_capacity_av = 0.0
            self.throughput_capacity_hv = 0.0

            self.experiment_values = []

            for cs in self.av_list:
                self.num_av += cs.total_cars

            for cs in self.hv_list:
                self.num_hv += cs.total_cars

            for cs in self.no_label_list:
                self.num_no_label += cs.total_cars

            self.num_of_all_cars += self.num_av + self.num_hv + self.num_no_label

            # get all the used routes
            all_cs_routes = [cs.route for cs in spawner_objects]
            all_cs_routes_unique = []

            all_cs_routes_unique = [route for route in all_cs_routes if route
                                    not in all_cs_routes_unique]

            self.normal_dist = None

            with open(os.path.dirname(
                    os.path.realpath(__file__)) + "/" + "state.pickle",
                      'wb') as g:
                pickle.dump(self.__dict__, g)
        else:
            try:
                with open(state_file, 'rb') as g:
                    self.__dict__ = pickle.load(g)
            except EOFError:
                if os.path.exists(backup_file):
                    with open(backup_file, 'rb') as g:
                        self.__dict__ = pickle.load(g)

        self.__start_simulation()

    def __calculate_blank(self):
        if isinstance(self.environment, Environment):
            layout_nodes = self.environment.road_system.nodes

            if len(layout_nodes) > 0:
                self.__min_bound = layout_nodes[0].position.copy()
                self.__max_bound = layout_nodes[0].position.copy()
            else:
                self.__min_bound = Vector2(-600, -600)
                self.__max_bound = Vector2(600, 600)

            for n in layout_nodes:
                # Min X
                if n.position.x < self.__min_bound.x:
                    self.__min_bound.x = n.position.x

                # Min Y
                if n.position.y < self.__min_bound.y:
                    self.__min_bound.y = n.position.y

                # Max X
                if n.position.x > self.__max_bound.x:
                    self.__max_bound.x = n.position.x

                # Max Y
                if n.position.y > self.__max_bound.y:
                    self.__max_bound.y = n.position.y

        border = 140
        self.__min_bound.x -= border
        self.__min_bound.y -= border
        self.__max_bound.x += border
        self.__max_bound.y += border - 80

        self.__scene = Drawing(
            "blank.svg",
            size=(abs(self.__max_bound.x - self.__min_bound.x),
                  abs(self.__max_bound.y - self.__min_bound.y))
        )

        self.__scene.add(Polygon(
            [
                # Bottom Left
                (0, 0),

                # Top Left
                (0, abs(self.__max_bound.y - self.__min_bound.y)),

                # Top Right
                (abs(self.__max_bound.x - self.__min_bound.x),
                 abs(self.__max_bound.y - self.__min_bound.y)),

                # Bottom Right
                (abs(self.__max_bound.x - self.__min_bound.x), 0)
            ],
            fill='white'
        ))

    def __calculate_layout(self):
        self.__calculate_blank()

        # for layout_type, layout in self.environment.layout.items():
        #     layout.draw_edges(canvas=self.__scene, offset=self.__min_bound)
        # for layout_type, layout in self.environment.layout.items():
        #     layout.draw_nodes(canvas=self.__scene, offset=self.__min_bound)
        #     layout.draw_text(canvas=self.__scene, offset=self.__min_bound)

        text = [
            ["Press SPACEBAR to play/pause the simulation and LEFT and RIGHT "
             "arrow keys to move between frames.", (40, 60)],
            ["Reached Destination", (50, 125)],
            ["Avg. Safe dist:", (230, 125)],
            ["AV:", (50, 150)],
            ["HV:", (50, 175)],
            ["No Label:", (50, 200)],
            ["Total Time Elapsed (s):", (50, 240)],
            ["No. of Cars in Sim.:", (50, 265)],
            ["Frame:", (50, 290)],
            ["(Simulation playback is faster)", (50, 320)],
            ["Active Routes:", (50, 620), 14],
            [str(self.active_routes[0]), (50, 645), 15],
            [str(self.active_routes[1]), (50, 665), 15],
            [str(self.active_routes[2]), (50, 685), 14],
            [str(self.active_routes[3]), (50, 705), 14],
            ["50m", (167, 492), 12],
            ["~ Trafiic Lights ~", (550, 125)],
            ["Cars braked:", (550, 160)],
            # ["Congestion:", (550, 187)],
            # ["Occurred Collisions:", (550, 214)],
            # ["Reservation Nodes Schematic", (550, 250), 16, "#0000FF",
            #  "font-family: Lucida Sans Unicode, Sans-serif; text-decoration: "
            #  "underline"]
        ]

        for t in text:
            font_size = 16
            fill = "#000000"
            style = "font-family: Lucida Sans Unicode, Sans-serif"

            if len(t) > 2:
                font_size = t[2]
            if len(t) > 3:
                fill = t[3]
            if len(t) > 4:
                style = t[4]

            self.__scene.add(
                self.__scene.text(t[0], insert=t[1],
                                  font_size=font_size,
                                  fill=fill,
                                  style=style))

        self.__scene.add(Rect(
            insert=(155, 471.5),
            size=(50, 7),
            fill='black'
        ))

        self.__scene.add(Line(
            start=([155, 475]),
            end=([165, 475]),
            stroke='black',
            stroke_width=6
        ))

        self.__scene.add(Line(
            start=([165, 475]),
            end=([175, 475]),
            stroke='white',
            stroke_width=6
        ))

        self.__scene.add(Line(
            start=([175, 475]),
            end=([185, 475]),
            stroke='black',
            stroke_width=6
        ))

        self.__scene.add(Line(
            start=([185, 475]),
            end=([195, 475]),
            stroke='white',
            stroke_width=6
        ))

        self.__scene.add(Line(
            start=([195, 475]),
            end=([205, 475]),
            stroke='black',
            stroke_width=6
        ))

        self.__scene.save()

    def __draw_current(self, time_step):
        """Draws a new canvas."""

        self.__frame = self.__scene.copy()
        self.__frame.filename = str.format("{:s}{:s}{:.2f}{:s}",
                                           self.__drawing_directory,
                                           self.__drawing_prefix,
                                           time_step,
                                           ".svg")

        # Draw elements and save
        # self.environment.draw(canvas=self.__frame, offset=self.__min_bound)

        text = [
            [f"{self.environment.passed_av_cars} / {self.num_av}", (90, 150)],
            [f"{self.av_average_safe_distance} m", (230, 150)],
            [f"{self.environment.passed_hv_cars} / {self.num_hv}", (90, 175)],
            [f"{self.hv_average_safe_distance} m", (230, 175)],
            [f"{self.environment.passed_nl_cars} / {self.num_no_label}",
             (130, 200)],
            [f"{self.no_label_average_safe_distance} m", (230, 200)],
            [f"{round(self.__running_time, 2)}", (240, 240)],
            [f"{self.num_of_all_cars} ", (240, 265)],
            [f"{round(self.current_time, 2)}", (240, 290)],
            [f"{self.environment.occurred_collisions}", (665, 160)],
            # [f"{self.environment.collisions_prevented}", (725, 187)],
        ]

        for t in text:
            font_size = 16
            fill = "#000000"
            style = "font-family: Lucida Sans Unicode, Sans-serif"

            if len(t) > 2:
                font_size = t[2]
            if len(t) > 3:
                fill = t[3]
            if len(t) > 4:
                style = t[4]

            self.__frame.add(
                self.__frame.text(t[0], insert=t[1],
                                  font_size=font_size,
                                  fill=fill,
                                  style=style)
            )

        self.__frame.save()

    def __start_simulation(self):
        self.__calculate_layout()

        if isinstance(self.environment, Environment):
            self.__reporter = StatisticsReporter(self.environment)

        # Drawing prep
        for frame in os.listdir(self.__drawing_directory):
            os.remove(self.__drawing_directory + frame)
        # self.__draw_current(self.current_time)

        self.current_time = load_checkpoint(self, os.path.dirname(
            os.path.realpath(__file__)) + "/" + "checkpoint.txt")

        print("\nAVHV Control with Traffic Lights - Please wait for a while...")

        # Progress bar
        progress_bar = Tqdm(self.current_time, total=self.end_time,
                            file=sys.stdout, initial=self.current_time)

        while self.current_time < self.end_time:
            debug = self.environment.update(delta_time=self.__time_increment,
                                            record=False)
            debug = str.format("Tick: {:3.3f}\t", self.current_time) + debug

            # Check if Debug should run
            if self.__debug_counter <= self.current_time:
                self.__debug_counter += self.__time_increment

                # Data recording
                self.environment.record_values(self.current_time)
                self.__reporter.record(self.__debug_counter)
                if self.debugging:
                    pass
                    # print(debug)

            if self.environment.passed_av_cars + \
                    self.environment.passed_hv_cars + \
                    self.environment.passed_nl_cars == self.num_of_all_cars:
                pass

            self.car_density.append(
                round(len(self.environment.environment_objects[Car]) * 2.5 / (
                        2.4 * 0.6214), 2))

            self.traffic_flow.append(
                round(
                    len(self.environment.environment_objects[Car]) * 3600 / self.__time_increment,
                    2))

            self.car_speed.append(round(sum([car.get_speed() * 2.237 for car in
                                             self.environment.environment_objects[
                                                 Car]]) / len(
                self.environment.environment_objects[Car]), 2))

            safe_distances = [car.safe_distance for car in
                              self.environment.environment_objects[Car] if
                              'Aggressive' in car.name]

            reaction_times = [car.reaction_time for car in
                              self.environment.environment_objects[
                                  Car] if
                              'Aggressive' in car.name]

            self.safe_distances.append(
                round(sum(safe_distances) / len(safe_distances),
                      2))

            self.reaction_times.append(round(sum(reaction_times) / len(
                reaction_times), 2))

            # Increment at the end

            if self.environment.passed_av_cars + \
                    self.environment.passed_hv_cars + \
                    self.environment.passed_nl_cars < self.num_of_all_cars:
                self.__running_time += self.__time_increment

                car_objects = self.environment.environment_objects[Car]

                av_objects = [car for car in car_objects if "Gentle" in
                              car.name]
                hv_objects = [car for car in car_objects if "Aggressive" in
                              car.name]
                no_label_objects = [car for car in car_objects if "Gentle" not
                                    in car.name and "Aggressive" not in
                                    car.name]

                self.av_total_safe_distance = sum([car.safe_distance for car in
                                                   av_objects])

                self.hv_total_safe_distance = sum([car.safe_distance for car in
                                                   hv_objects])

                self.no_label_total_safe_distance = sum([car.safe_distance for
                                                         car in
                                                         no_label_objects])

                self.total_braked_cars += len(self.environment.cars_braked)

                try:
                    self.av_averages_safe_distance += \
                        round(self.av_total_safe_distance / (len(
                            av_objects)), 2)
                except ZeroDivisionError:
                    self.av_average_safe_distance = 0

                try:
                    self.hv_averages_safe_distance += \
                        round(self.hv_total_safe_distance / (len(
                            hv_objects)), 2)
                except ZeroDivisionError:
                    self.hv_average_safe_distance = 0

                try:
                    self.no_label_averages_safe_distance += \
                        round(self.no_label_total_safe_distance / (len(
                            no_label_objects)), 2)
                except ZeroDivisionError:
                    self.no_label_average_safe_distance = 0

                # print([car.safe_distance for car in self.av_list])
            self.current_time += self.__time_increment

            save_checkpoint(self, self.current_time, self.end_time,
                            os.path.dirname(os.path.realpath(__file__)) + "/" + "checkpoint.txt",
                            os.path.dirname(os.path.realpath(__file__)) + "/" + "state.pickle")

            # self.__draw_current(self.current_time)

            progress_bar.update(self.__time_increment)

        progress_bar.close()

        if self.normal_dist is not None and self.file_names[0] is not None and \
                self.file_names[1] is not None:
            for file_name in self.file_names:
                self.normal_dist.read_csv(file_name)
                print(f'Open "{self.file_path}" for distributions and graphs')

                if self.file_names.index(file_name) == 1:
                    print('\n')

        self.av_average_safe_distance = round(
            self.av_averages_safe_distance / (self.__running_time / \
                                              self.__time_increment))

        self.hv_average_safe_distance = round(
            self.hv_averages_safe_distance / (self.__running_time / \
                                              self.__time_increment))

        self.no_label_average_safe_distance = round(
            self.no_label_average_safe_distance / (self.__running_time / \
                                                   self.__time_increment))

        try:
            self.throughput_capacity_av = round(
                self.environment.passed_av_cars * 60
                / (self.__running_time / self.__time_increment), 2)
        except ZeroDivisionError:
            self.throughput_capacity_av = 0.0

        try:
            self.throughput_capacity_hv = round(
                self.environment.passed_hv_cars * 60
                / (self.__running_time / self.__time_increment), 2)
        except ZeroDivisionError:
            self.throughput_capacity_hv = 0.0

        self.experiment_values = [self.environment.collisions_prevented,
                                  self.environment.occurred_collisions,
                                  round(self.total_braked_cars * 60 /
                                        (self.__running_time /
                                         self.__time_increment),
                                        2),
                                  round(self.av_average_safe_distance, 2),
                                  round(self.hv_average_safe_distance, 2),
                                  round(self.throughput_capacity_av, 2),
                                  round(self.throughput_capacity_hv, 2),
                                  round(self.current_time, 2),
                                  self.traffic_flow,
                                  self.car_density,
                                  self.car_speed,
                                  [self.environment.passed_av_cars,
                                   self.environment.passed_hv_cars,
                                   self.environment.passed_nl_cars],
                                  self.safe_distances,
                                  self.reaction_times]


if __name__ == '__main__':
    print(
        "Ekene's Simulation, please create a Simulation and add an Environment")
