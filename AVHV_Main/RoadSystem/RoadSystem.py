import copy

from AVHV_Main.RoadSystem.TrafficSystem import TrafficSystem


class RoadSystem(TrafficSystem):
    edges = []
    nodes = []
    route = {}  # The routing table

    def __init__(self, nodes, edges):
        colors = {
            'node': "#5555aa",
            'edge': '#9999aa',
            'text': 'white'
        }

        self.edges = edges
        self.nodes = nodes

        # The routing table will tell us what the next node is for the target
        # node (if any)

        route = {}

        # Implement BFS to find the route
        for x in nodes:
            route[x.id] = {}
        for e in edges:
            for x in edges[e]:
                route[e][x] = x

        super(RoadSystem, self).__init__(nodes=nodes, edges=edges,
                                         colors=colors)
        # print(route)
