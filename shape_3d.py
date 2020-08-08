# TODO:
#   A. Placeholder

# Library Imports
import numpy

# Local Imports
import nsvt_config as config

# Abstraction of any 3-dimensional shape via its vertices and their connections
# INVARIANTS:
#   A. vertices_ must be a list of X,Y,Z coordinates. It will be converted to a 2D NumPy array
#   B. edges_ must be a list of vertex pairs. It will be converted to a 2D NumPy array
class Shape3D():
    def __init__(self):
        self.vertices = None
        self.edges = None
        self.triangles = None
        self.triangleVertices = None
        self.hasVertices = False
        self.hasEdges = False
        self.hasTriangles = False
        self.hasTriangleVertices = False


    def setVertices(self, vertices_):
        # Invariant Checks (NOT YET IMPLEMENTED)
        invariantFail = False
        if invariantFail:
            print("ERROR: Failed invariant checks in Shape3D.setVertices()")
            return False

        self.vertices = numpy.asarray(vertices_, dtype=config.SHAPE3D_VERTICES_NUMPY_DTYPE)
        self.hasVertices = True


    def setEdges(self, edges_):
        # Invariant Checks (NOT YET IMPLEMENTED)
        invariantFail = False
        if invariantFail:
            print("ERROR: Failed invariant checks in Shape3D.setEdges()")
            return False

        self.edges = numpy.asarray(edges_, dtype=config.SHAPE3D_EDGES_NUMPY_DTYPE)
        self.hasEdges = True


    def setTriangles(self, triangles_):
        # Invariant Checks (NOT YET IMPLEMENTED)
        invariantFail = False
        if invariantFail:
            print("ERROR: Failed invariant checks in Shape3D.setTriangles()")
            return False

        self.triangles = numpy.asarray(triangles_, dtype=config.SHAPE3D_TRIANGLES_NUMPY_DTYPE)
        self.hasTriangles = True


    def generateTriangleVertices(self):
        # Invariant Checks (NOT YET IMPLEMENTED)
        #  - Must have already called self.setTriangles
        invariantFail = False
        if invariantFail:
            print("ERROR: Failed invariant checks in Shape3D.setTriangles()")
            return False

        self.triangleVertices = numpy.ones((self.triangles.shape[0], self.triangles.shape[1] * 3),
                                       dtype=config.SHAPE3D_VERTICES_NUMPY_DTYPE)
        for t, triangle in enumerate(self.triangles):
            for v, vertex in enumerate(triangle):
                for i in range(3):
                    self.triangleVertices[t, 3 * v + i] = self.vertices[int(vertex)][i]
        self.hasTriangleVertices = True
        #print(self.triangleVertices)
