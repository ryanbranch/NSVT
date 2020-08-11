# TODO:
#   A. PLACEHOLDER


# Library Imports
import random

# Local Imports
import tkinter_gui_app
import pygame_gui_app
import pyopengl_app
import graphics_engine
import shape_generator
import point_cloud
import nsvt_config as config


class PhysicsEngine():

    def __init__(self, wrapper_):
        self.wrapper = wrapper_
        self.playerX = 0
        self.playerY = 0


class Wrapper():

    def __init__(self):
        # RANDOM SEEDING
        random.seed(333)

        # MEMBER VARIABLE DECLARATION
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

        # Create a PointCloudGenerator instance
        self.pcGen = point_cloud.PointCloudGenerator(self)


        # POST-SETUP ACTIONS
        if config.RUN_GUI_APP:
            # Create and run the App instance
            if config.APP_TYPE_3D:
                self.app = pyopengl_app.PyopenglApp(self)
            else:
                if config.APP_TYPE_PYGAME:
                    self.app = pygame_gui_app.PygameGuiApp(self)
                else:
                    self.app = tkinter_gui_app.TkinterGuiApp(self)
                    self.app.mainloop()


def main():
    wr = Wrapper()


main()