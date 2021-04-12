from AVHV_Main.RoadNode import RoadNode
from AVHV_Main.Vector2 import Vector2
from AVHV_Main._EnvironmentObject import EnvironmentObject

from svgwrite import Drawing
from svgwrite.shapes import *


class TrafficLight(EnvironmentObject):

    def __init__(self, name=None, position=None, size=None, direction=None, traffic_node=None, timings=None,
                 timer=None, distance=None, throughput=None):
        if size is None:
            size = [20, 60]
        # Timings
        if timings is None:
            timings = [5, 1]
        if timer is None:
            timer = 0
        if distance is None:
            distance = 100
        self.cars = [4000]
        self.max_queue = 30
        if len(self.cars) > self.max_queue:
            self.max_queue = len(self.cars)
            # self.throughput = 100

        super(TrafficLight, self).__init__(name=name, position=position, size=size, direction=direction)
        self.traffic_node = traffic_node
        # Lights
        self.cycle = [
            [True, False, False],  # Green
            [False, True, False],  # Amber
            [False, False, True],  # Red
            [False, True, True]  # Red and Amber
        ]
        self.green, self.amber, self.red = self.cycle[0]
        self.phase = 0
        self.timings = timings
        self.timer = timer
        self.change(0)
        self.distance = distance

        # self.position = position
        self.lane = None
        self.count_cars = 0

    def set_environment(self, environment):
        super(TrafficLight, self).set_environment(environment=environment)
        if not isinstance(self.traffic_node, RoadNode):
            self.traffic_node = self.environment.road_system.node(self.traffic_node)
        if isinstance(self.traffic_node, RoadNode):
            self.traffic_node.traffic_light = self
            self.position = Vector2(
                [self.traffic_node.position.x + self.position.x, self.traffic_node.position.y + self.position.y])

    def set(self, phase=None):
        self.phase = (self.phase + 1 if phase is None else phase if isinstance(phase, int) else 0) % len(self.cycle)
        (self.green, self.amber, self.red) = self.cycle[self.phase % len(self.cycle)]

    def change(self, t):
        self.timer += t
        while self.timer >= self.timings[self.phase % len(self.timings)]:
            self.timer -= self.timings[self.phase % len(self.timings)]
            self.set()

    def behaviour_update(self, t):
        super(TrafficLight, self).behaviour_update(t)
        self.change(t)

    def car_queue_length(self):

        return len(self.cars)

    def traffic_light_decision(self, lane):
        self.lane = lane

    def lane_to_obey(self, car_queue_length, time):
        if self.car_queue_length() > 20 and self.car.idle_time < 10:
            pass  # Increment
        else:
            pass  # Do not increment
        self.count_cars += 1

    def get_info(self):
        return str.format(
            '{:s} {:10s} {:10s} {:10s} {:s} {:s}',
            super(TrafficLight, self).get_info(),
            'Red' if self.red else '',
            'Amber' if self.amber else '',
            'Green' if self.green else '',
            'Queue Length : ' + str(self.car_queue_length()),
            'Cars that pass :' + str(self.count_cars),
        )

    def draw(self, canvas, offset, rectangle=None, r=None):

        # if self.direction == 90 or self.direction == 270:
        #     canvas.add(Rect(
        #         insert=((self.position.draw(offset=offset).x - self.size.x / 2),
        #                 (self.position.draw(offset=offset).y - self.size.y / 2)),
        #         size=(self.size.x, self.size.y),
        #         fill="#222222"
        #     ))
        #
        #     def draw_light(active_color, inactive_color, active, location):
        #         canvas.add(Circle(
        #             fill=active_color if active else inactive_color,
        #             center=location,
        #             r=self.size.y * 0.4
        #         ))
        #
        #     draw_light("#E6342F", "#350604", self.red,
        #                (self.position.draw(offset=offset).x - self.size.x / 3, self.position.draw(offset=offset).y))
        #     draw_light("#E69C2F", "#422A05", self.amber,
        #                (self.position.draw(offset=offset).x, self.position.draw(offset=offset).y))
        #     draw_light("#32AD51", "#0B4219", self.green,
        #                (self.position.draw(offset=offset).x + self.size.x / 3, self.position.draw(offset=offset).y))
        # else:
        canvas.add(Rect(
            insert=((self.position.draw(offset=offset).x - self.size.x / 2),
                    (self.position.draw(offset=offset).y - self.size.y / 2)),
            size=(self.size.x, self.size.y),
            fill="#222222"
        ))

        def draw_light(active_color, inactive_color, active, location):
            canvas.add(Circle(
                fill=active_color if active else inactive_color,
                center=location,
                r=self.size.x * 0.4
            ))

        draw_light("#E6342F", "#350604", self.red, (
            self.position.draw(offset=offset).x, self.position.draw(offset=offset).y - self.size.y / 3))
        draw_light("#E69C2F", "#422A05", self.amber,
                   (self.position.draw(offset=offset).x, self.position.draw(offset=offset).y))
        draw_light("#32AD51", "#0B4219", self.green, (
            self.position.draw(offset=offset).x, self.position.draw(offset=offset).y + self.size.y / 3))
        super(TrafficLight, self).draw_direction(canvas=canvas, offset=offset)
