# Imports
import os

from AVHV_Main import LayoutList
from AVHV_Main.Agents.CarSpawner import CarSpawner
from AVHV_Main.Environment import Environment
from AVHV_Main.RoadSystem.RoadSystem import RoadSystem
from AVHV_Main.Simulator import Simulation

layout = LayoutList.cross_roads()

# get basename
basename = os.path.basename(__file__)

# get filename without extension
current_file_name = os.path.splitext(basename)[0]

file_path = "../output/AVHV_Reservation_Nodes/"

file_names = ["av", "hv"]

for _file_path in [file_path]:
    if not os.path.isdir(_file_path):
        os.mkdir(_file_path)

    for file_name in file_names:
        with open(_file_path + file_name + ".csv", "w", encoding="utf8") as f:
            f.write(
                "car_name,speed,safe_distance,reaction_time,stopping_time\n")

# Create Simulation
simulation = Simulation(
    debugging=True,
    time_end=400.0,
    time_increment=.1,
    environment=Environment(
        name="Test collision",
        layout=layout
    ).add_objects([
        # non-priority lane
        CarSpawner(name="GentleCar", node=layout.get(RoadSystem).node(11),
                   route=[11, 12, 8, 9], direction=0,
                   car_ratio=13, file_path=file_path, file_names=file_names),
        CarSpawner(name="AggressiveCar", node=layout.get(RoadSystem).node(11),
                   route=[11, 12, 8, 9], direction=0,
                   car_ratio=3, file_path=file_path, file_names=file_names),
        CarSpawner(name="GentleCar", node=layout.get(RoadSystem).node(11),
                   route=[11, 12, 8, 9], direction=0,
                   car_ratio=9, file_path=file_path, file_names=file_names),
        CarSpawner(name="AggressiveCar", node=layout.get(RoadSystem).node(11),
                   route=[11, 12, 8, 9], direction=0,
                   car_ratio=3, file_path=file_path, file_names=file_names),
        CarSpawner(name="GentleCar", node=layout.get(RoadSystem).node(11),
                   route=[11, 12, 8, 9], direction=0,
                   car_ratio=9, file_path=file_path, file_names=file_names),
        CarSpawner(name="AggressiveCar", node=layout.get(RoadSystem).node(11),
                   route=[11, 12, 8, 9], direction=0,
                   car_ratio=3, file_path=file_path, file_names=file_names),
        CarSpawner(name="GentleCar", node=layout.get(RoadSystem).node(11),
                   route=[11, 12, 8, 9], direction=0,
                   car_ratio=10, file_path=file_path, file_names=file_names),

        # priority lane
        CarSpawner(name="GentleCar", node=layout.get(RoadSystem).node(7),
                   route=[7, 6, 8, 9], direction=0,
                   car_ratio=13, file_path=file_path, file_names=file_names),
        CarSpawner(name="AggressiveCar", node=layout.get(RoadSystem).node(7),
                   route=[7, 6, 8, 9], direction=0,
                   car_ratio=3, file_path=file_path, file_names=file_names),
        CarSpawner(name="GentleCar", node=layout.get(RoadSystem).node(7),
                   route=[7, 6, 8, 9], direction=0,
                   car_ratio=18, file_path=file_path, file_names=file_names),
        CarSpawner(name="AggressiveCar", node=layout.get(RoadSystem).node(7),
                   route=[7, 6, 8, 9], direction=0,
                   car_ratio=3, file_path=file_path, file_names=file_names),
        CarSpawner(name="GentleCar", node=layout.get(RoadSystem).node(7),
                   route=[7, 6, 8, 9], direction=0,
                   car_ratio=13, file_path=file_path, file_names=file_names),
    ]),
    file_path=file_path,
    file_names=file_names
)
