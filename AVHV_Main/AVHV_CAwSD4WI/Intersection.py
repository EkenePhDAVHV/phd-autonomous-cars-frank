from AVHV_Main.AVHV_CAwSD4WI._EnvironmentObject import EnvironmentObject


class Intersection(EnvironmentObject):

    def __init__(self, name=None, position=None, size=None, direction=None, lanes=None):
        super(Intersection, self).__init__(name=name, position=position, size=size, direction=direction)
        self.lanes = lanes

    def update(self, t):
        super(Intersection, self).update(t)
