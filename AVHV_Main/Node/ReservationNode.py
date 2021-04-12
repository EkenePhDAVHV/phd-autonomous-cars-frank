from AVHV_Main.Node.TrafficNode import TrafficNode


class ReservationNode(TrafficNode):
    def __init__(self, name, position=None, traffic_light=None,
                 is_vertical=False, is_centered=False,
                 is_also_roadnode=False, is_invisible=False):
        super().__init__(name=name, position=position,
                         traffic_light=traffic_light)

        self.is_vertical = is_vertical
        self.is_centered = is_centered
        self.is_also_roadnode = is_also_roadnode
        self.is_invisible = is_invisible
