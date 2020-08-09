# TODO:
#   A. Placeholder

# Library Imports
import math
import numpy
from numba import jit
from numba.extending import overload

# Local Imports
import nsvt_config as config

# REQUIRES:
#  - theta is an angle in radians
#@jit(nopython=True)
def getRotationMatrixX(theta):
    if theta == 0:
        return numpy.identity(3, dtype=config.GEOMETRY_ROTATION_NUMPY_DTYPE)
    else:
        return numpy.array([
            [1.,              0.,                      0.],
            [0., math.cos(theta), (-1. * math.sin(theta))],
            [0., math.sin(theta),         math.cos(theta)]
        ], dtype=config.GEOMETRY_ROTATION_NUMPY_DTYPE)

# REQUIRES:
#  - theta is an angle in radians
#@jit(nopython=True)
def getRotationMatrixY(theta):
    if theta == 0:
        return numpy.identity(3, dtype=config.GEOMETRY_ROTATION_NUMPY_DTYPE)
    else:
        return numpy.array([
            [math.cos(theta),        0, math.sin(theta)],
            [0,                      1,               0],
            [(-1 * math.sin(theta)), 0, math.cos(theta)]
        ], dtype=config.GEOMETRY_ROTATION_NUMPY_DTYPE)

# REQUIRES:
#  - theta is an angle in radians
#@jit(nopython=True)
def getRotationMatrixZ(theta):
    if theta == 0:
        return numpy.identity(3, dtype=config.GEOMETRY_ROTATION_NUMPY_DTYPE)
    else:
        return numpy.array([
            [math.cos(theta), (-1 * math.sin(theta)), 0],
            [math.sin(theta), math.cos(theta),        0],
            [0,               0,                      1]
        ], dtype=config.GEOMETRY_ROTATION_NUMPY_DTYPE)


# MODIFIES:
#  - triangleVertices
@jit(nopython=True)
def updateTriangleVertices(vertices, triangles, triangleVertices):
    # Invariant Checks (NOT FULLY IMPLEMENTED)
    #  - Must have already built the base self.triangleVertices array
    invariantFail = (triangleVertices.size == 0)
    if invariantFail:
        print("ERROR: Failed invariant checks in nsvt_geometry.updateTriangleVertices()")
        return False

    for t, triangle in enumerate(triangles):
        for v, vertex in enumerate(triangle):
            for i in range(3):
                triangleVertices[t, 3 * v + i] = vertices[int(vertex)][i]

# MODIFIES:
#  - vertices
@jit(nopython=True)
def translateVertices(vertices, moveX, moveY, moveZ):
    # Invariant Checks (NOT YET IMPLEMENTED)
    invariantFail = False
    if invariantFail:
        print("ERROR: Failed invariant checks in nsvt_geometry.translate()")
        return False

    for vertex in vertices:
        vertex[0] += moveX
        vertex[1] += moveY
        vertex[2] += moveZ

    # Modify the X/Y/Z coordinates of each vertex
    #vertices[:, 0] += moveX
    #vertices[:, 1] += moveY
    #vertices[:, 2] += moveZ


# REQUIRES:
#  - rotateX/rotateY/rotateZ are angles in degrees
# MODIFIES:
#  - vertices
# TODO: Make this function Numba-compatible
#@jit(nopython=True)
def rotateVertices(vertices, rotateX, rotateY, rotateZ):
    # Invariant Checks (NOT YET IMPLEMENTED)
    invariantFail = False
    if invariantFail:
        print("ERROR: Failed invariant checks in nsvt_geometry.translate()")
        return False

    verticesTransposed = numpy.transpose(vertices)
    #rMatX = getRotationMatrixX(math.radians(rotateX))
    #rMatY = getRotationMatrixY(math.radians(rotateY))
    #rMatZ = getRotationMatrixZ(math.radians(rotateZ))
    #rMat = numpy.matmul(rMatX, rMatY)
    #rMat = numpy.matmul(rMat, rMatZ)
    #verticesTransposed = numpy.matmul(rMat, verticesTransposed)
    vertices = numpy.transpose(verticesTransposed)
    #return numpy.transpose(verticesTransposed)