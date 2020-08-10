# TODO:
#   A. Placeholder


class TkinterGuiUserInput():

    def __init__(self, wrapper_, app_):

        self.wrapper = wrapper_
        self.app = app_

    # Mouse Left Click - Advances the state
    def handleMouseClick(self, event=None):
        if event:
            print(event.x, event.y)
        self.wrapper.gEngines[-1].randomizeRandomPixel()
        self.app.advance()

    # Keyboard "ENTER" Press - Begins the animation process
    def handleKeyEnter(self, event=None):
        if event:
            print(event)
        if not self.app.animating:
            self.app.startAnimating()

    # Keyboard "SPACE" Press - Pauses the animation process
    def handleKeySpace(self, event=None):
        if event:
            print(event)
        self.app.stopAnimating()

    # Keyboard "C" Press - Clears/Resets the image
    def handleKeyC(self, event=None):
        if event:
            print(event)
        if self.app.animating:
            self.app.stopAnimating()
        self.wrapper.gEngines[-1].numpyImage = self.wrapper.gEngines[-1].clearImageNumba(
            self.wrapper.gEngines[-1].numpyImage)
        self.app.advance()

    # Keyboard "D" Press - Advances the state
    def handleKeyD(self, event=None):
        if event:
            print(event)
        if self.app.animating:
            self.app.stopAnimating()
        self.app.advance()
