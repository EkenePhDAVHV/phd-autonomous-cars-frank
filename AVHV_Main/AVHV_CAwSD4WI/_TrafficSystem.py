from svgwrite.shapes import *

from AVHV_Main.AVHV_CAwSD4WI.Vector2 import Vector2
from AVHV_Main.AVHV_CAwSD4WI._TrafficNode import TrafficNode


class TrafficSystem:
    def __init__(self, nodes=None, edges=None, colors=None, stroke_width=3):
        self.draw_node = True
        self.stroke_width = stroke_width

        # Make sure our nodes is not a None object
        if nodes is None:
            nodes = []
        self.nodes = nodes

        # Make sure edges is not a None object before adding it.
        if edges is not None:
            self.add_edges(edges)

        # Make sure our colors is not a None object
        if colors is None:
            colors = {}

        # Populate our colors dictionary
        if colors.get('node') is None:
            colors['node'] = 'blue'
        if colors.get('edge') is None:
            colors['edge'] = 'aqua'
        if colors.get('text') is None:
            colors['text'] = 'white'
        self.colors = colors

    def get_nodes(self):
        return self.nodes

    # Check to see if passed name is the name of a valid node
    def node(self, name):
        if isinstance(name, TrafficNode):
            return name

        # Or if a node instance with a name attribute equal to the string passed
        for node in self.nodes:
            if str(node.name) == str(name):
                return node
        return None

    # Add new node(s)
    def add_nodes(self, nodes=None):
        self.nodes += nodes
        return self

    def add_edges(self, edges=None):
        for node, destinations in edges.items():
            node = self.node(node)
            if isinstance(node, TrafficNode):
                for destination in destinations:
                    destination = self.node(destination)
                    if isinstance(destination, TrafficNode):
                        node.connect(destination)
        return self

    def print_system(self):
        print("\n\n\n\nNODE INFO")
        for n in self.nodes:
            print(n.get_info())

    def draw_edges(self, canvas, offset):
        for node in self.nodes:
            for con in node.destination_nodes:
                canvas.add(Line(
                    start=node.position.draw(offset).get_value(),
                    end=con.position.draw(offset).get_value(),
                    stroke=self.colors.get('edge'),
                    stroke_width=self.stroke_width
                ))

    def draw_nodes(self, canvas, offset):
        for node in self.nodes:

            color = self.colors.get('node')

            if int(node.name) % 2 == 0:
                color = self.colors.get('edge')

            if self.draw_node:
                canvas.add(Circle(
                    center=node.position.draw(offset=offset).get_value(),
                    r=12,
                    fill=color
                ))

    def draw_text(self, canvas, offset):
        for node in self.nodes:
            if int(node.name) % 2 != 0:
                canvas.add(canvas.text(
                    node.name,
                    insert=node.position.draw(offset=offset)
                        .add(Vector2([-9, 5])).get_value() if int(node.name) >=
                                                              10 else
                    node.position.draw(offset=offset).add(Vector2([-5,
                                                                   5])).get_value(),
                    font_size=14,
                    fill=self.colors.get('text'),
                    style="font-family: Lucida Sans Unicode, Sans-serif;"
                ))

    def draw(self, canvas, offset):
        self.draw_edges(canvas=canvas, offset=offset)
        self.draw_nodes(canvas=canvas, offset=offset)
        self.draw_text(canvas=canvas, offset=offset)
