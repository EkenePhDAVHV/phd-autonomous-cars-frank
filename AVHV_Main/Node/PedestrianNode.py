from AVHV_Main.Node.TrafficNode import TrafficNode


class PedestrianNode(TrafficNode):
    def __init__(self, name, position=None, traffic_light=None):
        super().__init__(name=name, position=position,
                         traffic_light=traffic_light)
