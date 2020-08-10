import numpy

# N U M P Y
# NUMPY DATATYPES
# NumPy Datatype for the Vertices array
#  - Must be some sort of floating point number
SHAPE3D_VERTICES_NUMPY_DTYPE = numpy.float32
# NumPy Datatype for the Edges array
#  - Values will always be zero or positive, so the type can be unsigned
#  - uint8 will only support up to 256 vertices in a shape, whereas uint16 allows up to 65536
SHAPE3D_EDGES_NUMPY_DTYPE = numpy.uint32
# NumPy Datatype for the Triangles array
#  - Values will always be zero or positive, so the type can be unsigned
#  - uint8 will only support up to 256 vertices in a shape, whereas uint16 allows up to 65536
SHAPE3D_TRIANGLES_NUMPY_DTYPE = numpy.uint32
# NumPy Datatype for Elemental Rotation Matrices
#  - Values are used in matrix multiplication and should match the vertex datatype for that reason
GEOMETRY_ROTATION_NUMPY_DTYPE = SHAPE3D_VERTICES_NUMPY_DTYPE


# G R A P H I C A L     U S E R     I N T E R F A C E S
# UNIVERSAL GUI DEFAULTS
DEFAULT_GUI_WIDTH = 1024
DEFAULT_GUI_HEIGHT = 768
DEFAULT_GUI_FRAMERATE = 15
# GUI TYPE SELECTION
# If True, uses the pyopengl_app.py App
# If False, defers to APP_TYPE_PYGAME
APP_TYPE_3D = False
# If True, uses the pygame_gui_app.py App
# If False, uses the tkinter_gui_app.py App
APP_TYPE_PYGAME = True