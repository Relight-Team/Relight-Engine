import os
import platform
import sys
import subprocess
import inspect
import importlib

from Internal import CompileEnvironment as CE
from Internal import ConfigManager as ConfigM
from Internal import Logger


from Configuration import Directory_Manager

from BaseSDK import PlatformFactory

EngineDir = Directory_Manager.Engine_Directory

ConfigDir = os.path.join(EngineDir, "Config")

_HostOS = platform.system()

# For scanning CustomSDK directory
sys.path.append(os.path.join(EngineDir, "Extras", "CustomSDK"))


# A class that stores information on the platform
class PlatformInfo:

    def __init__(self):
        self.Platform = ConfigM.ReadConfig(ConfigDir + "/BaseBuilder.cfg", "PlatformInformation", "PlatformName")

        self.Arch = ConfigM.ReadConfig(ConfigDir + "/BaseBuilder.cfg", "PlatformInformation", "PlatformArch")

    # Set Platform and Arch
    # <InPlatform> The platform to override, leave None to not override
    # <InArch> The arch to override, leave None to not override
    def OverrideWithCMD(self, InPlatform=None, InArch=None):
        if InPlatform is not None:
            self.Platform = InPlatform

        if InArch is not None:
            self.Arch = InArch

    # Import the FactorySDK file
    # <Return> the imported module of the Factory SDK file
    def ImportFactory(self):

        Logger.Logger(0, "Running ImportFactory() from PlatformInfo")

        # Check if PlatformFactory is in RelightBuildTool project
        if os.path.isfile(os.path.join(EngineDir, "Programs", "RelightBuildTool", "SDK", self.Platform, self.Platform + "PlatformFactory.py",)):

            Logger.Logger(1, "Platform Factory found in base SDK directory: " + EngineDir + "/Programs/RelightBuildTool/SDK/" + self.Platform + "/" + self.Platform + "PlatformFactory.py")
            return importlib.import_module("SDK." + self.Platform + "." + self.Platform + "PlatformFactory")


        # Check if PlatformFactory is in CustomSDK
        elif os.path.isfile(os.path.join(EngineDir, "Extras", "CustomSDK", self.Platform, self.Platform + "PlatformFactory.py")):

            Logger.Logger(1, "Platform Factory found in Custom SDK directory: " + EngineDir + "/Extras/CustomSDK/" + self.Platform + "/" + self.Platform + "PlatformFactory.py")
            return importlib.import_module(self.Platform + "." + self.Platform + "PlatformFactory")

        # If we can't find it, then return fatal error
        else:
            Logger.Logger(5, "Couldn't find " + self.Platform + "/" + self.Platform + "PlatformFactory.py in either RelightBuildTool's SDK directory or CustomSDK directory")

    # Return true if the config file's platform value is valid
    # <InPlatform> The platform to check
    # <Return> true if platform matches
    def IsValid(self, InPlatform):

        if self.Platform == InPlatform:
            return True

        return False


