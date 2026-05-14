import importlib
import sys
import os

from . import Common
from . import LinuxPlatform

from BaseSDK import PlatformSDK

from Configuration import Directory_Manager


class LinuxPlatformSDK(PlatformSDK.PlatformSDK):

    SDKVersionRecommended = "Clang"

    TargetPlatformName = "Linux"

    VerboseCompiler = False

    VerboseLinker = False

    # Get the recommended SDK
    # <Return> Recommended SDK as string
    def GetRecommendedSDKVersion(self):
        return self.SDKVersionRecommended

    # <Return> Target name
    def GetTargetName(self):
        return self.TargetPlatformName

    # Get SDK file name
    # <Return> SDK file name as string
    def SDKVersionFileName(self):
        return "LinuxToolchainVersion.txt"

    # If true, then we can use the compiler installed on the system, otherwise we will use a local executable
    # <Return> true if we are on linux
    def CanUseSystemCompiler(self):
        if self._HostOS == "Linux":
            return True
        return False

    # FIXME: Find a way to make this work, and test both internal and external SDK
    def GetTreeSDKRoot(self):
        pass

    # Return's the location of the SDK, will either retrieve it from environment variable "LINUX_ROOT_MULTIARCH", or generate one if it isn't set
    # <Return> Environment variable for LINUX_ROOT_MULTIARCH
    def GetSDKLoc(self):

        Env = os.getenv("LINUX_ROOT_MULTIARCH")

        if Env is None or Env == "":
            Dir = self.GetTreeSDKRoot()

            if Dir is not None and Dir != "":
                NewDir = os.path.join(Dir, self.SDKVersionFileName())

                if os.path.isdir(NewDir):
                    Env = NewDir

        return Env

    # Return's the location of the SDK for an arch
    # <Arch> The arch to use
    # <Return> SDK with specific arch directory
    def GetSDKArchPath(self, Arch):
        Env = self.GetSDKLoc()

        # If Environment is empty, we can get it from LINUX_ROOT
        if Env is None or Env == "":
            return str(os.environ.get("LINUX_ROOT"))

        # Else, we will get the directory from the LINUX_ROOT_MULTIARCH's archtecture path
        else:
            return str(os.path.join(Env, Arch))

    # Return's true if we found the Clang file
    # <BasePath> the base path of the bin
    # <Return> true if Clang file exists
    def IsClangValid(self, BasePath):
        FilePath = os.path.join(BasePath, "bin")

        # TODO: Add Window's support

        FileName = "Clang++"

        File = os.path.join(FilePath, FileName)

        return os.path.exists(File)

    # Check if we have required manual SDK
    # <Return> true if we have manual SDK
    def InternalHasRequiredManualSDK(self):

        LinuxPlat = LinuxPlatform.LinuxPlatform(self)

        BasePath = self.GetSDKArchPath(LinuxPlat.GetDefaultArch(None))  # TODO: Change the "None" in the args to ProjectFile

        if not (BasePath is None or BasePath == ""):

            if self.IsClangValid(BasePath):
                return True

        if self._HostOS == "Linux":

            # If Clang or G++ is valid, then it's true!
            if (Common.WhichClang() is not None and Common.WhichClang() != "") and (Common.WhichGCC() is not None and Common.WhichGCC() != ""):
                return True

        return False
