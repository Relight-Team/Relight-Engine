import os
import platform
import sys
import subprocess
import inspect
import importlib

from Internal import CompileEnvironment as CE
from Internal import ConfigManager as ConfigM
from Internal import Logger


from Configuration import TargetPlatforms as TP
from Configuration import Directory_Manager

from BaseSDK import PlatformFactory

EngineDir = Directory_Manager.Engine_Directory

ConfigDir = os.path.join(EngineDir, "Config")

_HostOS = platform.system()

# For scanning CustomSDK directory
sys.path.append(os.path.join(EngineDir, "Extras", "CustomSDK"))


# A class that stores information on the platform
class PlatformInfo:

    Platform = ConfigM.ReadConfig(
        ConfigDir + "/BaseBuilder.cfg", "PlatformInformation", "PlatformName"
    )
    Arch = ConfigM.ReadConfig(
        ConfigDir + "/BaseBuilder.cfg", "PlatformInformation", "PlatformArch"
    )

    def __init__(self):
        Platform = ConfigM.ReadConfig(
            ConfigDir + "/BaseBuilder.cfg", "PlatformInformation", "PlatformName"
        )
        Arch = ConfigM.ReadConfig(
            ConfigDir + "/BaseBuilder.cfg", "PlatformInformation", "PlatformArch"
        )

    def OverrideWithCMD(self, InPlatform=None, InArch=None):
        if InPlatform is not None:
            self.Platform = InPlatform

        if InArch is not None:
            self.Arch = InArch

    # Import the FactorySDK file based on the config
    def ImportFactory(self):

        Logger.Logger(0, "Running ImportFactory() from PlatformInfo")

        if os.path.isfile(
            os.path.join(
                EngineDir,
                "Programs",
                "RelightBuildTool",
                "SDK",
                self.Platform,
                self.Platform + "PlatformFactory.py",
            )
        ):
            Logger.Logger(
                1,
                "Platform Factory found in base SDK directory: "
                + EngineDir
                + "/Programs/RelightBuildTool/SDK/"
                + self.Platform
                + "/"
                + self.Platform
                + "PlatformFactory.py",
            )
            return importlib.import_module(
                "SDK." + self.Platform + "." + self.Platform + "PlatformFactory"
            )

        elif os.path.isfile(
            os.path.join(
                EngineDir,
                "Extras",
                "CustomSDK",
                self.Platform,
                self.Platform + "PlatformFactory.py",
            )
        ):
            Logger.Logger(
                1,
                "Platform Factory found in Custom SDK directory: "
                + EngineDir
                + "/Extras/CustomSDK/"
                + self.Platform
                + "/"
                + self.Platform
                + "PlatformFactory.py",
            )
            return importlib.import_module(
                self.Platform + "." + self.Platform + "PlatformFactory"
            )
        else:
            Logger.Logger(
                5,
                "Couldn't find "
                + self.Platform
                + "/"
                + self.Platform
                + "PlatformFactory.py in either RelightBuildTool's SDK directory or CustomSDK directory",
            )

    # Return true if the config file's platform value is valid
    def IsValid(self, InPlatform):
        Logger.Logger(0, "Running IsValid(" + InPlatform + ")")

        if self.Platform == InPlatform:
            Logger.Logger(1, "Returned True")
            return True
        Logger.Logger(1, "Returned False")
        return False


