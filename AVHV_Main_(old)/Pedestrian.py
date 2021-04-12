from AVHV_Main._EnvironmentObject import EnvironmentObject


class Pedestrian(EnvironmentObject):
    def __init__(self, name, position=None, velocity=None, acceleration=None, direction=None, size=10, mass=None,
                 route=None, color=None):
        if not isinstance(color, str):
            color = "green"
        if not isinstance(mass, int) and not isinstance(mass, float):
            mass = 1200
        super(Pedestrian, self).__init__(name=name, position=position, velocity=velocity, acceleration=acceleration,
                                         direction=direction, size=size, mass=mass, color=color)
        if not isinstance(route, list):
            route = []
        self.route = route
        self.idle_time = 0
        self.pedestrian_light = None

    def draw(self, canvas, offset):
        if isinstance(canvas, type(Drawing())):
            color = 'yellow'
            if len(self.route) > 0:
                color = 'grey' if self.pedestrian_light is None \
                    else 'green' if self.pedestrian_light.green \
                    else 'red' if self.pedestrian_light.red \
                    else 'green'
            canvas.add(Circle(
                center=self.position.draw(offset).get_value(),
                r=self.size.x,
                fill=color
            ))
            super(pedestrian, self).draw_direction(canvas=canvas, offset=offset)

    def obey_pedestrian_light(self, t):
        # Test for traffic Light
        if self.pedestrian_light is None:
            if len(self.route) > 0:
                if isinstance(self.route[0], PedestrianNode):
                    if self.route[0].pedestrian_light is not None:
                        self.pedestrian_light = self.route[0].pedestrian_light
