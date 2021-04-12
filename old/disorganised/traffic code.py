"""
1. First come, first served.

>    Car Arrives at Intersection (Car position is less than 10 meters from intersection 
    in the direction it is travelling)
>   If intersection has no traffic lights
    >    If there are cars,
        >    register which cars are there and wait for all of those cars to leave.
    >    Else
            move on
>    Else
    >    Obey Traffic lights (Red Amber Green)

    >    If there is a car on the right
        >    Wait till it has gone
        Else
        Move on
    Else 
        If Car arrives at the intersection in the opposite direction (distance apart = 10 meters)
            > wait for the car going straight
        Else
            Move on
            
    If car is turning left
        if there is a car on the opposite side turning right or going forwards
            wait till it has gone (or they, if more than one)
        move on 
> stop



~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
PROGRAM CODE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import pygame
from pygame.rect import Rect


class Vector2:
    def __init__(self, vector):
        if isinstance(vector[0], int):
            self.x = vector[0]
        if isinstance(vector[1], int):
            self.y = vector[1]


class SimulationObject:
    def __init__(self, position=None, size=None, direction=None, color=None):
        # Init
        if position is None:
            position = (0, 0)
        if size is None:
            size = (0, 0)
        if direction is None:
            direction = 0
        if color is None:
            color = (100, 0, 100)

        self.position = Vector2(position)
        self.size = Vector2(size)
        self.direction = direction
        self.__color = color

    def draw(self, screen):
        if isinstance(screen, pygame.Surface):
            shape = pygame.rect.Rect(
                self.position.x - self.size.x,
                self.position.y - self.size.y,
                self.size.x,
                self.size.y
            )
            pygame.draw.rect(screen, self.__color, shape)
            print(str.format("{:<20} [{:d}, {:d}], [{:d}, {:d}]", str(self), self.position.x, self.position.y,
                             self.size.x, self.size.y))


class Car(SimulationObject):
    def __init__(self, position, size, speed):
        super(Car, self).__init__(position, size)
        self.speed = Vector2(speed)


class Intersection(SimulationObject):
    def __init__(self, position, size):
        super(Intersection, self).__init__(position, size)


class TrafficLight(SimulationObject):
    def __init__(self, position):
        super(TrafficLight, self).__init__(position, (0, 0))


class Simulation:
    def __init__(self):
        # Colours
        self.__blank = (255, 255, 255)
        # Dimensions
        self.__screen_width = 1920
        self.__screen_height = 1080
        # PyGame Display
        self.screen = pygame.display.set_mode([self.__screen_width, self.__screen_height], pygame.FULLSCREEN)

        # Simulation Objects
        self.simulation_objects = {
            # Cars
            'Autonomous Vehicle': [],
            'Human Vehicle': [],
            'Autonomous Human Vehicle': [],
            # Intersections
            'Intersection': [],
            # Traffic Lights
            'Traffic Light': []
        }
        # Add Cars
        self.simulation_objects['Autonomous Vehicle'].append(Car(position=(100, 100), size=(100, 100), speed=(0, 0)))
        # Add Intersection and Traffic Light
        self.simulation_objects['Intersection'].append(Intersection(position=(500, 500), size=(200, 200)))
        self.simulation_objects['Traffic Light'].append(TrafficLight(position=(70, 70)))

    def start(self):
        if isinstance(self.screen, pygame.Surface):
            while True:
                self.screen.fill(self.__blank)
                for simulation_object_type, simulation_objects in self.simulation_objects.items():
                    for simulation_object in simulation_objects:
                        if isinstance(simulation_object, SimulationObject):
                            simulation_object.draw(self.screen)
                pygame.display.update()
                print("\n\n\n")


if __name__ == '__main__':
    Simulation().start()

"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Traffic rule2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
"""
while (HVs.pos.x < int_end):  # to cross the intersection space
    rate(100)  # maintain the screen
    HVs.pos = HVs.pos + HV_velocity.dt  # car movement along east west road
    AVs1.pos = HVs1.pos
    HVs1.pos = HVs1.pos

    time = time + dt

Class
TrafficRule:
def__init__rule(self, pos, environment, route):  # pos,environment and route are existing functions in the main program
car_arrival_at_intersections(self, route)
if self.pos[] < intersection.pos[10]:
    car_arrival.count += 1

def_rule_without_traffic
light(self, car_arrival)
if car_arrival == ALSE
    self.update_pos(car)
Else
# wait for the traffic cycle


def_with_trafficlight(Red, Amber, Green)
if light == 'Red'
    queue.append(car_arrival)
    wait
    Else
    if light == 'Amber'
        Get
        ready
        to
        move or stop
        Else
        if light == 'Green'
            self.update_pos(car)

if car_arrival_from_right == TRUE
    wait
Else
self.update_pos(car)
if car_arrival_from_opposite_directions == TRUE
    Car_going_straight == FALSE
    self.update_pos(car)
Else
wait
if car_arrival_turning_left == TRUE
    car_turning_right and car_going_forward == TRUE
    self.update_pos(car)
Else
self.update_pos(car)

"""

"""
Dear Tim, please i would like you to take a look at this and debug along with me 

        CTRL - A 
        Select all
        
        Ctrl - C
        Copy
        
        Ctrl - v
        Paste
        
        Ctrl x 
        cut

"""
