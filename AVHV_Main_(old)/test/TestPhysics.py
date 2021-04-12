import unittest
import math

from AVHV_Main.test.RoadSystemToolbox import RoadSystemToolbox
from AVHV_Main.Vector2 import Vector2

from AVHV_Main.constants import *


class PhysicalObject:
    def __init__(self, pos=[0, 0], mass=1020, max_acceleration=1, drag=1.0, max_deacceleration=1, acceleration=[0, 0],
                 velocity=[0, 0]):
        self.pos = pos  # in meters
        self.mass = mass  # kg
        self.max_acceleration = max_acceleration
        self.max_deacceleration = max_deacceleration
        self.acceleration = acceleration  # in m/s^2
        self.velocity = velocity  # in m/s
        self.drag = drag
        self.reachedEnd = False

    def get_speed(self):
        """Returns the absolute speed in m/s"""
        return math.sqrt(self.velocity[0] * self.velocity[0] + self.velocity[1] * self.velocity[1])

    def get_force(self):
        return math.sqrt(
            self.acceleration[0] * self.acceleration[0] + self.acceleration[1] * self.acceleration[1]) * self.mass

    def __str__(self):
        return "pos: %17s mass:%5s maxAccl:%5s maxDeaccl:%5s Accl:%15s Velocity:%16s" % (self.pos, self.mass,
                                                                                self.max_acceleration,
                                                                                self.max_deacceleration,
                                                                                self.acceleration, self.velocity)


class Physics:
    def __init__(self, friction=0.75, gravity=9.8):
        self.friction = friction
        self.gravity = gravity
        self.decelerate = False

    def update_acceleration(self, obj, delta_accl, nodes_left):
        delta_accel_vector = Vector2(delta_accl)
        accel_vector = Vector2(obj.acceleration)

        # if the supplied acceleration is higher than current acceleration, we are accelerating,
        # otherwise we are decelerating
        if delta_accel_vector.magnitude() < accel_vector.magnitude() and delta_accl[0] != 0 and delta_accl[1] != 0:
            self.decelerate = True

        obj.acceleration[0] = delta_accl[0]
        obj.acceleration[1] = delta_accl[1]

        if obj.reachedEnd:
            obj.acceleration[0] = accel_vector.reset_self().get_value()[0]
            obj.acceleration[1] = accel_vector.reset_self().get_value()[1]

        # if at the destination, reset acceleration
        if nodes_left < 1:
            obj.reachedEnd = True

    def update_velocity(self, obj, delta_t, easy_physics, direction, t_lights, nodes_left):
        # if self.decelerate:
        #     obj.velocity[0] = obj.acceleration[0] * delta_t
        #     obj.velocity[1] = obj.acceleration[1] * delta_t
        #     self.decelerate = False
        # else:

        obj.velocity[0] = obj.velocity[0] + delta_t * obj.acceleration[0]
        obj.velocity[1] = obj.velocity[1] + delta_t * obj.acceleration[1]

        # so we don't have negative velocity
        if obj.velocity[0] < 0:
            obj.velocity[0] = 0
        if obj.velocity[1] < 0:
            obj.velocity[1] = 0

        velocity_vector = Vector2(obj.velocity)

            # check if we are at the destination already
            # if obj.reachedEnd:
            #     obj.velocity[0] = velocity_vector.reset_self().get_value()[0]
            #     obj.velocity[1] = velocity_vector.reset_self().get_value()[1]

        # so we don't exceed maximum velocity
        if easy_physics:
            obj.velocity[0] = velocity_vector.cap(max_velocity).get_value()[0]
            obj.velocity[1] = velocity_vector.cap(max_velocity).get_value()[1]


            # if at the destination, reset velocity and halt the car
            # if nodes_left < 1:
            #     obj.reachedEnd = True

        # if this is a straight route
        # if direction == 0.0 or direction == 90.0 or direction == -90.0 or direction == 180.0:
        #     # if there are traffic lights
        #     if t_lights > 0:
        #         obj.velocity = velocity_vector.reset_self().get_value()
        #         obj.acceleration = accel_vector.reset_self().get_value()
        #     else:
        #         if easy_physics:
        #             obj.velocity = velocity_vector.cap_self(max_velocity).get_value()
        #             obj.acceleration = accel_vector.cap_self(max_acceleration).get_value()
        # # if this is a curved route
        # else:
        #     # if there are traffic lights
        #     if t_lights > 0:
        #         obj.velocity = velocity_vector.reset_self().get_value()
        #         obj.acceleration = accel_vector.reset_self().get_value()
        #     else:
        #         obj.velocity = velocity_vector.scale_self(0.1).get_value()
        #         obj.acceleration = accel_vector.reset_self().get_value()

    # def apply_force(self, obj, mass, delta_t, magnitude, decelerate=False, direction=None):
    #     if direction is None:
    #         direction = self.direction
    #     acceleration_due_to_force = Vector2((magnitude / self.mass) * delta_t).redirect(direction)
    #     # Apply force in a direction (changed from Degrees to Radians)
    #
    #     if self.decelerate:  # if the car is decelerating
    #         acceleration_due_to_force.x = -acceleration_due_to_force.x
    #         acceleration_due_to_force.y = -acceleration_due_to_force.y
    #
    #     obj.acceleration = self.acceleration.add(acceleration_due_to_force)

    def update_pos(self, obj, delta_t):
        obj.pos[0] = obj.pos[0] + delta_t * obj.velocity[0]
        obj.pos[1] = obj.pos[1] + delta_t * obj.velocity[1]

    def max_speed_curve(self, curve_radius):
        return math.sqrt(self.gravity * self.friction * curve_radius)


