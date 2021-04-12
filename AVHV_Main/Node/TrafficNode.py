from AVHV_Main.Utilities.Vector2 import Vector2


class TrafficNode:
    def __init__(self, name, position=None, traffic_light=None):
        if position is None:
            position = [0, 0]

        self.position = Vector2(position)
        self.id = name
        self.name = str(name)
        self.traffic_light = traffic_light
        self.destination_nodes = []

    def __str__(self):
        return str.format("{:7s} [{:3f}, {:3f}]", self.name, self.position.x,
                          self.position.y) + str(self.destination_nodes)

    def check(self, node):
        """Checks if the node object is this node object."""

        if isinstance(node, TrafficNode):
            return self.position == node.position and self.name == node.name

        return False

    def check_connected(self, node):
        """Checks if the passed node object has already been connected by
        looking in destination nodes."""

        for destination_node in self.destination_nodes:
            if destination_node.check(node):
                return True

        return False

    def get_info(self):
        return self.__str__()

    def connect(self, node, debug=False):
        """Connect the node object to this node object as far as they aren't
        the same object."""

        if isinstance(node, TrafficNode):
            if not self.check(node) and not self.check_connected(node):
                self.destination_nodes.append(node)

                # Connect in reverse as well
                node.connect(self)

                if debug:
                    print(f"Connecting {self.name} to {node.name}")
