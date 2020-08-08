# TODO:
#   A. Placeholder

# Library Imports
import numpy
from numba import jit

# Local Imports

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
def translate(vertices, moveX, moveY, moveZ):
    # Invariant Checks (NOT YET IMPLEMENTED)
    invariantFail = False
    if invariantFail:
        print("ERROR: Failed invariant checks in nsvt_geometry.translate()")
        return False

    for vertex in vertices:
        vertex[0] += moveX
        vertex[1] += moveY
        vertex[2] += moveZ
