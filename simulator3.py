"""
    phd-autonomous-cars-frank
"""
# Operating System
import os
import math
# Maths
import random
import numpy as np
# Drawing
import matplotlib.pyplot as plt
from svgwrite import Drawing
from svgwrite.shapes import *


class TrafficNode:
    def __init__(self, name, location=None):
        if location is None:
            location = [0, 0]
        self.__name = name
        self.__location = location
        self.destination_nodes = {}
        self.via = {}

    def name(self):
        return self.__name

    def location(self):
        return 1 * self.__location

    def x(self):
        return self.__location[0]

    def y(self):
        return self.__location[1]

    def check(self, node):
        if isinstance(node, TrafficNode):
            return self.location() == node.location() and self.__name == node.name
        return False

    def get_info(self):
        output = str.format("{:7s} [{:3d}, {:3d}]", self.name(), self.x(), self.y())
        return output + str(self.destination_nodes)

    def draw(self, canvas):
        if isinstance(canvas, type(Drawing())):
            canvas.add(Circle(center=self.__location, r=5, fill='blue'))
            for node in self.__connections:
                canvas.add(Line(
                    start=self.location(),
                    end=node.location(),
                    stroke='aqua',
                    stroke_width=2
                ))


class RoadSystem:
    def __init__(self):
        self.__nodes = {}

    def get_nodes(self):
      return self.__nodes

    def node(self, name):
        for node in self.__nodes:
            if node.name() == name:
                return node
        return None

    def add_nodes(self, nodes=None):
        for n in nodes:
          self.__nodes[n.name()] = n

    def add_roads(self, roads=None):
      for node in roads:
        n = self.__nodes[node]
        if not n:
          print("Error couldn't find the node " + n)
          return
        n.destination_nodes = roads[node]
        n.via = { r : r for r in roads[node]}
      # compute the routing table iteratively
      updated = True
      while updated:
        updated = False
        for node in roads:
          n = self.__nodes[node]
          for r in roads[node]:
            neighbor = self.__nodes[r]
            for v in neighbor.via:
              if v not in n.via:
                updated = True
                n.via[v] = r
      # finalize by replacing the routing table with the objects
      #nodes = self.__nodes
      #for node in roads:
      #  r = { nodes[n] for n in nodes[node].via}
      #  nodes[node].via = r
      #  print(r)

    def print_system(self):
        print("\n\n\n\nNODE INFO")
        for n in self.__nodes:
            print(self.__nodes[n].get_info())

    def draw(self, canvas):
        for node in self.__nodes:
            node.draw(canvas)

class _EnvironmentObject:

    def __init__(self, name=None, position=None, size=None):
        # Default Environment Object name is "Environment Object"
        if name is None:
            name = "Environment Object"
        # Default Position is [0, 0]
        if position is None:
            position = [0, 0]
        if size is None:
            size = [10, 10]
        # Set Values
        self.name = name
        self.position = position
        self.size = size

        # Initialise Data Collector
        self.data = {}
        self.data.update({'time': []})
        self.data.update({'position': []})
        self.environment = None

    def update(self, t):
        # Ignore Update for Abstract Class
        pass

    def get_info(self):
        # Return Position and Size as Default Information
        return (
                str.format("{:12s}", self.name) +
                self._format_components("Position", self.position[0], self.position[1]) +
                self._format_components("Size", self.size[0], self.size[1])
        )

    def write_data(self, t):
        # Update the Data Collector with Values for Time and Position
        self.data['time'].append(t)
        self.data['position'].append(self.position)

    def _format_components(self, name='', val_x=0, val_y=0):
        # Formatter for get_info()
        return str.format('{:<32s}', str.format(
            '{:12s} [{:.2f}, {:.2f}]',
            name,
            val_x,
            val_y
        ))

    def check_overlap(self, colliding):
        # Check if Objects are Colliding / Overlapping by Cropping infinite areas around the object away.
        # If the flow is not stopped by any check, then the objects are colliding
        """This method checks if this object and the other object overlaps, which could be a crash for cars and stuff"""
        # Crop the left side
        if colliding.position[0] + colliding.size[0] < self.position[0]:
            return False
        # Crop the bottom side
        if colliding.position[1] + colliding.size[1] < self.position[1]:
            return False
        # Crop the right side
        if self.position[0] + self.size[0] < colliding.position[0]:
            return False
        # Crop the top side
        if self.position[1] + self.size[1] < colliding.position[1]:
            return False
        return True

    def draw(self, canvas):
        if isinstance(canvas, type(Drawing())):
            canvas.add(Circle(
                center=self.position,
                r=self.size[0],
                fill='red'
            ))


