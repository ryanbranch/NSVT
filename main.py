# TODO:
#   A. PLACEHOLDER
#   B. OpenGL-Related
#     0. Useful Reading
#       a. "Modern OpenGL Introduction" (written for C++, but may be useful as a reference)
#           https://en.wikibooks.org/wiki/OpenGL_Programming/Modern_OpenGL_Introduction
#     1. Implement Vertex Buffers (as an alternative to the glBegin() and glEnd() calls)
#       a. IMPORTANT reading for implementation/troubleshooting:
#          https://stackoverflow.com/questions/13179565/how-to-get-vbos-to-work-with-python-and-pyopengl


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
from OpenGL.GL import *
from OpenGL.GLU import *

# Local Imports
import user_input_handler
import graphics_engine
import nsvt_config as config

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

# Abstraction of any 3-dimensional shape via its vertices and their connections
# INVARIANTS:
#   A. vertices_ must be a list of X,Y,Z coordinates. It will be converted to a 2D NumPy array
#   B. edges_ must be a list of vertex pairs. It will be converted to a 2D NumPy array
class Shape3D():
    def __init__(self, vertices_, edges_, triangles_=None):
        self.vertices = numpy.asarray(vertices_, dtype=config.SHAPE3D_VERTICES_NUMPY_DTYPE)
        self.edges = numpy.asarray(edges_, dtype=config.SHAPE3D_EDGES_NUMPY_DTYPE)

        # If a shape has triangles (As opposed to being only comprised of edges, with no surfaces)
        if triangles_:
            self.triangles = numpy.asarray(triangles_, dtype=config.SHAPE3D_TRIANGLES_NUMPY_DTYPE)


class OpenGLApp():
    def __init__(self, wrapper_):
        # Initialization method for PyGame library
        pygame.init()

        # MEMBER VARIABLE DEFINITIONS
        # References to external objects
        self.wrapper = wrapper_

        # PyGame Parameters
        self.display_width = 1000
        self.display_height = 1000
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height),  pygame.OPENGL | pygame.DOUBLEBUF | pygame.HWSURFACE)
        pygame.display.set_caption('OpenGL App Test')

        # App Control
        self.frameTime = default_timer()
        self.clock = pygame.time.Clock()
        self.crashed = False
        self.pgSurface = pygame.pixelcopy.make_surface(self.wrapper.gEngines[-1].numpyImage)

        self.verticesTemp = (
            (0, 0, 0),  # A
            (1, 0, 0),  # B
            (0, 1, 0),  # C
            (0, 0, 1),  # D
            (1, 1, 0),  # E
            (1, 0, 1),  # F
            (0, 1, 1),  # G
            (1, 1, 1)   # H
        )

        self.vertexColorsTemp = (
            (0, 0, 0),  # A (Black)
            (1, 0, 0),  # B (Red)
            (0, 1, 0),  # C (Green)
            (0, 0, 1),  # D (Blue)
            (1, 1, 0),  # E (Yellow)
            (1, 0, 1),  # F (Magenta)
            (0, 1, 1),  # G (Cyan)
            (1, 1, 1)   # H (White)
        )

        self.edgesTemp = (
            (0, 1),  # A to B
            (0, 2),  # A to C
            (0, 3),  # A to D
            (1, 4),  # B to E
            (1, 5),  # B to F
            (2, 4),  # C to E
            (2, 6),  # C to G
            (3, 5),  # D to F
            (3, 6),  # D to G
            (4, 7),  # E to H
            (5, 7),  # F to H
            (6, 7)   # G to H
        )

        self.trianglesTemp = (
            (0, 1, 4),  # A, B, E
            (0, 1, 5),  # A, B, F
            (0, 2, 4),  # A, C, E
            (0, 2, 6),  # A, C, G
            (0, 3, 5),  # A, D, F
            (0, 3, 6),  # A, D, G
            (1, 4, 7),  # B, E, H
            (1, 5, 7),  # B, F, H
            (2, 4, 7),  # C, E, H
            (2, 6, 7),  # C, G, H
            (3, 5, 7),  # D, F, H
            (3, 6, 7)   # D, G, H
        )

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        gluPerspective(25, (self.display_width / self.display_height), 0.1, 50.0)
        glTranslatef(-0.5, -0.5, -5.0)
        glRotatef(20, 0, 0, 0)

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
            self.drawGraphicsOpenGL()

        pygame.quit()
        print(fpsVals)
        quit()

    def Cube(self):
        # Drawing Edges
        glBegin(GL_LINES)
        for edge in self.edgesTemp:
            for vertex in edge:
                glVertex3fv(self.verticesTemp[vertex])
        glEnd()

        # Drawing Triangles
        glBegin(GL_TRIANGLES)
        for triangle in self.trianglesTemp:
            for vertex in triangle:
                #glColor3fv((random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)))
                glColor3fv(self.vertexColorsTemp[vertex])
                glVertex3fv(self.verticesTemp[vertex])
        glEnd()

    def drawGraphicsOpenGL(self):
        # REFRESH AND DISPLAY:
        glRotatef(3, 1, 1, 1)  # 3-degree rotation around the unit vector
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.Cube()
        # Update the display
        pygame.display.flip()


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
            self.advance()
        # REFERENCE: Fill the display with white (UNUSED)
        #self.gameDisplay.fill(self.white)
        # REFERENCE: Wait for 60 milliseconds (UNUSED)
        #self.clock.tick(60)

        pygame.quit()
        print(fpsVals)
        quit()


    def advance(self):
        # Updates the graphics
        self.drawGraphicsPyGame()
        # Computes the upcoming frame
        self.computeNextFramePyGame()

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
        #self.pygameapp = PyGameApp(self)


        # Create and run the OpenGL GUI instance
        self.openglapp = OpenGLApp(self)

def main():
    wr = Wrapper()



main()