from AVHV_Main.Vector2 import Vector2


class TrafficNode:
    def __init__(self, name, position=None, traffic_light=None):
        if position is None:
            position = [0, 0]

        self.pos = position
        self.id = name
        self.name = str(name)
        self.position = Vector2(position)
        self.traffic_lightt = traffic_light
        self.destination_nodes = []

    # the nodes concerned for test 4 = 2,4,6,7,8,12,14,16 and 18
    def check(self, node):
        if isinstance(node, TrafficNode):
            return self.position == node.position and self.name == node.name
        return False

    def get_info(self):
        output = str.format("{:7s} [{:3d}, {:3d}]", self.name, self.position.x, self.position.y)
        return output + str(self.destination_nodes)

    def connect(self, node, debug=False):
        if isinstance(node, TrafficNode):
            if not self.check(node) and not self.connected(node):
                self.destination_nodes.append(node)
                node.connect(self)
                if debug:
                    print("Connecting " + self.name + " to " + node.name)

    def connected(self, node):
        for destination_node in self.destination_nodes:
            if destination_node.check(node):
                return True
        return False
