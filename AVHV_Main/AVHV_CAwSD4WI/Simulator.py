#!/usr/bin/env python3
"""
    phd-autonomous-cars-frank
"""

# Operating System
import os
import sys

from svgwrite import Drawing
from svgwrite.shapes import *

from AVHV_Main.Logger.Tqdm import Tqdm

from AVHV_Main.AVHV_CAwSD4WI.Environment import Environment
from AVHV_Main.AVHV_CAwSD4WI.Plotter import Plotter
from AVHV_Main.AVHV_CAwSD4WI.StatisticsReporter import StatisticsReporter
from AVHV_Main.AVHV_CAwSD4WI.Vector2 import Vector2
from AVHV_Main.AVHV_CAwSD4WI.Car import Car
from AVHV_Main.AVHV_CAwSD4WI.CarSpawner import CarSpawner

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
        self.__end_time = time_end
        self.__time_increment = time_increment
        self.__debug_counter = 0
        self.__current_time = 0
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
        self.__drawing_directory = "../AVHV_CAwSD4WI/drawings/"
        self.__drawing_prefix = "svgwriter_frame_"

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
        self.hv_list = [cs for cs in spawner_objects if 'Aggressive' in cs.name]
        self.no_label_list = [cs for cs in spawner_objects if 'Gentle' not in
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

        if self.file_path is not None:
            self.normal_dist = Plotter(self.file_path)

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

        for layout_type, layout in self.environment.layout.items():
            layout.draw_edges(canvas=self.__scene, offset=self.__min_bound)
        for layout_type, layout in self.environment.layout.items():
            layout.draw_nodes(canvas=self.__scene, offset=self.__min_bound)
            layout.draw_text(canvas=self.__scene, offset=self.__min_bound)

        self.__scene.add(self.__scene.text("Press SPACEBAR to play/pause the "
                                           "simulation and LEFT and RIGHT "
                                           "arrow keys to move between frames.",
                                           insert=(40, 60),
                                           font_size=16,
                                           fill="#000000",
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif"))

        self.__scene.add(self.__scene.text("Reached Destination:",
                                           insert=(50, 125),
                                           font_size=16,
                                           fill="#000000",
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif;"))

        self.__scene.add(self.__scene.text("Avg. Safe dist:",
                                           insert=(230, 125),
                                           font_size=16,
                                           fill="#000000",
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif;"))

        self.__scene.add(self.__scene.text("AV:",
                                           insert=(50, 150),
                                           font_size=16,
                                           fill="#000000",
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif"))

        self.__scene.add(self.__scene.text("HV:",
                                           insert=(50, 175),
                                           font_size=16,
                                           fill="#000000",
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif"))

        self.__scene.add(self.__scene.text("No Label:",
                                           insert=(50, 200),
                                           font_size=16,
                                           fill="#000000",
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif"))

        self.__scene.add(self.__scene.text("Total Time Elapsed (s):",
                                           insert=(50, 240),
                                           font_size=16,
                                           fill="#000000",
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif"))

        self.__scene.add(self.__scene.text("No. of Cars in Sim.:",
                                           insert=(50, 265),
                                           font_size=16,
                                           fill="#000000",
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif"))

        self.__scene.add(self.__scene.text("Frame:",
                                           insert=(50, 290),
                                           font_size=16,
                                           fill="#000000",
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif"))

        self.__scene.add(self.__scene.text("(Simulation playback is faster)",
                                           insert=(50, 320),
                                           font_size=16,
                                           fill="#000000",
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif"))

        self.__scene.add(self.__scene.text("Active Routes:",
                                           insert=(50, 620),
                                           font_size=14,
                                           fill="#000000",
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif"))

        self.__scene.add(self.__scene.text(str(self.active_routes[0]),
                                           insert=(50, 645),
                                           font_size=14,
                                           fill="#000000",
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif"))

        self.__scene.add(self.__scene.text(str(self.active_routes[1]),
                                           insert=(50, 665),
                                           font_size=14,
                                           fill="#000000",
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif"))

        self.__scene.add(self.__scene.text(str(self.active_routes[2]),
                                           insert=(50, 685),
                                           font_size=14,
                                           fill="#000000",
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif"))

        self.__scene.add(self.__scene.text(str(self.active_routes[3]),
                                           insert=(50, 705),
                                           font_size=14,
                                           fill="#000000",
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif"))

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

        self.__scene.add(self.__scene.text("50m",
                                           insert=(167, 492),
                                           font_size=12,
                                           fill="#000000",
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif;"))

        self.__scene.add(self.__scene.text("~ Collision Avoidance with Safe ",
                                           insert=(550, 125),
                                           font_size=16,
                                           fill="#000000",
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif;"))

        self.__scene.add(self.__scene.text("Distance and 4 Way Intersection ~",
                                           insert=(550, 150),
                                           font_size=16,
                                           fill="#000000",
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif;"))

        self.__scene.add(self.__scene.text("Cars braked:",
                                           insert=(550, 185),
                                           font_size=16,
                                           fill="#000000",
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif;"))

        self.__scene.add(self.__scene.text("Congestion:",
                                           insert=(550, 212),
                                           font_size=16,
                                           fill="#000000",
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif;"))

        self.__scene.add(self.__scene.text("Occurred Collisions:",
                                           insert=(550, 239),
                                           font_size=16,
                                           fill="#000000",
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif;"))

        # self.__scene.add(self.__scene.text("Other Experiments:",
        #                                    insert=(550, 650),
        #                                    font_size=15,
        #                                    fill="#000000",
        #                                    style="font-family: Lucida Sans Unicode, "
        #                                          "Sans-serif;"))
        #
        # self.__scene.add(self.__scene.text("➤",
        #                                    insert=(550, 680),
        #                                    font_size=15,
        #                                    fill="#000000",
        #                                    style="font-family: Lucida Sans Unicode, "
        #                                          "Sans-serif;"))
        #
        # self.__scene.add(self.__scene.text("Experiment w/ Reservation
        # Node", insert=(570, 680), font_size=15, fill="#0000FF",
        # style="font-family: Lucida Sans Unicode, " "Sans-serif;" "text-decoration:
        # underline"))
        #
        # self.__scene.add(self.__scene.text("➤",
        #                                    insert=(550, 710),
        #                                    font_size=15,
        #                                    fill="#000000",
        #                                    style="font-family: Lucida Sans Unicode, "
        #                                          "Sans-serif;"))
        #
        # self.__scene.add(self.__scene.text("Experiment w/ Traffic Lights",
        # insert=(570, 710), font_size=15, fill="#0000FF",
        # style="font-family: Lucida Sans Unicode, " "Sans-serif;" "text-decoration:
        # underline"))

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
        self.environment.draw(canvas=self.__frame, offset=self.__min_bound)
        self.__frame.add(self.__frame.text(str(
            self.environment.passed_av_cars) + '/' + str(self.num_av),
                                           insert=(90, 150), font_size=16,
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif"))

        self.__frame.add(self.__frame.text(str(self.av_average_safe_distance) +
                                           " m",
                                           insert=(230, 150), font_size=16,
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif"))

        self.__frame.add(self.__frame.text(str(
            self.environment.passed_hv_cars) + '/' + str(self.num_hv),
                                           insert=(90, 175), font_size=16,
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif"))

        self.__frame.add(self.__frame.text(str(self.hv_average_safe_distance) +
                                           " m",
                                           insert=(230, 175), font_size=16,
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif"))

        self.__frame.add(self.__frame.text(str(
            self.environment.passed_nl_cars) + '/' + str(self.num_no_label),
                                           insert=(130, 200), font_size=16,
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif"))

        self.__frame.add(self.__frame.text(str(
            self.no_label_average_safe_distance) + " m",
                                           insert=(230, 200), font_size=16,
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif"))

        self.__frame.add(self.__frame.text(round(self.__running_time, 2),
                                           insert=(240, 240), font_size=16,
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif"))

        self.__frame.add(self.__frame.text(self.num_of_all_cars,
                                           insert=(240, 265), font_size=16,
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif"))

        self.__frame.add(self.__frame.text(round(self.__current_time, 2),
                                           insert=(240, 290), font_size=16,
                                           style="font-family: Lucida Sans Unicode, "
                                                 "Sans-serif"))

        self.__frame.add(
            self.__frame.text(str(len(self.environment.cars_braked)),
                              insert=(665, 185), font_size=16, fill="#000000",
                              style="font-family: Lucida Sans Unicode, "
                                    "Sans-serif;"))

        self.__frame.add(self.__frame.text(
            str(self.environment.collisions_prevented),
            insert=(725, 212),
            font_size=16,
            fill="#000000",
            style="font-family: Lucida Sans Unicode, "
                  "Sans-serif;"))

        self.__frame.add(self.__frame.text(
            str(self.environment.occurred_collisions),
            insert=(725, 239),
            font_size=16,
            fill="#000000",
            style="font-family: Lucida Sans Unicode, "
                  "Sans-serif;"))

        # self.__frame.add(self.__frame.text(str(self.environment.pas)))

        self.__frame.save()

    def __start_simulation(self):
        self.__calculate_layout()

        if isinstance(self.environment, Environment):
            self.__reporter = StatisticsReporter(self.environment)

        # Drawing prep
        for frame in os.listdir(self.__drawing_directory):
            os.remove(self.__drawing_directory + frame)
        self.__draw_current(self.__current_time)

        print("AVHV Control with CAwS4WI - Please wait for a while...")

        # Progress bar
        progress_bar = Tqdm(0, total=self.__end_time, file=sys.stdout)

        while self.__current_time < self.__end_time:
            debug = self.environment.update(delta_time=self.__time_increment,
                                            record=False)
            debug = str.format("Tick: {:3.3f}\t", self.__current_time) + debug

            # Check if Debug should run
            if self.__debug_counter <= self.__current_time:
                self.__debug_counter += self.__time_increment

                # Data recording
                self.environment.record_values(self.__current_time)
                self.__reporter.record(self.__debug_counter)
                if self.debugging:
                    pass
                    # print(debug)

            if self.environment.passed_av_cars + \
                    self.environment.passed_hv_cars + \
                    self.environment.passed_nl_cars == self.num_of_all_cars:
                pass

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
            self.__current_time += self.__time_increment
            self.__draw_current(self.__current_time)

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
            self.av_averages_safe_distance / (self.__running_time /
                                              self.__time_increment))

        self.hv_average_safe_distance = round(
            self.hv_averages_safe_distance / (self.__running_time /
                                              self.__time_increment))

        self.no_label_average_safe_distance = round(
            self.no_label_average_safe_distance / (self.__running_time /
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
                                  round(self.__current_time, 2)]


if __name__ == '__main__':
    print(
        "Ekene's Simulation, please create a Simulation and add an Environment")
