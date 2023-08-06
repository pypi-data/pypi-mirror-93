__all__ = ["apps"]

from aleat3 import (applications.diceInterface,
                    applications.rouletteWinners,
                    applications.coinWinners)

class Transfer:
    def __init__(self):
        self.diceInterface = applications.diceInterface
        self.rouletteWinners = applications.rouletteWinners
        self.coinWinners = applications.coinWinners

apps = Transfer()
