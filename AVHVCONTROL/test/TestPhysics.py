import unittest
import math

from AVHVCONTROL.Simulator import RoadNode
from AVHVCONTROL.test.RoadSystemToolbox import RoadSystemToolbox

class PhysicalObject():
    def __init__(self, pos=[0, 0], mass=1020, max_acceleration=1, drag=1.0, max_deacceleration=1, acceleration=[0, 0],
                 velocity=[0, 0]):
        self.pos = pos  # in meterso it
        self.mass = mass  # kg
        self.max_acceleration = max_acceleration
        self.max_deacceleration = max_deacceleration
        self.acceleration = acceleration  # in m/s^2
        self.velocity = velocity  # in m/s
        self.drag = drag

    def get_speed(self):
        """Returns the absolute speed in m/s"""
        return math.sqrt(self.velocity[0] * self.velocity[0] + self.velocity[1] * self.velocity[1])

    def get_force(self):
        return math.sqrt(
            self.acceleration[0] * self.acceleration[0] + self.acceleration[1] * self.velocity[1]) * self.mass

    def __str__(self):
        return "pos: %s mass:%s maxAccl:%s maxDeaccl:%s Accl:%s Velocity:%s" % (
        self.pos, self.mass, self.max_acceleration, self.max_deacceleration, self.acceleration, self.velocity)


class Physics():
    def __init__(self, friction=0.75, gravity=9.8):
        self.friction = friction
        self.gravity = gravity

    def update_acceleration(self, obj, delta_accl):
        obj.acceleration[0] = obj.acceleration[0] + delta_accl[0]
        obj.acceleration[1] = obj.acceleration[1] + delta_accl[1]

    def update_velocity(self, obj, delta_t):
        obj.velocity[0] = obj.velocity[0] + delta_t * obj.acceleration[0]
        obj.velocity[1] = obj.velocity[1] + delta_t * obj.acceleration[1]

    def update_pos(self, obj, delta_t):
        obj.pos[0] = obj.pos[0] + delta_t * obj.velocity[0]
        obj.pos[1] = obj.pos[1] + delta_t * obj.velocity[1]

    def max_speed_curve(self, curve_radius):
        return math.sqrt(self.gravity * self.friction * curve_radius)


class CurveMovement():
    def __init__(self, time, car, radius, curveCenter, startDegree, endDegree):
        self.curveCenter = curveCenter
        self.lengthCircle = 2 * math.pi * radius
        self.radius = radius
        self.startTime = time
        self.endDegree = endDegree
        self.actualDegree = startDegree
        self.startDegree = startDegree
        self.car = car
        if startDegree >= endDegree:
          self.direction = "left"
        else:
          self.direction = "right"

    def move(self, time):
        reachedEnd = False
        degree = 360 * self.car.get_speed() / self.lengthCircle
        if self.direction == "left":
            degree = -degree
        self.actualDegree = self.startDegree + (time - self.startTime) * degree

        if self.direction == "right":
            if (self.actualDegree >= self.endDegree):
                reachedEnd = True
        else:
            if (self.actualDegree <= self.endDegree):
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

        if (self.actualDegree == self.endDegree):
            return [True, timeAfterEndingCurve]
        return [False]


