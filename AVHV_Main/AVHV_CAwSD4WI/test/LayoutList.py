from AVHV_Main.AVHV_CAwSD4WI.RoadNode import RoadNode
from AVHV_Main.AVHV_CAwSD4WI.RoadSystem import RoadSystem
from AVHV_Main.AVHV_CAwSD4WI.PedestrianNode import PedestrianNode
from AVHV_Main.AVHV_CAwSD4WI.PedestrianSystem import PedestrianSystem


def cross_roads():
    return {
        RoadSystem: RoadSystem(
            nodes=[
                RoadNode(1, [-300, 0 + 15]),
                RoadNode(2, [-15, 0 + 15]),
                RoadNode(4, [15, 0 + 15]),
                RoadNode(5, [300, 0 + 15]),
                RoadNode(6, [0 - 15, 50]),
                RoadNode(7, [0 - 15, 300]),
                RoadNode(8, [0 - 15, -50]),
                RoadNode(9, [0 - 15, -300]),
                RoadNode(11, [-300, 0 - 15]),
                RoadNode(12, [-15, 0 - 15]),
                RoadNode(14, [15, 0 - 15]),
                RoadNode(15, [300, 0 - 15]),
                RoadNode(16, [0 + 15, 50]),
                RoadNode(17, [0 + 15, 300]),
                RoadNode(18, [0 + 15, -50]),
                RoadNode(19, [0 + 15, -300])
            ],
            edges={
                1: [2],
                2: [4, 1],
                5: [4],
                6: [7, 8],
                8: [9],
                11: [12],
                12: [14],
                14: [15, 12],
                16: [17, 18],
                18: [19],
            }
        ),
        PedestrianSystem: PedestrianSystem(
            nodes=[
                # PedestrianNode(1, [-300, 0 + 60]),
                # PedestrianNode(11, [-300, 0 - 60]),
                # PedestrianNode(5, [300, 0 + 60]),
                # PedestrianNode(15, [300, 0 - 60]),
                # PedestrianNode(9, [0 - 60, -300]),
                # PedestrianNode(19, [0 + 60, -300]),
                # PedestrianNode(7, [0 - 60, 300]),
                # PedestrianNode(17, [0 + 60, 300])
            ],
            edges={
                # 1: {11},
                # 11: {1},
                # 5: {15},
                # 15: {5},
                # 9: {19},
                # 19: {9},
                # 7: {17},
                # 17: {7}
            }
        )
    }
