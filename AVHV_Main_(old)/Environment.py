from AVHV_Main.Car import Car
from AVHV_Main.CarSpawner import CarSpawner
from AVHV_Main.Intersection import Intersection
from AVHV_Main.PedestrianSystem import PedestrianSystem
from AVHV_Main.RoadSystem import RoadSystem
from AVHV_Main.TrafficLight import TrafficLight
from AVHV_Main.Vector2 import Vector2


class Environment:

    def __init__(self, name, layout):
        self.total_cars_percent = 100
        self.name = name
        if not isinstance(layout, dict):
            layout = {layout.__class__: layout}
        if not layout.get(RoadSystem):
            layout[RoadSystem] = RoadSystem([], {})
        if not layout.get(PedestrianSystem):
            layout[PedestrianSystem] = PedestrianSystem([], {})
        self.layout = layout
        # Environment Objects
        self.environment_objects = {
            # Inanimate Objects
            Intersection: [],
            TrafficLight: [],
            CarSpawner: [],
            # Animate Objects
            Car: []
        }
        self.road_system = layout.get(RoadSystem)
        self.pedestrian_system = layout.get(PedestrianSystem)

    def draw(self, canvas, offset=None):
        if offset is None:
            offset = Vector2()
        for environment_object_type, environment_object_group in self.environment_objects.items():
            for environment_object in environment_object_group:
                environment_object.draw(canvas=canvas, offset=offset)

    def update(self, delta_time, record=False):
        output = ''
        # For each
        for environment_object_type, environment_object_group in self.environment_objects.items():
            for environment_object in environment_object_group:
                # Update
                environment_object.update(delta_time, record=record)
                # Increment Output
                output += "\n" + environment_object.get_info()
        # Record Values
        if record:
            self.record_values(delta_time)

        return output

    def add_objects(self, environment_objects):
        if not isinstance(environment_objects, list):
            environment_objects = [environment_objects]
        for environment_object in environment_objects:
            if environment_object.car_ratio is not None:
                if environment_object.name == 'GentleCar':
                    self.total_cars_percent += environment_object.car_ratio
                elif environment_object.name == 'AggressiveCar':
                    self.total_cars_percent += environment_object.car_ratio
            environment_object.total_cars_percent = self.total_cars_percent
            environment_object.set_environment(self)

            if not self.environment_objects.get(type(environment_object)):
                self.environment_objects[type(environment_object)] = []
            self.environment_objects[type(environment_object)].append(environment_object)
        return self

    def get_object(self, class_name, name):
        for environment_object in self.environment_objects[class_name]:
            if environment_object.name == name:
                return environment_object

    def record_values(self, t):
        for environment_object_type, environment_object_group in self.environment_objects.items():
            for environment_object in environment_object_group:
                environment_object.data_update(t)
