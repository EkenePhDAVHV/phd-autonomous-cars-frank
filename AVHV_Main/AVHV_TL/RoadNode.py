from AVHV_Main.AVHV_TL._TrafficNode import TrafficNode


# Inherits from TrafficNode but initializes this class's own members
class RoadNode(TrafficNode):
    def __init__(self, name, position=None, traffic_light=None):
        super(RoadNode, self).__init__(name=name, position=position, traffic_light=traffic_light)
