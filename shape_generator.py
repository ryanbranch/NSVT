# TODO:
#   A. Placeholder

# Library Imports
import numpy
from numba import jit

# Local Imports
import shape_3d
import nsvt_config as config

class ShapeGenerator():

    def __init__(self):
        self.shapeCount = 0
        print()

    @staticmethod
    @jit(nopython=True)
    def getCubeVertices():
        return numpy.array([[0, 0, 0],  # A
                            [1, 0, 0],  # B
                            [0, 1, 0],  # C
                            [0, 0, 1],  # D
                            [1, 1, 0],  # E
                            [1, 0, 1],  # F
                            [0, 1, 1],  # G
                            [1, 1, 1]]) # H

    @staticmethod
    @jit(nopython=True)
    def getCubeEdges():
        return numpy.array([[0, 1],   # A to B
                            [0, 2],   # A to C
                            [0, 3],   # A to D
                            [1, 4],   # B to E
                            [1, 5],   # B to F
                            [2, 4],   # C to E
                            [2, 6],   # C to G
                            [3, 5],   # D to F
                            [3, 6],   # D to G
                            [4, 7],   # E to H
                            [5, 7],   # F to H
                            [6, 7]])  # G to H

    @staticmethod
    @jit(nopython=True)
    def getCubeTriangles():
        return numpy.array([[0, 1, 4],   # A, B, E
                            [0, 1, 5],   # A, B, F
                            [0, 2, 4],   # A, C, E
                            [0, 2, 6],   # A, C, G
                            [0, 3, 5],   # A, D, F
                            [0, 3, 6],   # A, D, G
                            [1, 4, 7],   # B, E, H
                            [1, 5, 7],   # B, F, H
                            [2, 4, 7],   # C, E, H
                            [2, 6, 7],   # C, G, H
                            [3, 5, 7],   # D, F, H
                            [3, 6, 7]])  # D, G, H

    def generateCuboid(self, dimX, dimY, dimZ):
        # Creates an empty Shape3D object
        shape = shape_3d.Shape3D()
        # Initializes the vertex array as a unit cube
        vertexArray = numpy.asarray(self.getCubeVertices(), dtype=config.SHAPE3D_VERTICES_NUMPY_DTYPE)
        # Scales the vertex array by (dimX, dimY, dimZ) via matrix multiplication
        vertexArray[:, 0] *= dimX
        vertexArray[:, 1] *= dimY
        vertexArray[:, 2] *= dimZ
        # Calls the set() methods for the Shape's vertices/edges/triangles
        shape.setVertices(vertexArray)
        shape.setEdges(numpy.asarray(self.getCubeEdges(), dtype=config.SHAPE3D_EDGES_NUMPY_DTYPE))
        shape.setTriangles(numpy.asarray(self.getCubeTriangles(), dtype=config.SHAPE3D_TRIANGLES_NUMPY_DTYPE))
        shape.generateTriangleVertices()
        # Increments self.shapeCount and returns the new Shape3D object
        self.shapeCount += 1
        return shape
