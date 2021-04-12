from AVHCONTROLOLD.physics.physics import CurveMovement
from AVHVCONTROL.Simulator import *
from AVHVCONTROL.test import RoadSystemToolbox
from AVHVCONTROL.test import TestPhysics


road_system = RoadSystemToolbox.RoadSystemToolbox.crossroads()
physics = CurveMovement(time=2, car=Car, radius=3, curveCenter=4, startDegree=90, endDegree=360)
simulation = Simulation(
    debugging=False,
    time_end=50,
    time_increment=0.05,
    #testphysics=TestPhysics,
    environment=Environment(
        name="test_Car_Movement",
        layout=road_system
    ).add_objects([
        TrafficLight(name="Left Traffic Light  ", traffic_node=2, direction=270, timings=[4, 1], timer=0,position=[-20, +40]),
        TrafficLight(name="Right Traffic Light ", traffic_node=4, direction=90, timings=[4, 1], timer=0,position=[+20, +40]),
        TrafficLight(name="Top Traffic Light   ", traffic_node=6, direction=0, timings=[4, 1], timer=5,position=[+80, -112]),
        TrafficLight(name="Bottom Traffic Light", traffic_node=8, direction=180, timings=[4, 1], timer=5,position=[-60, -10]),
        Car(name="Car 1", route=[11, 12, 8, 9]),
        #Car(name="Car 2", route=[7, 6, 2, 1]),
        #Car(name="Car 3", route=[19, 18, 14, 15]),
        #Car(name="Car 4", route=[5, 4, 16, 17])
     ])
)
car = simulation.environment.environment_objects[Car][0]

time_data = car.data['time']
velocity_data = car.data['velocity']
speed_val = car.data['speed']

speed_list = []

for i in range(0, len(time_data)):
    time = time_data[i]
    velocity = velocity_data[i]
    speed = math.sqrt(velocity.x * velocity.x + velocity.y * velocity.y)
    speed_list.append(speed)

    #print(str.format("{:f} - {:f}, {:f}, {:f}", time, velocity.x, velocity.y))

print(speed_list)
print(len(time_data))
print(type(velocity))
plt.title("Speed / Time Graph " + car.name)

plt.xlabel('Time(s)')
plt.ylabel('Speed (m/s)')

plt.scatter(time_data, speed_list)
plt.show()

