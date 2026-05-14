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
            Logger.Logger(3, "Arch we are using (based on command line): "+ str(self.StartingTarget.Arch))
            self.ArchToUse = self.StartingTarget.Arch

        # Else, get the arch from target file
        else:
            Logger.Logger(3, "Arch we are using (based on target file): " + str(self.Target.Arch))
            self.ArchToUse = self.Target.Arch

        # If build type is set, use it
        if self.StartingTarget.BuildType is not None:
            Logger.Logger(3, "Using BuildType: " + self.StartingTarget.BuildType)
            self.BuildType = self.StartingTarget.BuildType

        # Otherwise we will use target's definition
        else:
            Logger.Logger(4, "BuildType not defined in command line, using target's definition: " + self.Target.BuildType)
            self.BuildType = self.Target.BuildType

        # Set PlatformIntermedFolder to 'Intermediate/Build/{Platform}/{Arch}'
        self.PlatformIntermedFolder = TargetBuilder.GetIntermediateProject(self.StartingTarget.Platform, self.ArchToUse)

        # Overwrite target file with starting target properties
        if self.StartingTarget.Modules != [] and self.StartingTarget.Modules is not None:
            self.Target.Modules = self.StartingTarget.Modules

        if self.Target._Project is not None and self.Target._Project != "":
            self.ProjectDir = os.path.dirname(self.Target._Project)
        # If Project file doesn't exist, then set project directory to engine directory
        else:
            self.ProjectDir = Directory_Manager.Engine_Directory

        # Set PlatformIntermed to '/Path/To/Project/Intermediate/Build/{Platform}/{Arch}/{TargetName}/{BuildType}'
        self.PlatformIntermed = os.path.join(self.ProjectDir, self.PlatformIntermedFolder, self.Target.Name, self.BuildType)

        # If intermediate type is unique, then set engine intermeidate to platform directory
        if self.Target.IntermediateType == "Unique":
            self.EngineIntermed = self.PlatformIntermed

        # Otherwise, set engine intermediate to the engine directory
        else:
            self.EngineIntermed = os.path.join(Directory_Manager.Engine_Directory, self.PlatformIntermed, self.Target.Name, self.BuildType)

    # Get the intermediate directory (example: {Intermediate/Build/{Platform}/{Arch}})
    # <Return> joined OS path
    @staticmethod
    def GetIntermediateProject(Platform, Arch):
        return os.path.join("Intermediate", "Build", Platform, Arch)

    # Create the toolchain class
    # <InPlatform> The platform to create the toolchain
    # <Return> The toolchain class
    def CreateToolchain(self, InPlatform):

        # If we are not overwriting toolchain
        if self.Target.ToolchainOverride is None:
            # Get target's platform class
            TargetPlatform = Platform.Platform.GetBuildPlatform(InPlatform)

            # Return toolchain from platform class
            return TargetPlatform.CreateToolChain(self.Target)

        # Else, get the override platform
        else:
            pass  # FIXME: Add support for ToolchainOverride

    # Get the output directory for executable
    # <Return> Output directory for first binary in list
    def GetExeDir(self):
        return self.Binaries[0].OutputDir

    # Check if engine is installed by checking Installed.txt
    # <Return> true if 'Installed.txt' exists
    def IsEngineInstalled(self):

        # Get Installed file
        InstalledEngineFileDir = os.path.join(Directory_Manager.Engine_Directory, "Build", "Installed.txt")

        # Return's if file exists
        return os.path.isfile(InstalledEngineFileDir)

    # Appends Compile Environment and Link Environment settings based on target and other settings
    # <CompileEnv> The Compile Environment to append
    # <LinkEnv> The Link Environment to append
    # MASSIVE TODO: add more appends stuff once we add more options to target reader
    def AppendGlobalEnv(self, CompileEnv, LinkEnv):

        # Append Global Compile Environment
        CompileEnv.Defines.extend(self.Target.Defines)
        CompileEnv.AdditionalArgs = self.Target.ExtraCompileArgs
        CompileEnv.CopyIncToIntermediate = self.Target.CopyIncToIntermediate

        # Append Global Link Environment
        LinkEnv.AdditionalArgs = self.Target.ExtraLinkingArgs

        # Set link intermediate to engine
        LinkInterTemp = os.path.join(Directory_Manager.Engine_Directory, self.PlatformIntermedFolder, self.Target.Name, self.BuildType)

        # If engine is installed or project is not none and is monolithic
        if self.IsEngineInstalled() or (self.Target._Project is not None and self.Target.LinkType == "Monolithic"):
            if self.Target._Project is not None:
                # Set intermediate to Project intermediate
                LinkInterTemp = os.path.join(os.path.dirname(self.Target._Project), self.PlatformIntermedFolder, self.Target.Name, self.BuildType)

        # Set intermeidate directory for link
        LinkEnv.IntermediateDir = LinkInterTemp

        # TODO: Add plugin support

        CompileEnv.UserIncPaths.append(Directory_Manager.Engine_Directory)

        LinkEnv.OutputDir = LinkEnv.IntermediateDir

        LinkEnv.LocalShadowDir = LinkEnv.OutputDir

        # TODO: Add custom defines here for some target settings

        InPlatform = Platform.Platform.GetBuildPlatform(self.StartingTarget.Platform)

        InPlatform.SetUpEnvironment(self.Target, CompileEnv, LinkEnv)

        InPlatform.SetUpConfigEnv(self.Target, self.BuildType, CompileEnv, LinkEnv)


    # Create Compile Environment for project
    # FIXME: UNUSED FOR NOW
    #def CreateProjectCompileEnv(self):
        #InPlatform = Platform.Platform.GetBuildPlatform(self.StartingTarget.Platform)

        #CPPPlatform = InPlatform.DefaultCPPPlatform

        #CompileEnv = CompileEnvironment.CompileEnvironment(
            #CPPPlatform.name, self.BuildType, self.ArchToUse
        #)
        #LinkEnv = LinkEnvironment.LinkEnvironment(
            #CPPPlatform.name, self.BuildType, self.ArchToUse
        #)

        #Toolchain = self.CreateToolchain(CPPPlatform)
        #self.AppendGlobalEnv(CompileEnv, LinkEnv)

        #return CompileEnv


    # Search through all files in directory for a certain file, ignores intermediate and bin directories
    # <Dir> The directory to look in
    # <Name> The name of file to search
    # <Return> The full path of file, return None if we couldn't find it
    def SearchThroughDir(self, Dir, Name):
        BlacklistFolders = ["Intermediate", "bin"]
        for Root, SubDirList, Files in os.walk(Dir):
            if Name in SubDirList and all(BlacklistItem not in Root for BlacklistItem in BlacklistFolders):
                return os.path.join(Root, Name)
        return None

    # Check if file is under dir
    # <Dir> The directory to search
    # <File> The file to search for
    # <Return> return's True if file exist
    def IsUnderDir(self, Dir, File):
        for Root, _, Files in os.walk(Dir):
            if File in Files:
                return True
        return False

    # Find's the module name defined in target file and create module builder (Note: These only check project/target modules, module dependencies are NOT checked here)
    # <Name> Name of module to build
    # <Return> Module builder for the module, None if not found
    # TODO: Add support for generated code!
    def FindModuleName(self, Name):

        Logger.Logger(1, "Looking For Module Name: " + Name)

        # Check Project directory
        if self.Target._Project is not None:
            ProjectDirSource = os.path.join(os.path.dirname(self.Target._Project))

        # If target directory is set, check it
        elif self.StartingTarget.TargetDir is not None:
            ProjectDirSource = os.path.join(self.StartingTarget.TargetDir)
        # else, check engine directory
        else:
            ProjectDirSource = Directory_Manager.Engine_Directory

        # Search module file through the directory we are checking
        ModuleFile = self.SearchThroughDir(ProjectDirSource, Name)

        # Let user know we are skipping module if we can't find it
        if ModuleFile is None:
            Logger.Logger(5, "We could not find Module " + Name + " because ModuleFile is none, Skipping...")

        if ModuleFile is not None:
            # Get the build file with '.Build' extension
            FullModuleFile = os.path.join(ModuleFile, Name + ".Build")
            # Read Build file
            ModReader = ModuleReader.Module(FullModuleFile, self.StartingTarget)

            # TODO: Add generated code stuff here

            # Create module builder
            ModuleRet = ModuleBuilder.ModuleBuilder(ModReader, os.path.join(ProjectDirSource, "Intermediate"), self.Target, self.StartingTarget, self.BuildType)

            # Add Module Builder to Map
            self.ModuleName_ModuleBuilder[ModReader.Name] = ModuleRet

            return ModuleRet

        Logger.Logger(5, "We could not find module name " + Name + ", Skipping...")

        return None

    # Return's the binary name
    # <Name> The name of the binary
    # <InPlatform> The platform we are compiling
    # <Arch> The arch we are compiling
    # <BinType> The binary type we are compiling
    # <Return> the full binary file name
    @staticmethod
    def CreateBinName(Name, InPlatform, LinkType, Arch, BinType):

        Ret = ""

        # If linux and bintype is a library, add 'lib' to front
        if InPlatform == "Linux" and (BinType == "Dynamic" or BinType == "Static"):
            Ret = "lib"

        Ret = Ret + Name

        BuildPlatform = Platform.Platform.GetBuildPlatform(InPlatform)

        if BuildPlatform.NeedsArchSuffix() is True:
            Ret = Ret + Arch

        Ret = Ret + BuildPlatform.GetBinExtension(BinType)

        return Ret

    # Create a list of paths for binaries we are gonna create
    # <Dir> The main directory the bin folder will be located in
    # <Name> Name of program
    # <InPlatform> The platform we are compiling to
    # <Arch> The Arch we will compile to
    # <ExeSubFolder> Subfolder a bin will be in, leave blank for parent directory
    # <ProjectFile> The project file
    # <TargetFile> The target file
    # <Return> List of all binary outputs
    def CreateBinPaths(self, Dir, Name, InPlatform, LinkType, BinType, Arch, ExeSubFolder, ProjectFile, TargetFile):

        # Get binary directory for project
        BinDir = os.path.join(Dir, "bin", Name, InPlatform, Arch, self.BuildType)

        # Create dir
        os.makedirs(BinDir, exist_ok=True)

        if ExeSubFolder is not None and ExeSubFolder != "":
            BinDir = os.path.join(BinDir, ExeSubFolder)

        # Create full binary path with file name
        Bin = os.path.join(
            BinDir,
            TargetBuilder.CreateBinName(Name, InPlatform, LinkType, Arch, BinType),
        )

        # Get Build Platform in registry
        BuildPlatform = Platform.Platform.GetBuildPlatform(InPlatform)

        # Return binary output file
        return BuildPlatform.FinalizeBinPaths(Bin, ProjectFile, TargetFile)

    # Create launch module binary class and store it in list
    def SetupBinaries(self):

        # if launch is not set, throw error
        if self.Target.IncludeLaunch == True and (self.Target.LaunchName is None or self.Target.LaunchName == ""):
            Logger.Logger(5, "Launch name is None or blank")

        # Get launch module if we are including launch
        if self.Target.IncludeLaunch == True:
            LaunchModule = self.FindModuleName(self.Target.LaunchName)
        else:
            # If we don't have Launch Module, just use the first module
            LaunchModule = self.FindModuleName(self.Target.Modules[0])

        # If Module Launch module is in directory and the target is monolithic, set the intermediate directory to engine, otherwise, set it to platform
        if self.IsUnderDir(Directory_Manager.Engine_Directory, LaunchModule.Module.FilePath) == True and self.Target.LinkType == "Monolithic":
            IntermediateDir = os.path.join(Directory_Manager.Engine_Directory, self.PlatformIntermedFolder, self.Target.Name, self.BuildType)
        else:
            IntermediateDir = self.PlatformIntermed

        # If we are compiling monolithic or if our intermediate type is unique, set our output directory to project
        if self.Target.LinkType == "Monolithic" or self.Target.IntermediateType == "Unique":
            OutputDir = self.ProjectDir
        # else, set it to engine
        else:
            OutputDir = Directory_Manager.Engine_Directory

        # If we are compiling a dynamic library and compiling as monolithic, then we will compile as dynamic
        if self.Target.IsDynamicLibrary is True and self.Target.LinkType == "Monolithic":
            CompileAsDynamic = True
        else:
            CompileAsDynamic = False

        # Set dynamic type
        if CompileAsDynamic is True:
            DynamicType = "Dynamic"
        else:
            DynamicType = "EXE"

        # Get list of all binary paths
        OutputList = self.CreateBinPaths(OutputDir, self.Target.Name, self.StartingTarget.Platform, self.Target.LinkType, DynamicType, self.ArchToUse, self.Target.BinSubPaths, self.Target._Project, self.Target)

        # Create binary class for LaunchModule
        Bin = Binary.Binary(DynamicType, OutputList, IntermediateDir, LaunchModule, False) # TODO: Replace 'False' with Preocmpiled

        # Append launch binary to binaries list
        self.Binaries.append(Bin)

        LaunchModule.Binary = Bin

    # Finds a target and reads it
    # <TargetName> The name of the target to find
    # <StartingTarget> The Starting target, mainly used for -TargetDir
    # <ProjectFile> The project file
    # <Return> Target Reader for the found target, None if not found
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
    # TODO: ADD ME
    def CreateModuleDynamicLib(self, ModuleBuilder):
        pass

    # Set's up all modules in the target list
    def SetupTargetModules(self):

        IndexToLook = 0

        # If the condition is set to make the Launch module in the modules list, we will skip the first entry
        if self.Target.IncludeLaunch is False:
            IndexToLook = 1

        # For each module
        while IndexToLook < len(self.Target.Modules):
            # Find Module and create builder
            Mod = self.FindModuleName(self.Target.Modules[IndexToLook])

            # If module builder doesn't have a binary, set it
            if Mod.Binary is None:
                if self.Target.LinkType == "Monolithic":
                    Mod.Binary = self.Binaries[0]  # Sync the Module binary to the first binary list (usually the Launch module
                    Mod.Binary.AddModule(Mod)  # Append the binary's Modules list
                else:
                    # Create dynamic module library and add it to binaries list
                    Mod.Binary = self.CreateModuleDynamicLib(Mod)
                    self.Binaries.append(Mod.Binary)

            # Increase index to search
            IndexToLook += 1

    # Functions to run before we prepare to build the Target
    def SetupPreBuild(self):
        self.SetupBinaries() # Create Launch Module
        self.SetupTargetModules() # Create binary class for each module

    # If arg set, we will run RelightCookerTool with correct params
    def StartCooker(self):
        Logger.Logger(3, "RBT Initialize CookerTool")
        # Directory for CookerTool python file
        RCT = os.path.join(Directory_Manager.Program_Directory, "RelightCookerTool", "main.py")

        # Set Project file if it exists
        ProjectFile = ""
        if self.Target._Project is not None:
            ProjectFile = str(os.path.basename(self.Target._Project))

        # Run via os.system
        os.system("python " + RCT + " -Project=" + ProjectFile + " -Target=" + self.Target.Name + " -SourceDir=" + str(os.path.dirname(self.Target.FilePath)) + " -Platform=" + self.StartingTarget.Platform + " -OutputDir=" + os.path.dirname(self.GetExeDir()))

    # Create's a TargetBuilder class based on StartingTarget
    # <StartingTarget> The starting target
    # <UsePrecompiled> If we are precompiling it
    # <Return> TargetBuilder class
    @staticmethod
    def Create(StartingTarget, UsePrecompiled):

        # Read target by finding target name
        TargetReader = TargetBuilder.CreateTargetReaderFromTargetName(StartingTarget.Name, StartingTarget, StartingTarget.Project)

        # TODO: Add precompile support here

        # Create Target
        Ret = TargetBuilder(StartingTarget, TargetReader)

        # Run prebuild on new target
        Ret.SetupPreBuild()

        return Ret

    # Build's the target, uses binary class to compile the files
    # <Return> File Builder class
    def Build(self):

        # If we want to bake, do it here
        if self.StartingTarget.GonnaCook is True:
            self.StartCooker()

        BinOriginal = []

        #  Get build platform class
        Plat = Platform.Platform.GetBuildPlatform(self.StartingTarget.Platform)

        # Get CPP Platform
        CppPlat = Plat.DefaultCPPPlatform

        # Create CompileEnv and LinkEnv
        CompileEnv = CompileEnvironment.CompileEnvironment(CppPlat, self.BuildType, self.ArchToUse)
        LinkEnv = LinkEnvironment.LinkEnvironment(CompileEnv.Plat, CompileEnv.Conf, CompileEnv.Arch)

        # Create Toolchain
        Toolchain = self.CreateToolchain(CppPlat.value)

        # Append both settings for CompileEnv and LinkEnv
        self.AppendGlobalEnv(CompileEnv, LinkEnv)

        # NewCompileEnv = self.CreateProjectCompileEnv()

        # Create FileBuilder
        InFileBuilder = FileBuilder.FileBuilder()

        # FIXME: Add binary filter

        # FIXME: Add plugin support

        # FIXME: Add code here that will let exe know all modules included if using monolithic

        # FIXME: Add code that tells the exe where the engine dir is and put it in compile defines

        # FIXME: Add UObject support and generated code support

        # Get Exe Output Directory
        ExeOutputDir = self.GetExeDir()

        OutputItems = []

        # Compile each binary
        for Item in self.Binaries:
            BinOutput = Item.Build(self.Target, Toolchain, CompileEnv, LinkEnv, InFileBuilder)

        # FIXME: Add runtime depends support

        # FIXME: Add precompile Plugin support

        # FIXME: Add metadata support

        return InFileBuilder
