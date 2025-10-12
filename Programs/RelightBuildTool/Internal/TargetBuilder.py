import os

from . import ModuleBuilder
from . import Binary
from . import CompileEnvironment
from . import LinkEnvironment
from . import FileBuilder
from . import Logger


from Readers import ModuleReader
from Readers import TargetReader

from BaseSDK import Platform

from Configuration import Directory_Manager


# Builds a target, will use ModuleBuilder
class TargetBuilder:

    Target = None  # The TargetReader class

    PlatformIntermed = None  # Intermediate directory for the platform

    PlatformIntermedFolder = None  #

    EngineIntermed = None  # Intermediate directory for engine binary

    ProjectDir = None  # The project directory, if doesn't exist, we will use engine directory instead

    Binaries = []

    StartingTarget = None

    ModuleName_ModuleBuilder = {}

    ArchToUse = None

    BuildType = None

    def __init__(self, InStartingTarget, InTarget=None):
        self.StartingTarget = InStartingTarget
        self.Target = InTarget

        # If arch set in command argument, we will use that, otherwise we will use target arch
        if self.StartingTarget.Arch is not None:
            Logger.Logger(
                3,
                "Arch we are using (based on command line): "
                + str(self.StartingTarget.Arch),
            )
            self.ArchToUse = self.StartingTarget.Arch
        else:
            Logger.Logger(
                3, "Arch we are using (based on target file): " + str(self.Target.Arch)
            )
            self.ArchToUse = self.Target.Arch

        if self.StartingTarget.BuildType is not None:
            Logger.Logger(3, "Using BuildType: " + self.StartingTarget.BuildType)
            self.BuildType = self.StartingTarget.BuildType
        else:
            Logger.Logger(
                4,
                "BuildType not defined in command line, using target's definition: "
                + self.Target.BuildType,
            )
            self.BuildType = self.Target.BuildType

        self.PlatformIntermedFolder = TargetBuilder.GetIntermediateProject(
            self.StartingTarget.Platform, self.ArchToUse
        )

        # Overwrite target file with starting target properties
        if (
            self.StartingTarget.Modules != []
            and self.StartingTarget.Modules is not None
        ):
            self.Target.Modules = self.StartingTarget.Modules

        if self.Target._Project is not None and self.Target._Project != "":
            self.ProjectDir = os.path.dirname(self.Target._Project)
        else:
            self.ProjectDir = Directory_Manager.Engine_Directory

        self.PlatformIntermed = os.path.join(
            self.ProjectDir,
            self.PlatformIntermedFolder,
            self.Target.Name,
            self.BuildType,
        )

        if self.Target.IntermediateType == "Unique":
            self.EngineIntermed = self.PlatformIntermed

        else:
            self.EngineIntermed = os.path.join(
                Directory_Manager.Engine_Directory,
                self.PlatformIntermed,
                self.Target.Name,
                self.BuildType,
            )

    @staticmethod
    def GetIntermediateProject(Platform, Arch):
        return os.path.join("Intermediate", "Build", Platform, Arch)

    def CreateToolchain(self, InPlatform):

        if self.Target.ToolchainOverride is None:
            PlatformClassTemp = Platform.Platform.GetBuildPlatform(InPlatform)

            return PlatformClassTemp.CreateToolChain(InPlatform, self.Target)

        else:

            pass  # FIXME: Add support for ToolchainOverride

    def GetExeDir(self):
        return self.Binaries[0].OutputDir

    def IsEngineInstalled(self):
        InstalledEngineFileDir = os.path.join(
            Directory_Manager.Engine_Directory, "Build", "Installed.txt"
        )

        if os.path.isfile(InstalledEngineFileDir):
            return True
        else:
            return False

    # MASSIVE TODO: add more appends stuff once we add more options to target reader
    def AppendGlobalEnv(self, Toolchain, CompileEnv, LinkEnv):
        Toolchain.SetGlobalEnv(self.Target)

        # Append Global Compile Environment
        CompileEnv.Defines.extend(self.Target.Defines)
        CompileEnv.AdditionalArgs = self.Target.ExtraCompileArgs
        CompileEnv.CopyIncToIntermediate = self.Target.CopyIncToIntermediate

        # Append Global Link Environment

        LinkEnv.AdditionalArgs = self.Target.ExtraLinkingArgs

        LinkInterTemp = os.path.join(
            Directory_Manager.Engine_Directory,
            self.PlatformIntermedFolder,
            self.Target.Name,
            self.BuildType,
        )

        if self.IsEngineInstalled() or (
            self.Target._Project is not None and self.Target.LinkType == "Monolithic"
        ):
            if self.Target._Project is not None:
                LinkInterTemp = os.path.join(
                    os.path.dirname(self.Target._Project),
                    self.PlatformIntermedFolder,
                    self.Target.Name,
                    self.BuildType,
                )
            # TODO: Add plugin support

        CompileEnv.UserIncPaths.append(Directory_Manager.Engine_Directory)

        LinkEnv.IntermediateDir = LinkInterTemp

        LinkEnv.OutputDir = LinkEnv.IntermediateDir

        LinkEnv.LocalShadowDir = LinkEnv.OutputDir

        # TODO: Add custom defines here for some target settings

        InPlatform = Platform.Platform.GetBuildPlatform(self.StartingTarget.Platform)

        InPlatform.SetUpEnvironment(self.Target, CompileEnv, LinkEnv)

        InPlatform.SetUpConfigEnv(self.Target, self.BuildType, CompileEnv, LinkEnv)

    def CreateProjectCompileEnv(self):
        InPlatform = Platform.Platform.GetBuildPlatform(self.StartingTarget.Platform)

        CPPPlatform = InPlatform.DefaultCPPPlatform

        CompileEnv = CompileEnvironment.CompileEnvironment(
            CPPPlatform.name, self.BuildType, self.ArchToUse
        )
        LinkEnv = LinkEnvironment.LinkEnvironment(
            CPPPlatform.name, self.BuildType, self.ArchToUse
        )

        Toolchain = self.CreateToolchain(CPPPlatform)
        self.AppendGlobalEnv(Toolchain, CompileEnv, LinkEnv)

        return CompileEnv

    def SearchThroughDir(self, Dir, TargetDir):
        BlacklistFolders = ["Intermediate", "bin"]
        for Root, SubDirList, Files in os.walk(Dir):
            if TargetDir in SubDirList and all(
                BlacklistItem not in Root for BlacklistItem in BlacklistFolders
            ):
                return os.path.join(Root, TargetDir)
        return None

    def IsUnderDir(self, Dir, File):
        Logger.Logger(
            1, "Checking if " + str(File) + " is under " + str(Dir) + ", please wait..."
        )
        for Root, _, Files in os.walk(Dir):
            if File in Files:
                return True
        return False

    # TODO: Add support for generated code!
    def FindModuleName(self, Name):

        Logger.Logger(1, "Looking For Module Name: " + Name)

        # Check Project directory
        if self.Target._Project is not None:
            ProjectDirSource = os.path.join(
                os.path.dirname(self.Target._Project), "Src"
            )
            # Temp = os.path.dirname(self.Target._Project)
        else:
            ProjectDirSource = Directory_Manager.Engine_Directory

        ModuleFile = self.SearchThroughDir(ProjectDirSource, Name)

        if ModuleFile is None:
            Logger.Logger(
                5,
                "We could not find Module "
                + Name
                + " because ModuleFile is none, Skipping...",
            )

        if ModuleFile is not None:
            FullModuleFile = os.path.join(ModuleFile, Name + ".Build")
            ModReader = ModuleReader.Module(FullModuleFile, self.StartingTarget)

            # TODO: Add generated code stuff here

            ModuleRet = ModuleBuilder.ModuleBuilder(
                ModReader,
                os.path.join(ProjectDirSource, "Intermediate"),
                self.Target,
                self.StartingTarget,
                self.BuildType,
            )

            self.ModuleName_ModuleBuilder[ModReader.Name] = ModuleRet

            return ModuleRet

        Logger.Logger(5, "We could not find module name " + Name + ", Skipping...")

        return None

    @staticmethod
    def CreateBinName(Name, InPlatform, LinkType, Arch, BinType):

        Ret = ""

        if InPlatform == "Linux" and (BinType == "Dynamic" or BinType == "Static"):
            Ret = "lib"

        Ret = Ret + Name

        BuildPlatform = Platform.Platform.GetBuildPlatform(InPlatform)

        if BuildPlatform.NeedsArchSuffix() is True:
            Ret = Ret + Arch

        Ret = Ret + BuildPlatform.GetBinExtension(BinType)

        return Ret

    def CreateBinPaths(
        self,
        Dir,
        Name,
        InPlatform,
        LinkType,
        BinType,
        Arch,
        ExeSubFolder,
        ProjectFile,
        TargetFile,
    ):

        BinDir = os.path.join(Dir, "bin", Name, InPlatform, Arch, self.BuildType)

        os.makedirs(BinDir, exist_ok=True)

        if ExeSubFolder is not None and ExeSubFolder != "":
            BinDir = os.path.join(BinDir, ExeSubFolder)

        # Create full binary path with file name
        Bin = os.path.join(
            BinDir,
            TargetBuilder.CreateBinName(Name, InPlatform, LinkType, Arch, BinType),
        )

        BuildPlatform = Platform.Platform.GetBuildPlatform(InPlatform)

        return BuildPlatform.FinalizeBinPaths(Bin, ProjectFile, TargetFile)

    def SetupBinaries(self):

        if self.Target.IncludeLaunch == True and (
            self.Target.LaunchName is None or self.Target.LaunchName == ""
        ):
            Logger.Logger(5, "Launch name is None or blank")

        if self.Target.IncludeLaunch == True:
            LaunchModule = self.FindModuleName(self.Target.LaunchName)
        else:
            # Logger.Logger(4, "LaunchModule is turned off, the main function MUST be the first on the Module List!")
            # If we don't have Launch Module, just use the first module
            LaunchModule = self.FindModuleName(self.Target.Modules[0])

        if (
            self.IsUnderDir(
                Directory_Manager.Engine_Directory, LaunchModule.Module.FilePath
            )
            is True
            and self.Target.LinkType == "Monolithic"
        ):
            # GetIntermediateModule()
            IntermediateDir = os.path.join(
                Directory_Manager.Engine_Directory,
                self.PlatformIntermedFolder,
                self.Target.Name,
                self.BuildType,
            )
        else:
            IntermediateDir = self.PlatformIntermed

        if (
            self.Target.LinkType == "Monolithic"
            or self.Target.IntermediateType == "Unique"
        ):
            OutputDir = self.ProjectDir
        else:
            OutputDir = Directory_Manager.Engine_Directory

        if (
            self.Target.IsDynamicLibrary is True
            and self.Target.LinkType == "Monolithic"
        ):
            CompileAsDynamic = True
        else:
            CompileAsDynamic = False

        if CompileAsDynamic is True:
            DynamicType = "Dynamic"
        else:
            DynamicType = "EXE"

        OutputList = self.CreateBinPaths(
            OutputDir,
            self.Target.Name,
            self.StartingTarget.Platform,
            self.Target.LinkType,
            DynamicType,
            self.ArchToUse,
            self.Target.BinSubPaths,
            self.Target._Project,
            self.Target,
        )

        Bin = Binary.Binary(
            DynamicType, OutputList, IntermediateDir, LaunchModule, None, None
        )  # FIXME: Haven't implemented Exports and Precompile, using none for now

        self.Binaries.append(Bin)

        LaunchModule.Binary = Bin

        # Bin.Modules.append(LaunchModule)

    @staticmethod
    def CreateTargetReaderFromTargetName(TargetName, StartingTarget, ProjectFile=None):

        # if Project File is defined, search in that directory, otherwise we will search through engine directory
        if ProjectFile is not None:
            DirToSearch = os.path.dirname(ProjectFile)
        else:
            DirToSearch = Directory_Manager.Engine_Directory

        # If we have -TargetDir set, then it will always overwrite everything else

        if StartingTarget.TargetDir is not None:
            DirToSearch = StartingTarget.TargetDir

        TargetSearchDir = os.path.join(DirToSearch)

        RetFile = None

        Logger.Logger(1, "Searching For Target File at: " + TargetSearchDir)
        # Search through directory
        # TODO: Unoptimized, since this will check every single file to see if it's a target file, is there an Optimized way?
        for RootDir, SubDirList, FilesList in os.walk(TargetSearchDir):
            for File in FilesList:
                if File == TargetName + ".Target":
                    RetFile = os.path.join(RootDir, File)

        if RetFile is None:
            Logger.Logger(5, "We could not find " + TargetName + ".Target")

        Logger.Logger(1, "Target file found: " + RetFile)

        Ret = TargetReader.Target(RetFile, StartingTarget, ProjectFile)

        return Ret

    # Set's up the binary for creating a dynamic lib
    def CreateModuleDynamicLib(self, ModuleBuilder):
        pass

    # Set's up all modules in the target list
    def SetupTargetModules(self):

        IndexToLook = 0

        # If the condition is set to make the Launch module in the modules list, we will skip the first entry
        if self.Target.IncludeLaunch is False:
            IndexToLook = 1

        while IndexToLook < len(self.Target.Modules):
            Mod = self.FindModuleName(self.Target.Modules[IndexToLook])

            if Mod.Binary is None:
                if self.Target.LinkType == "Monolithic":
                    Mod.Binary = self.Binaries[
                        0
                    ]  # Sync the Module binary to the first binary list (usually the Launch module
                    Mod.Binary.AddModule(Mod)  # Append the binary's Modules list
                else:
                    Mod.Binary = self.CreateModuleDynamicLib(Mod)
                    self.Binaries.append(Mod.Binary)

            IndexToLook += 1

    # Functions to run before we prepare to build the Target
    def SetupPreBuild(self):
        self.SetupBinaries()
        self.SetupTargetModules()

    # If arg set, we will run RelightCookerTool with correct params
    def StartCooker(self):
        Logger.Logger(3, "RBT Initialize CookerTool")
        RCT = os.path.join(
            Directory_Manager.Program_Directory, "RelightCookerTool", "main.py"
        )

        ProjectFile = ""

        if self.Target._Project is not None:
            ProjectFile = str(os.path.basename(self.Target._Project))

        os.system(
            "python "
            + RCT
            + " -Project="
            + ProjectFile
            + " -Target="
            + self.Target.Name
            + " -SourceDir="
            + str(os.path.dirname(self.Target.FilePath))
            + " -Platform="
            + self.StartingTarget.Platform
            + " -OutputDir="
            + os.path.dirname(self.GetExeDir())
        )

    # Create's a TargetBuilder class based on StartingTarget
    @staticmethod
    def Create(StartingTarget, UsePrecompiled):
        TargetReader = TargetBuilder.CreateTargetReaderFromTargetName(
            StartingTarget.Name, StartingTarget, StartingTarget.Project
        )

        # TODO: Add precompile support here

        Ret = TargetBuilder(StartingTarget, TargetReader)

        Ret.SetupPreBuild()

        return Ret

    # Build's the target, uses binary class to compile the files
    # FIXME: Just like with ModuleBuilder, this is a quick hack thrown to ensure at least the basics will work for the first testing. Once complete, please add these features
    # UNITY system, C++20 support, Precompiled headers, HeaderTool, Live Coding, Includes Header option
    def Build(self, BuildConf, WorkingSet, AreWeAssembilingBuild):

        # If we want to bake, do it here

        if self.StartingTarget.GonnaCook is True:
            self.StartCooker()

        BinOriginal = []

        Plat = Platform.Platform.GetBuildPlatform(self.StartingTarget.Platform)

        CppPlat = Plat.DefaultCPPPlatform

        CompileEnv = CompileEnvironment.CompileEnvironment(
            CppPlat, self.BuildType, self.ArchToUse
        )

        # Set Linkenv

        LinkEnv = LinkEnvironment.LinkEnvironment(
            CompileEnv.Plat, CompileEnv.Conf, CompileEnv.Arch
        )

        Toolchain = self.CreateToolchain(CppPlat.value)

        self.AppendGlobalEnv(Toolchain, CompileEnv, LinkEnv)

        # NewCompileEnv = self.CreateProjectCompileEnv()

        InFileBuilder = FileBuilder.FileBuilder()

        # FIXME: Add binary filter

        # FIXME: Add plugin support

        # FIXME: Add code here that will let exe know all modules included if using monolithic

        # FIXME: Add code that tells the exe where the engine dir is and put it in compile defines

        # FIXME: Add UObject support and generated code support

        ExeOutputDir = self.GetExeDir()

        OutputItems = []

        # Compile each binary

        for Item in self.Binaries:

            BinOutput = Item.Build(
                self.Target, Toolchain, CompileEnv, LinkEnv, ExeOutputDir, InFileBuilder
            )

        # FIXME: Add runtime depends support

        # FIXME: Add precompile Plugin support

        # FIXME: Add metadata support

        return InFileBuilder