class _AnimateObject(_EnvironmentObject):
    def __init__(self,
                 # Environment Object Values
                 name=None, position=None, size=None,
                 # Kinematic Values
                 velocity_x=0, velocity_y=0, acceleration_x=0, acceleration_y=0,
                 mass=0, friction=0, drag_area=0, gravity=9.81
                 ):
        # Super init abstract parent values
        super(_AnimateObject, self).__init__(name, position, size)
        # Animate Object Values
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.acceleration_x = acceleration_x
        self.acceleration_y = acceleration_y
        self.mass = mass
        self.friction = friction
        self.drag_area = drag_area
        self.gravity = gravity

    def update(self, t):
        # Calculate Drag - Not currently working
        # TODO Fix Calculation of Drag
        # self.apply_force(self._calculate_drag(time), self.direction()-180 , time)

        # Override super.update() and calculate the kinematics of the object
        self.update_velocity(t)  # Increment Velocity by Acceleration
        self.update_position(t)  # Increment Position by Velocity

    def write_data(self, t):
        # Update Data Collector with Default Values and Kinematic Values
        super(_AnimateObject, self).write_data(t)
        self.data['velocity'].append([self.velocity_x, self.velocity_y])
        self.data['acceleration'].append([self.acceleration_x, self.acceleration_y])

    def update_velocity(self, t):
        # Adjust velocity by acceleration relative to how much time has passed
        self.velocity_x += self.acceleration_x * t
        self.velocity_y += self.acceleration_y * t

    def update_position(self, t):
        # Adjust position by velocity relative to how much time has passed
        self.position[0] += self.velocity_x * t
        self.position[1] += self.velocity_y * t

    def get_info(self):
        return str.format(
            "{:s} {:s} {:s}",
            # (Object Info (Position)), Velocity, Acceleration
            super(_AnimateObject, self).get_info(),
            self._format_components('Velocity', self.velocity_x, self.velocity_y),
            self._format_components("Acceleration", self.acceleration_x, self.acceleration_y)
        )

    def apply_force(self, magnitude, direction):
        # Fix Values
        if magnitude < 0:
            magnitude *= -1
            direction -= 180
        while direction < 0:
            direction += 360
        # Apply force in a direction (changed from Degrees to Radians)
        self.acceleration_x += math.sin((math.pi / 180) * direction) * (magnitude / self.mass)
        self.acceleration_y += math.cos((math.pi / 180) * direction) * (magnitude / self.mass)

    def direction(self):
        # Calculate direction of travel based on velocity
        return math.atan2(self.velocity_x, self.velocity_y)

    def _calculate_drag(self, t):
        # Apply a force in the opposite direction to travel.
        friction = self.friction * (self.gravity / 2)
        air_resistance = (self.drag_area / 2) * self.get_speed() ** 2
        return (friction + air_resistance) * t

    def get_speed(self):
        # Calculate magnitude of velocity components added using pythagoras' theorem
        return math.sqrt(self.velocity_x ** 2 + self.velocity_y ** 2)


