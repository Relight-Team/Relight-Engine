import os
import sys

from . import LinuxPlatformSDK
from . import LinuxToolchain
from . import Common

from BaseSDK import Platform

from Environments import CompileEnvironment as CE
from Internal import ConfigManager
from Internal import Logger

from Configuration import Directory_Manager


class LinuxPlatform(Platform.Platform):

    Arch = ""

    SDK = LinuxPlatformSDK.LinuxPlatformSDK()

    def __init__(self, InSDK, InCEPlatform=CE.Platform.Linux, InPlatform="Linux"):
        super().__init__(InPlatform, InCEPlatform)
        self.SDK = InSDK

    # Get the Default Arch
    # <ProjectFile> The project file, leave None if doesn't exist
    # <Return> Arch name
    def GetDefaultArch(self, ProjectFile):
        Ret = self.Arch

        if ProjectFile is None:
            EngineIni = None
        else:
            EngineIni = os.path.abspath(ProjectFile)

        # If abspath fails, we shall get it from command line instead
        if EngineIni is None:
            EngineIni = os.path.join(Directory_Manager.Engine_Directory, "Config", "BaseBuilder.cfg")
            pass  # FIXME: Get from command line, else get from BaseBuilder

        TempConfig = ConfigManager.ReadConfig(EngineIni, "PlatformInformation", "PlatformArch")

        # TODO: Shitty hack to ensure compatibility, idk if this even works, if it doesn't FIX IT!
        if "X86-64".lower() in TempConfig:
            Ret = "x86_64-unknown-linux-gnu"

        elif "Arch".lower() in TempConfig and "Aarch64" not in TempConfig:
            Ret = "arm-unknown-linux-gnueabihf"

        elif "Aarch64".lower() in TempConfig:
            Ret = "aarch64-unknown-linux-gnueabi"

        elif "i386".lower() in TempConfig:
            Ret = "i686-unknown-linux-gnu"

        else:
            Logger.Logger(4, "Specified Arch not set, Using default arch")

        return Ret

    # Add defines to target
    # <Target> The target file
    def MakeTargetValid(self, Target):

        if Target.UseAddressSanitizer is True or Target.UseThreadSanitizer is True:
            Target.Defines.append("FORCE_ANSI_ALLOCATOR=1")

    # Reset the target
    # <Target> The target file
    def ResetTarget(self, Target):
        self.MakeTargetValid(Target)

    # Do not add arch to bin name on linux
    def NeedsArchSuffix(self):
        return False

    # Linux doesn't support XGE (or relight engine as a whole but ignore that)
    def CanUseXGE():
        return False

    # We can parallel execute on linux
    def CanParallelExecute():
        return True

    # Return's the platform binary extension based on the bin type
    # <InBinType> The binary type, can be "EXE", "Dynamic", or "Static"
    # <Return> What binary extension to use as a string
    def GetBinExtension(self, InBinType):
        if InBinType == "EXE":
            return ""
        elif InBinType == "Dynamic":
            return ".so"
        elif InBinType == "Static":
            return ".a"
        else:
            return None


    # Return's the extension for debug info based on bin type
    # <Target> The target file
    # <InBinType> The binary type
    # <Return> what debug binary extension to use
    def GetDebugExtension(Target, InBinType):
        Ret = []

        if InBinType == "EXE":
            Ret = [".sym", ".debug"]

            if Target.SavePSYM is True:
                Ret.append(".pysm")

        return Ret

    # Check conflits between Compile Environment and Link Environment
    # <CompileEnv> The compile Environment
    # <LinkEnv> The link environment
    def CheckEnvironmentConflicts(self, CompileEnv, LinkEnv):

        ErrMesg = "CompileEnv and LinkEnv mismatch: "

        if CompileEnv.PGOOptimize != LinkEnv.PGOOptimize:
            Logger.Logger(5, ErrMesg + " PGOOptimize, CompileEnv: " + str(CompileEnv.PGOOptimize) + " LinkEnv: " + str(LinkEnv.PGOOptimize))

        if CompileEnv.PGOProfile != LinkEnv.PGOProfile:
            Logger.Logger(5, ErrMesg + " PGOProfile, CompileEnv: " + str(CompileEnv.PGOProfile) + " LinkEnv: " + str(LinkEnv.PGOProfile))

        if CompileEnv.AllowLTCG != LinkEnv.AllowLTCG:
            Logger.Logger(5, ErrMesg + " AllowLTCG, CompileEnv: " + str(CompileEnv.AllowLTCG) + " LinkEnv: " + str(LinkEnv.AllowLTCG))


    # Set up the environments
    # <Target> The target file
    # <Compile Environment> The compile Environment
    # <Link Environment> The link environment
    def SetUpEnvironment(self, Target, CompileEnv, LinkEnv):

        BasePath = self.SDK.GetSDKArchPath(Target.Arch)

        if self.SDK._HostOS == "Linux" and (BasePath is None or BasePath == ""):
            CompileEnv.SysIncPaths.append("/usr/include")

        if CompileEnv.PGOProfile is True or CompileEnv.PGOOptimize is True:
            CompileEnv.AllowLTCG = True
            LinkEnv.AllowLTCG = True

        self.CheckEnvironmentConflicts(CompileEnv, LinkEnv)

        if Target.LinkType == "Monolithic":
            CompileEnv.HideSymbols = True

        LinkEnv.AdditionalLibs.append("pthread")

        CompileEnv.Defines.append("RE_PLATFORM_LINUX=1")
        CompileEnv.Defines.append("RE_PLATFORM_UNIX=1")

        # For libraries
        CompileEnv.Defines.append("LINUX=1")

    # If we should create debug stuff
    # <BuildType> The build type
    # <Return> true if we should create debug info
    def ShouldCreateDebugInfo(self, BuildType):
        if BuildType == "Final":
            return False
        else:
            return True

    # Create the linux Toolchain
    # <Target> The target file
    # <Return> Linux Toolchain class
    def CreateToolChain(self, Target):
        Options = LinuxToolchain.Options

        if Target.UseAddressSanitizer is True:
            Options.UseAddressSanitizer = True

        if Target.UseThreadSanitizer is True:
            Options.UseThreadSanitizer = True

        if Target.UseUnknownSanitizer is True:
            Options.UseUnknownSanitizer = True

        return LinuxToolchain.LinuxToolchain(Target.Arch, self.SDK, Target.SavePSYM, Options)

    def Deploy(Receipt):
        pass  # DEPLOY IS NOT SUPPORTED YET!
