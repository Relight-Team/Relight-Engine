import sys
import os

from Readers import ModuleReader

from Environments import CompileEnvironment

from Builders import FileBuilder

from Internal import Logger

from Internal import Unity

from Configuration import Directory_Manager


# Build's a module
class ModuleBuilder:

    def __init__(self, InModule, InIntermediateDir, TargetReader, StartingTarget, BuildType):
        self.Module = InModule
        self.IntermediateDir = InIntermediateDir
        self.TargetReader = TargetReader
        self.StartingTarget = StartingTarget
        self.BuildType = BuildType

        # HACK fix: if module is engine and isn't unique, then we will always set intermediate to engine dir
        if self.Module.IsEngineModule is True and self.TargetReader.IntermediateType != "Unique":
            self.IntermediateDir = os.path.join(Directory_Manager.Engine_Directory, "Intermediate")

        self.SourceDir = os.path.join(self.Module.ModuleDirectory, "Src")

    # Get all files in source
    # <Return> an array of every file in the Source Directory
    def GetInfoFiles(self):
        Ret = []

        # For each file in source directory, we will return it
        for Dirpath, _, filenames in os.walk(self.SourceDir):
            for f in filenames:
                Ret.append(os.path.abspath(os.path.join(Dirpath, f)))

        return Ret

    # Get all input files, sort them between Compile, Header, and Generated file
    def SortLists(self):

        Temp = self.GetInfoFiles()

        for Item in Temp:
            Extension = os.path.splitext(Item)[1]

            # Add c/cpp files in CompileFiles
            if Extension == ".cpp".lower() or Extension == ".c".lower():
                self.CompileFiles.append(Item)

            # Add h/hpp files in HeaderFiles
            elif Extension == ".h".lower() or Extension == ".hpp".lower():
                self.HeaderFiles.append(Item)

            # Always add file in AllFiles
            self.AllFiles.append(Item)

    # Return's a new Compile Environment, set's up new compile environment based on Module settings
    # <CompileEnv> The old compile environment
    # <Return> New Compile environment
    def CreateCompileEnv(self, CompileEnv):
        NewCompile = CompileEnv

        NewCompile.FalseUnityOverride = self.Module.DisableUnity
        NewCompile.UseRTTI |= self.Module.RTTI
        NewCompile.UseAVX = self.Module.AVX

        NewCompile.Defines.extend(self.Module.Defines)

        NewCompile.AdditionalLibs.extend(self.Module.AdditionalLibs)

        NewCompile.UserIncPaths.extend(self.Module.Includes)

        return NewCompile

    # Returns the full file path and file if file exist in directory, return's None otherwise
    # <Dir> The full directory to search in
    # <File> The file to seach for
    # <Return> The full dir and file if it exists, None otherwise
    def SearchThroughDir(self, Dir, File):
        for Root, SubDirList, Files in os.walk(Dir):
            if File in Files:
                return os.path.join(Root, File)
        return None

    # Finds the .Build file
    # <TargetReader> The target file itself
    # <ModuleName> The module name to search for
    def FindModuleReaderFile(self, TargetReader, ModuleName):

        SearchModule = os.path.join(os.path.basename(ModuleName) + ".Build")

        # First, check the project/Target directory itself
        if TargetReader._Project is not None:
            DirCheck = os.path.dirname(TargetReader._Project)
            FullDir = os.path.join(DirCheck, "Src")
        else:
            DirCheck = os.path.dirname(TargetReader.FilePath)
            FullDir = DirCheck

        # Scan if the module file exist
        SubDir = self.SearchThroughDir(FullDir, SearchModule)

        # If we cannot find it, then it's most likely in the Engine Directory
        if SubDir is None:
            DirCheck = Directory_Manager.Engine_Directory

            FullDir = os.path.join(DirCheck)
            SubDir2 = self.SearchThroughDir(FullDir, SearchModule)

            # If this still fails, we shall give an error
            if SubDir2 is None:
                Logger.Logger(5, "We could not find Module " + SearchModule + " in either ProjectDir, TargetDir, and EngineDir, please check your modules and try again!")
            else:
                return SubDir2 # Return engine module
        else:
            return SubDir # Return project module

    def IfListInSecondList(self, List1, List2):

        Ret = all(Item in List1 for Item in List2)

        return Ret

    # Recursively Run the Compile for each Modules
    # <InModuleBuilder> The module builder to run
    # <TargetReader> The target file itself
    # <InToolchain> The toolchain to use
    # <BinCompileEnv> The compile environment that we will use
    # <FileBuilder> The file builder class
    # <AlreadyBuiltModulesList> The list of all modules we already built
    def GetAndCompileDependencies(self, InModuleBuilder, TargetReader, InToolchain, BinCompileEnv, FileBuilder, AlreadyBuiltModulesList):

        # Set include directory to module source
        BinCompileEnv.UserIncPaths.append((os.path.join(os.path.dirname(self.Module.FilePath), "Src")))

        # If module have module dependencies
        if InModuleBuilder.Module.Modules:

            # For each dependencies
            for Item in InModuleBuilder.Module.Modules:

                # Find the Module and read it
                FilePathName = self.FindModuleReaderFile(TargetReader, Item)
                SubModuleReader = ModuleReader.Module(FilePathName, self.StartingTarget)

                # If module hasn't already been built
                if FilePathName not in AlreadyBuiltModulesList:

                    # Add it to already built module list
                    AlreadyBuiltModulesList.append(FilePathName)

                    # Create module builder for the dependency
                    NewModuleBuilder = ModuleBuilder(SubModuleReader, self.IntermediateDir, self.TargetReader, self.StartingTarget, self.BuildType)

                    # Get and compile the dependency's dependincies
                    self.GetAndCompileDependencies(NewModuleBuilder, TargetReader, InToolchain, BinCompileEnv, FileBuilder, AlreadyBuiltModulesList)

                    # Compile the module
                    NewModuleBuilder.Compile(TargetReader, InToolchain, BinCompileEnv, FileBuilder, AlreadyBuiltModulesList)

    # Copy all header files to intermediate
    # <Plat> The platform we will compile to
    # <TargetReader> The target file itself
    # <ModName> The module name
    def CopyIncToIntermed(self, Plat, TargetReader, ModName):

        # The path to the module we will put our includes in
        IncludeIntermediatePath = os.path.join(self.IntermediateDir, "Build", str(Plat.value), TargetReader.Arch, TargetReader.Name, "Inc", ModName)

        # For each header file
        for HeaderFileSource in self.HeaderFiles:

            # Get the local path between full source directory and Header
            RelPath = os.path.relpath(HeaderFileSource, self.SourceDir)

            # Get directory of Header
            Directory = os.path.dirname(RelPath)

            # If directory exists, we will make directory, else we will just make parent include directory
            if Directory is not None and Directory != "":
                os.makedirs(os.path.join(IncludeIntermediatePath, Directory), exist_ok=True)
            else:
                os.makedirs(IncludeIntermediatePath, exist_ok=True)

            # If include file does n't exist, then copy it
            # TODO: Add support to Windows
            if not os.path.exists(os.path.join(IncludeIntermediatePath, RelPath)):
                Logger.Logger(3, "cp " + HeaderFileSource + " " + os.path.join(IncludeIntermediatePath, RelPath))
                os.system("cp " + HeaderFileSource + " " + os.path.join(IncludeIntermediatePath, RelPath))

    # Compile's the Module
    # <TargetReader> The Target file itself
    # <InToolchain> The toolchain to use
    # <BinCompileEnv> The binary compile environment
    # <FileBuilder> A File Builder
    # <AlreadyBuiltModulesList> A list of modules we have already built
    # <Return> List of all compiled objects to link
    def Compile(self, TargetReader, InToolchain, BinCompileEnv, FileBuilder, AlreadyBuiltModulesList):
        self.CompileFiles = []
        self.HeaderFiles = []
        self.AllFiles = []

        Plat = BinCompileEnv.Plat

        LinkArray = []

        # Create new compile environment that matches settings from module reader
        NewCompileEnv = self.CreateCompileEnv(BinCompileEnv)

        # Create and sort CompileFiles, HeaderFiles, and AllFiles lists
        self.SortLists()

        # Compile 3rd party modules
        Logger.Logger(1, "Start Collecting Third Party dependencies for " + self.Module.Name)

        # For each third party in module
        for ThirdParty in self.Module.ThirdParty:
            Logger.Logger(3, "Searching for third party module: " + ThirdParty)

            # Find the Module file for the third party
            ThirdPartyFile = self.FindModuleReaderFile(TargetReader, ThirdParty)

            Logger.Logger(1, "File found: " + ThirdPartyFile)

            # Read the third party module and create external builder
            ThirdPartyReader = ModuleReader.Module(ThirdPartyFile, self.StartingTarget)
            ThirdPartyBuilder = ExternalBuilder(ThirdPartyReader, self.IntermediateDir, TargetReader)

            # Get all additional libraries from third party and put it in compiled objects list and Compile Environment's additional lib's list
            AdditionalLibs = ThirdPartyBuilder.Compile()
            LinkArray.extend(AdditionalLibs)
            NewCompileEnv.AdditionalLibs.extend(AdditionalLibs)

            # Add Third party Includes and SysIncludes to NewCompileEnb
            NewCompileEnv.UserIncPaths.extend(ThirdPartyReader.Includes)
            NewCompileEnv.SysIncPaths.extend(ThirdPartyReader.SysIncludes)

        Dict_SourceFiles = {}
        InputFiles = self.GetInfoFiles()

        # Get and compile each dependency in this module
        self.GetAndCompileDependencies(self, TargetReader, InToolchain, BinCompileEnv, FileBuilder, AlreadyBuiltModulesList)

        SourceFile_Unity = {}

        EveryFileToCompile = []

        # TODO: Add GenFIles here for when we create HeaderTool
        GenFiles = []

        # Check if we should be using Unity
        UsingUnity = False

        CppFilesForUnity = []

        SourceFileCount = 0

        MaxFileCount = 0

        # Check if we should use the max file count from module or target
        if self.Module.ModuleUnityMinSourceFiles < 0:
            MaxFileCount = self.Module.ModuleUnityMinSourceFiles
        else:
            MaxFileCount = TargetReader.UnityMinSourceFiles

        # Collect each file in sourcedir, if it's a cpp file, add it to CppFilesForUnity and count that file
        if TargetReader.Unity is True:
            for Root, Subdirlist, FileList in os.walk(self.SourceDir):
                for File in FileList:
                    if File.endswith(".cpp"):
                        CppFilesForUnity.append(os.path.join(Root, File))
                        SourceFileCount += 1

        # if the cpp file count is or over the max file, and the module allows us, then we can use unity
        if SourceFileCount >= MaxFileCount:
            if self.Module.DisableUnity is False and TargetReader.Unity is True:
                Logger.Logger(3, "Using UNITY System")
                UsingUnity = True

        # Add compiled files and generated files to every file to compile
        EveryFileToCompile.extend(self.CompileFiles)
        EveryFileToCompile.extend(GenFiles)

        OutputActionList = []

        # Either set Name or Object Name
        if self.Module.ObjectName == None or self.Module.ObjectName == "":
            ModName = self.Module.Name
        else:
            ModName = self.Module.ObjectName

        # If module doesn't have name, result in error
        if ModName == None:
                Logger.Logger(5, "Module Name and/or Module Short Name is None, we cannot continue! Module Name: (" + str(self.Module.Name) + "), Module Short Name: (" + str(self.Module.ObjectName)+ ")")
        if ModName == "":
            Logger.Logger(5, "Module Name and/or Module Short Name is empty, we cannot continue! Module Name: (" + str(self.Module.Name) + "), Module Short Name: (" + str(self.Module.ObjectName) + ")")


        # Set intermediate directory for module
        Intermed = os.path.join(self.IntermediateDir, "Build", str(Plat.value), TargetReader.Arch, TargetReader.Name, self.BuildType, ModName)

        # Copy header files to intermeidate if we are allowed to
        if NewCompileEnv.CopyIncToIntermediate is True:
            self.CopyIncToIntermed(Plat, TargetReader, ModName)

        # QUICK HACK: If we are using shared module and the module is engine, then change the intermediate to engine
        if self.Module.IsEngineModule is True and TargetReader.IntermediateType == "Shared":
            Intermed = os.path.join(Directory_Manager.Engine_Directory, "Intermediate", "Build", str(Plat.value), TargetReader.Arch, TargetReader.Name, self.BuildType, ModName)
            self.IntermediateDir = os.path.join(Directory_Manager.Engine_Directory, "Intermediate")

        # If we are not using precompiled, then just compile everything
        if TargetReader.Precompiled is False:

            # If using UNITY, then run Unite function
            if UsingUnity is True:
                LinkArray.extend(Unity.Unity.UniteCPPFiles(CppFilesForUnity, NewCompileEnv, InToolchain, Intermed, OutputActionList, ModName,))

            # If not using UNITY, then compile CPP for module
            else:
                LinkArray.extend(InToolchain.CompileMultiArchCPPs(NewCompileEnv, EveryFileToCompile, Intermed, OutputActionList))

        # else if it's precompiled
        else:
            # If it's an engine module, then collect all object files
            if self.Module.IsEngineModule is True:
                PrecompiledList = []  # All object files in the precompiled directory

                for Root, SubFolderList, Files in os.walk(Intermed):
                    for File in Files:
                        if File.endswith(".o") or File.endswith(".obj"):
                            PrecompiledList.append(os.path.join(Root, File))

                # If precompiled list is empty, warn user
                if not PrecompiledList:
                    Logger.Logger(4, "Warning: Precompiled engine code not found, continuing, but errors might occur!")

                LinkArray.extend(PrecompiledList)

                IncPath = os.path.join(self.IntermediateDir, "Build", str(Plat.value), TargetReader.Arch, TargetReader.Name, "Inc", ModName)

                NewCompileEnv.UserIncPaths.append(IncPath)

            # If the module is not an engine and it's precompiled mode, compile it as normal
            else:
                # Switch between UNITY and Each CPP mode
                if UsingUnity is True:
                    LinkArray.extend(Unity.Unity.UniteCPPFiles(CppFilesForUnity,NewCompileEnv, InToolchain, Intermed, OutputActionList, ModName))
                else:
                    LinkArray.extend(InToolchain.CompileMultiArchCPPs(NewCompileEnv, EveryFileToCompile, Intermed, OutputActionList))

        # Set action list in FileBuilder to OutputActionList
        FileBuilder.ActionList.extend(OutputActionList)

        # BUGFIX: Clear input files, so that if we are compiling multiple modules, it won't add extra to different Intermediate
        self.CompileFiles = []

        return LinkArray


# Used for third party
class ExternalBuilder(ModuleBuilder):

    # Module reader
    Module = None

    AllFiles = []
    CompileFiles = []
    HeaderFiles = []

    IntermediateDir = ""
    SourceDir = ""  # Directory for Module/Src
    TargetReader = None

    def __init__(self, InModule, InIntermediateDir, TargetReader):
        self.Module = InModule
        self.IntermediateDir = os.path.join(InIntermediateDir, "ThirdParty")
        self.TargetReader = TargetReader

        # HACK fix: if module is engine and isn't unique, then we will always set intermediate to engine dir
        if self.Module.IsEngineModule is True and self.TargetReader.IntermediateType != "Unique":
            self.IntermediateDir = os.path.join(Directory_Manager.Engine_Directory, "Intermediate", "ThirdParty")

        self.SourceDir = os.path.dirname(self.Module.FilePath)

    # Compile a third party library
    # <Return> Additional libraries from Third Party
    def Compile(self):

        # If AlwaysCompileThirdParty is false, we don't need to compile
        if self.TargetReader.AlwaysCompileThirdParty is False:
            return self.Module.AdditionalLibs

        # Run 3rd party script
        for Command in self.Module.CommandToRun:
            os.system(Command)

        return self.Module.AdditionalLibs