class Car(_AnimateObject):
    def __init__(self, name=None, position=None, size=None, mass=1600, friction=12, drag_area=24, autonomous=True, human_driven=True, start_node=None, target_node=None):
        super(Car, self).__init__(
            name=name, position=position, size=size, mass=mass, friction=friction, drag_area=drag_area
        )
        self.length = 10

        self.direction = 0
        self.turning_angle = 0

        if autonomous and human_driven:
            autonomous = False
        if not (autonomous or human_driven):
            autonomous = True

        self.autonomous = autonomous
        self.human_driven = human_driven
        self.start_node=start_node
        self.target_node=target_node
        self.current_node=start_node

        self.data.update({'velocity': []})
        self.data.update({'acceleration': []})

    def get_centripetal_force(self):
        return (self.mass * math.sqrt(self.velocity_x ** 2 + self.velocity_y ** 2)) / self.get_radius_of_turn()

    def get_radius_of_turn(self):
        return (self.length / 2) * math.tan(math.pi / 4 - self.turning_angle)

    def turn(self, turning_angle_adjustment):
        self.turning_angle -= turning_angle_adjustment

    def reset_turn(self):
        self.turning_angle = 0

    def turn_to_node(self):
        nodes = self.environment.road_system.get_nodes()
        # The simulator should do:
        # if car.target_node == car.current_node:
        # remove the car; call a function to update statistics
        next_node = nodes[self.current_node].via[self.target_node]
        try:
          nn_node = nodes[next_node].via[self.target_node]
          nn_node = nodes[self.nn_node]
        except:
          print("The next node is the final target")
          nn_node = None

        next_node = nodes[self.current_node]

        print(str(next_node) + " " + str(nn_node))
        # decide what action TODO to go based on the next_node and the next next node

        # after moving check if you reach the next node, then update self.current_node?
        if next_node.name == "null":
            self.acceleration_x = 0
            self.acceleration_y = 0
            self.velocity_x = 0
            self.velocity_y = 0
        else:
            next_node = next_node.location()
            if math.sqrt((next_node[0] - self.position[0]) ** 2 + (next_node[1] - self.position[1]) ** 2) < 10:
                self.route.next_target()
            angle_to_node = (math.atan2(next_node[0] - self.position[0],
                                        next_node[1] - self.position[1]) * 180 / math.pi) - self.direction
            self.direction += angle_to_node

    def apply_force(self, magnitude, direction=0):
        self.direction = direction
        super(Car, self).apply_force(magnitude, self.direction)

    def update(self, t):
        self.turn_to_node()

        self.apply_force(1000, self.direction)
        # self.direction += self.turning_angle * t

        # Override Velocity Updates direction
        (self.acceleration_x, self.acceleration_y) = \
            self.redirect(self.acceleration_x, self.acceleration_y, self.direction)
        self.velocity_x += self.acceleration_x * t
        self.velocity_y += self.acceleration_y * t
        (self.velocity_x, self.velocity_y) = \
            self.redirect(self.velocity_x, self.velocity_y, self.direction)
        self.update_position(t)

    def draw(self, canvas):
        super(Car, self).draw(canvas)
        #self.route.draw(canvas)

    def redirect(self, x, y, direction):
        direction *= (math.pi / 180)
        a = x * x
        b = y * y
        magnitude = a + b
        magnitude = math.sqrt(magnitude)
        return [magnitude * math.sin(direction), magnitude * math.cos(direction)]

    def get_info(self):
        return str.format("{:s} {:s} [{:s} {:s}] ",
                          super(Car, self).get_info(),
                          self._format_components("Direction", self.direction, 0),
                          "AV" if self.autonomous else " ",
                          "HV" if self.human_driven else " "
                          )


class _InanimateObject(_EnvironmentObject):

    def __init__(self, name=None, position=None, size=None):
        super(_InanimateObject, self).__init__(name=name, position=position, size=size)

    def update(self, t):
        pass


class TrafficLight(_InanimateObject):

    def __init__(self, name=None, position=None, red=False, amber=False, green=False):
        super(TrafficLight, self).__init__(name=name, position=position)
        self.red = red
        self.amber = amber
        self.green = green

    def update(self, t):
        pass

    def get_info(self):
        return str.format(
            '{:s} {:10s} {:10s} {:10s}',
            super(TrafficLight, self).get_info(),
            'Red' if self.red else '',
            'Amber' if self.amber else '',
            'Green' if self.green else ''
        )


