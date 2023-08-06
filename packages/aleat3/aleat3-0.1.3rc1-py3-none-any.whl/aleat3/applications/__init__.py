__all__ = ["apps"]

from aleat3 import applications.diceInterface, applications.rouletteWinners

class Transfer:
    def __init__(self):
        self.diceInterface = applications.diceInterface
        self.rouletteWinners = applications.rouletteWinners

apps = Transfer()