class PhyicsTest(unittest.TestCase):

    def testMovement1(self):
        p = Physics()
        c = PhysicalObject(pos=[0, 0], velocity=[1, 1])
        p.update_acceleration(c, [0, 0])
        p.update_velocity(c, 1.0)
        p.update_pos(c, 1.0)
        self.assertEqual(c.pos, [1.0, 1.0])
        self.assertEqual(c.get_speed(), 1.4142135623730951)

    def testMovement2(self):
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
        print("testCurveRight")
        p = Physics()

        radius = 3
        timestep = 0.1
        max_speed_curve = p.max_speed_curve(radius)
        c = PhysicalObject(pos=[0, 3], velocity=[max_speed_curve, 0], acceleration=[0, 0])

        curve = CurveMovement(0, c, radius, [0, 0], 0, 90)

        print(c.pos)
        time = 0
        while (curve.actualDegree < curve.endDegree):
            time = time + timestep
            curve.move(time)
            print(c.pos)


    def testCurveLeft(self):
        """This test shall do a 90° curve to the left"""
        print("testCurveLeft")
        p = Physics()

        radius = 3
        timestep = 0.1
        max_speed_curve = p.max_speed_curve(radius)
        c = PhysicalObject(pos=[3, 0], velocity=[max_speed_curve, 0], acceleration=[0, 0])

        curve = CurveMovement(0, c, radius, [0, 0], 90, 0)

        print(c.pos)
        time = 0
        while (curve.actualDegree > curve.endDegree):
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
        #print(roads.route)
        # simulates the movement
        while True:
          print(currentNode.id)
          if currentNode.id == targetNodeID:
            print("Reached goal")
            # Remove the car
            break
          nextNode = roads.getNextNode(currentNode.id, targetNodeID)
          if nextNode == None:
            print("Error: Cannot find the next route")
          currentNode = nextNode
        # add some test conditions

    def testAcceleration(self):
      p = Physics()
      c = PhysicalObject(pos=[0, 0], velocity=[0, 0], acceleration=[0, 0])

      # Simulate
      # - 10 timesteps of acceleration
      # - 10 timesteps of constant speed
      # - 10 timesepts of deceleration

      delta_t = 0.1
      print("Acceleration phase")
      p.update_acceleration(c, [1, 0])
      for i in range(0, 10):
        p.update_velocity(c, delta_t)
        p.update_pos(c, delta_t)
        print(c)

      print("Constant phase")
      p.update_acceleration(c, [-1, 0])
      for i in range(0, 10):
        p.update_velocity(c, delta_t)
        p.update_pos(c, delta_t)
        print(c)

      print("Deceleration phase")
      p.update_acceleration(c, [-1, 0])
      for i in range(0, 10):
        p.update_velocity(c, delta_t)
        p.update_pos(c, delta_t)
        print(c)

    def testPhysics(self):
        print('\n\ntestPhysics')

        """Test the routing of three connections, straight, curve, straight"""
        print("testCurveLeft")
        p = Physics()

        radius = 35
        timestep = 1

        max_speed_curve = p.max_speed_curve(radius)
        print('max_curve ' + str(max_speed_curve))
        roads = RoadSystemToolbox.crossroads()
        carStart = 5
        targetNodeID = 17

        startNode = roads.getNode(carStart)
        c = PhysicalObject(pos=startNode.pos, velocity=[max_speed_curve, 0], acceleration=[0, 0])

        currentNode = startNode
        #print(roads.route)
        # simulates the movement
        # Deal with physics
        # Assume the car goes 1 m/s

        speed = 1
        time = 0
        while True:
            time = time + timestep
            # need to check where are you?
            # are we in a curve:
            if currentNode.curve_radius :
              curve = CurveMovement(time, c, currentNode.curve_radius, currentNode.curve_center, 360, 270)
              while (curve.actualDegree > curve.endDegree):
                  print("degree: %d %d" % (curve.actualDegree, curve.endDegree))
                  time = time + timestep
                  curve.move(time)
                  print(c.pos)
            # are we straight: do sth else

            # The array that will be returned from this function.
            response_positions = []

            while True:
            # print(str(currentNode.id) + " " + str(c.pos))

                response_positions.append(RoadNode(currentNode.id, c.pos))
                if currentNode.id == targetNodeID:
                    print("Reached goal")

                    # Remove the car
                    break
                nextNode = roads.getNextNode(currentNode.id, targetNodeID)
                if nextNode == None:
                    print("Error: Cannot find the next route")
                    break
                # if nextNode.distance(c.pos) > speed:
                # pos
                currentNode = nextNode
                c.pos = currentNode.pos

            return response_positions

if __name__ == '__main__':
   unittest.main()