class Intersection(_InanimateObject):

    def __init__(self, name=None, position=None, size=None, lanes=None):
        super(Intersection, self).__init__(
            name=name,
            position=position,
            size=size
        )
        self.lanes = lanes

    def update(self, t):
        pass


class Environment:

    def __init__(self, road_system, name=None):
        self.name = name
        # Environment Objects
        self.environment_objects = {
            # Inanimate Objects
            Intersection.__name__: [],
            TrafficLight.__name__: [],
            # Animate Objects
            Car.__name__: []
        }
        self.road_system = road_system

    def getCars(self):
        return self.environment_objects["Car"]

    def getObjects(self, _type):
        for __type, __environment_objects in self.environment_objects.items():
            if _type is __type:
                return __environment_objects

    def getIntersections(self):
        return self.environment_objects["Intersection"]

    def update(self, delta_time, record=False, canvas=None):
        output = ''
        # For each
        for environment_object_type, environment_object_group in self.environment_objects.items():
            for environment_object in environment_object_group:
                # Update
                environment_object.update(delta_time)
                # Increment Output
                output += "\n" + environment_object.get_info()
                # Draw to Canvas
                if isinstance(canvas, type(Drawing())):
                    environment_object.draw(canvas)
        # Record Values
        if record:
            self.record_values(delta_time)
            environment_object

        return output

    def add_object(self, environment_object):
      environment_object.environment = self
      self.environment_objects[type(environment_object).__name__].append(environment_object)

    def get_object(self, name):
        for environment_object_type, environment_object_group in self.environment_objects.items():
            for environment_object in environment_object_group:
                if environment_object.name == name:
                    return environment_object

    def record_values(self, t):
        for environment_object_type, environment_object_group in self.environment_objects.items():
            for environment_object in environment_object_group:
                environment_object.write_data(t)


class StatisticsReporter:
    def __init__(self, environment):
        # History
        self.history = {}
        # Records
        self.history.update({'time': []})
        self.history.update({'collisions': []})
        self.history.update({'intersections': []})
        self.environment = environment

    def record(self, t):
        # Time
        self.history['time'].append(t)
        # Values
        self.record_car_collisions()
        self.record_cars_in_intersections()

    def record_car_collisions(self):
        __collisions = []
        for __car_a in self.environment.getCars():
            for __car_b in self.environment.getCars():
                if __car_a is not __car_b:
                    if __car_a.check_overlap(__car_b):
                        __collisions.append([__car_a, __car_b])
                        # print("Collision : " + __car_a.name + ", " + __car_b.name)
        self.history['collisions'].append(__collisions)

    def record_cars_in_intersections(self):
        __intersections = []
        for __car in self.environment.getCars():
            for __intersection in self.environment.getIntersections():
                if __intersection.check_overlap(__car):
                    __intersections.append([__intersection, __car])
                    # print("Intersection : " + __car.name + ", " + __intersection.name)
        self.history['intersections'].append(__intersections)

    def frequency_dumper(self, metric):
        count = []
        for _ in metric:
            count.append(len(_))
        return count

    def calculate_car_collisions(self):
        return np.divide(self.frequency_dumper(self.history['collisions']), 2)

    def calculate_cars_in_intersection(self):
        return self.frequency_dumper(self.history['intersections'])

    def get_data_with_filter(self, set_name, name_filter):
        result = []
        intersection_collisions = self.history[set_name]
        for tick in intersection_collisions:
            tick_result = []
            for collision in tick:
                if collision[0].name == name_filter:
                    tick_result.append(collision)
            result.append(tick_result)
        return result

    def plot_graph_of_collisions(self):
        plt.plot(self.calculate_car_collisions())
        plt.show()

    def plot_graph_of_collisions_vs_intersection(self, intersection_name):
        collisions = []
        # For Each Frame
        for tick in range(0, len(self.history['time'])):
            # Register the Intersection and Collision Snapshot
            intersection_snapshot = self.history['intersections'][tick]
            collisions_snapshot = self.history['collisions'][tick]
            # For Every Intersection Record
            collisions_in_tick = []
            for intersection_record in intersection_snapshot:
                # Data
                intersection = intersection_record[0]
                car = intersection_record[1]
                # Check Intersection is Useful
                if intersection.name == intersection_name:
                    # Check if the Car in the Intersection was involved in any collisions
                    collision = None
                    for collision_record in collisions_snapshot:
                        # Data
                        car_a = collision_record[0]
                        car_b = collision_record[1]
                        # Check if it collided
                        if car_a.name == car.name or car_b.name == car.name:
                            collision = collision_record
                    if collision is not None:
                        collisions_in_tick.append(collision)
            collisions.append(collisions_in_tick)

        count_collisions = self.frequency_dumper(collisions)
        count_cars_in_intersection = self.frequency_dumper(
            self.get_data_with_filter('intersections', intersection_name))

        # Plot
        plt.scatter(count_cars_in_intersection, count_collisions)

    def result(self):
        # Plot
        intersection_names = ["First Intersection", "Second Intersection"]
        title = "Collisions in"
        for intersection_name in intersection_names:
            title += " " + intersection_name + ","
            self.plot_graph_of_intersection_vs_collisions(intersection_name)
            plt.show()

        title = title[:-1]
        plt.title(title)
        plt.xlabel('No of collisions')
        plt.ylabel('No of cars in Intersection')
        plt.savefig(self.environment.name + "_collisions.pdf")


