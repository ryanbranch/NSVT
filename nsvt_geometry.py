# TODO:
#   A. Placeholder

# Library Imports
import math
import numpy
from numba import double, jit
from numba.extending import overload

# Local Imports
import nsvt_config as config
import numba_vectorized as nv

# REQUIRES:
#  - vector is a 1-dimensional array of scalar values
@jit(nopython=True)
def calcMagnitude(vector):
    vectorSum = 0
    for val in vector:
        vectorSum += val * val
    return vectorSum

@jit(nopython=True)
def getUnitVector3D(vectorX, vectorY, vectorZ):
    magnitude = calcMagnitude([vectorX, vectorY, vectorZ])
    return (vectorX / magnitude, vectorY / magnitude, vectorZ / magnitude)

# REQUIRES:
#  - theta is an angle in radians
@jit(nopython=True)
def getRotationMatrixX(theta):
    if theta == 0:
        return numpy.asarray([
            [1., 0., 0.],
            [0., 1., 0.],
            [0., 0., 1.]
        ], dtype=config.GEOMETRY_ROTATION_NUMPY_DTYPE)
    else:
        return numpy.asarray([
            [1.,            0.,                     0.],
            [0., nv.cos(theta),   (-1 * nv.sin(theta))],
            [0., nv.sin(theta),          nv.cos(theta)]
        ], dtype=config.GEOMETRY_ROTATION_NUMPY_DTYPE)

# REQUIRES:
#  - theta is an angle in radians
@jit(nopython=True)
def getRotationMatrixY(theta):
    if theta == 0:
        return numpy.asarray([
            [1., 0., 0.],
            [0., 1., 0.],
            [0., 0., 1.]
        ], dtype=config.GEOMETRY_ROTATION_NUMPY_DTYPE)
    else:
        return numpy.array([
            [math.nv.cos(theta),        0.,  math.nv.sin(theta)],
            [0.,                        1.,                  0.],
            [(-1 * math.nv.sin(theta)), 0.,  math.nv.cos(theta)]
        ], dtype=config.GEOMETRY_ROTATION_NUMPY_DTYPE)

# REQUIRES:
#  - theta is an angle in radians
@jit(nopython=True)
def getRotationMatrixZ(theta):
    if theta == 0:
        return numpy.asarray([
            [1., 0., 0.],
            [0., 1., 0.],
            [0., 0., 1.]
        ], dtype=config.GEOMETRY_ROTATION_NUMPY_DTYPE)
    else:
        return numpy.array([
            [math.nv.cos(theta), (-1. * math.nv.sin(theta)), 0.],
            [math.nv.sin(theta), math.nv.cos(theta),         0.],
            [0.,             0.,                             1.]
        ], dtype=config.GEOMETRY_ROTATION_NUMPY_DTYPE)

# REQUIRES:
#  - (uX, uY, uZ) forms a unit vector of length 1
#  - theta is an angle in radians
@jit(nopython=True)
def getRotationMatrixAxisAngle(uX, uY, uZ, theta):
    if theta == 0:
        return numpy.asarray([
            [1., 0., 0.],
            [0., 1., 0.],
            [0., 0., 1.]
        ], dtype=config.GEOMETRY_ROTATION_NUMPY_DTYPE)
    else:
        return numpy.array([
            [(nv.cos(theta) + (uX * uX * (1. - nv.cos(theta)))),        ((uX * uY * (1. - nv.cos(theta))) - (uZ * nv.sin(theta))),  ((uX * uZ * (1. - nv.cos(theta))) + (uY * nv.sin(theta)))],
            [((uX * uY * (1. - nv.cos(theta))) + (uZ * nv.sin(theta))), (nv.cos(theta) + (uY * uY * (1. - nv.cos(theta)))),         ((uY * uZ * (1. - nv.cos(theta))) - (uX * nv.sin(theta)))],
            [((uX * uZ * (1. - nv.cos(theta))) - (uY * nv.sin(theta))), ((uY * uZ * (1. - nv.cos(theta))) + (uX * nv.sin(theta))),         (nv.cos(theta) + (uZ * uZ * (1. - nv.cos(theta))))]
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
def rotateVertices(vertices, degreesX, degreesY, degreesZ):
    # Invariant Checks (NOT YET IMPLEMENTED)
    invariantFail = False
    if invariantFail:
        print("ERROR: Failed invariant checks in nsvt_geometry.translate()")
        return False

    verticesTransposed = numpy.transpose(vertices)
    rMatX = getRotationMatrixX(math.radians(degreesX))
    rMatY = getRotationMatrixY(math.radians(degreesY))
    rMatZ = getRotationMatrixZ(math.radians(degreesZ))
    rMat = numpy.matmul(rMatX, rMatY)
    rMat = numpy.matmul(rMat, rMatZ)
    verticesTransposed = numpy.matmul(rMat, verticesTransposed)
    verticesTransposed = numpy.transpose(verticesTransposed)
    vertices[:] = verticesTransposed[:]
    return vertices

# REQUIRES:
#  - rotateX/rotateY/rotateZ are angles in degrees
# MODIFIES:
#  - vertices
# TODO: Make this function Numba-compatible
#@jit(nopython=True)
def rotateVerticesAxisAngle(vertices, axisX, axisY, axisZ, degrees):
    # Invariant Checks (NOT YET IMPLEMENTED)
    invariantFail = False
    if invariantFail:
        print("ERROR: Failed invariant checks in nsvt_geometry.translate()")
        return False

    verticesTransposed = numpy.transpose(vertices)
    unitVec = getUnitVector3D(axisX, axisY, axisZ)
    rMat = getRotationMatrixAxisAngle(unitVec[0], unitVec[1], unitVec[2], math.radians(degrees))
    verticesTransposed = numpy.matmul(rMat, verticesTransposed)
    verticesTransposed = numpy.transpose(verticesTransposed)
    vertices[:] = verticesTransposed[:]
    return vertices
