import os

from BaseSDK import Cook

class LinuxCooker(Cook.BaseCooker):

    def Name(self):
        return "Linux"
