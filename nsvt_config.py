import numpy

# NumPy Datatype for the Vertices array
#  - Must be some sort of floating point number
SHAPE3D_VERTICES_NUMPY_DTYPE = numpy.float32

# NumPy Datatype for the Edges array
#  - Values will always be zero or positive, so the type can be unsigned
#  - uint8 will only support up to 256 vertices in a shape, whereas uint16 allows up to 65536
SHAPE3D_EDGES_NUMPY_DTYPE = numpy.uint16

# NumPy Datatype for the Triangles array
#  - Values will always be zero or positive, so the type can be unsigned
#  - uint8 will only support up to 256 vertices in a shape, whereas uint16 allows up to 65536
SHAPE3D_TRIANGLES_NUMPY_DTYPE = numpy.uint16
