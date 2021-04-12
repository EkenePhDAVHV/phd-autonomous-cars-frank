# Imports
import numpy as np
import matplotlib.pyplot as plt
from AVHVCONTROL.Simulator import Simulation, Environment, Car, TrafficLight, Vector2, \
    Aggressive_Car, Gentle_Car, CarSpawner, RoadSystem
from AVHVCONTROL.test import LayoutList

layout = LayoutList.cross_roads()
# Create Simulation
simulation = Simulation(
    debugging=True,
    time_end=30,
    time_increment=1,
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
        CarSpawner(
            name="GentleCar",
            node=layout.get(RoadSystem).node(7),
            direction=270,
            safe_distance=50,
            route=[7, 6, 2, 1]
        ),
    ])
)
cars = simulation.environment.environment_objects[Car][0]

time = cars.data['time']
acceleration_data = cars.data['acceleration']
# New Graph
plt.close()
# Graph Info
plt.title("Acceleration vs Time")
plt.ylabel('Acceleration (m/s^2)')
plt.xlabel('Time (s)')

# Extract Acceleration
acc = []
for acceleration in acceleration_data:
    if isinstance(acceleration, Vector2):
        acc.append(acceleration.magnitude())
# Plot
plt.plot(time, acc)
print(time)
print(acc)
plt.show()
