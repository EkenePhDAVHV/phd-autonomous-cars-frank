# Imports
import numpy as np
import matplotlib.pyplot as plt
from AVHVCONTROL.Simulator import Simulation, Environment, Car, TrafficLight, Vector2, \
    Aggressive_Car, Gentle_Car, CarSpawner, RoadSystem
from AVHVCONTROL.test import LayoutList, TestPhysics

#car = Car(name="Car 1", route=[1, 2, 6, 7], direction=100)
#ag_car = Aggressive_Car(name="Car 1", route=[1, 2, 4, 5], direction=100)
#gentle_car = Gentle_Car(name="Car 1", route=[1, 2, 4, 5], direction=100)
layout = LayoutList.cross_roads()
# Create Simulation
simulation = Simulation(
    debugging=True,
    time_end=30,
    time_increment=1.5,
    physics=TestPhysics.CurveMovement(
        time=1, car=CarSpawner, radius=3, curveCenter=5, startDegree=90, endDegree=360
    ),
    environment=Environment(
        name="Test collision",
        layout=layout
    ).add_objects([
        TrafficLight(name="Left Traffic Light  ", traffic_node=2, direction=270, timings=[4, 1], timer=0),
        TrafficLight(name="Right Traffic Light ", traffic_node=4, direction=90, timings=[4, 1], timer=0,
                     position=[+20, +40]),
        TrafficLight(name="Top Traffic Light   ", traffic_node=6, direction=0, timings=[4, 1], timer=5,
                     position=[+80, -112]),
        TrafficLight(name="Bottom Traffic Light", traffic_node=8, direction=180, timings=[4, 1], timer=5,
                     position=[-60, -10]),
        CarSpawner(
            name="AggressiveCar",
            node=layout.get(RoadSystem).node(5),
            direction=360,
            safe_distance=100,
            route=[5, 4, 8, 9]
        ),
    ])
)
cars = simulation.environment.environment_objects[Car][0]

time = cars.data['time']
velocity = cars.data['velocity']
# New Graph
plt.close()
# Graph Info
plt.title("Speed vs Time")
plt.ylabel('Speed (m/s)')
plt.xlabel('Time (s)')

# Extract Speed
speed = []
for v in velocity:
    if isinstance(v, Vector2):
        speed.append(v.magnitude())

# Plot
plt.plot(time, speed)
print(time)
print(speed)
plt.show()
