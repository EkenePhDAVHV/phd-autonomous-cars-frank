import unittest
import math

class PhysicalObject():
  def __init__(self, pos=[0, 0], mass=1020, max_acceleration=1, drag=1.0, max_deacceleration=1, acceleration=[0,0], velocity=[0,0]):
    self.pos = pos # in meters
    self.mass = mass # kg
    self.max_acceleration = max_acceleration
    self.max_deacceleration = max_deacceleration
    self.acceleration = acceleration # in m/s^2
    self.velocity = velocity # in m/s
    self.drag = drag

  def get_speed(self):
    """Returns the absolute speed in m/s"""
    return math.sqrt(self.velocity[0] * self.velocity[0] + self.velocity[1]*self.velocity[1])

  def get_force(self):
    return math.sqrt(self.acceleration[0] * self.acceleration[0] + self.acceleration[1]*self.velocity[1]) * self.mass

  def __str__(self):
    return "pos: %s mass:%s maxAccl:%s maxDeaccl:%s Accl:%s Velocity:%s" % (self.pos, self.mass, self.max_acceleration, self.max_deacceleration, self.acceleration, self.velocity)

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


  def move(self, time):
    reachedEnd = False
    degree = 360 * self.car.get_speed() / self.lengthCircle
    if self.endDegree < self.startDegree:
      degree = - degree
    self.actualDegree = (time - self.startTime) * degree

    if self.endDegree >= self.startDegree:
      if (self.actualDegree >= self.endDegree):
        reachedEnd = True
    else:
      degree = - degree
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
    pass
    p = Physics()
    c = PhysicalObject(pos=[0,0], velocity=[1,1])
    p.update_acceleration(c, [0,0])
    p.update_velocity(c, 1.0)
    p.update_pos(c, 1.0)
    self.assertEqual(c.pos, [1.0, 1.0])
    self.assertEqual(c.get_speed(), 1.4142135623730951)

  def testMovement2(self):
    pass
    p = Physics()
    c = PhysicalObject(pos=[0,0], velocity=[1,1], acceleration=[1,1])
    p.update_acceleration(c, [1,1])
    p.update_velocity(c, 1.0)
    p.update_pos(c, 1.0)
    self.assertEqual(c.pos, [3.0, 3.0])


  def testMovement3(self):
    p = Physics()
    c = PhysicalObject(pos=[0,0], velocity=[1,1], acceleration=[1,1])
    p.update_acceleration(c, [1,1])
    p.update_velocity(c, 1.0)
    p.update_pos(c, 1.0)
    self.assertEqual(c.pos, [3.0, 3.0])
    p.update_acceleration(c, [-2.0,-2.0])
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
    c = PhysicalObject(pos=[0,3], velocity=[max_speed_curve, 0], acceleration=[0,0])

    curve = CurveMovement(0, c, radius, [0,0], 0, 90)

    print(c.pos)
    time = 0
    while(curve.actualDegree < curve.endDegree):
      time = time + timestep
      curve.move(time)
      print(c.pos)


  def testCurveLeft(self):
    """This test shall do a 90° curve to the right"""
    print("testCurveLeft")
    p = Physics()

    radius = 3
    timestep = 0.1
    max_speed_curve = p.max_speed_curve(radius)
    c = PhysicalObject(pos=[0,3], velocity=[max_speed_curve, 0], acceleration=[0,0])

    curve = CurveMovement(0, c, radius, [0,0], 0, -90)

    print(c.pos)
    time = 0
    while(curve.actualDegree > curve.endDegree):
      time = time + timestep
      c.velocity = [0, time] # can even adjust the speed in the curve
      curve.move(time)
      print(c.pos)

    #self.assertEqual(c.pos, [5.9544232590366235, 0.5209445330007912],[4.928362829059617, 2.298133329356934])

#import self



if __name__ == '__main__':
    unittest.main()