class FileHandler:

    def __init__(self, directory='output'):
        # Init Data
        self.directory = self.fix_directory(directory)
        self.files = []

        # Create Directory
        if not os.path.isdir(directory):
            os.mkdir(directory)
        self.update_files()

    @staticmethod
    def fix_directory(directory):
        if not directory.endswith('/'):
            directory += '/'
        return directory

    def update_files(self):
        self.files = os.listdir(self.directory)

    def list_files(self, display=False):
        self.update_files()
        if display:
            for file in self.files:
                print(file)
        return self.files

    def write_file(self, filename='', file_contents='', sub_directory=''):
        file = open(self.directory + self.fix_directory(sub_directory) + filename, 'w')
        file.write(file_contents)

    def remove_files(self, files, display=False):
        self.update_files()
        if files is None:
            files = self.files
        for file in files:
            if display:
                print('Menus ' + file)
            os.remove(file)
        self.update_files()


class Simulation:

    def __init__(self, environment, time_end=10, time_increment=0.5):
        # Environment
        self.__environment = environment
        # Timing Control
        self.__end_time = time_end
        self.__time_increment = time_increment
        self.__debug_counter = 0
        self.__current_time = 0
        # Statistics
        self.__reporter = None
        # Drawings
        self.__frame = None
        self.__drawing_directory = "drawings/"
        self.__drawing_prefix = "svgwriter_frame_"
        # Start
        self.__start_simulation()

    def __start_simulation(self):
        if self.__environment is not None:
            self.__reporter = StatisticsReporter(self.__environment)
            self.__debug_counter = 0
            self.__current_time = 0
            # Drawing Prep
            for frame in os.listdir(self.__drawing_directory):
                os.remove(self.__drawing_directory + frame)
            # Canvas and Line
            while self.__current_time <= self.__end_time:
                # New Canvas
                self.__frame = Drawing(str.format(
                    "{:s}{:s}{:.2f}{:s}",
                    self.__drawing_directory, self.__drawing_prefix, self.__current_time, ".svg"
                ))
                # Make Blank
                self.__frame.add(Polygon([[0, 0], [0, 600], [600, 600], [600, 0]], fill='black'))

                # Calculate Time Change
                debug = self.__environment.update(delta_time=self.__time_increment, canvas=self.__frame)
                debug = str.format("\nTick : {:3.3f}\t", self.__current_time) + debug

                # Check if Debug should be run
                if self.__debug_counter <= self.__current_time:
                    self.__debug_counter += self.__time_increment
                    # Data Recording
                    self.__environment.record_values(self.__current_time)
                    self.__reporter.record(self.__current_time)
                    # Draw
                    self.__frame.save()

                    # Finish Data Reporting
                # Increment at end
                self.__current_time = self.__current_time + self.__time_increment


