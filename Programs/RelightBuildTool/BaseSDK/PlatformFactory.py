import os
import platform
import sys
import subprocess

sys.path.append("../")


class FactorySDK:

    # Return's the target platform for this factory
    def TargetPlatform(self):
        return

    # Register the Build Platform w/ Platform Class
    def RegBuildPlatform(self):
        pass  # Will be overwritten with child class
