import unittest

from AVHVCONTROL.Simulator import *
from AVHVCONTROL.physics.physics import *
from AVHVCONTROL.test import RoadSystemToolbox
from numpy import random

from AVHVCONTROL.test.Test_2 import simulation


class SingleStreetTest(unittest.TestCase):
    car = Car(
        name="Car",
        route=[1, 2, 3, 4, 5],
        acceleration_max=1,
        speed_max=10,
        deacceleration_max=-1,
        mass=1000,
    )

    env = Environment(
        name="Test 3",
        layout=RoadSystemToolbox.RoadSystemToolbox.singleStreet(),
        physics=SimplePhysics()
    ).add_objects([
        TrafficLight(name="Left Traffic Light  ", traffic_node=3, direction=90, timings=[3, 1])
    ]).add_objects(
        car
    )

    def test_step1(self):
      Simulation(debugging=False,time_end=1,time_increment=1,environment=self.env)
      self.assertEqual(self.car.position.x, -999.0)
      Simulation(debugging=False,time_end=1,time_increment=1,environment=self.env)
      self.assertEqual(self.car.position.x, -997.0)
      Simulation(debugging=False,time_end=1,time_increment=1,environment=self.env)
      self.assertEqual(self.car.position.x, -994.0)

    def test_step10(self):
      Simulation(debugging=False,time_end=1,time_increment=10,environment=self.env)
      self.assertEqual(self.car.position.x, -999.0)
      Simulation(debugging=False,time_end=1,time_increment=10,environment=self.env)
      self.assertEqual(self.car.position.x, -997.0)
      Simulation(debugging=False,time_end=1,time_increment=10,environment=self.env)
      self.assertEqual(self.car.position.x, -994.0)

    def step2(self):
      Simulation(debugging=False,time_end=5,time_increment=1,environment=self.env)
      self.assertEqual(self.car.position.x, 105.0)

SimplePhysics = simulation.environment.environment_objects[Car][0].data["position"]
u =0.6,
Engineforce =214,
C_drag = 0.5
pos = [0, 0]
v = velocity = [3,0]
f_traction = u * Engineforce
c_rr = C_drag * 30

speed = math.sqrt(v.pos.x * velocity.pos.x + velocity.pos.y *velocity.pos.y);
f_drag = - C_drag * velocity * speed
f_drag.pos.x = -C_drag * v.pos.x * speed ;
f_drag.pos.y = -C_drag * v.pos.y * speed ;

f_rr = -c_rr * velocity

f_long = f_traction + f_drag + f_rr


if __name__ == '__main__':
    unittest.main()
