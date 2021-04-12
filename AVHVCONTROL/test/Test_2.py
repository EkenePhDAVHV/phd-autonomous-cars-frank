from AVHVCONTROL.Simulator import *
from AVHVCONTROL.test import RoadSystemToolbox

road_system = RoadSystemToolbox.RoadSystemToolbox.crossroads()
simulation = Simulation(
    debugging=True,
    time_end=30,
    time_increment=0.5,
    environment=Environment(
        name="Test 2",
        layout=road_system
    ).add_objects([
        #TrafficLight(name="Left Traffic Light  ", traffic_node=2, direction=270, timings=[4, 1], timer=0, position=[-20, +40]),
        #TrafficLight(name="Right Traffic Light ", traffic_node=4, direction=90, timings=[4, 1], timer=0, position=[+20, +40]),
        #TrafficLight(name="Top Traffic Light   ", traffic_node=6, direction=0, timings=[4, 1], timer=5, position=[+80, -112]),
        #TrafficLight(name="Bottom Traffic Light", traffic_node=8, direction=180, timings=[4, 1], timer=5, position=[-60, -10]),
        #Car(name="Car 1", route=[11, 12, 8, 9]),
        #Car(name="Car 2", route=[7, 6, 2, 1]),
        #Car(name="Car 3", route=[19, 18, 14, 15]),
        Car(name="Car 4", route=[5, 4, 16, 17])
     ])
)
car = simulation.environment.environment_objects[Car][0]
plt.close()
plt.title("Position of " + car.name)
plt.xlabel('Time ')
plt.ylabel('position')


for position in car.data['position']:
    if isinstance(position, Vector2):
        plt.plot(time(), position.get_value()[0])
       # plt.savefig('car position.png')

plt.show()

