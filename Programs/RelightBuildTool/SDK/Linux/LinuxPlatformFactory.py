import os
import sys

from . import LinuxPlatform
from . import LinuxPlatformSDK

from BaseSDK import PlatformFactory
from BaseSDK import Platform


class LinuxFactory(PlatformFactory.FactorySDK):

    # Return's the target platform for this factory
    def TargetPlatform(self):
        return "Linux"

    # Register the Build Platform w/ Platform Class
    def RegBuildPlatform(self):

        SDK = LinuxPlatformSDK.LinuxPlatformSDK()

        SDK.ManageAndValidate()

        Plat = LinuxPlatform.LinuxPlatform(SDK)

        Platform.Platform.RegBuildPlatform(Plat)

        Platform.Platform.RegBuildPlatformGroup("Linux", "Unix")

        # TODO: FINISH ONCE GENERATE PROJECT FILES IS FINISHED
