import copy

from svgwrite.shapes import *

from AVHV_Main.RoadSystem.TrafficSystem import TrafficSystem


class ReservationSystem(TrafficSystem):

    def __init__(self, nodes, edges):
        colors = {
            'node': "#ee2222",
            'edge': '#9999aa',
            'text': 'white'
        }

        super().__init__(nodes=nodes, edges=edges, colors=colors)

    def draw_nodes(self, canvas, offset):
        """Draws all the nodes in this object on the canvas."""

        arc_1 = canvas.path(
            d="M 400 500 q 40 -20 80 0",
            fill="none",
            stroke='#222222',
            stroke_width=3)

        arc_1.rotate(45, (430, 485))
        arc_1.translate(-35, -38)

        canvas.add(arc_1)

        arc_2 = canvas.path(
            d="M 400 500 q 40 -20 80 0",
            fill="none",
            stroke='#222222',
            stroke_width=3)

        arc_2.rotate(-45, (430, 485))
        arc_2.translate(30, -24)

        canvas.add(arc_2)

        arc_3 = canvas.path(
            d="M 400 500 q 40 -20 80 0",
            fill="none",
            stroke='#222222',
            stroke_width=3)

        arc_3.rotate(135, (430, 485))
        arc_3.translate(-50, 25)

        canvas.add(arc_3)

        arc_3 = canvas.path(
            d="M 400 500 q 40 -20 80 0",
            fill="none",
            stroke='#222222',
            stroke_width=3)

        arc_3.rotate(-135, (430, 485))
        arc_3.translate(15, 40)

        canvas.add(arc_3)

        for node in self.nodes:
            radius = 5
            fill = self.colors.get('node')
            stroke = 'none'
            stroke_width = 0

            if node.is_also_roadnode:
                radius = 12
                fill = 'none'
                stroke = self.colors.get('node')
                stroke_width = 0

            if node.is_invisible:
                fill = 'none'

            if self.draw_node:
                canvas.add(Circle(
                    center=node.position.draw(offset=offset).get_value(),
                    r=radius,
                    fill=fill,
                    stroke=stroke,
                    stroke_width=stroke_width
                ))

                # canvas.add(Rect(
                #     insert=node.position.draw(offset=offset).get_value(),
                #     size=size,
                #     fill=self.colors.get('node')
                # ))

    def draw_text(self, canvas, offset):
        return
