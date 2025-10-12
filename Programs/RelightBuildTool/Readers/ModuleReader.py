import os
import sys

from Internal import Core as C


class Module:

    # The name of the module
    Name = ""

    # The name of the object, mainly should be used for long module names
    ObjectName = ""

    # The description of the module, mainly used for documentation and debugging
    Description = ""

    # The type of module, can either be Internal or External (Internal: Relight-based project. External: 3rd-party project)
    Type = ""

    # The list of dependencies this module requires
    Modules = []

    # Names of Modules we will include
    ModulesIncludes = []

    # All directories we will include
    Includes = []

    # includes that act like system (might be used by some 3rd party
    SysIncludes = []

    # Defines for this specific module
    Defines = []

    # Directories to search for dynamic libraries
    DynamicModulePaths = []

    # Static libraries for 3rd parties
    Static3rdParty = []

    # Third party, will be added to Static3rdParty and Includes
    ThirdParty = []

    # What level of optimization we should use, less optimization = faster compiling and debugging, but bigger file size
    Optimization = "Default"

    # If true, we will not use UNITY system on this module, even if the target/project file allows UNITY
    DisableUnity = False

    # if we should use RTTI (run time type information)
    RTTI = False

    # if we should use AVX instructions
    AVX = False

    # If true, then we will automatically append Includes to have Modules, you will have to manually do it if false
    AutoIncludeModules = True

    # If true, we will treat it as a engine module (put module in engine dir instead of project dir)
    IsEngineModule = False

    # The amount of source files needed to use Unity files, will override Target. Leave number negative to disable override, requires Unity to be true in target
    ModuleUnityMinSourceFiles = -1

    # -- Read Only -- #

    # The entire file path (Dir1/Dir2/Example.Module)
    FilePath = ""

    # The directory to the file (Dir1/Dir2/)
    ModuleDirectory = ""

    # -- Third Party -- #

    AdditionalLibs = []  # Additional Libraries to append

    CommandToRun = []  # The command to run for third party

    def __init__(self, BuildFile, StartingTarget):

        self.FilePath = BuildFile

        self.ModuleDirectory = os.path.dirname(self.FilePath)

        C.ChangeVar(StartingTarget, self)

        # Set public variables

        self.Name = C.GetVar(BuildFile, "Name", self.Name)
        self.ObjectName = C.GetVar(BuildFile, "ObjectName", self.ObjectName)
        self.Description = C.GetVar(BuildFile, "Description", self.Description)
        self.Type = C.GetVar(BuildFile, "Type", self.Type)
        self.Modules = C.GetVar(BuildFile, "Modules", self.Modules)
        self.ModulesIncludes = C.GetVar(
            BuildFile, "ModulesIncludes", self.ModulesIncludes
        )
        self.Includes = C.GetVar(BuildFile, "Includes", self.Includes)
        self.SysIncludes = C.GetVar(BuildFile, "SysIncludes", self.SysIncludes)
        self.Defines = C.GetVar(BuildFile, "Defines", self.Defines)
        self.DynamicModulePaths = C.GetVar(
            BuildFile, "DynamicModulePaths", self.DynamicModulePaths
        )
        self.Static3rdParty = C.GetVar(BuildFile, "Static3rdParty", self.Static3rdParty)
        self.ThirdParty = C.GetVar(BuildFile, "ThirdParty", self.ThirdParty)
        self.Optimization = C.GetVar(BuildFile, "Optimization", self.Optimization)
        self.DisableUnity = C.GetVar(BuildFile, "DisableUnity", self.DisableUnity)
        self.RTTI = C.GetVar(BuildFile, "RTTI", self.RTTI)
        self.AVX = C.GetVar(BuildFile, "AVX", self.AVX)
        self.AutoIncludeModules = C.GetVar(
            BuildFile, "AutoIncludeModules", self.AutoIncludeModules
        )
        self.IsEngineModule = C.GetVar(BuildFile, "IsEngineModule", self.IsEngineModule)
        self.ModuleUnityMinSourceFiles = C.GetVar(
            BuildFile, "ModuleUnityMinSourceFiles", self.ModuleUnityMinSourceFiles
        )
        self.AdditionalLibs = C.GetVar(BuildFile, "AdditionalLibs", self.AdditionalLibs)
        self.CommandToRun = C.GetVar(BuildFile, "CommandToRun", self.CommandToRun)
