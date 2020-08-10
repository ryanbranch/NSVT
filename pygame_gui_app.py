# TODO:
#   A. Placeholder

# Library Imports
import pygame
from timeit import default_timer

# Local Imports


class PygameGuiApp():

    def __init__(self, wrapper_, gIndex_=0):
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
        # Graphics Engine Index
        self.gIndex = gIndex_
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

        # Run the Pygame GUI App
        self.runApp()

    def runApp(self):
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
        pygame.surfarray.blit_array(self.pgSurface, self.wrapper.gEngines[self.gIndex].numpyImage)

        # Blit the image to self.gameDisplay
        self.gameDisplay.blit(self.pgSurface, (0, 0))
        # Update the display
        pygame.display.update()


    def computeNextFramePyGame(self):
        # Compute a new frame to prepare for future display
        self.wrapper.gEngines[self.gIndex].numpyImage = self.wrapper.gEngines[self.gIndex].manipulateImageNumba(self.wrapper.gEngines[self.gIndex].numpyImage)
        self.nextFrameComputed = True