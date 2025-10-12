import os
import platform
import sys
import subprocess

from . import PlatformSDK


from Internal import LinkEnvironment as LE


class ToolchainSDK:

    CppPlatform = ""

    def __init__(self, CppPlat):
        CppPlatform = CppPlat

    # Returns the version info
    def ReturnVerInfo():
        return ""

    # Compile the inputted C++ files
    def CompileFiles(self, CompileEnv, InputFiles, OutDir, OutputActionList):
        pass  # Will be overwritten with child class

    # FIXME: This isn't complete, as a placeholder just returns CompileCPPs, please replace!
    # CompileCPPs for multi-arch compiles
    def CompileMultiArchCPPs(self, CompileEnv, InputFiles, OutputDir, OutputActionList):
        return self.CompileFiles(CompileEnv, InputFiles, OutputDir, OutputActionList)

    # Compiles the inputted RCF files
    def CompileRCFs(CompileEnv, InputFiles, OutDir, OutputActionList):
        pass  # TODO: Make this return new instance of CppOutput

    # Link files in the LinkEnvironment
    def LinkFiles(LinkEnv, LibraryImportOnly, OutputActionList):
        pass  # Will be overwritten with child class

    # Link every file in the LinkEnvironment
    def LinkEveryFiles(self, LinkEnv, BuiltLibraryImportOnly, ActionList):
        FileList = []

        FileList.append(self.LinkFiles(LinkEnv, BuiltLibraryImportOnly, ActionList))

        return FileList

    # Return's the actions to do after building
    def PostBuilt(self, File, LinkEnv, ActionList):
        Temp = []

        return Temp

    # Setup global environment
    def SetGlobalEnv(self, Target):
        pass  # Will be overwritten with child class

    # Modify the build
    def ModifyBuild(Target, Binary, LibrariesList, BuildResList, BuildProductList):
        pass  # Will be overwritten with child class

    # Actions to finish the output
    def FinishOutput(Target, FileBuilder):
        pass  # Will be overwritten with child class

    # Return's true if we should add debug information
    def ShouldAddDebug(File, BuildType):
        return True

    # Setup the Bundle Dependencies
    def SetBundleDepend(Binary, SoftwareName):
        pass  # Will be overwritten with child class

    # Return's the SDK Version
    def ReturnSDKVersion():
        return "None"
