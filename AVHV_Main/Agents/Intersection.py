from AVHV_Main.Agents._EnvironmentObject import EnvironmentObject


class Intersection(EnvironmentObject):
    def __init__(self, name=None, position=None, size=None, direction=None,
                 lanes=None):
        super().__init__(name=name, position=position, size=size,
                         direction=direction)
        self.lanes = lanes

    def update(self, t):
        super().update(t)