class CurveMovement:
    def __init__(self, time, car, radius, curveCenter, startDegree, endDegree):
        self.curveCenter = curveCenter
        self.lengthCircle = 2 * math.pi * radius
        self.radius = radius
        self.startTime = time
        self.endDegree = endDegree
        self.actualDegree = startDegree
        self.startDegree = startDegree
        self.car = car

    def move(self, time):
        reachedEnd = False
        degree = 360 * self.car.get_speed() / self.lengthCircle
        if self.endDegree < self.startDegree:
            degree = - degree
        self.actualDegree = (time - self.startTime) * degree

        if self.endDegree >= self.startDegree:
            if self.actualDegree >= self.endDegree:
                reachedEnd = True
        else:
            degree = - degree
            if self.actualDegree <= self.endDegree:
                reachedEnd = True

        if reachedEnd:
            # compute amount of way driven
            timeAfterEndingCurve = (self.actualDegree - self.endDegree) / 360 * self.lengthCircle / self.car.get_speed()
            self.actualDegree = self.endDegree
            # use up timeAfterEndingCurve for moving straight ...
            absSpeed = self.car.get_speed()
            # self.car.velocity =

        alpha = self.actualDegree / 180 * math.pi
        # in this case it is a 270 - 360° turn
        self.car.pos[0] = self.curveCenter[0] + self.radius * math.sin(alpha)
        self.car.pos[1] = self.curveCenter[1] + self.radius * math.cos(alpha)

        if self.actualDegree == self.endDegree:
            return [True, timeAfterEndingCurve]
        return [False]


