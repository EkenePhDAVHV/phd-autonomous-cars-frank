from AVHV_Main.AVHV_TL._TrafficNode import TrafficNode
from AVHV_Main.AVHV_TL.RoadSystem import RoadSystem


class RoadSystemToolbox:
    @staticmethod
    def crossroads():
        return RoadSystem(
            nodes=[
                TrafficNode(1, [-300, 0 + 15]),
                TrafficNode(2, [-50, 0 + 15]),
                TrafficNode(4, [50, 0 + 15]),
                TrafficNode(5, [300, 0 + 15]),
                TrafficNode(6, [0 - 15, 50]),
                TrafficNode(7, [0 - 15, 300]),
                TrafficNode(8, [0 - 15, -50]),
                TrafficNode(9, [0 - 15, -300]),

                TrafficNode(11, [-300, 0 - 15]),
                TrafficNode(12, [-50, 0 - 15]),
                TrafficNode(14, [50, 0 - 15]),
                TrafficNode(15, [300, 0 - 15]),
                TrafficNode(16, [0 + 15, 50]),
                TrafficNode(416, [0 + 15, 50]),
                TrafficNode(17, [0 + 15, 300]),
                TrafficNode(18, [0 + 15, -50]),
                TrafficNode(19, [0 + 15, -300]),
             ],
            edges={
                1: [2],
                2: [1, 18],
                4: [2, 8, 416],
                5: [4],
                6: [7, 8, 2, 14],
                4: [2, 8, 416],
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
        )
