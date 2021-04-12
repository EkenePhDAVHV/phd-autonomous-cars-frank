# https://en.wikipedia.org/wiki/Automobile_drag_coefficient
# https://en.wikipedia.org/wiki/Automotive_aerodynamics#Drag_Coefficient_and_Drag_Area
import svgwrite
import math


class lane():
  """This is a straight lane"""
  pos1 = [0,0]
  pos2 = [0,0]
  width = 0

  def __init__(self, pos1, pos2, width):
    self.pos1 = pos1
    self.pos2 = pos2
    self.width = width

  def draw(self, dwg):
    dwg.add(dwg.line((self.pos1[0], self.pos1[1]),(self.pos2[0], self.pos2[1]), stroke=svgwrite.rgb(200, 200, 200, '%')))


class curve():
  pos1 = []
  pos2 = []
  radius = 0
  curve_center = []

  def __init__(self, pos1, pos2, curve_center):
    self.pos1 = pos1
    self.pos2 = pos2
    self.curve_center = curve_center
    self.radius = math.sqrt((pos1[0] - curve_center[0])*(pos1[0] - curve_center[0])+(pos1[1] - curve_center[1])*(pos1[1] - curve_center[1]))

  def draw(self, dwg):
    dwg.path(d="M %f,%f a %f,%f %f 0,0 %f,%f"
     % (self.pos1[0], self.pos1[1], 5, 5, 0, self.pos2[0], self.pos2[1]),
     stroke=svgwrite.rgb(200, 200, 200, '%'))
     
    dwg.add(dwg.line((self.pos1[0], self.pos1[1]),(self.pos2[0], self.pos2[1]), stroke=svgwrite.rgb(200, 200, 200, '%')))

class lights():
  pos = []

  def draw(self, dwg):
    pass

class intersection():
  lanes = []
  curves = []
  lights = []
  crosswalks = []

  def __init__(self, lanes, curves, lights, crosswalks):
    self.lanes = lanes
    self.curves = curves
    self.lights = lights
    self.crosswalks = crosswalks

  def draw(self, dwg):
    for x in self.lanes:
      x.draw(dwg)
    for x in self.curves:
      x.draw(dwg)
    for x in self.lights:
      x.draw(dwg)
    for x in self.crosswalks:
      x.draw(dwg)

class physics():
  def windforce(self, v):
    return v[0]*v[0]*0.6*0.26*6

p = physics()

class car():
  posx = 0
  posy = 0
  drag_area = 6 # lamborgini
  v = []
  m = 1500

  def __init__(self, posx, posy, v):
    self.posx = posx
    self.posy = posy
    self.v = v

  def move(self, t, step):
    # let's assume the car wants to move along x
    # let's accelerate all the time
    # a = uHf * g / 2
    # f_wind = p.windforce(self.v)
    a = 0.5 * 9.81 / 2 * step
    self.posx = self.posx + self.v[0] + a/2
    self.v[0] = self.v[0] + a

  def draw(self, dwg):
    dwg.add(dwg.circle((self.posx, self.posy), 2, stroke=svgwrite.rgb(255, 0, 0, '%')))

  def __str__(self):
    return "car(pos(%s,%s), v=%s m/s)" %(self.posx, self.posy, self.v)


class simulator():
  timestep = 0.1 # in seconds
  end_time = 10 # in seconds
  cars = []
  intersection = ""

  def __init__(self, cars, intersection):
    self.cars = cars
    self.intersection = intersection

  def start(self):
    iter = 0
    t = 0
    d = self.timestep
    while(t < self.end_time):
      for c in self.cars:
        c.move(t, d)
      self.save(iter)
      t += d
      iter = iter + 1

  def save(self, iter):
    dwg = svgwrite.Drawing('out%0.5d.svg' % iter, profile='tiny')
    #dwg.add(dwg.rect((0,0), size=(100,100), stroke=svgwrite.rgb(0, 0, 255, '%')))

    self.intersection.draw(dwg)

    for c in self.cars:
      c.draw(dwg)
    dwg.save()
  # mencoder mf://*.svg -mf w=800:h=600:fps=1:type=jpg -ovc lavc -lavcopts vcodec=mpeg4:mbd=2:trell -oac copy -o output.avi

if __name__ == '__main__':
  lanes = [lane([0,0], [20,0], 2), lane([5,20],[5,10], 2)]
  curves = [curve([5,10], [10,0], [10,10])]
  s = simulator([car(0, 0, [0,0])], intersection(lanes, curves, [], []))
  s.start()
  for c in s.cars:
    print(c)
