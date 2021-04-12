from AVHV_Main.AVHV_CAwSD4WI._TrafficSystem import TrafficSystem
import copy as copy_module


class RoadSystem(TrafficSystem):
    edges = []
    nodes = []
    route = {}  # The routing table

    def __init__(self, nodes, edges):
        colors = {
            'node': '#5555aa',
            'edge': '#9999aa',
            'text': 'white'
        }

        self.edges = edges
        self.nodes = nodes

        # The routing table will tell us what is the next node for the target node (if any)
        route = {}

        # Implement BFS to find the route
        changed = True

        # Proceed with initial route
        for x in nodes:
            route[x.id] = {}
        for e in edges:
            for x in edges[e]:
                route[e][x] = x

        # From node 1 to go to node 2 you go via node 2
        # {1: {2: 2},
        #  2: {3: 3, 4: 4, 18: 18} }
        # Next step: go over all edges
        # Results must be:
        # {1: {2:2, 3:2, 4:2, 18:2}}

        while changed:
            changed = False
            oldRoute = copy_module.deepcopy(route)
            for r in oldRoute:
                for c in oldRoute[r]:
                    for n in oldRoute[c]:
                        if n not in route[r]:
                            route[r][n] = c
                            changed = True
        self.route = route
        super(RoadSystem, self).__init__(nodes=nodes, edges=edges, colors=colors)

    def getNextNode(self, nodeID, targetID):
        if nodeID not in self.route:
            return None
        tgt = self.route[nodeID][targetID]
        if tgt is None:
            return tgt
        return self.getNode(tgt)

    def getNode(self, _id):
        for x in self.nodes:
            if x.id == _id:
                return x
        return None

    def getAllNextNodes(self, node):
        return self.edges[node]
