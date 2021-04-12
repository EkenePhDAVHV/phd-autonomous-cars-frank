# Imports
import numpy as np
import matplotlib.pyplot as plt
from AVHVCONTROL.Simulator import Simulation, Environment, Car, TrafficLight, Vector2, \
    Aggressive_Car, Gentle_Car, CarSpawner, RoadSystem
from AVHVCONTROL.test import LayoutList

#car = Car(name="Car 1", route=[1, 2, 6, 7], direction=100)
#ag_car = Aggressive_Car(name="Car 1", route=[1, 2, 4, 5], direction=100)
#gentle_car = Gentle_Car(name="Car 1", route=[1, 2, 4, 5], direction=100)
layout = LayoutList.cross_roads()
# Create Simulation
simulation = Simulation(
    debugging=True,
    time_end=50,
    time_increment=0.1,
    environment=Environment(
        name="Test collision",
        layout=layout
    ).add_objects([
        TrafficLight(name="Left Traffic Light  ", traffic_node=2, direction=0, timings=[4, 1], timer=0),
        TrafficLight(name="Right Traffic Light ", traffic_node=4, direction=0, timings=[4, 1], timer=0,
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
            route=[5, 4, 8, 9],
            car_ratio=40,
            #car_percent=10,
        ),
        CarSpawner(
            name="GentleCar",
            node=layout.get(RoadSystem).node(7),
            direction=270,
            safe_distance=50,
            route=[7, 6, 8, 9],
            car_ratio=60,
            #car_percent = 30,
        ),
    ])
)

plt.close()

# Graph Infowa
plt.title("Speed vs Time")
plt.ylabel('Speed (m/s)')
plt.xlabel('Time (s)')
time_values = {}

i= 0
time_arr = []
pos_sum = {}
vel_sum = {}
for cars in simulation.environment.environment_objects[Car]:
    time = cars.data['time']
    car_name = cars.name
    if i == 0:
        time_arr = time
    i = i + 1
    velocity = cars.data['velocity']
    position = cars.data['position']
    # Extract Speed
    speed = []
    vel_total_values = 0
    for v in velocity:
        if isinstance(v, Vector2):
            speed.append(v.magnitude())
            vel_sum[car_name] = speed
            if ('AggressiveCar' in car_name):
                #if vel_total_values > 700:
                    #print(v.magnitude())
                vel_total_values += 1
                time_values['AggressiveCar'] = vel_total_values
                time_values['time_agg_car'] = time_arr[vel_total_values - 1]
            elif ('GentleCar' in car_name):
                vel_total_values += 1
                time_values['GentleCar'] = vel_total_values
                time_values['time_gentle_car'] = time_arr[vel_total_values - 1]
    pos = []
    for p in position:
        if isinstance(p, Vector2):
            pos.append(p.magnitude())
        pos_sum[car_name] = pos
    plt.plot(time, speed)
#print(time_values)
position_arr = {}
velocity_arr = {}
time_cal_arr = {}
for data in pos_sum:
    position_arr[data] = sum(pos_sum[data])
    velocity_arr[data] = sum(vel_sum[data])
    time_cal_arr[data] = position_arr[data]/ velocity_arr[data]
print(time_cal_arr)
plt.show()

#for cars in simulation.environment.environment_objects[CarSpawner]:
    #pass