class Platform:

    BuildPlatform = {}

    PlatformGroup = {}

    Plat = ""

    DefaultCPPPlatform = ""

    def __init__(self, InPlatform, InCppPlatform):
        self.Plat = InPlatform
        self.DefaultCPPPlatform = InCppPlatform

    # Create PlatformFactory instance and run the class's "RegBuildPlatform" function
    # <>
    @staticmethod
    def RegPlatform(Args, IncNonInstalledPlats):

        Logger.Logger(0, "Running RegPlatform(" + str(IncNonInstalledPlats) + ")")

        PlatInfo = PlatformInfo()

        PlatInfo.OverrideWithCMD(Args.GetAndParse("Platform"), None)

        Module = PlatInfo.ImportFactory()

        Types = []

        # Store each Factory class from the FactorySDK file into types
        for Name, Object in inspect.getmembers(Module):

            if inspect.isclass(Object):
                Types.append(Object)


        # For each instance, run the RegBuildPlatform
        for T in Types:
            if issubclass(T, PlatformFactory.FactorySDK):
                TempInit = T()

                if IncNonInstalledPlats is True or PlatInfo.IsValid(TempInit.TargetPlatform()) is True:
                    Logger.Logger(1, "Registering " + TempInit.TargetPlatform() + " to Types")
                    TempInit.RegBuildPlatform()

    # Return's true if we have the required SDK installed on this device
    def HasRequiredSDK(self):
        pass  # Will be overwritten with child class

    # Return's all platforms that are registered
    # <Return> List of registered platforms
    @staticmethod
    def GetRegPlatforms(self):
        Logger.Logger(0, "Running GetRegPlatforms()")
        List = []

        for Key in self.ReturnGroupDict():
            List.append(Key)

        return List

    # Return's the default architecture
    # <ProjectFile> The project file, can be used for platform-specific settings
    # <Return> The default architecture to use as a string
    def GetDefaultArch(ProjectFile):
        return ""

    # Stuff to execute after the build process has been done but before we sync the target platform (which is when we prepare and transfer build artifacts to the target platform)
    def PostBuildBeforeSync(Target):
        pass  # Will be overwritten with child class

    # Return the bundle directory for the Link Environment
    def GetBundleDir(Target, FileOutputs):
        return None

    # Set Input to BuildPlatform instance
    # <InBuildPlatform> The platform to register
    @staticmethod
    def RegBuildPlatform(InBuildPlatform):
        Logger.Logger(1,"Adding platform " + str(InBuildPlatform.Plat) + " to BuildPlatform array")
        Platform.BuildPlatform[InBuildPlatform.Plat] = InBuildPlatform

    # Set PlatformGroup to the input group key with the value of input build platform
    # <InBuildPlatform> The platform to use
    # <InBuildPlatformGroup> The platform group to use
    @staticmethod
    def RegBuildPlatformGroup(InBuildPlatform, InBuildPlatformGroup):

        # Add platform group if it doesn't exist
        if InBuildPlatformGroup not in Platform.PlatformGroup:
            Platform.PlatformGroup[InBuildPlatformGroup] = []

        # Add platform to platform group
        Platform.PlatformGroup[InBuildPlatformGroup].append(InBuildPlatform)


    # Return's the BuildPlatform value if it exist, return's None if we allow failure, otherwise it will raise an error
    # <InPlatform> The platform to get
    # <AllowFailure> True if it's okay if the platform doesn't exist
    # <Return> The BuildPlatform value, None if it doesn't exist and we allow failure
    @staticmethod
    def GetBuildPlatform(InPlatform, AllowFailure=False):
        if InPlatform in Platform.BuildPlatform:
            return Platform.BuildPlatform[InPlatform]

        elif AllowFailure is True:
            return None

        else:
            Logger.Logger(5, "BuildPlatform does not has key '" + str(InPlatform) + "' when running GetBuildPlatform")

    # modify each moudle in the target
    def ActivePlatformModuleRulesToModify(ModName, Target, Module):
        pass  # Will be overwritten with child class

    # return's the Delimiter based on the platform
    # <Return> character ';' if windows, otherwise use ':'
    @staticmethod
    def GetPathDelimiter():
        if _HostOS == "Windows":
            return ";"
        else:
            return ":"

    # Return's the platform name
    # <Return> class name
    def GetPlatformName(self):
        return self.__class__.__name__

    # Return's if this platform supports XGE (Incredibuild or equivalent)
    # <Return> true if we can use XGE
    def CanUseXGE(self):
        return True

    # Return's if this platform supports multiple execution at once
    # <Return> true if we can use multiple execution at once
    def CanParallelExecute(self):
        return self.CanUseXGE()

    # If the platform support distributed compilation (Distcc, DMUCS, etc)
    # <Return> true if we can use Distcc
    def CanUseDistcc(self):
        return False

    # If this platform support's SN-DBS (SN System's Distributed Build Server)
    # <Return> true if we can use SN-DBS
    def CanUseSNDBS(self):
        return False

    # Set the new target to platform-specific defaults
    # <Target> The target file
    def ResetTarget(Target):
        pass  # Will be overwritten with child class

    # Validate the Target File
    # <Target> The target file
    def MakeTargetValid(Target):
        pass  # Will be overwritten with child class

    # Return's the platform binary extension based on the bin type
    # <InBinType> The binary type can be "EXE", "Dynamic", or "Static"
    # <Return> What binary extension to use
    def GetBinExtension(InBinType):
        return None

    # Return's the extension for debug info based on bin type
    # <Target> The target file
    # <InBinType> The binary type
    # <Return> what debug binary extension to use
    def GetDebugExtension(Target, InBinType):
        return None

    # Returns if we should override whether to append the arch to bin name
    # <Return> true if we need arch suffix
    def NeedsArchSuffix(self):
        return True

    # Return's the array of binary output files (by default, it will only return 1 item)
    # <BinName> The binary name
    # <ProjectFile> The project file
    # <Target> The target file
    # <Return> list of binary output files
    def FinalizeBinPaths(self, BinName, ProjectFile, Target):
        Tmp = []
        Tmp.append(BinName)
        return Tmp

    # Setup the target environment
    # <Target> The target file
    # <CompileEnv> The Compile Environment
    # <LinkEnv> The Link Environment
    def SetUpEnvironment(Target, CompileEnv, LinkEnv):
        pass  # Will be overwritten with child class

    # Setup the config enviornment
    # <Target> The target file
    # <BuildType> The build type
    # <CompileEnv> The compile environment
    # <LinkEnv> The link environment
    def SetUpConfigEnv(self, Target, BuildType, CompileEnv, LinkEnv):
        # This if statement is for 3rd party only, as some of them require this define to access debug features
        if CompileEnv.UseDebugCRT is True:
            CompileEnv.Defines.append("_DEBUG=1")
        else:
            CompileEnv.Defines.append("NDEBUG=1")

        # Set Define based on why type of build it is
        if BuildType == "Debug":
            CompileEnv.Defines.append("RE_BUILDTYPE_DEBUG=1")

        elif BuildType == "Development":
            CompileEnv.Defines.append("RE_BUILDTYPE_DEVELOPMENT=1")

        elif BuildType == "Final":
            CompileEnv.Defines.append("RE_BUILDTYPE_FINAL=1")

        # Set Debug info to true if we are using debug

        if not Target.DisableDebugInfo and self.ShouldCreateDebugInfo(BuildType):
            CompileEnv.AddDebugInfo = True

        LinkEnv.AddDebugInfo = CompileEnv.AddDebugInfo

    # If we should Create debug information if the config file is not set
    # <BuildType> The buildtype
    # <Return> true if we should create debug info
    def ShouldCreateDebugInfo(self, BuildType):
        pass  # Will be overwritten with child class

    # Create the platform's toolchain instance
    # <Target> the target file
    def CreateToolChain(Target):
        pass  # Will be overwritten with child class

    # Deploy the target
    def Deploy(Receipt):
        pass  # Will be overwritten with child class