class Platform:

    BuildPlatform = {}

    PlatformGroup = {}

    Plat = ""

    DefaultCPPPlatform = CE.Platform

    PlatformCachedFolder = []

    IncludeCachedFolder = []

    ExcludeCachedFolder = []

    def __init__(self, InPlatform, InCppPlatform):
        self.Plat = InPlatform
        self.DefaultCPPPlatform = InCppPlatform

    # Create PlatformFactory instance and run the class's "RegBuildPlatform" function
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

                if (
                    IncNonInstalledPlats is True
                    or PlatInfo.IsValid(TempInit.TargetPlatform()) is True
                ):
                    Logger.Logger(
                        1, "Registering " + TempInit.TargetPlatform() + " to Types"
                    )
                    TempInit.RegBuildPlatform()

    # Return's the array of platform folders
    @staticmethod
    def GetPlatformFolders(self):
        Logger.Logger(0, "Running GetPlatformFolders()")
        if self.PlatformCachedFolder is None or self.PlatformCachedFolder == []:
            PlatFolder = []

            for i in TP.TargetPlatform:
                if TP.Valid(i) is True:
                    PlatFolder.append(i)

            for i in TP.TargetGroupPlatform:
                PlatFolder.append(i)

            self.PlatformCachedFolder = PlatFolder

        Logger.Logger(1, "Running GetPlatformFolders()")
        return self.PlatformCachedFolder

    # Return's all folders that we are going to include for this platform
    def GetIncludeFolders(self):
        Logger.Logger(0, "Running GetIncludeFolders()")
        if self.IncludeCachedFolder is None or self.IncludeCachedFolder == []:
            IncFolder = []

            IncFolder.append(self.Plat)

            temp = TP.GetPlatformGroup(self.Plat)
            for i in TP.ReturnTargetGroupVar(temp):
                IncFolder.append(i)

            self.IncludeCachedFolder = IncFolder

        return self.IncludeCachedFolder

    # Return's all folder that we are going to exclude for this platform
    def GetExcludeFolders(self):
        Logger.Logger(0, "Running GetExcludeFolders()")
        if self.ExcludeCachedFolder is None or self.ExcludeCachedFolder == []:
            self.ExcludeCachedFolder = self.GetPlatformFolders().difference(
                self.GetIncludeFolders()
            )

        return self.ExcludeCachedFolder

    # Return's true if we have the required SDK installed on this device
    def HasRequiredSDK(self):
        pass  # Will be overwritten with child class

    # Return's all platforms that are registered
    @staticmethod
    def GetRegPlatforms(self):
        Logger.Logger(0, "Running GetRegPlatforms()")
        List = []
        for Key in self.ReturnGroupDict():
            List.append(Key)
        return List

    # Return's the default architecture
    def GetDefaultArch(ProjectFile):
        return ""

    # Return's the folder name of the architecture
    def GetFolderNameArch(Arch):
        Logger.Logger(0, "Platform class's arch is " + Arch)
        return Arch

    # Return's true if the name is the main RBT name format without extension
    # Example: Test-Linux-Debug.so
    @staticmethod
    def IsBuildProductNameNoIndex(Name, TitlePrefixes, TitleSuffixes, Extension):
        return Platform.IsBuildProductName(
            Name, 0, len(Name), TitlePrefixes, TitleSuffixes, Extension
        )

    # Stuff to execute after the build process has been done but before we sync the target platform (which is when we prepare and transfer build artifacts to the target platform)
    def PostBuildBeforeSync(Target):
        pass  # Will be overwritten with child class

    # Return the bundle directory for the Link Environment
    def GetBundleDir(Target, FileOutputs):
        return None

    # Return's true if the plaform can be used
    @staticmethod
    def CanUsePlatform(Platform):
        for Index in TP.TargetPlatform:
            if Index.name.lower == Platform.lower:
                return True

        return False

    #  Set Input to BuildPlatform instance
    @staticmethod
    def RegBuildPlatform(InBuildPlatform):
        Logger.Logger(
            1,
            "Adding platform " + str(InBuildPlatform.Plat) + " to BuildPlatform array",
        )
        Platform.BuildPlatform[InBuildPlatform.Plat] = InBuildPlatform

    # Set PlatformGroup to the input group key with the value of input build platform
    @staticmethod
    def RegBuildPlatformGroup(InBuildPlatform, InBuildPlatformGroup):
        if InBuildPlatformGroup not in Platform.PlatformGroup:
            Platform.PlatformGroup[InBuildPlatformGroup] = []
        Platform.PlatformGroup[InBuildPlatformGroup].append(InBuildPlatform)

    # Return's all groups with the given platform
    @staticmethod
    def GetAllGroupsWithPlatform(Platform):
        GroupList = []

        for Group in TP.TargetGroupPlatform:
            PlatList = Group.value

            for Platfor in PlatList:
                if Platfor.name.lower == Platform.lower:
                    GroupList.append(Platfor.name)
        return GroupList

    # Return's the BuildPlatform value if it exist, return's None if we allow failure, otherwise it will raise an error
    @staticmethod
    def GetBuildPlatform(InPlatform, AllowFailure=False):
        if InPlatform in Platform.BuildPlatform:
            return Platform.BuildPlatform[InPlatform]
        elif AllowFailure is True:
            return None
        else:
            Logger.Logger(
                5,
                "BuildPlatform does not has key '"
                + str(InPlatform)
                + "' when running GetBuildPlatform",
            )

    # modify each Module in BuildPlatform
    @staticmethod
    def ModifyHostModuleConfig(ModName, Target, Module):
        for Item in Platform.BuildPlatform:
            Tmp = Item.value
            Tmp.ActivePlatformModuleRulesToModify(ModName, Target, Module)

    # modify each moudle in the target
    def ActivePlatformModuleRulesToModify(ModName, Target, Module):
        pass  # Will be overwritten with child class

    # return's the Delimiter based on the platform
    @staticmethod
    def GetPathDelimiter():
        if _HostOS == "Windows":
            return ";"
        else:
            return ":"

    # Return's the platform is
    def GetPlatformName(self):
        return self.__class__.__name__

    # Return's if this platform supports XGE (Incredibuild or equivalent)
    def CanUseXGE(self):
        return True

    # Return's if this platform supports multiple execution at once
    def CanParallelExecute(self):
        return self.CanUseXGE()

    # If the platform support distributed compilation (Distcc, DMUCS, etc)
    def CanUseDistcc(self):
        return False

    # If this platform support's SN-DBS (SN System's Distributed Build Server)
    def CanUseSNDBS(self):
        return False

    # Set the new target to platform-specific defaults
    def ResetTarget(Target):
        pass  # Will be overwritten with child class

    # Validate the Target File
    def MakeTargetValid(Target):
        pass  # Will be overwritten with child class

    # Return's if the platform requires a monolithic build (All modules into a single binary)
    @staticmethod
    def RequireMonolithicBuild(self, InPlatform, InConfig):
        BuildPlat = self.GetBuildPlatform(InPlatform, True)
        if BuildPlat is not None:
            return self.ShouldCompileMonolithic(InPlatform)

        return False

    # Return's the platform binary extension based on the bin type
    def GetBinExtension(InBinType):
        return None

    # Return's the extension for debug info based on bin type
    def GetDebugExtension(Target, InBinType):
        return None

    # If we should make the compile Monolithic if the config file is not set
    def ShouldCompileMonolithic(self, Name, Target, Module):
        return False

    # Returns if we should override whether to append the arch to bin name
    def NeedsArchSuffix(self):
        return True

    # Return's the array of binary output files (by default, it will only return 1 item)
    def FinalizeBinPaths(self, BinName, ProjectFile, Target):
        Tmp = []
        Tmp.append(BinName)
        return Tmp

    # Return the array of configs we are using
    def GetConfig(Target, IncludeDebug):
        Config = []

        Config.append("Development")

        if IncludeDebug is True:
            Config.insert(0, "Debug")

        return Config

    # Return's true if the Project Settings are the same as the defualt settings
    @staticmethod
    def IsProjectSettingsDefault(
        Platform, ProjectDir, Section, IntKeys, BoolKeys, StringKeys
    ):
        pass  # TODO: DO ONCE FINISH CONFIG

    # Returns if we have the following default build config settings
    def HasDefaultBuildConfig(Platform, ProjectDir):
        pass

    # Returns if we required a build
    def RequiresBuild(Platform, ProjectDir):
        return False

    # Add the extra modules the platform requires, without exposing information about the platform
    def AddExtraModules(Target, ModuleNames):
        pass  # Will be overwritten with child class

    # Setup the target environment
    def SetUpEnvironment(Target, CompileEnv, LinkEnv):
        pass  # Will be overwritten with child class

    # Setup the config enviornment
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

    # returns metadata that is not tracked
    def GetExternalBuildMetadata(ProjectFile):
        pass  # Will be overwritten with child class

    # Return's true if platform is in group
    @staticmethod
    def IsPlatformInGroup(Platform, Group):
        Plat = TP.ReturnTargetGroupVar(Group)

        if Plat is not None and Platform in Plat:
            return True
        return False

    # If we should Create debug information if the config file is not set
    def ShouldCreateDebugInfo(self, BuildType):
        pass  # Will be overwritten with child class

    # Create the platform's toolchain instance
    def CreateToolChain(InCppPlatform, Target):
        pass  # Will be overwritten with child class

    # Deploy the target
    def Deploy(Receipt):
        pass  # Will be overwritten with child class
