from AVHV_Main.Car import Car
from AVHV_Main.AggressiveCar import AggressiveCar


class GentleCar(Car):
    def __init__(self, name=None, route=None, direction=None, car_type='gentle'):
        self.car_type = car_type
        self.route = route
        super(GentleCar, self).__init__(name=name, route=self.route, direction=direction, car_type = car_type)
        print('__init__', car_type)

        self.direction = direction

    def behaviour_update1(self, t):
        # color=color.green

        print('gentle car')
        if isinstance(self.car, AggressiveCar):
            self.next_node()
            if self.aggressive_car is None and self.Traffic_light is True:
                if self.safe_distance < 30:
                    self.direction = self.direction_to_next_node()
                    self.turning(t)
                    self.oby_traffic()
                    self.velocity.scale(0.9)
                    self.acceleration.re
        else:
            self.apply_force(t, 5000)

    '''def behaviour_update(self, t):
        print('beh', t)
        super(Car, self).behaviour_update(t)
        self.next_car()
        if len(self.car) > 0:
            self.turning(t)
            # Obey obstacle
            self.obey_obstacle(t)'''
