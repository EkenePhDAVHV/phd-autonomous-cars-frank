from AVHV_Main.Node.RoadNode import RoadNode
from AVHV_Main.RoadSystem.RoadSystem import RoadSystem
from AVHV_Main.Node.PedestrianNode import PedestrianNode
from AVHV_Main.RoadSystem.PedestrianSystem import PedestrianSystem
from AVHV_Main.Node.ReservationNode import ReservationNode
from AVHV_Main.RoadSystem.ReservationSystem import ReservationSystem


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
        ),

        ReservationSystem: ReservationSystem(
            nodes=[
                # ReservationNode(1, [-225, 0 + 15]),
                # ReservationNode(2, [-125, 0 + 15]),
                # ReservationNode(4, [125, 0 + 15]),
                # ReservationNode(5, [225, 0 + 15]),
                # ReservationNode(6, [0 - 15, 125], is_vertical=True),
                # ReservationNode(7, [0 - 15, 225], is_vertical=True),
                # ReservationNode(8, [0 - 15, -125], is_vertical=True),
                # ReservationNode(9, [0 - 15, -225], is_vertical=True),
                # ReservationNode(11, [-225, 0 - 15]),
                # ReservationNode(12, [-125, 0 - 15]),
                # ReservationNode(14, [125, 0 - 15]),
                # ReservationNode(15, [225, 0 - 15]),
                # ReservationNode(16, [0 + 15, 125], is_vertical=True),
                # ReservationNode(17, [0 + 15, 225], is_vertical=True),
                # ReservationNode(18, [0 + 15, -125], is_vertical=True),
                # ReservationNode(19, [0 + 15, -225], is_vertical=True),
                # ReservationNode(2, [-50, 0 + 15], is_also_roadnode=True),
                # ReservationNode(4, [50, 0 + 15], is_also_roadnode=True),
                # ReservationNode(6, [0 - 15, 50], is_also_roadnode=True),
                # # ReservationNode(8, [0 - 15, -50], is_also_roadnode=True),
                # ReservationNode(12, [-50, 0 - 15], is_also_roadnode=True),
                # ReservationNode(14, [50, 0 - 15], is_also_roadnode=True),
                # ReservationNode(16, [0 + 15, 50], is_also_roadnode=True),

                # ReservationNode(18, [0 + 15, -50], is_also_roadnode=True),
                # ReservationNode(101, [0 - 32.5, 0 - 32.5], is_centered=True,
                #                 is_invisible=True),
                # ReservationNode(102, [0 + 32.5, 0 - 32.5], is_centered=True,
                #                 is_invisible=True),
                # ReservationNode(103, [0 + 32.5, 0 + 32.5], is_centered=True,
                #                 is_invisible=True),
                # ReservationNode(104, [0 - 32.5, 0 + 32.5], is_centered=True,
                #                 is_invisible=True),
                # ReservationNode(201, [0, 0 - 35], is_centered=True),
                # ReservationNode(202, [0 + 35, 0], is_centered=True),
                # ReservationNode(203, [0, 0 + 35], is_centered=True),
                # ReservationNode(204, [0 - 35, 0], is_centered=True),
                ReservationNode(301, [0 - 22.5, 0 - 10], is_centered=True),
                ReservationNode(302, [0 + 22.5, 0 - 10], is_centered=True),
                ReservationNode(303, [0 - 22.5, 0 + 10], is_centered=True),
                ReservationNode(304, [0 + 22.5, 0 + 10], is_centered=True),
                ReservationNode(305, [0 - 10, 0 - 22.5], is_centered=True),
                ReservationNode(306, [0 + 10, 0 - 22.5], is_centered=True),
                ReservationNode(307, [0 - 10, 0 + 22.5], is_centered=True),
                ReservationNode(308, [0 + 10, 0 + 22.5], is_centered=True),
                ReservationNode(309, [0, 0 - 10], is_centered=True),
                ReservationNode(310, [0 - 10, 0], is_centered=True),
                ReservationNode(311, [0 + 10, 0], is_centered=True),
                ReservationNode(312, [0, 0 + 10], is_centered=True),
            ],
            edges={

            }
        )
    }


cross_roads()
