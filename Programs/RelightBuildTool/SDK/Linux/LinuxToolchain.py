import importlib
import os
import re
import subprocess
import sys
import platform

from . import LinuxPlatformSDK
from . import Common

from BaseSDK import Toolchain


from Internal import CompileEnvironment
from Internal import Action
from Internal import File_Manager
from Internal import Logger

from Configuration import Directory_Manager as Dir_Manager

# Options for the linux compiling
class Options:

    UseAddressSanitizer = False

    UseThreadSanitizer = False

    UseUnknownSanitizer = False

    # check if all 3 options are false
    # <Return> true if all 3 options are false
    def IsNone(self):
        if self.UseAddressSanitizer is False and self.UseThreadSanitizer is False and self.UseUnknownSanitizer is False:
            return True
        return False


class LinuxToolchain(Toolchain.ToolchainSDK):

    # The Architecture
    Arch = ""

    # If true, we should NOT produce PIE exe by default
    NotUsingPIE = False

    # If true, we should save PYSM (portable symbol files) that was produced by dump_syms
    SavePYSM = False

    # Information we will print for debug info
    Info = ""

    Version = [0, 0, 0]

    VersionString = ""

    # Cashe variables
    IsCrossCompiling = False
    MultiArchRoot = ""
    BasePath = ""
    ClangPath = ""
    GCCPath = ""
    ArPath = ""
    LlvmArPath = ""
    RanLibPath = ""
    StripPath = ""
    ObjectCopyPath = ""
    DumpSymsPath = ""
    BreakpadEncoderPath = ""

    UseFixedDepends = False

    Bin = []

    HasPrintedDetails = False

    CanUseSystemCompiler = False

    # If we already used LLD
    _LldUsed = False

    _HostOS = platform.system()

    SDK = LinuxPlatformSDK.LinuxPlatformSDK()

    Option = Options

    def __init__(self, InArch, InSDK, InSavePYSM=False, InOptions=None, InPlatform=None):

        Logger.Logger(3, "Using Linux Toolchain")

        # If InPlatform is none, we will use Linux, otherwise we will use InPlatform
        if InPlatform is None:
            self._RunBase(InArch, InSDK, CompileEnvironment.Platform.Linux, InSavePYSM, InOptions)
        else:
            self._RunBase(InArch, InSDK, InPlatform, InSavePYSM, InOptions)

        # Set values
        self.MultiArchRoot = self.SDK.GetSDKLoc()
        self.BasePath = self.SDK.GetSDKArchPath(self.Arch)
        CanUseSystemCompiler = self.SDK.CanUseSystemCompiler()
        IsCompilerValid = False
        self.DumpSymsPath = os.path.join(Dir_Manager.Engine_Directory, "bin", "DumpSyms", "Linux", "x86", "Final", "DumpSyms")
        self.BreakpadEncoderPath = os.path.join(Dir_Manager.Engine_Directory, "bin", "CrashpadEncoder", "Linux", "x86", "Final", "CrashpadEncoder")

        # Throw error if LINUX_ROOT is not set and we cannot use system compiler
        if CanUseSystemCompiler is False and (self.BasePath is None or self.BasePath == ""):
            Logger.Logger(5, "ERROR: LINUX_ROOT environment variable is not set!")

        # If base path is not empty but Arch is empty, then change Arch root to the base path
        if (self.BasePath is not None or self.BasePath != "") and (self.MultiArchRoot is None or self.MultiArchRoot == ""):
            self.MultiArchRoot = self.BasePath

        # Validate the Compiler if we are using a system, but the compiler isn't valid
        if CanUseSystemCompiler is True and IsCompilerValid is False:
            # self.ClangPath = os.path.join(self.BasePath, "bin", "clang++") # FIXME: Doesn't work in this prototype, using WhichClang() as temp solution
            self.ClangPath = Common.WhichClang()
            self.GCCPath = Common.WhichGCC()
            self.ArPath = Common.WhichAR()
            self.llvmArPath = Common.WhichLLVM()
            self.RanLibPath = Common.WhichRanLib()
            self.StripPath = Common.WhichStrip()
            self.ObjectCopyPath = Common.WhichObjCopy()

            # FixDepends supports only on windows
            if self._HostOS == "Windows":
                self.UseFixedDepends = True

            # if the currently running OS is Linux, we will ensure all lang types are overwritten by POSIX ASCII only system
            if self._HostOS == "Linux":
                os.environ["LC_ALL"] = "C"

            # These settings allow us to cross compile
            self.IsCrossCompiling = True

            # FIXME: Make sure this is accuate once we add it!
            self.IsCompilerValid = self.GetCompilerVersion()

        # Validate system Toolchain
        self._ValidateSystemToolchain()

        # Check the compiler settings
        self.SetDefaultCompilerSettings()

        # TODO: Add proper detection
        self._LldUsed = True

    # Validate system Toolchain
    def _ValidateSystemToolchain(self):
        if self.CanUseSystemCompiler is True and self.IsCompilerValid is False:
            self.ClangPath = Common.WhichClang()
            self.GCCPath = Common.WhichGCC()
            self.ArPath = Common.WhichAR()
            self.llvmArPath = Common.WhichLLVM()
            self.RanLibPath = Common.WhichRanLib()
            self.StripPath = Common.WhichStrip()
            self.ObjectCopyPath = Common.WhichObjCopy()

            self.UseFixedDepends = False

            # These settings allow us to cross compile
            self.IsCrossCompiling is False

            # FIXME: Make sure this is accuate once we add it!
            self.IsCompilerValid = self.GetCompilerVersion()

    # Run's the parent init and set some values
    # <InArch> The Arch to use
    # <InSDK> The SDK to use
    # <InPlatform> The platform to use
    # <InSavePYSM> true if we should save PYSM
    # <InOptions> Any options for linux
    def _RunBase(self, InArch, InSDK, InPlatform, InSavePYSM=False, InOptions=None):
        super().__init__(InPlatform)
        self.Arch = InArch
        self.SDK = InSDK
        self.SavePYSM = InSavePYSM
        self.Option = InOptions

    # Return's true if we are using clang
    # <Return> true if we are using Clang
    def IsUsingClang(self):
        if self.ClangPath is not None and self.ClangPath != "":
            return True
        return False

    # Set the array version from string
    def SetVersionArray(self):
        VersionArrayString = self.Version.split(".")

        tmp = 0

        while tmp < len(VersionArrayString) - 1:
            self.Version[tmp] = int(VersionArrayString[tmp])
            tmp += 1

    # Get .debug and run Encoder
    # <LinkEnv> The link environment
    # <OutputFile> The output file name, for naming
    # <Return> String of commands to run to activate debug, empty if we are not using it
    def GetEncodeCommand(self, LinkEnv, OutputFile):
        # FIXME: Add Windows Support!

        # if Crashpad encoder or dump syms tools don't exist, exit early
        if not os.path.isfile(self.DumpSymsPath) or not os.path.isfile(self.BreakpadEncoderPath):
            Logger.Logger(4, "DumpSyms and/or Crashpadencoder tool could not be found, skipping encoder...")
            return ""

        OutputFileFullLoc = os.path.abspath(OutputFile)  # Get full file path

        OutputFileWithoutExt = os.path.splitext(OutputFileFullLoc)[0]  # Removes the extension

        Base = os.path.basename(OutputFileWithoutExt)
        EncodeSymbolFile = os.path.join(LinkEnv.OutputDir, Base + ".sym")

        SymbolFile = os.path.join(LinkEnv.LocalShadowDir, OutputFile + ".pysm")

        StripFile = os.path.join(LinkEnv.LocalShadowDir, OutputFile + "_nodebug")

        DebugFile = os.path.join(LinkEnv.OutputDir, Base + ".debug")

        # If SavePYSM is true, then we will store the symbol file in the output directory instead of the shadow directory
        if self.SavePYSM is True:
            SymbolFile = os.path.join(LinkEnv.OutputDir, Base + ".pysm")

        # Compile dump_syms
        Ret = ('"'+ self.DumpSymsPath + '" -c -o "' + OutputFileFullLoc + '" "' + os.path.abspath(SymbolFile) + '"\n')

        # encode breakpad symbols
        Ret += ('"' + self.BreakpadEncoderPath + '" "' + os.path.abspath(SymbolFile) + '" "' + os.path.abspath(EncodeSymbolFile) + '" \n')

        # Write debug information
        if LinkEnv.AddDebugInfo is True:

            # use objcopy on strip file
            Ret += ('"' + self.ObjectCopyPath + '" --strip-all "' + os.path.abspath(OutputFile) + '" "' + os.path.abspath(StripFile) + '"\n')

            # use objcopy on debug file
            Ret += ('"' + self.ObjectCopyPath + '" --only-keep-debug "' + os.path.abspath(OutputFile) + '" "' + os.path.abspath(DebugFile) + '"\n')

            # use objcopy to link Debug file to the Final .so file, using temp to avoid corruption
            Ret += ('"' + self.ObjectCopyPath + '" --add-gnu-debuglink="' + os.path.abspath(DebugFile) + '" "' + os.path.abspath(StripFile) + '" "' + os.path.abspath(OutputFile) + '.temp" \n')

            # Rename the .temp to the final name
            Ret += ('mv "' + os.path.abspath(OutputFile) + '.temp" "' + os.path.abspath(OutputFile) + '"\n')

            # Change permission to normal (this permission allows main user to read and write, but other users can only read it)
            Ret += 'chmod 644 "' + os.path.abspath(DebugFile) + '"\n'

        else:
            Ret += '"' + StripFile + '" "' + os.path.abspath(OutputFile) + '"'

        return Ret

    # Set the version string of the compiler
    def GetCompilerVersion(self):
        # Check Clang
        if self.ClangPath != "":
            App = subprocess.run([self.ClangPath, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

            Out = App.stdout

            Match = re.search(r"clang version (\d+\.\d+(\.\d+)?)", Out)

            if Match:
                self.VersionString = Match.group(1)

    # Get settings from compiler, and change settings based on it's options
    def SetDefaultCompilerSettings(self):
        if self.ClangPath != "":

            # Check settings for clang
            App = subprocess.run("echo '' | " + self.ClangPath + " -E -dM -", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True, shell=True)

            for Line in App.stdout:
                LineStrip = Line.strip()

                if LineStrip is None or LineStrip == "":
                    break

                if "__pie__" in LineStrip or "__PIE__" in LineStrip:
                    self.NotUsingPIE = True

    # Set switches depending on architecture
    # <Arch> The arch to switch
    # <Return> commands as strings for specific arch switches
    @staticmethod
    def ArchSwitch(Arch):
        if Arch.startswith("arm") or Arch.startswith("aarch64"):
            return " -fsigned-char"  # Tells the compiler to treat char as signed chars
        return ""

    # Set defines based on the architecture
    # <Arch> The Arch to define
    # <Return> Commands as strings for specific arch defines
    @staticmethod
    def ArchDefine(Arch):
        if Arch.startswith("x86_64") or Arch.startswith("aarch64"):
            return " -D_LINUX64"
        return ""


    @staticmethod
    # Check if we are using LibCXX
    # <Arch> The arch to use
    # <Return> true if we are using LibCXX
    def UseLibCXX(Arch):
        Override = os.environ.get("RBT_Use_LibCXX", "0")

        # If Override is valid
        if Override is None or Override == "":

            # If Override is true
            if Override == "True" or Override == "true" or Override == "1":

                # If Override starts with supported arch, return true
                if (Override.startswith("i686") or Override.startswith("x86_64") or Override.startswith("aarch64")):
                    return True

        return False

    # Fix the args to make it compatable
    # <Arg> The argument
    # <Return> Reformatted argument
    @staticmethod
    def EscapeArgs(Arg):
        ArgArray = Arg.split("=")

        try:
            Key = ArgArray[0]
        except Exception:
            Key = None

        try:
            Value = ArgArray[1]
        except Exception:
            Value = None

        if Key is None:
            return ""

        else:

            if not Value.startswith('"') and (" " in Value or "$" in Value):
                Value = Value.trim('"') # Trim value
                Value = '"' + Value + '"' # Add quotes around value

            # TODO: Dawg this doesn't do anything
            Value.replace('"', '\\"')

        # TODO: Do we need this?
        if Value is None:
            return Key
        else:
            return Key + "=" + Value

    # Get the arguments for C++
    # <Return> Command as string
    @staticmethod
    def ArgCPP():
        return " -x c++ -std=c++17"

    # Get the arguments for PCH
    # <Return> Command as string
    @staticmethod
    def ArgPCH():
        return " -x c++-header -std=c++17"

    # Whether to use llvm-ar or ar
    # <Return> the program to use for archiving as string
    # TODO: Temp solution, assumes it's system-wide, add support for non-system wide
    def ArchiveProgram(self):
        if self.LlvmArPath != "":
            return "llvm-ar"
        elif self.ArPath != "":
            return "ar"
        else:
            Logger.Logger(5, "Cannot create llvm-ar or ar. Both tools cannot be found")

    # Get arguments for archive
    # <Return> arguments for archive
    def ArgArchive():
        return " rcs"

    # Check if we are using Lld
    # <Arch> The arch to use
    # <Return> true if Lld is supported and being used
    def UsingLld(self, Arch):
        if self._LldUsed is True and Arch.startswith("x86_64"):
            return True
        return False

    # Return if we can use Advance Features
    # <Arch> The arch to use
    # <Return> True if we can use advance features
    def CanAdvanceFeatures(self, Arch):
        # We can only use advance features if we are using Lld and Llvm-Ar is valid
        if self.UsingLld(Arch) is True:
            if self.LlvmArPath is not None and self.LlvmArPath != "":
                return True
        return False

    # TODO: Add this!
    def SDKVersionCorrect():
        pass

    # Get the full response name of a file
    # <LinkEnv> The link environment
    # <OutputFile> The output file, for naming
    # <Return> The full intermediate and rsp name as string
    def GetResponseName(self, LinkEnv, OutputFile):
        return os.path.join(LinkEnv.IntermediateDir, os.path.basename(OutputFile) + ".rsp")

    # Archive and index the input files and turn them into static libraries
    # <LinkEnv> The link environment
    # <OutputActionList> The Action list that will be appended
    # <Return> The output .lib file
    def ArchiveAndIndex(self, LinkEnv, OutputActionList):

        # Create .lib action
        Archive = Action.Action

        Archive.CommandPath = self.ArchiveProgram()

        Archive.Arguments = "-c '"

        Archive.CreateImportLib = True

        OutputFile = LinkEnv.OutputDir
        Archive.OutputItems.append(OutputFile)

        # Get argument for archive
        Arg = (' "' + self.ArPath + '" ' + self.ArgArchive + ' "' + os.path.abspath(OutputFile))
        Archive.Arguments += Arg

        InputFiles = []

        for File in LinkEnv.InputFiles:
            Temp = os.path.abspath(File)
            InputFiles.append('"' + Temp + '"')

        # TODO: Why do we have this? This seems important but unused. Is this what is supposed to be returned?
        ResponsePath = self.GetResponseName(LinkEnv, OutputFile)

        # FIXME: Add support for not generating project files support (Requires class that doesn't exist yet) This will create intermediate file and add it to precondition list

        if self.LlvmArPath is None or self.LlvmArPath == "":
            Archive.Arguments += (' && "' + self.RanlibPath + '" "' + os.path.abspath(OutputFile) + '"')

        Archive.Arguments += " " + LinkEnv.AdditionalArgs

        Archive.Arguments += "'"

        OutputActionList.append(Archive)

        return OutputFile

    # Import CXX
    # <Arch> The arch to use
    # <Return> The command to run if we are using LibCXX
    # FIXME: ADD IMPORTS AFTER ADDING CXX LIBRARY!
    def _ImportCXX(self, Arch):
        Ret = ""
        CanUse = self.UseLibCXX(Arch)
        if CanUse is True:
            Ret += "-nostdinc++"
        return Ret

    # Sanitize based on options
    # <Return> All stuff to sanitize as string
    def _AddSanitize(self):
        Ret = ""
        if self.Option is not None and self.Option.UseAddressSanitizer is True:
            Ret += " -fsanitize=address"
        if self.Option is not None and self.Option.UseThreadSanitizer is True:
            Ret += " -fsanitize=thread"
        if self.Option is not None and self.Option.UseUnknownSanitizer is True:
            Ret += " -fsanitize=undefined"
        return Ret

    # Get global clang flags
    # <Return> command to run as string, specific for clang compiler
    def _Global_Clang_Flags(self):
        Ret = " -Wno-tautological-compare -Wno-unused-private-field --Wno-undefined-bool-conversion"
        return Ret

    # Add optimized flag based on settings
    # <CompileEnv> The Compile Environment
    # <Return> command to run as string, contains flag for optimization level
    def _Optimize(self, CompileEnv):

        # If Optimize setting is false, then turn off all optimization
        if CompileEnv.Optimize is False:
            Ret = " -O0"

        # If Optimize setting is true, and we are using address or Thread Sanitizer, then set level to 1
        elif (self.Option.UseAddressSanitizer is True or self.Option.UseThreadSanitizer is True):
            Ret = " -O1 -g"

            # Add additional optimization if we are using address sanitizer
            if self.OptionUseAddressSanitizer is True:
                Ret += " -fno-optimize-sibling-calls -fno-omit-frame-pointer"

        # Else if Optimize setting is false and we don't have Address Sanitizer and Thread Sanitizer, then use standard optimization
        else:
            Ret = " -O2"

        return Ret

    # Change command based on BuildType
    # <BuildType> The BuildType we will compile with
    # <Return> Command as string that contains custom command based on BuildType
    def _OutputConfig(self, BuildType):
        Ret = ""
        if BuildType == "Final":
            Ret = " -Wno-unused-value -fomit-frame-pointer"

        elif BuildType == "Debug":
            Ret = " -fno-inline -fno-omit-frame-pointer -fstack-protector"

        return Ret

    # If we should add exceptions
    # <ShouldAddExceptions> True if we will add exceptions
    # <Return> Command as string that will tell the compiler if we should check or ignore exceptions
    def _Exceptions(self, ShouldAddExceptions):
        if ShouldAddExceptions is True:
            Ret = " -fexceptions -DUSE_EXCEPTIONS=1"
        else:
            Ret = " -fno-exceptions"

        return Ret

    # Add commands if we are cross-compiling
    # <Arch> The arch we are using
    # <Return> the command to run if we are using cross compiling as a string
    def _CrossCompile(self, Arch):
        Ret = ""

        if self.IsCrossCompiling is False:
            return ""

        if self.IsUsingClang is True and (Arch is not None or Arch != ""):
            Ret += " -target " + Arch

        # Ret += ' --sysroot="' + self.BasePath + '"' # FIXME: This breaks my current code, since we are using system shit for now, once I replace those code, re-add this

        return Ret

    # Global Arguments that we will use for both Compiling and Linking
    # <CompileEnv> The compile environment
    # <Return> The command to run as a string
    def GetGlobalArg(self, CompileEnv):

        # Add beginning stuff
        Ret = " -c -pipe"

        # Add CXX and Sanitize if we are using it
        Ret += self._ImportCXX(CompileEnv.Arch)

        Ret += self._AddSanitize()

        Ret += " -Wall -Werror"

        if not CompileEnv.Arch.startswith("X86_64") and CompileEnv.Arch.startswith("AARCH64"):
            Ret += " -funwind-tables"

        Ret += (" -Wsequence-point -Wdelete-non-virtual-dtor" + self.ArchSwitch(CompileEnv.Arch) + " -fno-math-errno")

        if CompileEnv.HideSymbols is True:
            Ret += " -fvisibility=hidden -fvisibility-inlines-hidden"

        # TODO: Add GCC Support

        if self.IsUsingClang is True:

            Ret += self._Global_Clang_Flags()

        Ret += " -Wno-unused-variable -Wno-unused-function -Wno-switch -Wno-unknown-pragmas -Wno-gnu-string-literal-operator-template -Wno-invalid-offsetof"


        if CompileEnv.PGOOptimize is True:
            Ret += (' -Wno-backend-plugin -fprofile-instr-use="' + os.path.join(CompileEnv.PGODirectory, CompileEnv.PGOFilePrefix) + '"')

        elif CompileEnv.PGOProfile is True:
            Ret += " -fprofile-generate"

        if CompileEnv.ShadowVariableWarnings is True:
            Ret += " -Wshadow"

            if CompileEnv.ShadowVariableAsError is False:
                Ret += " -Wno-error=shadow"

        if CompileEnv.UndefinedIdentifierWarnings is True:
            Ret += " -Wundef"

            if CompileEnv.UndefinedIdentifierAsError is False:
                Ret += " -Wno-error=undef"

        Ret += self._OutputConfig(CompileEnv.Conf)

        if CompileEnv.UseInlining is False:
            Ret += " -fno-inline-functions"

        if CompileEnv.IsDynamic is True:
            Ret += " -fPIC -ftls-model=local-dynamic"

        Ret += self._Exceptions(CompileEnv.ExceptionHandling)

        if self.NotUsingPIE is True and CompileEnv.IsDynamic is False:
            Ret += " -fno-PIE"

        if self.SDK.VerboseCompiler is True:
            Ret += " -v"

        Ret += self.ArchDefine(CompileEnv.Arch)

        Ret += self._CrossCompile(CompileEnv.Arch)

        return Ret

    # Check if we have printed details
    # <CompileEnv> The Compiler Environment
    def _SetPrintedDetails(self, CompileEnv):
        if self.HasPrintedDetails is False:
            self.Print(CompileEnv)

            # If MultiArchRoot is set but SDK version is not correct, then Third Party is not complete!
            if self.MultiArchRoot is not None and self.MultiArchRoot != "":
                if self.SDKVersionCorrect is False:
                    raise ValueError("FATAL: ThirdParty for Linux is incomplete!")

            self.HasPrintedDetails is True

    # Compiles the list of files together into object files
    # <CompileEnv> The Compile Environment
    # <InputFilesList> The list of files to compile
    # <DirOutput> The intermediate output
    # <OutputActionList> The action list that we will append
    # <Return> List of output files that will be generated
    def CompileFiles(self, CompileEnv, InputFilesList, DirOutput, OutputActionList):

        Logger.Logger(1, "Input Files List: " + str(InputFilesList))
        Logger.Logger(1, "Directory Output: " + DirOutput)

        # Get global arguments
        Args = self.GetGlobalArg(CompileEnv)

        PCH = ""

        self._SetPrintedDetails(CompileEnv)

        # Check and return an error if we cannot use advance features, but we are using LTCG or PGO Optimized
        if self.CanAdvanceFeatures(CompileEnv.Arch) is False:
            if CompileEnv.AllowLTCG is True or CompileEnv.PGOOptimize is True:
                Logger.Logger(5, "LTCG and/or PGO Optimize cannot be true if we are not allowed to use advance features!",)

        if CompileEnv.PCH_Act == CompileEnv.PCH_Act.Include:
            PCH += " -include " + CompileEnv.PCHIncludeName

        for Item in CompileEnv.UserIncPaths:
            Args += " -I" + Item

        for Item in CompileEnv.SysIncPaths:
            Args += " -isystem" + Item

        if CompileEnv.Defines is not None and CompileEnv.Defines:
            for Item in CompileEnv.Defines:
                Args += " -D" + self.EscapeArgs(Item)

        if CompileEnv.BufferSecurityChecks is True:
            # Best equivalent for BufferSecurityChecks
            Args += " -fstack-protector-strong"
            Args += " -D" + "_FORTIFY_SOURCE=2"

        Args += self._Optimize(CompileEnv)

        CPPOut = CompileEnv.Out.ObjectFiles

        CPPOut.extend(CompileEnv.Out.DebugFiles)

        for InputFile in InputFilesList:

            # Create and set up action
            NewAction = Action.Action()

            NewAction.InputFiles.append(InputFile)  # Store all code files into InputFiles

            NewAction.PreconditionItems.extend(CompileEnv.ForceIncFiles)

            NewArgs = ""

            Extension = (os.path.splitext(os.path.abspath(InputFile))[1]).lower()

            # TODO: Add support for other file extension
            if CompileEnv.PCH_Act == CompileEnvironment.PCHAction.Create:
                NewArgs = self.ArgPCH()

            # Assume it's C++
            else:
                NewArgs = self.ArgCPP()
                NewArgs += PCH

            for F in CompileEnv.ForceIncFiles:
                NewArgs += ' -include "' + os.path.abspath(F) + '"'

            NewAction.PreconditionItems.append(InputFile)

            # Create gch file
            if CompileEnv.PCH_Act == CompileEnvironment.PCHAction.Create:
                InPCH = os.path.join(DirOutput, os.path.abspath(InputFile) + ".gch")

                CPPOut.PCHFile = InPCH

                NewAction.OutputItems.append(InPCH)

                NewArgs += ' -o "' + os.path.abspath(InPCH) + '"'

            else:
                # If we are including it, then add it to Precondition Items
                if CompileEnv.PCH_Act == CompileEnvironment.PCHAction.Include:
                    NewAction.PreconditionItems.append(CompileEnv.PCHFile)
                    NewAction.UsingPCH = True


                # Create full directory of object file
                Obj = os.path.join(DirOutput, os.path.basename(InputFile) + ".o")

                CompileEnv.Out.ObjectFiles.append(Obj)
                NewAction.OutputItems.append(Obj)

                NewArgs += ' -o "' + os.path.abspath(Obj) + '"'

            # Add input file to arguments
            NewArgs += ' "' + os.path.abspath(InputFile) + '"'

            # If we are using the "Dependency file" option, add stuff to create .d file
            if CompileEnv.GenerateDependFile is True:
                DependFile = os.path.join(DirOutput, os.path.basename(InputFile) + ".d")
                NewArgs += ' -MD -MF "' + os.path.abspath(DependFile) + '"'
                NewAction.OutputItems.append(DependFile)
                NewAction.DependencyListFile = DependFile

            # Set current directory to engine
            NewAction.CurrentDirectory = Dir_Manager.Engine_Directory

            # Set command path based on what compiler we are using
            if self.ClangPath is not None and self.ClangPath != "":
                NewAction.CommandPath = self.ClangPath

            elif self.GCCPath is not None and self.GCCPath != "":
                NewAction.CommandPath = self.GCCPath

            else:
                Logger.Logger(5, "CLANGPATH AND GCCPATH IS EMPTY OR NONE!")

            AllArgs = Args + NewArgs + CompileEnv.AdditionalArgs

            # FIXME: REPLACE THIS WITH CUSTOM FUNCTION, LET'S JUST CREATE A NEW FILE VIA NORMAL METHOD FOR NOW!

            # Create response file
            RespFileName = os.path.join(DirOutput, os.path.basename(InputFile) + ".rsp")

            Logger.Logger(2, "Creating dir: " + RespFileName)

            os.makedirs(os.path.dirname(RespFileName), exist_ok=True)

            RespFile = open(RespFileName, "w")

            # Write AllArgs to Response file
            RespFile.write(AllArgs)

            RespFile.close()

            CompileEnv.LinkEnvPrecondition.append(RespFileName)  # Put's Response name into LinkEnvPrecondition

            NewAction.Arguments = "@" + RespFileName

            NewAction.UsingGCCCompiler is True

            if CompileEnv.PCH_Act is True:
                if (CompileEnv.PCH_Act == CompileEnvironment.PCHAction.Create or CompileEnv.AllowRemotelyCompiledPCHs is True):
                    NewAction.CanRunRemotely = True

            OutputActionList.append(NewAction)

        return CPPOut


    # Get link arguments
    # <LinkEnv> The Link Environment
    # <Return> commands to run as string
    def _LinkArgs(self, LinkEnv):
        Ret = ""

        if self.UsingLld(LinkEnv.Arch) is True and LinkEnv.IsBuildingDynamic is False:
            Ret += " -Wl,-fuse-ld=lld"

        Ret += " -rdynamic"

        # Add commands based on if we are building dynmaic or not
        if LinkEnv.IsBuildingDynamic is True:
            Ret += " -shared"

        else:
            Ret += " -Wl,--unresolved-symbols=ignore-in-shared-libs"

        # Add Sanitizer stuff
        if self.Option.UseAddressSanitizer is True:
            Ret += " -g -fsanitize=address"

        elif self.Option.UseThreadSanitizer is True:
            Ret += " -g -fsanitize=thread"

        elif self.Option.UseUnknownSanitizer is True:
            Ret += " -g -fsanitize=undefined"

        Ret += ' -Wl,-rpath="${ORIGIN}" -Wl,-rpath-link="${ORIGIN}"'

        Ret += " -Wl,-rpath='${ORIGIN}/../../bin/Linux' -Wl,-rpath='${ORIGIN}/ThirdParty'"

        Ret += " -Wl,--as-needed -Wl,--hash-style=gnu -Wl,--build-id"

        if self.NotUsingPIE is True and LinkEnv.IsBuildingDynamic is False:
            Ret += " -Wl,-nopie"

        if LinkEnv.PGOOptimize is True:
            Ret += ' -Wno-backend-plugin -fprofile-instr-use="' + os.path.join(LinkEnv.PGODirectory, LinkEnv.PGOFilePrefix) + '"'

        elif LinkEnv.PGOProfile is True:
            Ret += " -fprofile-generate"

        if LinkEnv.AllowLTCG is True:
            Ret += " -flto"

        # If we are cross compiling and we are using clang, then use system stuff
        if self.IsCrossCompiling is True:

            if self.IsUsingClang is True:

                Ret += " -target " + LinkEnv.Arch

                # Ret += ' "--sysroot=' + BasePath + '"' # FIXME: This breaks my current code, since we are using system shit for now, once I replace those code, re-add this

                Ret += "-B" + self.BasePath + "/usr/lib/"

                Ret += "-B" + self.BasePath + "/usr/lib64/"

                Ret += "-L" + self.BasePath + "/usr/lib/"

                Ret += "-L" + self.BasePath + "/usr/lib64/"

        return Ret

    # Create group for external libraries
    # <LinkEnv> The link environment
    # <OutputResp> The output to append to
    # <OutputAction> The action list to append
    # <Return> named of the external dynamic library
    def _LinkGroups(self, LinkEnv, OutputResp, OutputAction):

        # Start group
        OutputResp.append(" --start-group")

        ExternalLibs = ""

        # For each additional library
        for Item in LinkEnv.AdditionalLibs:
            Extension = os.path.splitext(Item)[1]  # Get extension

            if os.path.dirname(Item) is None or os.path.dirname(Item) == "":
                ExternalLibs += " -l" + Item

            elif Extension == ".a":

                Abs = os.path.abspath(Item)

                # Add quotes if there's a space, so that there wouldn't be any errors
                if " " in Abs:
                    Abs = '"' + Abs + '"'

                if LinkEnv.IsBuildingDynamic is True and ("libcrypto" in Abs or "libssl" in Abs):
                    OutputResp.append(" --whole-archive" + Item + " --no-whole-archive")

                else:
                    OutputResp.append(" " + Item)

                AllFiles = File_Manager.GetAllFilesFromDir(Item)

            else:

                Depend = File_Manager.GetAllFilesFromDir(Item)

                Name = os.path.splitext(Item)[0]

                # removes the lib text if it exists
                NameDir = os.path.dirname(Name)
                NameBase = os.path.basename(Name)

                if "lib" in NameBase:
                    Name = Name[3:]

                Name = os.path.join(NameDir, NameBase)

                OutputAction.PreconditionItems.append(Depend)
                ExternalLibs += " " + Name + ".so"

        OutputResp.append(" --end-group")

        return ExternalLibs


    # Create the bash script for linking
    # <LinkEnv> The link environment
    # <Output> The name of output minus the '.sh'
    # <Com> The content to be written
    # <Action> The action to append
    # TODO: Add windows support!
    def CreateLinkScriptFile(self, LinkEnv, Output, Com, Action):
        LinkName = "link-" + os.path.basename(Output) + ".sh"

        LinkFile = os.path.join(LinkEnv.IntermediateDir, LinkName)

        Logger.Logger(2, "Creating ShadowDir: " + LinkEnv.LocalShadowDir)

        os.makedirs(LinkEnv.LocalShadowDir, exist_ok=True)

        Logger.Logger(2, "Creating file: " + LinkFile)

        with open(LinkFile, "w") as f:
            Logger.Logger(2, "writing: " + LinkFile)
            f.write("#!/bin/sh\n")
            f.write("set -o errexit\n")
            f.write(Com + "\n")
            f.write(self.GetEncodeCommand(LinkEnv, Output)) # FIXME: Readd this once we add Breakpad!

        Action.CommandPath = "/bin/sh"
        Action.Arguments = LinkFile

        LinkScriptFile = os.path.join(LinkEnv.LocalShadowDir, "remove-sym.ldscript")

        if os.path.exists(LinkScriptFile):
            Logger.Logger(2, "Removing file: " + LinkScriptFile)
            # os.remove(LinkScriptFile)

    # Create the bash script for relinking
    # <LinkEnv> The link environment
    # <Output> The name of output minus the '.sh'
    # <Com> The content to be written
    # <Action> The action to append
    # <RelinkedFile> The new name of relinked file
    def _STEP2LinkShellFiles(self, LinkEnv, Output, Com, Action, RelinkedFile):
        RelinkName = "Relink-" + os.path.basename(Output) + ".sh"

        RelinkFile = os.path.join(LinkEnv.LocalShadowDir, RelinkName)

        Logger.Logger(2, "Creating dir: " + RelinkFile)

        os.makedirs(RelinkFile, exist_ok=True)

        NewCom = Com

        NewCom = NewCom.replace(Output, RelinkedFile)
        NewCom = NewCom.replace("$", "\\$")

        Logger.Logger(2, "Creating file: " + RelinkFile)

        with open(RelinkFile, "w") as f:
            Logger.Logger(2, "writing: " + RelinkFile)
            f.write("#!/bin/sh\n")
            f.write("set -o errexit\n")

            # Write contents
            f.write(Com + "\n")

            f.write("TIMESTAMP='stat --format %y \"" + os.path.abspath(Output) + '"\n')
            f.write("cp " + RelinkFile + " " + os.path.abspath(Output) + "\n")

            f.write("mv " + os.path.abspath(Output) + ".temp " + os.path.abspath(Output) + "\n")

            # Get encoding command
            f.write(self.GetEncodeCommand(LinkEnv, Output) + "\n")
            f.write('touch -d "$TIMESTAMP"' + os.path.abspath(Output))

        Action.CommandPath = "/bin/sh"
        Action.Arguments = '"' + RelinkFile + '"'
        Action.InputFiles.append(RelinkFile)


    # Link the object files into binary file
    # <LinkEnv> The Link Environment
    # <ImportLibraryOnly> If we should only import library (aka archiving and indexing)
    # <OutputActionList> List of actions to append
    # <Return> List of binary files we will create
    def LinkFiles(self, LinkEnv, ImportLibraryOnly, OutputActionList):

        # Throw error if LTCG or PGO is being used, but we cannot use advance features
        if (LinkEnv.AllowLTCG is True or LinkEnv.PGOProfile is True or LinkEnv.PGOOptimize) and self.CanAdvanceFeatures(LinkEnv.Arch) is False:
            Logger.Logger(5, "FATAL: AllowLTCG, PGOProfile, and/or PGOOptimize is true, but we cannot use advance features!")

        # If we are building libraries, or if we are only importing library, then return the archived and indexed files (.a_
        if LinkEnv.IsBuildingLibrary is True or ImportLibraryOnly is True:
            return self.ArchiveAndIndex(LinkEnv, OutputActionList)

        RPath = []

        # Create New Action
        NewAction = Action.Action()

        NewAction.InputFiles.extend(LinkEnv.InputFiles)

        NewAction.PreconditionItems.extend(LinkEnv.LinkEnvPrecondition)

        NewAction.CurrentDirectory = Dir_Manager.Engine_Directory

        Com = ""

        if self.ClangPath is not None and self.ClangPath != "":
            Com += '"' + self.ClangPath + '"'

        else:
            Com += '"' + self.GCCPath + '"'

        # Get linked arguments
        Com += self._LinkArgs(LinkEnv)

        NewAction.CreateImportLib = LinkEnv.IsBuildingDynamic

        Output = LinkEnv.OutputPaths[0]

        NewAction.OutputItems.append(Output)

        # TODO: Add description debugging support

        # Set output
        Com += " -o " + os.path.abspath(Output)

        Resp = [] # List of all lines for response file

        # For every input files, add it to response
        for Item in LinkEnv.InputFiles:
            # Add input files to response file
            Resp.append(os.path.abspath(Item) + " ")

        # Add soname if we are building dynamic
        if LinkEnv.IsBuildingDynamic is True:
            Resp.append(" -soname=" + Output)

        AllLib = LinkEnv.LibraryPaths  # All libs combined

        # For every additional library
        for Item in LinkEnv.AdditionalLibs:

            ItemPath = os.path.dirname(Item)

            # If Item contains Plugin or ThirdParty, and is not the absolute file
            if ("Plugin" in Item or "bin/ThirdParty" in Item) and os.path.dirname(Item) != os.path.abspath(Output):

                Relative = os.path.relpath(Item, os.path.dirname(Output))

                if (self.IsCrossCompiling is True and Dir_Manager.Engine_Directory in Relative):
                    Temp = Relative.replace(Dir_Manager.Engine_Directory, "")

                    # If we are on Linux Root Directory, we just need to move back the directory, otherwise we will include Temp
                    Relative = "../../../"
                    if not Temp.startswith("/"):
                        Relative += Temp

                if Relative not in RPath:
                    RPath.append(Relative)
                    Resp.append(' -rpath=$"{{ORIGIN}}' + Relative + '"')

        # For every Runtime library path
        for Item in LinkEnv.RuntimeLibPaths:

            # Temp var so we can modify it if needed
            ItemTemp = Item

            if not ItemTemp.startswith("$"):
                RootPath = os.path.relpath(ItemTemp, Dir_Manager.Engine_Directory)
                ItemTemp = os.path.join("..", "..", "..", RootPath)

            if ItemTemp not in RPath:
                RPath.append(ItemTemp)
                Resp.append(' -rpath="${{ORIGIN}}' + ItemTemp + '"')

        Resp.append(' -rpath-link="' + os.path.dirname(Output) + '"')

        for Item in AllLib:
            Resp.append(' -L"' + Item + '"')

        ExternalLibs = self._LinkGroups(LinkEnv, Resp, NewAction)

        RespFile = self.GetResponseName(LinkEnv, Output)

        File_Manager.CreateIntermedFile(RespFile, Resp)

        Com += ' -Wl,@"' + RespFile + '"'

        Com += " -Wl,--start-group" + ExternalLibs + " -Wl,--end-group -lrt -lm"

        # FIXME: Add libCXX support

        if self.SDK.VerboseLinker is True:
            Com += " -Wl,--verbose -Wl,--trace -v"

        Com += LinkEnv.AdditionalArgs

        self.CreateLinkScriptFile(LinkEnv, Output, Com, NewAction)

        # Add action to list
        OutputActionList.append(NewAction)

        # If we are building dynamic, start relink
        if LinkEnv.IsBuildingDynamic is True:
            # -- Start Relink -- #

            RelinkAction = Action.Action()

            RelinkAction.CurrentDirectory = NewAction.CurrentDirectory

            RelinkAction.OutputItems.append(Output)

            RelinkedFile = os.path.join(LinkEnv.LocalShadowDir, Output + ".Relink")

            Dummy = os.path.join(LinkEnv.LocalShadowDir, Output + ".Relink_Action_Ran")

            RelinkAction.OutputItems.append(Dummy)

            self._STEP2LinkShellFiles(LinkEnv, Output, Com, RelinkAction, RelinkedFile)

            OutputActionList.append(RelinkAction)

        # Put all dynamic modules, copy them into ThirdParty. QUICK HACK
        for Item in LinkEnv.AdditionalLibs:
            ItemNoDir = os.path.basename(Item)
            OutputToCopy = os.path.dirname(LinkEnv.OutputPaths[0])

            if Item.endswith(".so"):
                if "ThirdParty" in Item:
                    DynamicOutputDir = os.path.join(OutputToCopy, "ThirdParty")
                    os.makedirs(os.path.join(OutputToCopy, "ThirdParty"), exist_ok=True)
                else:
                    DynamicOutputDir = OutputToCopy

                # Copy and paste dynamic library into
                Logger.Logger(2, "Copying " + str(ItemNoDir) + "To name " + str(ItemNoDir + ".0") + "Under output directory " + str(os.path.basename(DynamicOutputDir)))
                os.system("cp " + Item + " " + os.path.join(DynamicOutputDir, ItemNoDir + ".0"))

        return Output

    # Return's the actions to do after building
    # <File> The file to apply post building stuff
    # <LinkEnv> The link environment
    # <ActionList> The list of actions, will be appended
    # <Return> List of Relink map if needed
    def PostBuilt(self, File, LinkEnv, ActionList):

        Output = super().PostBuilt(File, LinkEnv, ActionList)

        # If we are building dynamic and we are cross-referencing, create .Relink_Action_Ran file
        if LinkEnv.IsBuildingDynamic is True and LinkEnv.CrossedReference is True:
            RelinkMap = os.path.join(LinkEnv.LocalShadowDir, Output + ".Relink_Action_Ran")
            Output.append(RelinkMap)

        return Output

    @staticmethod
    def Print(CompileEnv):
        return ""
