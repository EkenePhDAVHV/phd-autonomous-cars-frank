#!/usr/bin/env python3
"""
    phd-autonomous-cars-frank
"""

# Operating System
import os
from svgwrite import Drawing
from svgwrite.shapes import *

# create directory if it does not exist
from AVHV_Main.Environment import Environment
from AVHV_Main.StatisticsReporter import StatisticsReporter
from AVHV_Main.Vector2 import Vector2

os.chdir(os.path.dirname(__file__))
if not os.path.exists("drawings"):
    os.mkdir("drawings")


class Simulation:

    def __init__(self, environment, time_end=10, time_increment=0.1, debugging=False):
        # Environment
        self.environment = environment
        # Timing Control
        self.time_end = time_end
        self.__end_time = time_end
        self.time_increment = time_increment
        self.__time_increment = time_increment
        self.__debug_counter = 0
        self.__current_time = 0
        # Statistics
        self.debugging = debugging
        self.__reporter = None
        # Drawings
        self.__frame = None
        self.__scene = Drawing()
        self.__min_bound = Vector2([0, 0])
        self.__max_bound = Vector2([0, 0])
        # File Path
        self.__drawing_directory = "drawings/"
        self.__drawing_prefix = "svgwriter_frame_"
        # Start
        self.__start_simulation()

    def __calculate_blank(self):
        if isinstance(self.environment, Environment):
            layout_nodes = self.environment.road_system.nodes + self.environment.pedestrian_system.nodes
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
        border = 100
        self.__min_bound.x -= border
        self.__min_bound.y -= border
        self.__max_bound.x += border
        self.__max_bound.y += border

        self.__scene = Drawing(
            "blank.svg",
            size=[
                abs(self.__max_bound.x - self.__min_bound.x),
                abs(self.__max_bound.y - self.__min_bound.y)
            ]
        )
        self.__scene.add(Polygon(
            [
                # Bottom Left
                [0, 0],
                # Top Left
                [0, abs(self.__max_bound.y - self.__min_bound.y)],
                # Top Right
                [abs(self.__max_bound.x - self.__min_bound.x), abs(self.__max_bound.y - self.__min_bound.y)],
                # Bottom Right
                [abs(self.__max_bound.x - self.__min_bound.x), 0],
            ],
            fill='white'
        ))

    def __calculate_layout(self):
        self.__calculate_blank()
        for layout_type, layout in self.environment.layout.items():
            layout.draw_edges(canvas=self.__scene, offset=self.__min_bound)
        for layout_type, layout in self.environment.layout.items():
            layout.draw_nodes(canvas=self.__scene, offset=self.__min_bound)
        for layout_type, layout in self.environment.layout.items():
            layout.draw_text(canvas=self.__scene, offset=self.__min_bound)
        self.__scene.add(self.__scene.text("Press SPACEBAR' to simulate and LEFT and RIGHT Arrow keys to move "
                                           "between frames", insert=(70, 50), font_size=18,
                                           fill='#000000'))

    def __draw_current(self, timestep):
        # New Canvas
        self.__frame = self.__scene.copy()
        self.__frame.filename = str.format(
            "{:s}{:s}{:.2f}{:s}",
            self.__drawing_directory, self.__drawing_prefix, timestep, ".svg"
        )
        # Draw Elements and Save
        self.environment.draw(canvas=self.__frame, offset=self.__min_bound)
        self.__frame.save()

    def __start_simulation(self):
        self.__calculate_layout()
        if isinstance(self.environment, Environment):
            self.__reporter = StatisticsReporter(self.environment)
            self.__debug_counter = 0
            self.__current_time = 0
            # Drawing Prep
            for frame in os.listdir(self.__drawing_directory):
                os.remove(self.__drawing_directory + frame)
            self.__draw_current(self.__current_time)
            # Canvas and Line
            print("Please be patient")
            while self.__current_time < self.__end_time:

                percent_complete = round(self.__current_time/self.__end_time * 100, 2)
                if percent_complete % 1.0 == 0:
                    print("Simulating:", percent_complete, "% done")

                # Calculate Time Change
                debug = self.environment.update(delta_time=self.__time_increment, record=False)
                debug = str.format("\nTick : {:3.3f}\t", self.__current_time) + debug
                # Check if Debug should be run
                if self.__debug_counter <= self.__current_time:
                    self.__debug_counter += self.__time_increment
                    # Data RecordingpendingCars
                    self.environment.record_values(self.__current_time)
                    self.__reporter.record(self.__debug_counter)
                    if self.debugging:
                        pass

                    # Finish Data Reporting
                # Increment at end
                self.__current_time = self.__current_time + self.__time_increment
                self.__draw_current(self.__current_time)


if __name__ == '__main__':
    print("Ekene's Simulation, please create a Simulation and add and Environment")
