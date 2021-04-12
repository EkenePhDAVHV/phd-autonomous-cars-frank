from AVHV_Main._TrafficSystem import TrafficSystem


class PedestrianSystem(TrafficSystem):
    def __init__(self, nodes, edges):
        colors = {
            'node': '#aa0000',
            'edge': '#330000',
            'text': 'white'
        }
        super(PedestrianSystem, self).__init__(nodes=nodes, edges=edges, colors=colors)
