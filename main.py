# TODO:
#   A. Placeholder


# Library Imports
import random
import timeit
from timeit import default_timer
import PIL
from PIL import Image, ImageTk
import numpy
import pathlib
from pathlib import Path
import glob
from numba import jit
import tkinter
from tkinter import ttk, CENTER, NW
from functools import partial

# Local Imports
import user_input_handler

# G L O B A L     V A R I A B L E S
# TESTING CONTROLS
DEFAULT_TEST_ITERATIONS = 5
# FILE NAMES AND PATHS
OUTPUT_DIRECTORY = "output/"
DEFAULT_SAVE_NAME_DIGITS = 6
DEFAULT_SAVE_NAME_SUFFIX = ""
DEFAULT_SAVE_FORMAT = ".png"
FRAMES_FOLDER = "frames/"
DEFAULT_FRAME_NAME_DIGITS = 6
DEFAULT_FRAME_NAME_SUFFIX = ""
DEFAULT_FRAME_FORMAT = ".png"
# IMAGE METADATA
DEFAULT_IMAGE_WIDTH = 100
DEFAULT_IMAGE_HEIGHT = 100
# NUMPY IMAGE (META)METADATA
DEFAULT_NUMPY_DATATYPE = numpy.uint8
# PIL METADATA
DEFAULT_PIL_RESIZE_RESAMPLE_MODE = PIL.Image.NEAREST

NUM_COLOR_CHANNELS = 3

APP_WIDTH = 1024
APP_HEIGHT = 768

DEFAULT_FRAMERATE = 20

class PhysicsEngine():

    def __init__(self, wrapper_):
        self.wrapper = wrapper_
        self.playerX = 0
        self.playerY = 0

class GraphicsEngine():

    def __init__(self, wrapper_):

        self.wrapper = wrapper_

        self.saveCount = 0
        self.pilImageScaleX = 10.0
        self.pilImageScaleY = 10.0

        self.numpyImage = numpy.ones(shape=(DEFAULT_IMAGE_HEIGHT, DEFAULT_IMAGE_WIDTH, NUM_COLOR_CHANNELS),
                                     dtype=DEFAULT_NUMPY_DATATYPE
                                     ) * 255
        self.pilImage: Image
        # Sets the value of self.pilImage
        self.refreshPilImage()

        self.makeDirectories()

        self.saveImage(self.getFramePath(self.saveCount))
        self.saveCount += 1




        # Creates the folder(s) in which outputs will be saved
    def makeDirectories(self):
        cwDir = Path.cwd()
        dirs = [cwDir / OUTPUT_DIRECTORY,  # MAIN OUTPUT DIRECTORY
                cwDir / OUTPUT_DIRECTORY / FRAMES_FOLDER]  # FRAMES DIRECTORY
        for newDir in dirs:
            if not newDir.is_dir():
                newDir.mkdir()

    # NOTE: Call this function before any use of self.pilImage,
    #       unless it is clear that self.numpyImage has not been modified since the last refreshPilImage() call.
    def refreshPilImage(self):
        if (self.pilImageScaleX == 1.0 and self.pilImageScaleY == 1.0):
            self.pilImage = Image.fromarray(self.numpyImage[:, :, 0:NUM_COLOR_CHANNELS].astype("uint8"))
        else:
            self.pilImage = Image.fromarray(self.numpyImage[:, :, 0:NUM_COLOR_CHANNELS].astype("uint8")).resize(
                (int(self.numpyImage.shape[1] * self.pilImageScaleX),
                 int(self.numpyImage.shape[0] * self.pilImageScaleY)),
                DEFAULT_PIL_RESIZE_RESAMPLE_MODE)


    def getSavePath(self, fileIndex, digits=DEFAULT_SAVE_NAME_DIGITS, suffix=DEFAULT_SAVE_NAME_SUFFIX,
                    format=DEFAULT_SAVE_FORMAT):
        return OUTPUT_DIRECTORY + str(fileIndex).zfill(digits) + suffix + format

    def getFramePath(self, fileIndex, digits=DEFAULT_FRAME_NAME_DIGITS, suffix=DEFAULT_FRAME_NAME_SUFFIX,
                     format=DEFAULT_FRAME_FORMAT):
        return OUTPUT_DIRECTORY + FRAMES_FOLDER + str(fileIndex).zfill(digits) + suffix + format

    def saveImage(self, path):
        Image.fromarray(self.numpyImage[:,:,0:NUM_COLOR_CHANNELS].astype("uint8")).save(path)

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

# Stores metadata for the app to reference (e.g. target width and height of the window)
class AppInfo():

    def __init__(self, width_, height_):
        self.width = width_
        self.height = height_

