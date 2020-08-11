# TODO:
#   A. Placeholder

# Library Imports
import numpy
from numba import jit
import PIL
from PIL import Image
from pathlib import Path
import random

# Local Imports
import nsvt_config as config

class GraphicsEngine():
    # C L A S S      A T T R I B U T E S

    # NUMPY IMAGE (META)METADATA
    # PIL METADATA

    def __init__(self, wrapper_):

        self.wrapper = wrapper_

        self.saveCount = 0
        self.pilImageScaleX = 1.0
        self.pilImageScaleY = 1.0

        self.numpyImage = numpy.ones(shape=(config.DEFAULT_GUI_WIDTH,
                                            config.DEFAULT_GUI_HEIGHT,
                                            config.GRAPHICS_IMAGE_NUMPY_ZDIM),
                                     dtype=config.GRAPHICS_IMAGE_NUMPY_DTYPE
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
        dirs = [cwDir / config.GRAPHICS_OUTPUT_DIRECTORY,  # MAIN OUTPUT DIRECTORY
                cwDir / config.GRAPHICS_OUTPUT_DIRECTORY / config.GRAPHICS_FRAMES_FOLDER]  # FRAMES DIRECTORY
        for newDir in dirs:
            if not newDir.is_dir():
                newDir.mkdir()

    # NOTE: Call this function before any use of self.pilImage,
    #       unless it is clear that self.numpyImage has not been modified since the last refreshPilImage() call.
    def refreshPilImage(self):
        if (self.pilImageScaleX == 1.0 and self.pilImageScaleY == 1.0):
            self.pilImage = Image.fromarray(self.numpyImage[:, :, 0:config.GRAPHICS_IMAGE_NUMPY_ZDIM].astype("uint8"))
        else:
            self.pilImage = Image.fromarray(self.numpyImage[:, :, 0:config.GRAPHICS_IMAGE_NUMPY_ZDIM].astype("uint8")).resize(
                (int(self.numpyImage.shape[1] * self.pilImageScaleX),
                 int(self.numpyImage.shape[0] * self.pilImageScaleY)),
                config.PIL_DEFAULT_RESIZE_RESAMPLE_MODE)


    def getSavePath(self,
                    fileIndex,
                    digits=config.GRAPHICS_DEFAULT_SAVE_NAME_DIGITS,
                    suffix=config.GRAPHICS_DEFAULT_SAVE_NAME_SUFFIX,
                    format=config.GRAPHICS_DEFAULT_SAVE_FORMAT):
        return config.GRAPHICS_OUTPUT_DIRECTORY + str(fileIndex).zfill(digits) + suffix + format

    def getFramePath(self,
                     fileIndex,
                     digits=config.GRAPHICS_DEFAULT_FRAME_NAME_DIGITS,
                     suffix=config.GRAPHICS_DEFAULT_FRAME_NAME_SUFFIX,
                     format=config.GRAPHICS_DEFAULT_FRAME_FORMAT):
        return config.GRAPHICS_OUTPUT_DIRECTORY + config.GRAPHICS_FRAMES_FOLDER + str(fileIndex).zfill(digits) + suffix + format

    def saveImage(self, path):
        Image.fromarray(self.numpyImage[:,:,0:config.GRAPHICS_IMAGE_NUMPY_ZDIM].astype("uint8")).save(path)

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
        return imageData

    @staticmethod
    @jit(nopython=True)
    def manipulateImageNumba2(imageData):
        dims = imageData.shape
        for y in range(dims[0]):
            for x in range(dims[1]):
                imageData[y, x] += numpy.uint8(y + x)

                tempInt1 = (y + x) % 256
                if tempInt1 == 0:
                    tempInt1 += 1
                imageData[y, x] -= (numpy.uint8(y * x) % numpy.uint8(tempInt1))

        return imageData

    def drawPlayer(self):
        self.numpyImage[self.wrapper.pEngines[-1].playerY,
                        self.wrapper.pEngines[-1].playerX] = [0, 255, 255]