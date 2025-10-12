from enum import Enum


class Platform(Enum):
    Linux = "Linux"
    Windows = "Windows"


class PCHAction(Enum):
    Null = 0
    Include = 1
    Create = 2


class Output:
    ObjectFiles = []
    DebugFiles = []
    PCHFile = ""


# Configuration to compile source files into oject files
class CompileEnvironment:

    Plat = Platform  # The platform we are compiling

    Conf = None  # What debugging mode we will use

    PCH_Act = PCHAction.Null  # The action we will use for PCH files

    Out = Output  # All output info

    Arch = ""  # The CPU architecture

    SharedPCH = []  # The Precompiled Header file we will use globally

    PCHIncludeName = ""  # The name of the header file we will precompile

    UseSharedBuildEnv = False  # Create shared environment

    UseAVX = False  # If we should use Advanced Vector Extensions

    UseRTTI = False  # If we should use Run-Time Type Information

    UseInlining = False  # If we should use function inlining

    BufferSecurityChecks = True  # If we should use buffer security checks

    FalseUnityOverride = False  # Use if it's faster to not use UNITY system, will disable UNITY even if it's on

    MinUnitySource = 0  # The amount of files needed to enable Unity

    MinPCHSource = 0  # The amount of files needed before we use Precompiled Header

    BuildLocallySNDBS = False  # Build Locally when using SN-DBS

    ExceptionHandling = False  # If we should do Exception Handling

    ShadowVariableWarnings = True  # If we should give warnings about Shadow Variables

    ShadowVariableAsError = (
        False  # If we shall give an error if there's a shadow variable
    )

    UndefinedIdentifierWarnings = (
        True  # IF we should give warnings about Undefined Identifiers
    )

    UndefinedIdentifierAsError = (
        False  # If we shall give an error if there's an Undefined Identifiers
    )

    Optimize = False  # If true, we will optimize the binary

    OptimizeSize = False  # If true, we will optimize for smallest possible size

    AddDebugInfo = True  # If we should create Debug information

    IsLibrary = False  # If we are compiling static library (.a/.lib)

    IsDynamic = False  # If we are compiling dynamically (.so/.dll)

    UseStaticCRT = False  # If we should compile using statically-linked CRT

    UseDebugCRT = False  # If we should use Debug CRT

    ExcludeFramePointers = True  # If true, we shall not include frame pointers

    IncrementalLinking = True  # If true, we shall only link files that are updated

    AllowLTCG = False  # If we should use link time code generation

    PGOProfile = False  # If we should use Profile Guided Optimization Instrumentation

    PGOOptimize = False  # If we should optimize using Profile Guided Optimization

    PGODirectory = ""  # Directory where PGO is stored

    PGOFilePrefix = ""  # Filename where PGO is stored

    PrintTimingInfo = (
        False  # If true, we will log timing info from the compiler we are using
    )

    GenerateDependFile = (
        True  # If true, we shall Put Dependencies file along with output build products
    )

    AllowRemotelyCompiledPCHs = False  # If true, we shall let XGE compile PCH files externally, instead of locally

    UserIncPaths = []  # Included paths

    SysIncPaths = []  # Included System paths, will supress warnings

    CheckSysHeaderForChanges = (
        False  # If headers in SysIncPaths are modified, then the action is outdated
    )

    ForceIncFiles = []  # Paths to include no matter what

    Defines = []  # Definitions we will use across the engine

    AdditionalArgs = ""  # Any additional arguments we will use

    AdditionalFrameworks = []  # Any additional Frameworks we will use

    PCHFile = None  # The Precompiled Header file

    UsingRHT = False  # If we are using Relight Header Tool

    HideSymbols = False  # If we should hide Symbols by default

    LinkEnvPrecondition = (
        []
    )  # Fixes a bug, this will put any Precondition from CompileEnv to LinkEnv

    CopyIncToIntermediate = False

    # Quick HACK Here just to sync with LinkEnv
    AdditionalLibs = []

    def __init__(self, InPlatform, InConfig, InArch):
        self.Plat = InPlatform

        self.Conf = InConfig

        self.Arch = InArch

        self.SharedPCH = []

        self.UserIncPaths = []

        self.SysIncPaths = []

    def Dup(self, Second):
        self.Plat = Second.Plat
        self.Conf = Second.Conf
        self.PCH_Act = Second.PCH_Act
        self.Out = Second.Out
        self.Arch = Second.Arch
        self.SharedPCH = Second.SharedPCH
        self.PCHIncludeName = Second.PCHIncludeName
        self.UseSharedBuildEnv = Second.UseSharedBuildEnv
        self.UseAVX = Second.UseAVX
        self.UseRTTI = Second.UseRTTI
        self.UseInlining = Second.UseInlining
        self.BufferSecurityChecks = Second.BufferSecurityChecks
        self.FalseUnityOverride = Second.FalseUnityOverride
        self.MinUnitySource = Second.MinUnitySource
        self.MinPCHSource = Second.MinPCHSource
        self.BuildLocallySNDBS = Second.BuildLocallySNDBS
        self.ExceptionHandling = Second.ExceptionHandling
        self.ShadowVariableWarnings = Second.ShadowVariableWarnings
        self.ShadowVariableAsError = Second.ShadowVariableAsError
        self.UndefinedIdentifierWarnings = Second.UndefinedIdentifierWarnings
        self.UndefinedIdentifierAsError = Second.UndefinedIdentifierAsError
        self.Optimize = Second.Optimize
        self.OptimizeSize = Second.OptimizeSize
        self.AddDebugInfo = Second.AddDebugInfo
        self.IsLibrary = Second.IsLibrary
        self.IsDynamic = Second.IsDynamic
        self.UseStaticCRT = Second.UseStaticCRT
        self.UseDebugCRT = Second.UseDebugCRT
        self.ExcludeFramePointers = Second.ExcludeFramePointers
        self.incrementalLinking = Second.incrementalLinking
        self.AllowLTCG = Second.AllowLTCG
        self.PGOProfile = Second.PGOProfile
        self.PGOOptimize = Second.PGOOptimize
        self.PGODirectory = Second.PGODirectory
        self.PGOFilePrefix = Second.PGOFilePrefix
        self.PrintTimingInfo = Second.PrintTimingInfo
        self.GenerateDependFile = Second.GenerateDependFile
        self.AllowRemotelyCompiledPCHs = Second.AllowRemotelyCompiledPCHs
        self.UserIncPaths = Second.UserIncPaths
        self.SysIncPaths = Second.SysIncPaths
        self.CheckSysHeaderForChanges = Second.CheckSysHeaderForChanges
        self.ForceIncFiles = self.ForceIncFiles + Second.ForceIncFiles
        self.Defines = self.Defines + Second.Defines
        self.AdditionalArgs = Second.AdditionalArgs
        self.AdditionalFrameworks = self.AdditionalArgs + Second.AdditionalArgs
        self.PCHFile = Second.PCHFile
        self.UsingRHT = Second.UsingRHT
        self.HideSymbols = Second.DefaultHideSymbols
        self.LinkEnvPrecondition = Second.LinkEnvPrecondition