class App(tkinter.Tk):

    def __init__(self, wrapper_):
        # BASE CLASS CONSTRUCTOR
        tkinter.Tk.__init__(self)

        # MEMBER VARIABLE DEFINITIONS
        # References to external objects
        self.wrapper = wrapper_
        # UserInputHandler instance
        self.uih = user_input_handler.UserInputHandler(self.wrapper, self)
        # App Parameters
        self.msPerFrame = int(round(1000 / DEFAULT_FRAMERATE))
        self.animating = False
        self.frameTime = default_timer()
        self.timeDelta = default_timer() - self.frameTime
        self.currentFPS = DEFAULT_FRAMERATE
        self.nextFrameComputed = False



        # WINDOW PROPERTY DEFINITIONS
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # USER INPUT EVENT CONTROL
        self.bind("<Button-1>", self.uih.handleMouseClick)
        self.bind("<Return>", self.uih.handleKeyEnter)
        self.bind("<space>", self.uih.handleKeySpace)
        self.bind("c", self.uih.handleKeyC)
        self.bind("d", self.uih.handleKeyD)


        self.defineGraphics()
        self.advance()




    def advance(self):
        # Updates the graphics
        self.drawGraphics()
        # Computes the upcoming frame
        self.computeNextFrame()

    def stopAnimating(self):
        self.animating = False

    def startAnimating(self):
        self.animating = True
        self.frameTime = default_timer()
        self.animate()

    def animate(self):
        while not self.nextFrameComputed:
            self.after(10)
        if self.animating:
            # NOTE: self.after() call of self.animate() should be the FIRST ACTION in this method
            self.after(self.msPerFrame, self.animate)
            # These lines track the amount of time that has elapsed since the last self.after() call
            self.timeDelta = default_timer() - self.frameTime
            self.frameTime = default_timer()
            self.currentFPS = int(round(1 / self.timeDelta))

            # Updates the graphics
            self.drawGraphics()
            # Computes the upcoming frame
            self.computeNextFrame()



    def defineGraphics(self):
        # Refresh the values of the PIL Image
        self.wrapper.gEngines[-1].refreshPilImage()
        # Define self.graphicsTkImage based on the refreshed PIL Image
        self.graphicsTkImage = ImageTk.PhotoImage(self.wrapper.gEngines[-1].pilImage)
        # Define a tkinter Frame in which to place GUI elements
        # WARNING: No width and height are specified for this frame, be careful!
        self.graphicsTkFrame = tkinter.Frame(self, bg="red")
        # Create a tkinter Label within the frame for displaying the image
        self.graphicsTkImageLabel = tkinter.Label(self.graphicsTkFrame, image=self.graphicsTkImage)
        # Assign the Frame a grid location within the GUI window
        self.graphicsTkFrame.grid(row=0, column=0, sticky="nsew", ipadx=0, ipady=0)

        self.fpsTkTextLabel = tkinter.Label(self.graphicsTkFrame, text=("FPS: NULL"))
        self.fpsTkTextLabel.grid(row=0, column=0, sticky="nw", ipadx=0, ipady=0)


    def drawGraphics(self):
        # REFRESH AND DISPLAY:
        # Refresh the values of the PIL Image
        self.wrapper.gEngines[-1].refreshPilImage()
        # Update self.graphicsTkImage to match the new PIL image
        self.graphicsTkImage = ImageTk.PhotoImage(self.wrapper.gEngines[-1].pilImage)
        # Update the image label to refer to the new self.graphicsTkImage value
        self.graphicsTkImageLabel = tkinter.Label(self.graphicsTkFrame, image=self.graphicsTkImage)
        # Assign the image label a grid location within its frame
        self.graphicsTkImageLabel.grid(row=0, column=0, sticky="nsew", ipadx=0, ipady=0)

        self.fpsTkTextLabel = tkinter.Label(self.graphicsTkFrame, text=("FPS: " + str(self.currentFPS)))
        self.fpsTkTextLabel.grid(row=0, column=0, sticky="nw", ipadx=0, ipady=0)

    def computeNextFrame(self):
        # Compute a new frame to prepare for future display
        self.wrapper.gEngines[-1].numpyImage = self.wrapper.gEngines[-1].manipulateImageNumba(self.wrapper.gEngines[-1].numpyImage)
        self.wrapper.gEngines[-1].drawPlayer()
        self.nextFrameComputed = True

class Wrapper():

    def __init__(self):

        # MEMBER VARIABLE DECLARATION
        # AppInfo instance
        self.appInfo = AppInfo(APP_WIDTH, APP_HEIGHT)
        # GraphicsEngine instances
        self.gEngines = []
        self.gEngines.append(GraphicsEngine(self))
        # PhysicsEngine instances
        self.pEngines = []
        self.pEngines.append(PhysicsEngine(self))

        # SETUP ACTIONS
        # Placeholder

        # POST-SETUP ACTIONS
        # Create and run the Tkinter GUI instance
        self.app = App(self)
        self.app.mainloop()

def main():
    wr = Wrapper()



main()