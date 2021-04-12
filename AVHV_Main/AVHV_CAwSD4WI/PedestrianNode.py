from AVHV_Main.AVHV_CAwSD4WI._TrafficNode import TrafficNode


class PedestrianNode(TrafficNode):
    def __init__(self, name, position=None, traffic_light=None):
        super(PedestrianNode, self).__init__(name=name, position=position, traffic_light=traffic_light)