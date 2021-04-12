import copy
import math

class RoadSystem():
  edges = []
  nodes = []
  route = {} # The routing table looks like:
  #


  def __init__(self, nodes, edges):
    self.edges = edges
    self.nodes = nodes
    # The routing table shall tell us what is the next node for the target node (if any)
    route = {}
    # Implement BFS to find the route
    changed = True
    # Preseed with initial route
    print(nodes)
    print(edges)
    for x in nodes:
      print(x.id)
      print('x')
      route[x.id] = {}
    for e in edges:
      for x in edges[e]:
        route[e][x] = x
    print('route')
    print(route)
    # From node 1 to go to node 2 you go via node 2
    # {1: {2: 2},
    #  2: {3: 3, 4: 4, 18: 18} }
    # Next step: go over all edges
    # Results must be:
    # {1: {2:2, 3:2, 4:2, 18:2}}
    while(changed):
      changed = False
      oldRoute = copy.deepcopy(route)
      for r in oldRoute:
        for c in oldRoute[r]:
          for n in oldRoute[c]:
            if n not in route[r]:
              route[r][n] = c
              changed = True
    self.route = route

  def getNextNode(self, nodeID, targetID):
    if not nodeID in self.route:
      return None
    tgt = self.route[nodeID][targetID]
    if tgt == None:
      return tgt
    return self.getNode(tgt)

  def getNode(self, id):
    for x in self.nodes:
      if x.id == id:
        return x
    return None

  def getAllNextNodes(self, node):
    return self.edges[node]
