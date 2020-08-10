# TODO:
#   A. Placeholder

# Library Imports
import random
from timeit import default_timer
import pygame
import numpy
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo

# Local Imports
import nsvt_geometry as geo


class PyopenglApp():
    def __init__(self, wrapper_):
        # MEMBER VARIABLE DEFINITIONS
        # References to external objects
        self.wrapper = wrapper_

        # Initialization method for PyGame library
        pygame.init()
        # PyGame Parameters
        self.display_width = self.wrapper.appInfo.width
        self.display_height = self.wrapper.appInfo.height
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height),
                                                   pygame.OPENGL | pygame.DOUBLEBUF | pygame.HWSURFACE)
        pygame.display.set_caption('OpenGL App Test')

        # Shapes
        self.shapes = []
        for i in range(100):
            shapeX = random.randrange(5, 16) / 200
            shapeY = random.randrange(5, 16) / 200
            shapeZ = random.randrange(5, 16) / 200
            moveX = random.randrange(-50, 50) / 10
            moveY = random.randrange(-50, 50) / 10
            moveZ = random.randrange(-50, 50) / 10
            rotateX = random.randrange(-90, 91)
            rotateY = random.randrange(-90, 91)
            rotateZ = random.randrange(-90, 91)
            self.shapes.append(self.wrapper.shapeGen.generateCuboid(shapeX, shapeY, shapeZ))
            geo.translateVertices(self.shapes[-1].vertices, moveX, moveY, moveZ)
            # self.shapes[-1].vertices = geo.rotateVertices(self.shapes[-1].vertices, rotateX, rotateY, rotateZ)
            geo.rotateVertices(self.shapes[-1].vertices, rotateX, rotateY, rotateZ)
            geo.updateTriangleVertices(self.shapes[-1].vertices, self.shapes[-1].triangles,
                                       self.shapes[-1].triangleVertices)


        # PyOpenGL
        # SETUP OPERATIONS
        glViewport(0, 0, self.display_width, self.display_height)
        glClearColor(0.0, 0.5, 0.5, 1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glPointSize(5)

        # Set camera perspective
        gluPerspective(25, (self.display_width / self.display_height), 0.1, 50.0)

        # Translate and rotate to initial position
        glTranslatef(-0.5, -0.5, -10.0)
        # glRotatef(20, 0, 0, 0)

        # SHADER OPERATIONS
        # (placeholder)

        # VBO OPERATIONS
        self.allVertices = numpy.concatenate([shape.vertices for shape in self.shapes], 0)
        self.allTriangleVertices = numpy.concatenate([shape.triangleVertices for shape in self.shapes], 0)
        self.vbo = vbo.VBO(self.allVertices)
        self.vbo2 = vbo.VBO(self.allTriangleVertices)

        # App Control
        self.frameTime = default_timer()
        self.clock = pygame.time.Clock()
        self.crashed = False
        fpsVals = []

        # APPLICATION LOOP
        while not self.crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        glTranslatef(0, 0, 1)
                    if event.key == pygame.K_q:
                        glTranslatef(0, 0, -1)
                    if event.key == pygame.K_s:
                        glTranslatef(0, 1, 0)
                    if event.key == pygame.K_w:
                        glTranslatef(0, -1, 0)
                    if event.key == pygame.K_a:
                        glTranslatef(1, 0, 0)
                    if event.key == pygame.K_d:
                        glTranslatef(-1, 0, 0)

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

    def drawGraphicsOpenGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the current display

        # glRotatef(0.3, 1, 1, 1)  # 3-degree rotation around the unit vector


        # VBO OPERATIONS
        self.allVertices = numpy.concatenate([shape.vertices for shape in self.shapes], 0)
        self.allTriangleVertices = numpy.concatenate([shape.triangleVertices for shape in self.shapes], 0)
        self.vbo = vbo.VBO(self.allVertices)
        self.vbo2 = vbo.VBO(self.allTriangleVertices)

        for shape in self.shapes:
            randomAxis = (random.randrange(-100, 100), random.randrange(-100, 100), random.randrange(-100, 100))
            randomAngle = random.randrange(-90, 91) / 10
            geo.rotateVerticesAxisAngle(shape.vertices, randomAxis[0], randomAxis[1], randomAxis[2], randomAngle)
            geo.updateTriangleVertices(shape.vertices, shape.triangles, shape.triangleVertices)

        tempCounter = 0

        try:
            # VERTICES
            self.vbo.bind()
            try:
                glEnableClientState(GL_VERTEX_ARRAY);
                glVertexPointer(3, GL_FLOAT, 0, self.vbo)
                glDrawArrays(GL_POINTS, 0, len(self.allVertices))
            finally:
                self.vbo.unbind()
                glDisableClientState(GL_VERTEX_ARRAY);

            # TRIANGLES
            self.vbo2.bind()
            try:
                glEnableClientState(GL_VERTEX_ARRAY);
                glVertexPointer(3, GL_FLOAT, 0, self.vbo2)
                glDrawArrays(GL_TRIANGLES, 0, len(self.allTriangleVertices) * 3)
            finally:
                self.vbo2.unbind()
                glDisableClientState(GL_VERTEX_ARRAY);
        finally:
            # Shader stuff will go here
            # print("PLACEHOLDER 1")
            tempCounter += 1

        pygame.display.flip()
