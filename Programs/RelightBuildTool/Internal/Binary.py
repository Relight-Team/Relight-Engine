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

    ExportLibs = False  # If true, we will export lib

    Precompiled = False  # If Precompiled mode is activated

    AdditionalLibs = []  # Cashe of additional libraries we will link to binary

    def __init__(
        self,
        InType,
        InOutputFilePaths,
        InIntermediateDir,
        InLaunchModule,
        InExportLibs,
        InPrecompiled,
    ):
        self.Type = InType
        self.OutputFilePaths = InOutputFilePaths
        self.IntermediateDir = InIntermediateDir
        self.LaunchModule = InLaunchModule
        self.ExportLibs = InExportLibs
        self.Precompiled = InPrecompiled

        self.OutputDir = self.OutputFilePaths[0]
        self.Modules.append(self.LaunchModule)

    # Create all modules in the list
    def CreateModules(self, FuncName):

        for Item in self.Modules:
            Item.CreateModule(FuncName, "Target")

    # Adds the module to list if it doesn't exist
    def AddModule(self, InModule):
        if InModule not in self.Modules:
            self.Modules.append(InModule)

    # Returns the new Compile Environment that adds binary information from already existing compile environment
    def ReturnBinCompileEnv(self, OutputCompileEnv):

        CompileEnv = OutputCompileEnv

        if self.Type == "Dynamic":
            CompileEnv.IsDynamic = True

        if self.Type == "Static":
            CompileEnv.IsLibrary = True

        return CompileEnv

    # return's true if the path is contained in the parent
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
    def CreateLinkEnv(
        self, Target, Toolchain, LinkEnv, CompileEnv, ExeDir, FileBuilder
    ):

        NewLinkEnv = LinkEnvironment.LinkEnvironment()

        NewLinkEnv.Dup(LinkEnv)

        LinkEnvModuleList = []

        BinList = []

        NewCompileEnv = self.ReturnBinCompileEnv(CompileEnv)

        NewLinkEnv.AdditionalLibs.extend(CompileEnv.AdditionalLibs)

        if (
            Target._Project is not None
            and self.IsUnderDir(os.path.dirname(Target._Project), self.IntermediateDir)
            and NewCompileEnv.UseSharedBuildEnv is True
        ):
            NewCompileEnv.UseSharedBuildEnv = False

        for Item in self.Modules:
            LinkFiles = []

            NewLinkEnv.AdditionalLibs.extend(Item.Module.AdditionalLibs)

            # Compile Modules
            if Item.Binary is None or Item.Binary == self:
                NewList = []

                # Compile via ModuleBuilder
                LinkFiles = Item.Compile(
                    Target, Toolchain, NewCompileEnv, FileBuilder, NewList
                )  # Compile Module

                NewLinkEnv.AdditionalLibs.extend(NewCompileEnv.AdditionalLibs)

                for LinkFilesItem in LinkFiles:

                    if LinkFilesItem not in NewLinkEnv.InputFiles:
                        # Extend InputFiles in LinkEnv to LinkFiles
                        NewLinkEnv.InputFiles.append(LinkFilesItem)

            else:

                BinList.append(Item.Binary)

            NewLinkEnv.OutputPaths = self.OutputFilePaths
            NewLinkEnv.IntermediateDir = self.IntermediateDir
            NewLinkEnv.OutputDir = self.OutputFilePaths[0]
            NewLinkEnv.LinkEnvPrecondition = (
                CompileEnv.LinkEnvPrecondition
            )  # Set's LinkEnv Precondition from the CompileEnv one

        return NewLinkEnv

    # Create the binary, mainly involves compiling and linking. Returns output files
    def Build(self, TargetReader, Toolchain, CompileEnv, LinkEnv, ExeDir, FileBuilder):

        if self.Precompiled is True and TargetReader.LinkFilesTogether is True:
            return []

        BinLinkEnv = self.CreateLinkEnv(
            TargetReader, Toolchain, LinkEnv, CompileEnv, ExeDir, FileBuilder
        )

        if TargetReader.LinkFilesTogether is False:
            return BinLinkEnv.InputFiles

        OutputFiles = []

        Exes = Toolchain.LinkEveryFiles(BinLinkEnv, False, FileBuilder.ActionList)

        # TODO: Add ModuleNameToOutputItems FileBuilder function

        for Item in Exes:
            Temp = Toolchain.PostBuilt(Item, BinLinkEnv, FileBuilder.ActionList)
            OutputFiles.extend(Temp)

        return OutputFiles
