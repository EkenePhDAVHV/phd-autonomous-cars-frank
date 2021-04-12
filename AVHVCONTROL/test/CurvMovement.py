# imports
from AVHVCONTROL.test.TestPhysics import PhyicsTest, CurveMovement
from AVHVCONTROL.Simulator import *
from AVHVCONTROL.test import RoadSystemToolbox, LayoutLis
from AVHVCONTROL.test import TestPhysics
from AVHVCONTROL.Simulator import Environment

# Car object
car = Car(name="Car 1", route=[1, 2, 18, 19], direction=360, easy_physics=False,
          velocity=0, velocity_max=20,
          acceleration=0, acceleration_max=2, position=[0, 0])
# car.turn(360)
print(car.turning_angle)
# Car in curved movement
curve_movement = CurveMovement(time=2, car=car, radius=4, curveCenter=[3, 3],
                               startDegree=0, endDegree=360)
simulation = Simulation(
    debugging=False,
    time_end=20,
    time_increment=0.1,
    environment=Environment(
        name="test_Car_Movement",
        layout=LayoutList.cross_roads()
    ).add_objects([
        TrafficLight(name="Left Traffic Light   ", traffic_node=2,
                     direction=0, timings=[4, 1], timer=0),
        TrafficLight(name="Right Traffic Light ", traffic_node=4, direction=0,
                     timings=[4, 1], timer=0,
                     position=[+20, +40]),
        TrafficLight(name="Top Traffic Light   ", traffic_node=6, direction=0,
                     timings=[4, 1], timer=5,
                     position=[+80, -112]),
        TrafficLight(name="Bottom Traffic Light", traffic_node=8, direction=0,
                     timings=[4, 1], timer=5,
                     position=[-60, -10]),
        car
    ])
)
car = simulation.environment.environment_objects[Car][0]
time = car.data['time']
velocity = car.data['velocity']
speed = car.data['speed']
speed_list = []
for i in range(0, len(velocity)):
    speed = math.sqrt(velocity[i].x * velocity[i].x + velocity[i].y *
                      velocity[i].y)
    speed_list.append(speed)
    # print(str.format("{:f} - {:f}, {:f}, {:f}", time, velocity.x, velocity.y))
print(speed)
print(type(time))
print(type(velocity))
print(type(speed_list))
plt.title("Speed / Time Graph " + car.name)
plt.xlabel('Time(s)')
plt.ylabel('Speed (m/s)')
plt.plot(time, speed_list)
plt.show()
