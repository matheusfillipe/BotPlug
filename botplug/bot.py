from dataclasses import dataclass
from botplug.config import Config

@dataclass
class BotPlug:
    config: Config

class BotInstanceHolder:
    def __init__(self):
        self._instance = None

    def get(self):
        return self._instance

    def set(self, value):
        self._instance = value

    @property
    def config(self):
        if not self.get():
            raise ValueError("No bot instance available")

        return self.get().config


# Store a global instance of the bot to allow easier access to global data
bot = BotInstanceHolder()
