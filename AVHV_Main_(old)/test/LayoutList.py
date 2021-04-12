from AVHV_Main.RoadNode import RoadNode
from AVHV_Main.RoadSystem import RoadSystem
from AVHV_Main.PedestrianNode import PedestrianNode
from AVHV_Main.PedestrianSystem import PedestrianSystem


def cross_roads():
    return {
        RoadSystem: RoadSystem(
            nodes=[
                RoadNode(1, [-300, 0 + 15]),
                RoadNode(2, [-50, 0 + 15]),
                RoadNode(4, [50, 0 + 15]),
                RoadNode(5, [300, 0 + 15]),
                RoadNode(6, [0 - 15, 50]),
                RoadNode(7, [0 - 15, 300]),
                RoadNode(8, [0 - 15, -50]),
                RoadNode(9, [0 - 15, -300]),
                RoadNode(11, [-300, 0 - 15]),
                RoadNode(12, [-50, 0 - 15]),
                RoadNode(14, [50, 0 - 15]),
                RoadNode(15, [300, 0 - 15]),
                RoadNode(16, [0 + 15, 50]),
                RoadNode(416, [0 + 15, 50]),
                RoadNode(17, [0 + 15, 300]),
                RoadNode(18, [0 + 15, -50]),
                RoadNode(19, [0 + 15, -300]),
            ],
            edges={
                1: [2],
                2: [1, 18],
                4: [2, 8, 416],
                5: [4],
                6: [7, 8, 2, 14],
                7: [],
                8: [9],
                9: [],
                11: [12],
                12: [8, 14, 16],
                14: [15, 12],
                15: [],
                16: [17, 18],
                416: [16],
                17: [],
                18: [19],
                19: []
            }
        ),
        PedestrianSystem: PedestrianSystem(
            nodes=[
                PedestrianNode(1, [-300, 0 + 60]),
                PedestrianNode(11, [-300, 0 - 60]),
                PedestrianNode(5, [300, 0 + 60]),
                PedestrianNode(15, [300, 0 - 60]),
                PedestrianNode(9, [0 - 60, -300]),
                PedestrianNode(19, [0 + 60, -300]),
                PedestrianNode(7, [0 - 60, 300]),
                PedestrianNode(17, [0 + 60, 300])
            ],
            edges={
                1: {11},
                11: {1},
                5: {15},
                15: {5},
                9: {19},
                19: {9},
                7: {17},
                17: {7}
            }
        )
    }
