# ExamplePlatform handles the configs and definitions of a platform, many of which may require SDK class in order to run

# Examples include: can use parallel executors, binary extensions for this platform, and creating the toolcahin

from BaseSDK import Platform
from Internal import CompileEnvironment as CE

class ExamplePlatform(Platform.Platform):

    # Init class, usually used for setting SDK but can also be used to set up other values
    # <InSDK> - Platform SDK to use
    def __init__(self, InSDK):
        pass

    # Return's true if we have the required SDK installed on this device
    # <Returns> - True if we have the required SDK
    def HasRequiredSDK(self):
        return False

    # If this platform can use XGE
    # XGE is mainly used by Incredibuild, a proprietary grid computing system
    # <Returns> - True if SDK supports Incredibuild
    def CanUseXGE(self):
        return False

    # If the platform support distributed compilation (Distcc, DMUCS, etc)
    # <Returns> - True if we can use Distcc
    def CanUseDistcc(self):
        return False

    # If this platform support's SN-DBS (SN System's Distributed Build Server)
    # <Returns> - True if we can use SN-DBS
    def CanUseSNDBS(self):
        return False

    # Set the new target to platform-specific defaults
    # <Target> - The target to reset
    def ResetTarget(Target):
        pass

    # Validate the Target File
    # <Target> - The Target file to make valid
    def MakeTargetValid(Target):
        pass

    # Get's the file extension based on Bin Type
    # <InBinType> The bin type string, can be EXE, Dynamic, or Static
    # <Returns> - File extension (.bin), or None if it's not correct
    def GetBinExtension(self, InBinType):
        return None

    # Get all file extensions for debug files depending on BinType
    # <Target> - The target to use
    # <InBinType> - The bin type string, can be EXE, Dynamic, or Static
    # <Returns> - An array of all debug extensiosn
    def GetDebugExtensions(Target, InBinType):
        return []

    # If we should add Arch to bin name
    # <Returns> - True if we should append Arch to bin name
    def NeedsArchSuffix(self):
        return True

    # Any modules we need to add because of the platform, should only use this instead of in target/module if module is proprietary
    # <Target> - The target to use
    # <ModuleNames> - List of modules to include
    def AddExtraModules(Target, ModuleNames):
        pass

    # Set's up platform-specific settings for Compile and Link Environment
    # <Target> - The target reader, used for reading settings
    # <CompileEnv> - The Compile Environment to change settings
    # <LinkEnv> - The Link Environment to change settings
    def SetUpEnvironment(self, Target, CompileEnv, LinkEnv):
        pass

    # returns metadata that is not tracked
    # <ProjectFile> - The project file to check for external metadata
    def GetExternalBuildMetadata(ProjectFile):
        pass

    # If we should Create debug information based on BuildType
    # <BuildType> - The bin type string, can be EXE, Dynamic, or Static
    # <Returns> - True if we should create debug info
    def ShouldCreateDebugInfo(self, BuildType):
        return False

    # Create the platform's toolchain instance
    # <InCppPlatform> the CPP Platform
    # <Target> - The Target Reader file
    # <Returns> the Platform's Toolchain class
    def CreateToolChain(InCppPlatform, Target):
        return "TOOLCHAIN CLASS"
