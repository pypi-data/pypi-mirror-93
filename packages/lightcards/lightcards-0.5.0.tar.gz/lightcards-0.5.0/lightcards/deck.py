# Classes pertaining to the card deck
# Armaan Bhojwani 2021

class Card(list):
    """Card extends the list class, and adds ability to star them."""
    def __init__(self, inp):
        super().__init__(inp)
        self.starred = False

    def unStar(self):
        self.starred = False

    def star(self):
        self.starred = True

    def toggleStar(self):
        if self.starred:
            self.starred = False
        else:
            self.starred = True

    def getStar(self):
        return self.starred

    def printStar(self):
        if self.starred:
            return "★ Starred ★"
        else:
            return "Not starred"


class Status():
    """The status class keeps track of where in the deck the user is"""
    def __init__(self):
        self.index = 0
        self.side = 0

    def forward(self, stack):
        if not self.index == len(stack):
            self.index += 1

    def back(self):
        if not self.index < 1:
            self.index -= 1

    def flip(self):
        if self.side == 0:
            self.side = 1
        else:
            self.side = 0

    def setSide(self, inp):
        self.side = inp

    def setIdx(self, inp):
        self.index = inp

    def getSide(self):
        return self.side

    def getIdx(self):
        return self.index
