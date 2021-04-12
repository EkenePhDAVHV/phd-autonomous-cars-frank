from svgwrite.shapes import *

from AVHV_Main.Utilities.Vector2 import Vector2
from AVHV_Main.Node.TrafficNode import TrafficNode


class TrafficSystem:
    def __init__(self, nodes=None, edges=None, colors=None, stroke_width=3):
        self.draw_node = True
        self.stroke_width = stroke_width

        # Make sure `nodes`, `edges` and `colors` are not None
        nodes = [] if nodes is None else nodes
        self.nodes = nodes

        edges = {} if edges is None else edges
        self.add_edges(edges)

        colors = {} if colors is None else colors

        # Populate `colors` dictionary
        if colors.get('node') is None:
            colors['node'] = 'blue'
        if colors.get('edge') is None:
            colors['edge'] = 'aqua'
        if colors.get('text') is None:
            colors['text'] = 'white'

        self.colors = colors

    def get_nodes(self):
        return self.nodes

    def node(self, name):
        """Checks that passed node object is a TrafficNode object."""

        if isinstance(name, TrafficNode):
            return name

        for node in self.nodes:
            if str(node.name) == str(name):
                return node

        return None

    def add_nodes(self, nodes=None):
        """Adds new node(s)."""

        if isinstance(nodes, list):
            self.nodes.extend(nodes)
        else:
            self.nodes.append(nodes)

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
        """Prints information about all the nodes in this object.
        Information includes: name, position.x, position.y and destination
        nodes."""

        print("\n\n\n\nNODE INFO")
        for n in self.nodes:
            print(n.get_info())

    def draw_edges(self, canvas, offset):
        """Connect the nodes with lines and draw on the canvas."""

        for node in self.nodes:
            for con in node.destination_nodes:
                # if node.id == 12 and con.id == 8 or \
                #         node.id == 8 and con.id == 12 or \
                #         node.id == 18 and con.id == 14 or \
                #         node.id == 14 and con.id == 18 or \
                #         node.id == 6 and con.id == 2 or \
                #         node.id == 2 and con.id == 6 or \
                #         node.id == 4 and con.id == 16 or \
                #         node.id == 16 and con.id == 4:
                #     stroke_width = 20
                # else:
                #     stroke_width = self.stroke_width

                canvas.add(Line(
                    start=node.position.draw(offset).get_value(),
                    end=con.position.draw(offset).get_value(),
                    stroke=self.colors.get('edge'),
                    stroke_width=self.stroke_width
                ))

    def draw_nodes(self, canvas, offset):
        """Draws all the nodes in this object on the canvas."""

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
