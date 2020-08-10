# TODO:
#   A. Placeholder

# Library Imports
import tkinter
from timeit import default_timer
from PIL import ImageTk

# Local Imports
import tkinter_gui_user_input
import nsvt_config as config

class TkinterGuiApp(tkinter.Tk):

    def __init__(self, wrapper_, gIndex_=0):
        # BASE CLASS CONSTRUCTOR
        tkinter.Tk.__init__(self)

        # MEMBER VARIABLE DEFINITIONS
        # Graphics Engine Index
        self.gIndex = gIndex_
        # References to external objects
        self.wrapper = wrapper_

        # TkinterGuiUserInput instance
        self.userInput = tkinter_gui_user_input.TkinterGuiUserInput(self.wrapper, self)
        # App Parameters
        self.msPerFrame = int(round(1000 / config.DEFAULT_GUI_FRAMERATE))
        self.animating = False
        self.frameTime = default_timer()
        self.timeDelta = default_timer() - self.frameTime
        self.currentFPS = config.DEFAULT_GUI_FRAMERATE
        self.nextFrameComputed = False

        # WINDOW PROPERTY DEFINITIONS
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # USER INPUT EVENT CONTROL
        self.bind("<Button-1>", self.userInput.handleMouseClick)
        self.bind("<Return>", self.userInput.handleKeyEnter)
        self.bind("<space>", self.userInput.handleKeySpace)
        self.bind("c", self.userInput.handleKeyC)
        self.bind("d", self.userInput.handleKeyD)

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
        self.wrapper.gEngines[self.gIndex].refreshPilImage()
        # Define self.graphicsTkImage based on the refreshed PIL Image
        self.graphicsTkImage = ImageTk.PhotoImage(self.wrapper.gEngines[self.gIndex].pilImage)
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
        self.wrapper.gEngines[self.gIndex].refreshPilImage()
        # Update self.graphicsTkImage to match the new PIL image
        self.graphicsTkImage = ImageTk.PhotoImage(self.wrapper.gEngines[self.gIndex].pilImage)
        # Update the image label to refer to the new self.graphicsTkImage value
        self.graphicsTkImageLabel = tkinter.Label(self.graphicsTkFrame, image=self.graphicsTkImage)
        # Assign the image label a grid location within its frame
        self.graphicsTkImageLabel.grid(row=0, column=0, sticky="nsew", ipadx=0, ipady=0)

        self.fpsTkTextLabel = tkinter.Label(self.graphicsTkFrame, text=("FPS: " + str(self.currentFPS)))
        self.fpsTkTextLabel.grid(row=0, column=0, sticky="nw", ipadx=0, ipady=0)

    def computeNextFrame(self):
        # Compute a new frame to prepare for future display
        self.wrapper.gEngines[self.gIndex].numpyImage = self.wrapper.gEngines[self.gIndex].manipulateImageNumba(self.wrapper.gEngines[self.gIndex].numpyImage)
        self.wrapper.gEngines[self.gIndex].drawPlayer()
        self.nextFrameComputed = True
