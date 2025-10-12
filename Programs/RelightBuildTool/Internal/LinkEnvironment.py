from . import CompileEnvironment as CE


# Configuration to link all objects file into the final binary file
class LinkEnvironment:

    Platform = None  # The platform we are compiling

    Config = None  # The config we are compiling

    Arch = ""  # The arch we are borrowing

    BundleDir = ""  # Bundle software path on MacOS

    OutputDir = ""  # The directory that will store non-binary data in

    IntermediateDir = ""  # The intermediate directory

    LocalShadowDir = None  # The local shadow directory, this directory serves as a temp directory of source files, mainly used when linking via mutliple servers

    OutputPaths = (
        []
    )  # The full output binary files and it's path that this linker will produce

    LibraryPaths = []  # Paths to search for libraries

    ExcludeLibs = []  # Libraries we will not link

    AdditionalLibs = []  # Additional Libraries we will link

    RuntimeLibPaths = []  # Paths to search for Runtime Libraries

    AdditionalFrameworks = []  # Additional framworks to link

    AdditionalBundlesRes = []  # Additional bundles to link

    DelayLoadDynamics = (
        []
    )  # A list of "Delayed Load Dynamics". These are Dynamic libraries that will not load into the software until they are first called

    AdditionalArgs = ""  # Additional arguments to pass

    AddDebugInfo = True  # If we should create debug information

    DisableSymbolCashe = False  # If true, we shall not create cached symbols

    IsBuildingLibrary = (
        False  # If true, then we are linking to a static Library (.a, .lib, etc)
    )

    IsBuildingDynamic = (
        False  # If true, then we are linking to a dynamic Library (.so, .dll, etc)
    )

    IsTerminalSoftware = False  # TODO: Do we even need this? Unlike The parent reference, RBT doesn't care if the software is terminal or not, might remove this

    DefaultStackSize = 5000000  # Default memory size allocation

    OptimizeSize = False  # If True, the software will be optimize for size

    ExcludeFramePointers = True  # If true, we will not include frame pointers

    IncrementalLinking = False  # If true, then we will use Incremental Linking. A system which modifies the Output executable instead of rebuilding everything from scratch

    AllowLTCG = False  # If true, then we will use LTCG (Link Time Code Generation)

    PGOProfile = (
        False  # If true, then we will use PGO Profile (Profile Guided Optimization)
    )

    PGOOptimize = False  # If true, then we will use PGO Optimize

    PGODirectory = ""  # Directory that PGO Profiling will be saved

    PGOFilePrefix = ""  # file prefix for the PGO Profiling, usually platform specific

    CreateMapFile = False  # If true, we will attempt to create map file, which stores detailed overview about the linker

    AllowASLR = (
        False  # If true, we will attempt ASLR (address space layout randomization)
    )

    UseFastPDBLinking = False  # If we should use Fast PDB when linking

    PrintTimingInfo = False  # Print Timing info when linking

    InputFiles = []  # A list of files that will be linked

    InputLibs = []  # # Libraries we will link

    DefaultResFiles = []  #

    GlobalResFiles = []  #

    IncFunctions = []  #

    DefineFiles = []  # Files that contains definitions

    AdditionalProperty = []  # Additional Properties

    CrossedReference = False  #

    LinkEnvPrecondition = (
        []
    )  # Fixes a bug, this will put any Precondition from CompileEnv to LinkEnv

    def __init__(self, InPlatform=None, InConfig=None, InArch=None):
        self.Platform = InPlatform
        self.Config = InConfig
        self.Arch = InArch

    # combine all values to a second LinkEnvironment, Prioritizes second LinkEnv
    def Dup(self, Second):
        self.Platform = Second.Platform
        self.Config = Second.Config
        self.Arch = Second.Arch
        self.BundleDir = Second.BundleDir
        self.OutputDir = Second.OutputDir
        self.IntermediateDir = Second.IntermediateDir
        self.LocalShadowDir = Second.LocalShadowDir
        self.OutputPaths = self.OutputPaths + Second.OutputPaths
        self.LibraryPaths = self.LibraryPaths + Second.LibraryPaths
        self.ExcludeLibs = self.ExcludeLibs + Second.ExcludeLibs
        self.AdditionalLibs = self.AdditionalLibs + Second.AdditionalLibs
        self.RuntimeLibPaths = self.RuntimeLibPaths + Second.RuntimeLibPaths
        self.AdditionalFrameworks = (
            self.AdditionalFrameworks + Second.AdditionalFrameworks
        )
        self.AdditionalBundlesRes = (
            self.AdditionalBundlesRes + Second.AdditionalBundlesRes
        )
        self.DelayLoadDynamics = self.DelayLoadDynamics + Second.DelayLoadDynamics
        self.AdditionalArgs = Second.AdditionalArgs
        self.AddDebugInfo = Second.AddDebugInfo
        self.DisableSymbolCashe = Second.DisableSymbolCashe
        self.IsBuildingLibrary = Second.IsBuildingLibrary
        self.IsBuildingDynamic = Second.IsBuildingDynamic
        self.IsTerminalSoftware = Second.IsTerminalSoftware
        self.DefaultStackSize = Second.DefaultStackSize
        self.OptimizeSize = Second.OptimizeSize
        self.ExcludeFramePointers = Second.ExcludeFramePointers
        self.IncrementalLinking = Second.IncrementalLinking
        self.AllowLTCG = Second.AllowLTCG
        self.PGOProfile = Second.PGOProfile
        self.PGOOptimize = Second.PGOOptimize
        self.PGODirectory = Second.PGODirectory
        self.PGOFilePrefix = Second.PGOFilePrefix
        self.CreateMapFile = Second.CreateMapFile
        self.AllowASLR = Second.AllowASLR
        self.UseFastPDBLinking = Second.UseFastPDBLinking
        self.PrintTimingInfo = Second.PrintTimingInfo
        self.InputFiles = self.InputFiles + Second.InputFiles
        self.InputLibs = self.InputLibs + Second.InputLibs
        self.DefaultResFiles = self.DefaultResFiles + Second.DefaultResFiles
        self.GlobalResFiles = self.GlobalResFiles + Second.GlobalResFiles
        self.IncFunctions = self.IncFunctions + Second.IncFunctions
        self.DefineFiles = self.DefineFiles + Second.DefineFiles
        self.AdditionalProperty = self.AdditionalProperty + Second.AdditionalProperty
        self.CrossedReference = Second.CrossedReference

    def OutputFilePath(self):
        if len(self.OutputPaths) == 1:
            return self.OutputPaths[0]
        else:
            raise ValueError(
                "OutputPaths must only have 1 item when attempting to run LinkEnvironment.OutputFilePaths(), the count we detected is "
                + str(len(self.OutputPaths))
            )