def scenario_1():
    road_system = RoadSystem()
    road_system.add_nodes([
        TrafficNode("1", [150, 300]),
        TrafficNode("2", [250, 300]),
        TrafficNode("3", [350, 300]),
        TrafficNode("4", [450, 300]),
        TrafficNode("5", [300, 350]),
        TrafficNode("6", [300, 450]),
        TrafficNode("7", [300, 250]),
        TrafficNode("8", [300, 150]),
    ])
    road_system.add_roads({"1" : {"2"}, "2" : {"3", "4", "7"}, "3" : {"7", "9"}, "7" : {"8"}, "4" : {"5", "7"}})

    environment = Environment(road_system, name="Environment")
    for i in range(0, 4):
        environment.add_object(Car(
            name="Car " + str(i + 1),
            autonomous=random.randint(0, 1) == 0,
            human_driven=random.randint(0, 1) == 0,
            route=["1", "2", "5", "3", "4", "7", "8"]
        ))

    road_system.print_system()
    return environment


def scenario_2():
    road_system = RoadSystem()
    road_system.add_nodes([
        TrafficNode("1", [150, 300]),
        TrafficNode("2", [250, 300]),
        TrafficNode("3", [350, 300]),
        TrafficNode("4", [450, 300]),
        TrafficNode("5", [300, 350]),
        TrafficNode("6", [300, 450]),
        TrafficNode("7", [300, 250]),
        TrafficNode("8", [300, 150]),
    ])
    road_system.add_roads({"1" : {"2"}, "2" : {"3", "4", "7"}, "3" : {"7", "9"}, "7" : {"8"}, "4" : {"5", "7"}})

    environment = Environment(road_system, name="Environment")
    environment.add_object(Car(
        name="Car 1",
        autonomous=False,
        human_driven=True,
        route=["8", "7", "5", "6"]
    ))
    environment.add_object(Car(
        name="Human Car 2",
        autonomous=False,
        human_driven=True,
        route=["1", "2", "3", "4"]
    ))
    environment.add_object(Car(
        name="Car 3",
        autonomous=False,
        human_driven=True,
        route=["1", "2", "5", "3", "4", "7", "8"]
    ))
    environment.add_object(Car(
        name="Car 4",
        autonomous=False,
        human_driven=True,
        route=["1", "2", "3", "5", "2", "1"]
    ))

    road_system.print_system()
    return environment



def scenario_3():
  road_system = RoadSystem()
  road_system.add_nodes([
      TrafficNode("1", [150, 300]),
      TrafficNode("2", [250, 300]),
      TrafficNode("3", [350, 300]),
      TrafficNode("4", [450, 300]),
      TrafficNode("5", [300, 350]),
      TrafficNode("6", [300, 450]),
      TrafficNode("7", [300, 250]),
      TrafficNode("8", [300, 150]),
      TrafficNode("9", [450, 300]),
  ])
  road_system.add_roads({"1" : {"2"}, "2" : {"3", "4", "7"}, "3" : {"7", "9"}, "7" : {"8"}, "4" : {"5", "7"}})

  environment = Environment(road_system, name="Environment")
  environment.add_object(Car(
      name="Car 1",
      autonomous=False,
      human_driven=True,
      start_node="3",
      target_node="9"
  ))
  road_system.print_system()
  return environment


plt.xlim(0, 600)
plt.ylim(0, 600)
Simulation(environment=scenario_3(), time_end=20, time_increment=0.1)
