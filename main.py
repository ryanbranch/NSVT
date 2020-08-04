# TODO:
#   A. Placeholder


# Library Imports
import random
import timeit
from timeit import default_timer
import PIL
from PIL import Image, ImageTk
import numpy
from numba import jit
import tkinter
from tkinter import ttk, CENTER, NW
from functools import partial
import pygame

# Local Imports
import user_input_handler
import graphics_engine

# G L O B A L     V A R I A B L E S
# TESTING CONTROLS
DEFAULT_TEST_ITERATIONS = 5

# GUI  CONTROLS
APP_WIDTH = 1024
APP_HEIGHT = 768
DEFAULT_FRAMERATE = 20


class PhysicsEngine():

    def __init__(self, wrapper_):
        self.wrapper = wrapper_
        self.playerX = 0
        self.playerY = 0



# Stores metadata for the app to reference (e.g. target width and height of the window)
class AppInfo():

    def __init__(self, width_, height_):
        self.width = width_
        self.height = height_

class PyGameApp():

    def __init__(self, wrapper_):
        # Initialization method for PyGame library
        pygame.init()
        # TODO: Implement the following pygame methods
        #   A. pygame.pixelcopy
        #     1. pygame.pixelcopy.make_surface(<array>) -> <surface>
        #       a. Should be used to create surfaces but not necessarily to update them, see pygame.surfarray
        #     2. pygame.pixelcopy.array_to_surface(<surface>, <array>) -> None
        #   B. pygame.surfarray
        #     1. pygame.surfarray.blit_array(<surface>, <array>) -> None
        #       a. FASTER than converting array to a surface and then blitting


        # MEMBER VARIABLE DEFINITIONS
        # References to external objects
        self.wrapper = wrapper_

        # PyGame Parameters
        self.display_width = 1000
        self.display_height = 1000
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('PyGame App Test')

        # App Control
        self.frameTime = default_timer()
        self.clock = pygame.time.Clock()
        self.crashed = False
        self.pgSurface = pygame.pixelcopy.make_surface(self.wrapper.gEngines[-1].numpyImage)

        fpsVals = []

        while not self.crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True

            # These lines track the amount of time that has elapsed since the last self.after() call
            self.timeDelta = default_timer() - self.frameTime
            self.frameTime = default_timer()
            self.currentFPS = int(round(1 / self.timeDelta))
            fpsVals.append(self.currentFPS)

            # Updates the graphics
            self.drawGraphicsPyGame()
            # Computes the upcoming frame
            self.computeNextFramePyGame()
        # REFERENCE: Fill the display with white (UNUSED)
        #self.gameDisplay.fill(self.white)
        # REFERENCE: Wait for 60 milliseconds (UNUSED)
        #self.clock.tick(60)

        pygame.quit()
        print(fpsVals)
        quit()


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


    def drawGraphicsPyGame(self):
        # REFRESH AND DISPLAY:
        # Update self.pgSurface to match the new Numpy image
        pygame.surfarray.blit_array(self.pgSurface, self.wrapper.gEngines[-1].numpyImage)

        # Blit the image to self.gameDisplay
        self.gameDisplay.blit(self.pgSurface, (0, 0))
        # Update the display
        pygame.display.update()


    def computeNextFramePyGame(self):
        # Compute a new frame to prepare for future display
        self.wrapper.gEngines[-1].numpyImage = self.wrapper.gEngines[-1].manipulateImageNumba(self.wrapper.gEngines[-1].numpyImage)
        self.nextFrameComputed = True

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

        # MEMBER FUNCTION CALLS
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
        # GraphicsEngine list
        self.gEngines = []
        # PhysicsEngine list
        self.pEngines = []

        # SETUP ACTIONS
        # Create a GraphicsEngine instance and a PhysicsEngine instance
        self.gEngines.append(graphics_engine.GraphicsEngine(self))
        self.pEngines.append(PhysicsEngine(self))


        # POST-SETUP ACTIONS
        # Create and run the Tkinter GUI instance
        # NOTE: The two lines below are commented out for the purposes of testing PyGame implementation
        #self.app = App(self)
        #self.app.mainloop()

        # Create and run the PyGame GUI instance
        self.pygameapp = PyGameApp(self)

def main():
    wr = Wrapper()



main()