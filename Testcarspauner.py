import unittest
from operator import pos

from AVHVCONTROL.Simulator import *
from AVHVCONTROL.test import TestPhysics
from AVHVCONTROL.test import RoadSystemToolbox
from numpy import random

from AVHVCONTROL.test.Test_2 import simulation


class CarSpawner:
    _InanimateObject = []  # new car arrivals to grow the queue length

    def CarSpawn(self, name, node, direction, safe_distance=None):
        if safe_distance is None:
            safe_distance = 30
        self.node = node
        super(CarSpawner, self).__init__(name=name, position=self.node.position, direction=direction)
        self.cars = []
        self.safe_distance = safe_distance

    def update(self, t):
        super(CarSpawner, self).update(t)
        # If no cars have been spawned
        if len(self.cars) <= 0:
            # Spawn a new car
            self.spawn_another_car()
        else:
            # Otherwise, get the last car that was spawned
            last_car = self.cars[-1]
            # Check that the car is actually a car (this should always be the case)
            if isinstance(last_car, Car):
                # Set the distance to the car as the distance between the spawner and the car
                distance_to_last_car = self.position.distance(last_car.position)
                # If the distance to the car is greater than the minimum safe distance, it's safe to spawn a car
                if distance_to_last_car >= self.safe_distance:
                    # Spawn another car
                    self.spawn_another_car()


if __CarSpawn == '__main__':
    CarSpawn = CarSpawn()
    print('Car CarSpawn = ', set.CarSpawn('car'))
    print('car with is 0 is ', set.CarSpawn(0))
