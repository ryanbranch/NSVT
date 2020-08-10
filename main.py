# TODO:
#   A. PLACEHOLDER
#   B. OpenGL-Related
#     0. Useful Reading
#       a. "Modern OpenGL Introduction" (written for C++, but may be useful as a reference)
#           https://en.wikibooks.org/wiki/OpenGL_Programming/Modern_OpenGL_Introduction
#     1. Implement Vertex Buffers (as an alternative to the glBegin() and glEnd() calls)
#       a. IMPORTANT reading for implementation/troubleshooting:
#          https://stackoverflow.com/questions/13179565/how-to-get-vbos-to-work-with-python-and-pyopengl
#       b. This looks like a very helpful StackOverflow answer:
#          https://stackoverflow.com/a/14365737 (How to draw with Vertex Array Objects and glDrawElements in PyOpenGL)


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
import pygame




# Local Imports
import tkinter_gui_app
import pygame_gui_app
import user_input_handler
import graphics_engine
import pyopengl_app
import shape_generator
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



class Wrapper():

    def __init__(self):
        # RANDOM SEEDING
        random.seed(333)

        # MEMBER VARIABLE DECLARATION
        # AppInfo instance
        self.appInfo = AppInfo(APP_WIDTH, APP_HEIGHT)
        # ShapeGenerator instance
        self.shapeGen = shape_generator.ShapeGenerator()
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
        self.app = tkinter_gui_app.TkinterGuiApp(self)
        self.app.mainloop()


        # Create and run the PyGame GUI instance
        #self.pygameapp = pygame_gui_app.PygameGuiApp(self)


        # Create and run the OpenGL GUI instance
        #self.openglapp = pyopengl_app.PyopenglApp(self)

def main():
    wr = Wrapper()



main()