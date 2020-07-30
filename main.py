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
DEFAULT_IMAGE_WIDTH = 500
DEFAULT_IMAGE_HEIGHT = 500
# NUMPY IMAGE (META)METADATA
DEFAULT_NUMPY_DATATYPE = numpy.float32
# PIL METADATA
DEFAULT_PIL_RESIZE_RESAMPLE_MODE = PIL.Image.NEAREST

NUM_COLOR_CHANNELS = 3
NUM_EXTRA_CHANNELS = 5

APP_WIDTH = 1024
APP_HEIGHT = 768
FRAME_WIDTH = 500
FRAME_HEIGHT = 500

DEFAULT_FRAMERATE = 30

class GraphicsEngine():

    def __init__(self):

        self.saveCount = 0

        self.numpyImage = numpy.ones(shape=(DEFAULT_IMAGE_HEIGHT,
                                           DEFAULT_IMAGE_WIDTH,
                                           (NUM_COLOR_CHANNELS + NUM_EXTRA_CHANNELS)),
                                     dtype=DEFAULT_NUMPY_DATATYPE) * 32
        self.pilImage = Image.fromarray(self.numpyImage[:, :, 0:NUM_COLOR_CHANNELS].astype("uint8"))

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
        self.pilImage = Image.fromarray(self.numpyImage[:, :, 0:NUM_COLOR_CHANNELS].astype("uint8"))

    def getSavePath(self, fileIndex, digits=DEFAULT_SAVE_NAME_DIGITS, suffix=DEFAULT_SAVE_NAME_SUFFIX,
                    format=DEFAULT_SAVE_FORMAT):
        return OUTPUT_DIRECTORY + str(fileIndex).zfill(digits) + suffix + format

    def getFramePath(self, fileIndex, digits=DEFAULT_FRAME_NAME_DIGITS, suffix=DEFAULT_FRAME_NAME_SUFFIX,
                     format=DEFAULT_FRAME_FORMAT):
        return OUTPUT_DIRECTORY + FRAMES_FOLDER + str(fileIndex).zfill(digits) + suffix + format

    def saveImage(self, path):
        Image.fromarray(self.numpyImage[:,:,0:NUM_COLOR_CHANNELS].astype("uint8")).save(path)

    def manipulateImage(self):
        print("Placeholder")

    @staticmethod
    @jit(nopython=True)
    def manipulateImageNumba(imageData):
        dims = imageData.shape
        for y in range(dims[0]):
            for x in range(dims[1]):
                imageData[y, x] += (y + x)
        #imageData += 32
        return imageData

# Stores metadata for the app to reference (e.g. target width and height of the window)
class AppInfo():

    def __init__(self, width_, height_):
        self.width = width_
        self.height = height_

class App(tkinter.Tk):

    def __init__(self, wrapper_, info_):
        # BASE CLASS CONSTRUCTOR
        tkinter.Tk.__init__(self)

        # MEMBER VARIABLE DEFINITIONS
        # References to external objects
        self.wrapper = wrapper_
        self.info = info_
        # App Parameters
        self.msPerFrame = int(round(1000 / DEFAULT_FRAMERATE))

        # WINDOW PROPERTY DEFINITIONS
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


        self.defineGraphics()



        self.bind('<Button-1>', self.startAnimating)

    def startAnimating(self, event):
        self.oldTime = default_timer()
        self.animate()

    def animate(self):
        # NOTE: self.after() call of self.animate() should be the FIRST ACTION in this method
        self.after(self.msPerFrame, self.animate)
        # These two lines print the amount of time that has elapsed since the last self.after() call
        print(default_timer() - self.oldTime)
        self.oldTime = default_timer()

        # Updates the graphics
        self.drawGraphics()



    def defineGraphics(self):
        self.wrapper.gEngines[-1].refreshPilImage()
        self.graphicsTkImage = ImageTk.PhotoImage(self.wrapper.gEngines[-1].pilImage)
        self.graphicsTkFrame = tkinter.Frame(self, width=self.info.width, height=self.info.height, bg="red")
        self.graphicsTkImageLabel = tkinter.Label(self.graphicsTkFrame, image=self.graphicsTkImage)
        self.graphicsTkFrame.grid(row=0, column=0, sticky="nsew", ipadx=0, ipady=0)


    def drawGraphics(self):
        # Refresh the values of the PIL Image
        self.wrapper.gEngines[-1].refreshPilImage()
        # Update self.graphicsTkImage to match the new PIL image
        self.graphicsTkImage = ImageTk.PhotoImage(self.wrapper.gEngines[-1].pilImage)
        # Update the image label to refer to the new self.graphicsTkImage value
        self.graphicsTkImageLabel = tkinter.Label(self.graphicsTkFrame, image=self.graphicsTkImage)
        # Display the image label to the grid
        self.graphicsTkImageLabel.grid(row=0, column=0, sticky="nsew", ipadx=0, ipady=0)

        # Compute a new frame to prepare for future display
        self.wrapper.gEngines[-1].numpyImage = self.wrapper.gEngines[-1].manipulateImageNumba(self.wrapper.gEngines[-1].numpyImage)

class Wrapper():

    def __init__(self):

        # MEMBER VARIABLE DECLARATION
        # AppInfo instance
        self.appInfo = AppInfo(APP_WIDTH, APP_HEIGHT)
        # Frame instances
        self.gEngines = []
        self.gEngines.append(GraphicsEngine())

        # SETUP ACTIONS
        # Placeholder

        # POST-SETUP ACTIONS
        # Create and run the Tkinter GUI instance
        self.app = App(self, self.appInfo)
        self.app.mainloop()

def main():
    wr = Wrapper()



main()