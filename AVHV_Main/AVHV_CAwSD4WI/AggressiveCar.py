from AVHV_Main.AVHV_CA4WI.Car import Car


class AggressiveCar(Car):
    def __init__(self, name=None, route=None, direction=None, car_type='aggressive'):
        self.car_type = car_type
        self.route = route
        super(AggressiveCar, self).__init__(name=name, route=route, direction=direction, car_type=car_type)
        print('__init__', car_type)

        self.direction = direction

    # def behaviour_update1(self, t):
    #     super(Car, self).behaviour_update(t)
    #     print('next_node', self.next_node())
    #     self.next_node(t)
    #     self.direction
    #     self.turning(t)
    #     # color = color.red
    #     if len(self.route):
    #         if self.Traffic_light is None and self.Car is None and self.Car > 0:
    #             self.apply_force(t, 4000)
    #         else:
    #             self.obey_traffic_light()
