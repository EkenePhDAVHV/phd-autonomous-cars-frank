from AVHV_Main.AVHV_CAwSD4WI.Car import Car
from AVHV_Main.AVHV_CAwSD4WI.Intersection import Intersection

import matplotlib.pyplot as plt


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
        collisions = []
        for car_a in self.environment.environment_objects[Car]:
            for car_b in self.environment.environment_objects[Car]:
                if car_a is not car_b:
                    if car_a.is_colliding(car_b):
                        collisions.append([car_a, car_b])
        self.history['collisions'].append(collisions)

    def record_cars_in_intersections(self):
        intersections = []
        for car in self.environment.environment_objects[Car]:
            for intersection in self.environment.environment_objects[Intersection]:
                if intersection.is_colliding(car):
                    intersections.append([intersection, car])
        self.history['intersections'].append(intersections)

    @staticmethod
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
