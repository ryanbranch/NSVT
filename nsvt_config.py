import numpy
import PIL


# G R A P H I C A L     U S E R     I N T E R F A C E S
# UNIVERSAL GUI DEFAULTS
DEFAULT_GUI_WIDTH = 1024
DEFAULT_GUI_HEIGHT = 768
DEFAULT_GUI_FRAMERATE = 15
# GUI CONTROL SELECTION
# If True, a GUI program will run (dependent on APP_TYPE_3D and/or APP_TYPE_PYGAME)
# If False, no GUI program will be launched
RUN_GUI_APP = True
# If True, uses the pyopengl_app.py App
# If False, defers to APP_TYPE_PYGAME
APP_TYPE_3D = False
# If True, uses the pygame_gui_app.py App
# If False, uses the tkinter_gui_app.py App
APP_TYPE_PYGAME = True


# F I L E     I N P U T     A N D     O U T P U T
# GRAPHICS ENGINE FILE I/O
GRAPHICS_OUTPUT_DIRECTORY = "output/"
GRAPHICS_DEFAULT_SAVE_NAME_DIGITS = 6
GRAPHICS_DEFAULT_SAVE_NAME_SUFFIX = ""
GRAPHICS_DEFAULT_SAVE_FORMAT = ".png"
GRAPHICS_FRAMES_FOLDER = "frames/"
GRAPHICS_DEFAULT_FRAME_NAME_DIGITS = 6
GRAPHICS_DEFAULT_FRAME_NAME_SUFFIX = ""
GRAPHICS_DEFAULT_FRAME_FORMAT = ".png"


# N U M P Y  -  R E L A T E D
# GRAPHICS ENGINE (graphics_engine.py)
# NumPy Datatype for the Graphics Engine "Numpy Image" instances
GRAPHICS_IMAGE_NUMPY_DTYPE = numpy.uint8
# Z-dimension length of the "Numpy Image" instances, AKA number of "color channels"
GRAPHICS_IMAGE_NUMPY_ZDIM = 3
# 3D PYOPENGL GRAPHICS (pyopengl_app.py, nsvt_geometry.py)
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
# POINT CLOUDS (point_cloud.py)
POINTCLOUD_IMAGE_NUMPY_DTYPE = numpy.uint8
POINTCLOUD_ARRAY_NUMPY_DTYPE = numpy.float32

# P I L  /  P I L L O W  -  R E L A T E D
# GRAPHICS ENGINE (graphics_engine.py)
PIL_DEFAULT_RESIZE_RESAMPLE_MODE = PIL.Image.NEAREST
