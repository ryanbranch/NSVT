# TODO:
#   A. Placeholder

# Library Imports
import numpy

# Local Imports
import nsvt_config as config

class PointCloudGenerator():

    def __init__(self, wrapper_):

        self.wrapper = wrapper_

    @staticmethod
    def cloudToNumpyImage(cloudIn):
        imageOut = numpy.ones((1), dtype=config.GRAPHICS_IMAGE_NUMPY_DTYPE)
        print()

    @staticmethod
    def numpyImageToCloud(imageIn):
        print()

class PointCloud():

    def __init__(self):
        print()
