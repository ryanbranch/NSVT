# TODO:
#   A. Placeholder

# Library Imports
import numpy
import numba
from numba import jit
import PIL
from PIL import Image
from pathlib import Path
import glob
import random

# Local Imports


class GraphicsEngine():
    # C L A S S      A T T R I B U T E S
    DEFAULT_GRAPHICS_WIDTH = 100
    DEFAULT_GRAPHICS_HEIGHT = 100
    DEFAULT_NUMPY_DATATYPE = numpy.uint8
    NUM_COLOR_CHANNELS = 3
    OUTPUT_DIRECTORY = "output/"
    DEFAULT_SAVE_NAME_DIGITS = 6
    DEFAULT_SAVE_NAME_SUFFIX = ""
    DEFAULT_SAVE_FORMAT = ".png"
    FRAMES_FOLDER = "frames/"
    DEFAULT_FRAME_NAME_DIGITS = 6
    DEFAULT_FRAME_NAME_SUFFIX = ""
    DEFAULT_FRAME_FORMAT = ".png"
    # NUMPY IMAGE (META)METADATA
    # PIL METADATA
    DEFAULT_PIL_RESIZE_RESAMPLE_MODE = PIL.Image.NEAREST

    def __init__(self, wrapper_):

        self.wrapper = wrapper_

        self.saveCount = 0
        self.pilImageScaleX = 10.0
        self.pilImageScaleY = 10.0

        self.numpyImage = numpy.ones(shape=(GraphicsEngine.DEFAULT_GRAPHICS_HEIGHT,
                                            GraphicsEngine.DEFAULT_GRAPHICS_WIDTH,
                                            GraphicsEngine.NUM_COLOR_CHANNELS),
                                     dtype=GraphicsEngine.DEFAULT_NUMPY_DATATYPE
                                     ) * 255
        self.pilImage: Image
        # Sets the value of self.pilImage
        self.refreshPilImage()

        self.makeDirectories()

        self.saveImage(self.getFramePath(self.saveCount))
        self.saveCount += 1

    # TODO: Fix so that this function works even when directory variables are multiple folders deep
    # Creates the folder(s) in which outputs will be saved
    def makeDirectories(self):
        cwDir = Path.cwd()
        dirs = [cwDir / GraphicsEngine.OUTPUT_DIRECTORY,  # MAIN OUTPUT DIRECTORY
                cwDir / GraphicsEngine.OUTPUT_DIRECTORY / GraphicsEngine.FRAMES_FOLDER]  # FRAMES DIRECTORY
        for newDir in dirs:
            if not newDir.is_dir():
                newDir.mkdir()

    # NOTE: Call this function before any use of self.pilImage,
    #       unless it is clear that self.numpyImage has not been modified since the last refreshPilImage() call.
    def refreshPilImage(self):
        if (self.pilImageScaleX == 1.0 and self.pilImageScaleY == 1.0):
            self.pilImage = Image.fromarray(self.numpyImage[:, :, 0:GraphicsEngine.NUM_COLOR_CHANNELS].astype("uint8"))
        else:
            self.pilImage = Image.fromarray(self.numpyImage[:, :, 0:GraphicsEngine.NUM_COLOR_CHANNELS].astype("uint8")).resize(
                (int(self.numpyImage.shape[1] * self.pilImageScaleX),
                 int(self.numpyImage.shape[0] * self.pilImageScaleY)),
                GraphicsEngine.DEFAULT_PIL_RESIZE_RESAMPLE_MODE)


    def getSavePath(self, fileIndex, digits=DEFAULT_SAVE_NAME_DIGITS, suffix=DEFAULT_SAVE_NAME_SUFFIX,
                    format=DEFAULT_SAVE_FORMAT):
        return GraphicsEngine.OUTPUT_DIRECTORY + str(fileIndex).zfill(digits) + suffix + format

    def getFramePath(self, fileIndex, digits=DEFAULT_FRAME_NAME_DIGITS, suffix=DEFAULT_FRAME_NAME_SUFFIX,
                     format=DEFAULT_FRAME_FORMAT):
        return GraphicsEngine.OUTPUT_DIRECTORY + GraphicsEngine.FRAMES_FOLDER + str(fileIndex).zfill(digits) + suffix + format

    def saveImage(self, path):
        Image.fromarray(self.numpyImage[:,:,0:GraphicsEngine.NUM_COLOR_CHANNELS].astype("uint8")).save(path)

    def randomizeRandomPixel(self):
        self.numpyImage[random.randrange(self.numpyImage.shape[0]),
                        random.randrange(self.numpyImage.shape[0])] = [random.randint(0, 255),
                                                                       random.randint(0, 255),
                                                                       random.randint(0, 255)]

    @staticmethod
    @jit(nopython=True)
    def clearImageNumba(imageData, color=255):
        imageData[:, :, :] = color
        return imageData

    @staticmethod
    @jit(nopython=True)
    def manipulateImageNumba(imageData):
        dims = imageData.shape
        for y in range(dims[0]):
            for x in range(dims[1]):
                imageData[y, x] += numpy.uint8(y + x)
        #imageData += 32
        return imageData

    def drawPlayer(self):
        self.numpyImage[self.wrapper.pEngines[-1].playerY,
                        self.wrapper.pEngines[-1].playerX] = [0, 255, 255]