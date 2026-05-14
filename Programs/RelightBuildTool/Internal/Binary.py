from pathlib import Path
import os

from . import ModuleBuilder
from . import CompileEnvironment
from . import LinkEnvironment

from . import Logger

# Class representation of a binary, can be dynamic, static, or executable. This will help us manage, compile, and link environments


class Binary:

    Type = ""  # Can be EXE, Dynamic, or Static

    OutputDir = ""  # The directory for our output

    OutputFilePaths = []

    IntermediateDir = ""  # The directory all our modules will be compiled for

    LaunchModule = None  # This is our launch module, will always be included if the configs allow us to

    Modules = (
        []
    )  # List of modules we will use for this binary, should be ModuleBuilder class

    AdditionalLibs = []  # Cashe of additional libraries we will link to binary

    Precompiled = False # If Precompiled mode is activated

    def __init__(self, InType, InOutputFilePaths, InIntermediateDir, InLaunchModule, Precompiled):
        self.Type = InType
        self.OutputFilePaths = InOutputFilePaths
        self.IntermediateDir = InIntermediateDir
        self.LaunchModule = InLaunchModule
        self.Precompiled = Precompiled

        self.OutputDir = self.OutputFilePaths[0]
        self.Modules.append(self.LaunchModule)

    # Adds the module to list if it doesn't exist
    # <InModule> Module Reader
    def AddModule(self, InModule):
        if InModule not in self.Modules:
            self.Modules.append(InModule)

    # Returns the new Compile Environment that adds binary information from already existing compile environment
    # <OutputCompileEnv> The Compile Environment the new bin compile environment is based on
    # <Return> New compile environment
    def ReturnBinCompileEnv(self, OutputCompileEnv):

        CompileEnv = OutputCompileEnv

        # Set IsDynamic and IsLibrary based on binary type
        if self.Type == "Dynamic":
            CompileEnv.IsDynamic = True

        if self.Type == "Static":
            CompileEnv.IsLibrary = True

        return CompileEnv

    # return's true if the path is contained in the parent
    # <InPath> The path we will check
    # <InParent> The directory we will check InPath
    # <Return> True if path is contained in parent
    def IsUnderDir(InPath, InParent):
        try:
            InputPath = Path(InPath).resolve(strict=False)
            InputDirectory = Path(InParent).resolve(strict=False)

            if InputDirectory in InputPath.parents or InputPath == InputDirectory:
                return True

        except Exception:
            return False

    # Create's a link environment, we will compile each module associated with the binary
    # and put it in the InputFiles
    # <Target> The target file itself
    # <Toolchain> The toolchain to use
    # <LinkEnv> The link environment
    # <CompileEnv> The LinkEnv to use
    # <FileBuilder> The File Builder
    # <Return> The new link environment
    def CreateLinkEnv(self, Target, Toolchain, LinkEnv, CompileEnv, FileBuilder):

        NewLinkEnv = LinkEnvironment.LinkEnvironment()

        NewLinkEnv.Dup(LinkEnv)

        BinList = []

        NewCompileEnv = self.ReturnBinCompileEnv(CompileEnv)

        NewLinkEnv.AdditionalLibs.extend(CompileEnv.AdditionalLibs)

        # If project is not none and Project in Intermediate directory and we are using shared build environment, enable it in Compile Environment
        if Target._Project is not None and self.IsUnderDir(os.path.dirname(Target._Project), self.IntermediateDir) and NewCompileEnv.UseSharedBuildEnv is True:
            NewCompileEnv.UseSharedBuildEnv = False

        # For each module
        for ModuleBuilder in self.Modules:
            LinkFiles = []

            # Add additional libs from module to Link Environment
            NewLinkEnv.AdditionalLibs.extend(ModuleBuilder.Module.AdditionalLibs)

            # Compile Modules if binary is not set or is self
            if ModuleBuilder.Binary is None or ModuleBuilder.Binary == self:
                NewList = []

                # Compile via ModuleBuilder
                LinkFiles = ModuleBuilder.Compile(Target, Toolchain, NewCompileEnv, FileBuilder, NewList)

                # Sync Compile Environment to Link Environment
                NewLinkEnv.AdditionalLibs.extend(NewCompileEnv.AdditionalLibs)

                # For each item to link
                for LinkFilesItem in LinkFiles:

                    # If item is not in input files, Extend input files to contain Item
                    if LinkFilesItem not in NewLinkEnv.InputFiles:
                        NewLinkEnv.InputFiles.append(LinkFilesItem)

            else:
                BinList.append(Item.Binary)

            # Sync LinkEnv to Binary settings
            NewLinkEnv.OutputPaths = self.OutputFilePaths
            NewLinkEnv.IntermediateDir = self.IntermediateDir
            NewLinkEnv.OutputDir = self.OutputFilePaths[0]
            NewLinkEnv.LinkEnvPrecondition = CompileEnv.LinkEnvPrecondition  # Set's LinkEnv Precondition from the CompileEnv one

        return NewLinkEnv

    # Create the binary, mainly involves compiling and linking. Returns output files
    # <TargetReader> The target file itself
    # <Toolchain> The toolchain to compile
    # <CompileEnv> The compile environment
    # <LinkEnv> The link environment
    # <FileBuilder> The File Builder
    # <Return> All linked files
    def Build(self, TargetReader, Toolchain, CompileEnv, LinkEnv, FileBuilder):

        # If we are using precompile and we are linking files together, then return empty
        if self.Precompiled is True and TargetReader.LinkFilesTogether is True:
            return []

        # Create binary link environment
        BinLinkEnv = self.CreateLinkEnv(TargetReader, Toolchain, LinkEnv, CompileEnv, FileBuilder)

        # If we are not linking files together, then just return input files
        if TargetReader.LinkFilesTogether is False:
            return BinLinkEnv.InputFiles

        OutputFiles = []

        # Link files together
        Exes = Toolchain.LinkEveryFiles(BinLinkEnv, False, FileBuilder.ActionList)

        # TODO: Add ModuleNameToOutputItems FileBuilder function

        # For each linked file, apply PostBuilt to each binary and return the output file
        for Item in Exes:
            Temp = Toolchain.PostBuilt(Item, BinLinkEnv, FileBuilder.ActionList)
            OutputFiles.extend(Temp)

        return OutputFiles
