# Imports

from AVHV_Main import LayoutList
from AVHV_Main.Agents.CarSpawner import CarSpawner
from AVHV_Main.Environment import Environment
from AVHV_Main.RoadSystem import RoadSystem
from AVHV_Main.Simulator import Simulation

layout = LayoutList.cross_roads()

# Create Simulation
simulation = Simulation(
    debugging=True,
    time_end=60.0,
    time_increment=.2,
    environment=Environment(
        name="Test collision",
        layout=layout
    ).add_objects([
        CarSpawner(name="AggressiveCar", node=layout.get(RoadSystem).node(11), route=[11, 12, 8, 9], direction=0,
                   car_ratio=3),
        CarSpawner(name="GentleCar", node=layout.get(RoadSystem).node(7), route=[7, 6, 8, 9], direction=0,
                   car_ratio=1)
    ])
)

