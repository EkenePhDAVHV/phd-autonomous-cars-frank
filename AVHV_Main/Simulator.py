#!/usr/bin/env python3
"""
    phd-autonomous-cars-frank
"""
import os
import sys
from datetime import datetime

import matplotlib.pyplot as plt
from svgwrite import Drawing
from svgwrite.shapes import *

from AVHV_Main.Agents.Car import Car
from AVHV_Main.Agents.CarSpawner import CarSpawner
from AVHV_Main.Environment import Environment
from AVHV_Main.Logger.Tqdm import Tqdm
from AVHV_Main.StatisticsReporter.PDFDocumenter import PDFDocumenter
from AVHV_Main.StatisticsReporter.Plotter import Plotter
from AVHV_Main.StatisticsReporter.StatisticsReporter import StatisticsReporter
from AVHV_Main.Utilities.Vector2 import Vector2


class Simulation:
    def __init__(self, environment, time_end=10, time_increment=0.1,
                 debugging=False, active_routes=[None, None, None, None],
                 file_path=None, file_names=[None, None],
                 current_file_name=None, simulation_TL_values=None,
                 simulation_CAwSD4WI_values=None, file_path_TL=None,
                 file_path_CAwSD4WI=None):

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
        self.file_path_TL = file_path_TL
        self.file_path_CAwSD4WI = file_path_CAwSD4WI

        # Drawings
        self.__frame = None
        self.__scene = Drawing()
        self.__min_bound = Vector2([0, 0])
        self.__max_bound = Vector2([0, 0])

        # File Path
        self.__drawing_directory = "../drawings/"
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

        self.simulation_TL_values = simulation_TL_values
        self.simulation_CAwSD4WI_values = simulation_CAwSD4WI_values

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

        car_spawners = [cs for cs in
                        self.environment.environment_objects[CarSpawner]]

        self.route1_num_cars = sum([cs.total_cars for cs in car_spawners if \
                                    cs.route_list == self.active_routes[0]])
        self.route2_num_cars = sum([cs.total_cars for cs in car_spawners if \
                                    cs.route_list == self.active_routes[1]])
        self.route3_num_cars = sum([cs.total_cars for cs in car_spawners if \
                                    cs.route_list == self.active_routes[2]])
        self.route4_num_cars = sum([cs.total_cars for cs in car_spawners if \
                                    cs.route_list == self.active_routes[3]])

        self.normal_dist = None

        self.throughput_capacity_av = 0
        self.throughput_capacity_hv = 0

        self.experiment_values = []

        if self.file_path is not None:
            self.normal_dist = Plotter(self.file_path)

        self.__start_simulation()
        self.__write_documentation()

    def __write_documentation(self):
        current_time = datetime.now()
        file_to_write_to = str(current_time.year) + "_" + \
                           str(current_time.month) + "_" + \
                           str(current_time.day) + "_" + \
                           str(current_time.hour) + str(current_time.minute) + \
                           str(current_time.second)

        pdf = PDFDocumenter()
        pdf.add_page()
        pdf.titles()
        pdf.write(10, f'Experiment {file_to_write_to}\n')

        # Remember to always put one of these at least once.
        pdf.set_font('Times', '', 10.0)

        # Effective page width, or just epw
        epw = pdf.w - 2 * pdf.l_margin

        # Set column width to 1/6 of effective page width to distribute content
        # evenly across table and page
        col_width = epw / 6
        summary_col_width = epw / 6

        # Since we do not need to draw lines anymore, there is no need to
        # separate headers from data matrix.

        summary_data = [
            ['Car Mixture', 'Active Reservation Nodes'],
            [f"AV: {self.num_av}", f"{self.active_routes[0]} - "
                                   f"{self.route1_num_cars} cars"],
            [f"HV: {self.num_hv}", f"{self.active_routes[1]} - "
                                   f"{self.route2_num_cars} cars"],
            [f"No Label: {self.num_no_label}", f"{self.active_routes[2]} - "
                                               f"{self.route3_num_cars} cars"],
            ["", f"{self.active_routes[3]} - {self.route1_num_cars} cars"],
            [f"AV Car Spawner: {len(self.av_list)}", ],
            [f"HV Car Spawner: {len(self.hv_list)}"],
            [f"No Label: {len(self.no_label_list)}"],
        ]

        # Text height is the same as current font size
        th = pdf.font_size

        # Line break equivalent to 4 lines
        pdf.ln(3 * th)

        pdf.set_font('Times', 'B', 14.0)
        pdf.cell(epw, 0.0, 'Experiment Details',
                 align='C')
        pdf.set_font('Times', '', 10.0)
        pdf.ln(6)

        for row in summary_data:
            if summary_data.index(row) == 0:
                pdf.set_font('Times', 'B', 10.0)
            else:
                pdf.set_font('Times', '', 10.0)

            for datum in row:
                # Enter data in columns
                if row.index(datum) == 1:
                    pdf.cell(summary_col_width * 3, 2 * th, str(datum),
                             border=0, align='L')
                else:
                    pdf.cell(summary_col_width * 2, 2 * th, str(datum),
                             border=0, align='L')

            pdf.ln(1.5 * th)

        if self.simulation_TL_values is not None and \
                self.simulation_CAwSD4WI_values is not None:

            data = [['', 'w/ Reservation Nodes', 'w/ Traffic Lights',
                     "w/ Safe Distance and 4 Way Intersection"],
                    ['Congestion',
                     str(self.environment.collisions_prevented),
                     str(self.simulation_TL_values[0]),
                     str(self.simulation_CAwSD4WI_values[0])],
                    ['No. of Collisions',
                     str(self.environment.occurred_collisions),
                     str(self.simulation_TL_values[1]),
                     str(self.simulation_CAwSD4WI_values[1])],
                    ['Avg. Braked Cars per min',
                     str(round(self.total_braked_cars * 60 /
                               (self.__running_time / self.__time_increment),
                               2)),
                     str(self.simulation_TL_values[2]),
                     str(self.simulation_CAwSD4WI_values[2])],
                    ['Avg. Safe Distance (AV)',
                     str(round(self.av_average_safe_distance, 2)),
                     str(self.simulation_TL_values[3]),
                     str(self.simulation_CAwSD4WI_values[3])],
                    ['Avg. Safe Distance (HV)', str(round(
                        self.hv_average_safe_distance, 2)),
                     str(self.simulation_TL_values[4]),
                     str(self.simulation_CAwSD4WI_values[4])],
                    ['Capacity AV - car(s)/min',
                     str(self.throughput_capacity_av),
                     str(self.simulation_TL_values[5]),
                     str(self.simulation_CAwSD4WI_values[5])],
                    ['Capacity HV - car(s)/min',
                     str(self.throughput_capacity_hv),
                     str(self.simulation_TL_values[6]),
                     str(self.simulation_CAwSD4WI_values[6])],
                    ['Total Simulation Time (s)',
                     str(round(self.__running_time, 2)),
                     str(self.simulation_TL_values[7]),
                     str(self.simulation_CAwSD4WI_values[7])]
                    ]

            pdf.ln(12)
            pdf.set_font('Times', 'B', 14.0)
            pdf.cell(epw, 0.0, 'Comparison of Experiment Metrics',
                     align='C')
            pdf.set_font('Times', '', 10.0)
            pdf.ln(6)

            # Here we add more padding by passing 2*th as height
            for row in data:
                if data.index(row) == 0:
                    pdf.set_font('Times', 'B', 10.0)
                else:
                    pdf.set_font('Times', '', 10.0)

                for idx in range(len(row)):

                    if idx == 0:
                        align = 'L'
                        width = col_width * 1.4
                    elif idx == 3:
                        align = 'R'
                        width = col_width * 2
                    else:
                        align = 'R'
                        width = col_width * 1.3

                    if data.index(row) == 0:
                        align = 'C'

                    # Enter data in columns
                    if idx == 3:
                        pdf.cell(width, 2.5 * th, str(row[idx]),
                                 border=1, align=align)
                    else:
                        pdf.cell(width, 2.5 * th, str(row[idx]),
                                 border=1, align=align)

                pdf.ln(2.5 * th)

        pdf.ln(18)
        pdf.set_font('Times', '', 10.0)
        pdf.write(h=th,
                  txt=f'Open "{self.file_path[1:]}" for distributions and '
                      f'graphs of Experiment with RN')

        if self.simulation_TL_values is not None:
            pdf.ln(6)
            pdf.write(h=th,
                      txt=f'Open "{self.file_path_TL[1:]}" for distributions and '
                          f'graphs of Experiment with TL')

        if self.simulation_CAwSD4WI_values is not None:
            pdf.ln(6)
            pdf.write(h=th,
                      txt=f'Open "{self.file_path_CAwSD4WI[1:]}" for distributions '
                          f'and graphs of Experiment with CAwSD4WI')

        pdf.ln(12)
        pdf.write(h=th, txt="RN - Reservation Nodes")
        pdf.ln(6)
        pdf.write(h=th, txt="TL - Traffic Lights")
        pdf.ln(6)
        pdf.write(h=th, txt="CAwSD4WI - Collision Avoidance with Safe "
                            "Distance and 4 Way Intersection")

        file_path = "../" + self.file_path.split("/")[1] + "/"

        pdf.output(f"{file_path}Experiment_Summary.pdf", "F")

        if self.simulation_TL_values is not None and \
                self.simulation_CAwSD4WI_values is not None:
            self.draw_metrics_plots()

    def draw_metrics_plots(self):

        file_path = "../" + self.file_path.split("/")[1] + "/"

        data = [self.experiment_values,
                self.simulation_TL_values,
                self.simulation_CAwSD4WI_values]

        plt.figure(figsize=(10, 10))
        labels = ['RN', 'TL', 'CAwSD4WI']

        for i in range(8):
            ax = plt.subplot(3, 3, i + 1)
            values = [data[0][i], data[1][i], data[2][i]]
            if i == 0:
                plt.title('Congestion')
            if i == 1:
                plt.title('Occurred Collisions')
            if i == 2:
                plt.title('Braked Cars per Min')
            if i == 3:
                plt.title('Average Safe Distance (AV)')
            if i == 4:
                plt.title('Average Safe Distance (HV)')
            if i == 5:
                plt.title('Capacity AV - car(s) / min')
            if i == 6:
                plt.title('Capacity HV - car(s) / min')
            if i == 7:
                plt.title('Total Simulation Time (s)')

            plt.bar(labels, values)

            plt.tight_layout(pad=2)
            plt.savefig(f"{file_path}Experiment_Summary.png")

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
            ["~ Reservation Nodes C.A Control ~", (550, 125)],
            ["Cars braked:", (550, 160)],
            ["Congestion:", (550, 187)],
            ["Occurred Collisions:", (550, 214)],
            # ["Reservation Nodes Schematic", (550, 250), 16, "#0000FF",
            #  "font-family: Lucida Sans Unicode, Sans-serif; text-decoration: "
            #  "underline"],
            ["HOW TO USE", (550, 550), 15, "#0000FF",
             "font-family: Lucida Sans Unicode, Sans-serif; text-decoration: "
             "underline"],
            ["Features/Inclusions", (550, 580), 15, "#0000FF",
             "font-family: Lucida Sans Unicode, Sans-serif; text-decoration: "
             "underline"],
            ["Experiment Summary (PDF)", (550, 610), 15, "#0000FF",
             "font-family: Lucida Sans Unicode, Sans-serif; text-decoration: "
             "underline"],
            ["Experiment with previous methods", (550, 650), 15],
            ["➤", (550, 680), 15],
            ["Experiment w/ Traffic Lights", (570, 680), 15, "#0000FF",
             "font-family: Lucida Sans Unicode, Sans-serif; text-decoration: "
             "underline"],
            ["➤", (550, 710), 15],
            ["Experiment w/ Safe Distance &", (570, 710), 15, "#0000FF",
             "font-family: Lucida Sans Unicode, Sans-serif; text-decoration: "
             "underline"],
            ["4-Way Intersection Collision Control", (570, 735), 15, "#0000FF",
             "font-family: Lucida Sans Unicode, Sans-serif; text-decoration: "
             "underline"],
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

        self.__scene.add(Line(start=([155, 475]),
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
        self.environment.draw(canvas=self.__frame, offset=self.__min_bound)

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
            [f"{round(self.__current_time, 2)}", (240, 290)],
            [f"{len(self.environment.cars_braked)}", (665, 160)],
            [f"{self.environment.collisions_prevented}", (725, 187)],
            [f"{self.environment.occurred_collisions}", (725, 214)],
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
                                  style=style))

        self.__frame.save()

    def __start_simulation(self):
        self.__calculate_layout()

        if isinstance(self.environment, Environment):
            self.__reporter = StatisticsReporter(self.environment)

        # Drawing prep
        for frame in os.listdir(self.__drawing_directory):
            os.remove(self.__drawing_directory + frame)
        self.__draw_current(self.__current_time)

        print("AVHV Control with Reservation Nodes - Please wait for a "
              "while...")

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
                    print(debug)

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
                    self.av_averages_safe_distance = 0

                try:
                    self.hv_averages_safe_distance += \
                        round(self.hv_total_safe_distance / (len(
                            hv_objects)), 2)
                except ZeroDivisionError:
                    self.hv_averages_safe_distance = 0

                try:
                    self.no_label_averages_safe_distance += \
                        round(self.no_label_total_safe_distance / (len(
                            no_label_objects)), 2)
                except ZeroDivisionError:
                    self.no_label_averages_safe_distance = 0

                # print([car.safe_distance for car in self.av_list])
            self.__current_time += self.__time_increment
            self.__draw_current(self.__current_time)

            progress_bar.update(self.__time_increment)

        progress_bar.close()

        if self.normal_dist is not None and self.file_names[0] is not None and \
                self.file_names[1] is not None:
            for file_name in self.file_names:
                try:
                    self.normal_dist.read_csv(file_name)
                except:
                    pass
                print(f'Open "{self.file_path}" for distributions and graphs')

        try:
            self.av_average_safe_distance = round(
                self.av_averages_safe_distance / (self.__running_time / \
                                                  self.__time_increment))
        except ZeroDivisionError:
            self.av_average_safe_distance = 0.0

        try:
            self.hv_average_safe_distance = round(
                self.hv_average_safe_distance / (self.__running_time / \
                                                  self.__time_increment))
        except ZeroDivisionError:
            self.hv_average_safe_distance = 0.0

        try:
            self.no_label_averages_safe_distance = round(
                self.no_label_averages_safe_distance / (self.__running_time / \
                                                        self.__time_increment))
        except ZeroDivisionError:
            self.no_label_average_safe_distance = 0.0

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

        try:
            average_braked_cars = round(self.total_braked_cars * 60 /
                                        (self.__running_time /
                                         self.__time_increment),
                                        2)
        except ZeroDivisionError:
            average_braked_cars = 0.0

        self.experiment_values = [self.environment.collisions_prevented,
                                  self.environment.occurred_collisions,
                                  average_braked_cars,
                                  round(self.av_average_safe_distance, 2),
                                  round(self.hv_average_safe_distance, 2),
                                  round(self.throughput_capacity_av, 2),
                                  round(self.throughput_capacity_hv, 2),
                                  round(self.__running_time, 2)]


if __name__ == '__main__':
    print(
        "Ekene's Simulation, please create a Simulation and add an Environment")