class PhysicsTest(unittest.TestCase):

    def testMovement(self, pos=[0, 0], accel=[1, 1], speed=1, t=1.0, easy_physics=True, direction=0, t_lights=0,
                     nodes_left=0, nth_time=1):
        p = Physics()
        c = PhysicalObject(pos=pos)
        p.update_acceleration(c, accel, nodes_left)
        p.update_velocity(c, t, easy_physics, direction, t_lights, nodes_left)
        p.update_pos(c, t)
        print(c.velocity, c.get_speed(), speed, c.acceleration, accel, '--', 'traffic lights', t_lights, nth_time)
        self.assertEqual(c.get_speed(), speed)

    def testMovement1(self):
        pass
        p = Physics()
        c = PhysicalObject(pos=[0, 0], velocity=[1, 1])
        p.update_acceleration(c, [0, 0])
        p.update_velocity(c, 1.0)
        p.update_pos(c, 1.0)
        self.assertEqual(c.pos, [1.0, 1.0])
        self.assertEqual(c.get_speed(), 1.4142135623730951)

    def testMovement2(self):
        pass
        p = Physics()
        c = PhysicalObject(pos=[0, 0], velocity=[1, 1], acceleration=[1, 1])
        p.update_acceleration(c, [1, 1])
        p.update_velocity(c, 1.0)
        p.update_pos(c, 1.0)
        self.assertEqual(c.pos, [3.0, 3.0])

    def testMovement3(self):
        p = Physics()
        c = PhysicalObject(pos=[0, 0], velocity=[1, 1], acceleration=[1, 1])
        p.update_acceleration(c, [1, 1])
        p.update_velocity(c, 1.0)
        p.update_pos(c, 1.0)
        self.assertEqual(c.pos, [3.0, 3.0])
        p.update_acceleration(c, [-2.0, -2.0])
        p.update_pos(c, 1.0)
        self.assertEqual(c.pos, [6.0, 6.0])
        p.update_pos(c, 1.0)
        self.assertEqual(c.pos, [9.0, 9.0])

    def testCurveRight(self):
        """This test shall do a 90° curve to the right"""
        p = Physics()

        radius = 3
        timestep = 0.1
        max_speed_curve = p.max_speed_curve(radius)
        c = PhysicalObject(pos=[0, 3], velocity=[max_speed_curve, 0], acceleration=[0, 0])

        curve = CurveMovement(0, c, radius, [0, 0], 0, 90)

        print(c.pos)
        time = 0
        while curve.actualDegree < curve.endDegree:
            time = time + timestep
            curve.move(time)
            print(c.pos)

    def testRouting(self):
        """Test the routing of three connections, straight, curve, straight"""
        print("testRouting")
        p = Physics()

        radius = 3
        timestep = 0.1

        max_speed_curve = p.max_speed_curve(radius)
        roads = RoadSystemToolbox.crossroads()
        carStart = 5
        targetNodeID = 17

        startNode = roads.getNode(carStart)
        c = PhysicalObject(pos=startNode.pos, velocity=[max_speed_curve, 0], acceleration=[0, 0])
        print('routing')
        print('routing')
        print('routing')
        currentNode = startNode
        # print(roads.route)

        # simulates the movement
        while True:
            print(currentNode.id)
            if currentNode.id == targetNodeID:
                print("Reached goal")
                # Remove the car
                break
            nextNode = roads.getNextNode(currentNode.id, targetNodeID)
            if nextNode is None:
                print("Error: Cannot find the next route")
            currentNode = nextNode
        # add some test conditions

    def testPhysics(self):
        print('\n\ntestPhysics')

        """Test the routing of three connections, straight, curve, straight"""
        print("testCurveLeft")
        p = Physics()

        radius = 3
        timestep = 0.1

        max_speed_curve = p.max_speed_curve(radius)
        print('max_curve' + str(max_speed_curve))
        roads = RoadSystemToolbox.crossroads()
        carStart = 5
        targetNodeID = 17

        startNode = roads.getNode(carStart)
        c = PhysicalObject(pos=startNode.pos, velocity=[max_speed_curve, 0], acceleration=[0, 0])

        currentNode = startNode
        # print(roads.route)
        # simulates the movement
        # Deal with physics
        # Assume the car goes 1 m/s
        speed = 1

        while True:
            print(str(currentNode.id) + " " + str(c.pos))
            if currentNode.id == targetNodeID:
                print("Reached goal")
                # Remove the car
                break
            nextNode = roads.getNextNode(currentNode.id, targetNodeID)
            if nextNode is None:
                print("Error: Cannot find the next route")
                break

            # if nextNode.distance(c.pos) > speed:
                # pos

            currentNode = nextNode
            c.pos = currentNode.pos


if __name__ == '__main__':
    unittest.main()
