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


class Options:

    UseAddressSanitizer = False

    UseThreadSanitizer = False

    UseUnknownSanitizer = False

    def IsNone(self):
        if (
            self.UseAddressSanitizer is False
            and self.UseThreadSanitizer is False
            and self.UseUnknownSanitizer is False
        ):
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

    def __init__(
        self, InArch, InSDK, InSavePYSM=False, InOptions=None, InPlatform=None
    ):

        Logger.Logger(3, "Using Linux Toolchain")

        # If InPlatform is none, we will use Linux, otherwise we will use InPlatform
        if InPlatform is None:
            self._RunBase(
                InArch, InSDK, CompileEnvironment.Platform.Linux, InSavePYSM, InOptions
            )
        else:
            self._RunBase(InArch, InSDK, InPlatform, InSavePYSM, InOptions)

        self.MultiArchRoot = self.SDK.GetSDKLoc()
        self.BasePath = self.SDK.GetSDKArchPath(self.Arch)

        CanUseSystemCompiler = self.SDK.CanUseSystemCompiler()
        IsCompilerValid = False

        if CanUseSystemCompiler is False and (
            self.BasePath is None or self.BasePath == ""
        ):
            Logger.Logger(5, "ERROR: LINUX_ROOT environment variable is not set!")

        self.DumpSymsPath = os.path.join(
            Dir_Manager.Engine_Directory, "bin", "Linux", "DumpSyms"
        )
        self.BreakpadEncoderPath = os.path.join(
            Dir_Manager.Engine_Directory, "bin", "Linux", "BreakpadEncoder"
        )

        if (self.BasePath is not None or self.BasePath != "") and (
            self.MultiArchRoot is None or self.MultiArchRoot == ""
        ):
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
    def _RunBase(self, InArch, InSDK, InPlatform, InSavePYSM=False, InOptions=None):
        super().__init__(InPlatform)
        self.Arch = InArch
        self.SDK = InSDK
        self.SavePYSM = InSavePYSM
        self.Option = InOptions

    # Return's true if we are using clang
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

    def GetEncodeCommand(self, LinkEnv, OutputFile):
        # FIXME: Add Windows Support!

        OutputFileFullLoc = os.path.abspath(OutputFile)  # Get full file path

        OutputFileWithoutExt = os.path.splitext(OutputFileFullLoc)[
            0
        ]  # Removes the extension

        EncodeSymbolFile = os.path.join(
            LinkEnv.OutputDir, OutputFileWithoutExt + ".sym"
        )

        SymbolFile = os.path.join(LinkEnv.LocalShadowDir, OutputFile + ".pysm")

        StripFile = os.path.join(LinkEnv.LocalShadowDir, OutputFile + "_nodebug")

        DebugFile = os.path.join(LinkEnv.OutputDir, OutputFileWithoutExt + ".debug")

        # If SavePYSM is true, then we will store the symbol file in the output directory instead of the shadow directory
        if self.SavePYSM is True:
            SymbolFile = os.path.join(LinkEnv.OutputDir, OutputFileWithoutExt + ".pysm")

        # Compile dump_syms
        Ret = (
            '"'
            + self.DumpSymsPath
            + '" -c -o "'
            + OutputFileFullLoc
            + '" "'
            + os.path.abspath(SymbolFile)
            + '"\n'
        )

        # encode breakpad symbols
        Ret += (
            '"'
            + self.BreakpadEncoderPath
            + '" "'
            + os.path.abspath(SymbolFile)
            + '" "'
            + os.path.abspath(EncodeSymbolFile)
            + '" \n'
        )

        # Write debug information
        if LinkEnv.AddDebugInfo is True:

            # use objcopy on strip file
            Ret += (
                '"'
                + self.ObjectCopyPath
                + '" --strip-all "'
                + os.path.abspath(OutputFile)
                + '" "'
                + os.path.abspath(StripFile)
                + '"\n'
            )

            # use objcopy on debug file
            Ret += (
                '"'
                + self.ObjectCopyPath
                + '" --only-keep-debug "'
                + os.path.abspath(OutputFile)
                + '" "'
                + os.path.abspath(DebugFile)
                + '"\n'
            )

            # use objcopy to link Debug file to the Final .so file, using temp to avoid corruption
            Ret += (
                '"'
                + self.ObjectCopyPath
                + '" --add-gnu-debuglink="'
                + os.path.abspath(DebugFile)
                + '" "'
                + os.path.abspath(StripFile)
                + '" "'
                + os.path.abspath(OutputFile)
                + '.temp" \n'
            )

            # Rename the .temp to the final name

            Ret += (
                'mv "'
                + os.path.abspath(OutputFile)
                + '.temp" "'
                + os.path.abspath(OutputFile)
                + '"\n'
            )

            # Change permission to normal (this permission allows main user to read and write, but other users can only read it)
            Ret += 'chmod 644 "' + os.path.abspath(DebugFile) + '"\n'

        else:

            Ret += '"' + StripFile + '" "' + os.path.abspath(OutputFile) + '"'

        return Ret

    def GetCompilerVersion(self):
        # Check Clang
        if self.ClangPath != "":
            App = subprocess.run(
                [self.ClangPath, "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )

            Out = App.stdout

            Match = re.search(r"clang version (\d+\.\d+(\.\d+)?)", Out)

            if Match:
                self.VersionString = Match.group(1)

    def SetDefaultCompilerSettings(self):
        if self.ClangPath != "":

            App = subprocess.run(
                "echo '' | " + self.ClangPath + " -E -dM -",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
                shell=True,
            )

            for Line in App.stdout:
                LineStrip = Line.strip()

                if LineStrip is None or LineStrip == "":
                    break

                if "__pie__" in LineStrip or "__PIE__" in LineStrip:
                    self.NotUsingPIE = True

    # Set switches depending on architecture
    @staticmethod
    def ArchSwitch(Arch):
        if Arch.startswith("arm") or Arch.startswith("aarch64"):
            return " -fsigned-char"  # Tells the compiler to treat char as signed chars
        return ""

    # Set defines based on the architecture
    @staticmethod
    def ArchDefine(Arch):
        if Arch.startswith("x86_64") or Arch.startswith("aarch64"):
            return " -D_LINUX64"
        return ""

    @staticmethod
    def UseLibCXX(Arch):
        Override = os.environ.get("RBT_Use_LibCXX", "0")

        # If Override is valid
        if Override is None or Override == "":

            # If Override is true
            if Override == "True" or Override == "true" or Override == "1":

                # If Override starts with supported arch, return true
                if (
                    Override.startswith("i686")
                    or Override.startswith("x86_64")
                    or Override.startswith("aarch64")
                ):
                    return True

        return False

    # Fix the args to make it compatable
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
                Value = Value.trim('"')
                Value = '"' + Value + '"'

            Value.replace('"', '\\"')

        if Value is None:
            return Key
        else:
            return Key + "=" + Value

    @staticmethod
    def ArgCPP():
        return " -x c++ -std=c++14"

    @staticmethod
    def ArgPCH():
        return " -x c++-header -std=c++14"

    # Whether to use llvm-ar or ar
    # TODO: Temp solution, assumes it's system-wide, add support for non-system wide
    def ArchiveProgram(self):
        if self.LlvmArPath != "":
            return "llvm-ar"
        elif self.ArPath != "":
            return "ar"
        else:
            Logger.Logger(5, "Cannot create llvm-ar or ar. Both tools cannot be found")

    def ArgArchive():
        return " rcs"

    def UsingLld(self, Arch):
        if self._LldUsed is True and Arch.startswith("x86_64"):
            return True
        return False

    def CanAdvanceFeatures(self, Arch):
        if self.UsingLld(Arch) is True:
            if self.LlvmArPath is not None and self.LlvmArPath != "":
                return True
        return False

    def SDKVersionCorrect():
        pass

    def GetResponseName(self, LinkEnv, OutputFile):
        return os.path.join(
            LinkEnv.IntermediateDir, os.path.basename(OutputFile) + ".rsp"
        )

    def ArchiveAndIndex(self, LinkEnv, OutputActionList):
        Archive = Action.Action

        Archive.CommandPath = self.ArchiveProgram()

        Archive.Arguments = "-c '"

        Archive.CreateImportLib = True

        OutputFile = LinkEnv.OutputDir
        Archive.OutputItems.append(OutputFile)

        Arg = (
            ' "'
            + self.ArPath
            + '" '
            + self.ArgArchive
            + ' "'
            + os.path.abspath(OutputFile)
        )
        Archive.Arguments += Arg

        InputFiles = []

        for File in LinkEnv.InputFiles:
            Temp = os.path.abspath(File)
            InputFiles.append('"' + Temp + '"')

        ResponsePath = self.GetResponseName(LinkEnv, OutputFile)

        # FIXME: Add support for not generating project files support (Requires class that doesn't exist yet) This will create intermediate file and add it to precondition list

        if self.LlvmArPath is None or self.LlvmArPath == "":
            Archive.Arguments += (
                ' && "' + self.RanlibPath + '" "' + os.path.abspath(OutputFile) + '"'
            )

        Archive.Arguments += " " + LinkEnv.AdditionalArgs

        Archive.Arguments += "'"

        OutputActionList.append(Archive)

        return OutputFile

    # FIXME: ADD IMPORTS AFTER ADDING CXX LIBRARY!
    def _ImportCXX(self, Arch):
        Ret = ""
        CanUse = self.UseLibCXX(Arch)
        if CanUse is True:
            Ret += "-nostdinc++"
        return Ret

    def _AddSanitize(self):
        Ret = ""
        if self.Option is not None and self.Option.UseAddressSanitizer is True:
            Ret += " -fsanitize=address"
        if self.Option is not None and self.Option.UseThreadSanitizer is True:
            Ret += " -fsanitize=thread"
        if self.Option is not None and self.Option.UseUnknownSanitizer is True:
            Ret += " -fsanitize=undefined"
        return Ret

    def _Global_Clang_Flags(self):
        Ret = " -Wno-tautological-compare -Wno-unused-private-field --Wno-undefined-bool-conversion"
        return Ret

    def _Optimize(self, CompileEnv):
        if CompileEnv.Optimize is False:
            Ret = " -O0"
        elif (
            self.Option.UseAddressSanitizer is True
            or self.Option.UseTreeadSanitizer is True
        ):
            Ret = " -O1 -g"

            if self.OptionUseAddressSanitizer is True:
                Ret += " -fno-optimize-sibling-calls -fno-omit-frame-pointer"
        else:

            Ret = " -O2"

        return Ret

    def _OutputConfig(self, Config):
        Ret = ""
        if Config == "Final":
            Ret = " -Wno-unused-value -fomit-frame-pointer"
        elif Config == "Debug":
            Ret = " -fno-inline -fno-omit-frame-pointer -fstack-protector"
        return Ret

    def _Exceptions(self, Bool):
        if Bool is True:
            Ret = " -fexceptions -DUSE_EXCEPTIONS=1"
        else:
            Ret = " -fno-exceptions"

        return Ret

    def _CrossCompile(self, Arch):
        Ret = ""

        if self.IsCrossCompiling is False:
            return ""

        if self.IsUsingClang is True and (Arch is not None or Arch != ""):
            Ret += " -target " + Arch

        # Ret += ' --sysroot="' + self.BasePath + '"' # FIXME: This breaks my current code, since we are using system shit for now, once I replace those code, re-add this

        return Ret

    # Global Arguments that we will use for both Compiling and Linking
    def GetGlobalArg(self, CompileEnv):
        Ret = " -c -pipe"

        Ret += self._ImportCXX(CompileEnv.Arch)

        Ret += self._AddSanitize()

        Ret += " -Wall -Werror"

        if not CompileEnv.Arch.startswith("X86_64") and CompileEnv.Arch.startswith(
            "AARCH64"
        ):
            Ret += " -funwind-tables"

        Ret += (
            " -Wsequence-point -Wdelete-non-virtual-dtor"
            + self.ArchSwitch(CompileEnv.Arch)
            + " -fno-math-errno"
        )

        if CompileEnv.HideSymbols is True:
            Ret += " -fvisibility=hidden -fvisibility-inlines-hidden"

        # TODO: Add GCC Support

        if self.IsUsingClang is True:

            Ret += self._Global_Clang_Flags()

        Ret += " -Wno-unused-variable -Wno-unused-function -Wno-switch -Wno-unknown-pragmas -Wno-gnu-string-literal-operator-template -Wno-invalid-offsetof"

        if CompileEnv.PGOOptimize is True:
            Ret += (
                ' -Wno-backend-plugin -fprofile-instr-use="'
                + os.path.join(CompileEnv.PGODirectory, CompileEnv.PGOFilePrefix)
                + '"'
            )

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

    def _SetPrintedDetails(self, CompileEnv):
        if self.HasPrintedDetails is False:
            self.Print(CompileEnv)

            if self.MultiArchRoot is not None and self.MultiArchRoot != "":
                if self.SDKVersionCorrect is False:
                    raise ValueError("FATAL: ThirdParty for Linux is incomplete!")

            self.HasPrintedDetails is True

    # Compiles the list of files together
    def CompileFiles(self, CompileEnv, InputFilesList, DirOutput, OutputActionList):

        Logger.Logger(1, "Input Files List: " + str(InputFilesList))
        Logger.Logger(1, "Directory Output: " + DirOutput)

        Args = self.GetGlobalArg(CompileEnv)

        PCH = ""

        self._SetPrintedDetails(CompileEnv)

        if self.CanAdvanceFeatures(CompileEnv.Arch) is False:
            if CompileEnv.AllowLTCG is True or CompileEnv.PGOOptimize is True:
                Logger.Logger(
                    5,
                    "LTCG and/or PGO Optimize cannot be true if we are not allowed to use advance features!",
                )

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

        for Item in InputFilesList:

            NewAction = Action.Action()

            NewAction.InputFiles.append(Item)  # Store all code files into InputFiles

            NewAction.PreconditionItems.extend(CompileEnv.ForceIncFiles)

            NewArgs = ""

            Extension = (os.path.splitext(os.path.abspath(Item))[1]).lower()

            # TODO: Add support for other file extension
            if CompileEnv.PCH_Act == CompileEnvironment.PCHAction.Create:
                NewArgs = self.ArgPCH()

            # Assume it's C++
            else:
                NewArgs = self.ArgCPP()
                NewArgs += PCH

            for F in CompileEnv.ForceIncFiles:
                NewArgs += ' -include "' + os.path.abspath(F) + '"'

            NewAction.PreconditionItems.append(Item)

            if CompileEnv.PCH_Act == CompileEnvironment.PCHAction.Create:
                InPCH = os.path.join(DirOutput, os.path.abspath(Item) + ".gch")

                CPPOut.PCHFile = InPCH

                NewAction.OutputItems.append(InPCH)

                NewArgs += ' -o "' + os.path.abspath(InPCH) + '"'

            else:

                if CompileEnv.PCH_Act == CompileEnvironment.PCHAction.Include:
                    NewAction.PreconditionItems.append(CompileEnv.PCHFile)
                    NewAction.UsingPCH = True

                Obj = os.path.join(DirOutput, os.path.basename(Item) + ".o")

                CompileEnv.Out.ObjectFiles.append(Obj)
                NewAction.OutputItems.append(Obj)

                NewArgs += ' -o "' + os.path.abspath(Obj) + '"'

            NewArgs += ' "' + os.path.abspath(Item) + '"'

            if CompileEnv.GenerateDependFile is True:
                DependFile = os.path.join(DirOutput, os.path.basename(Item) + ".d")
                NewArgs += ' -MD -MF "' + os.path.abspath(DependFile) + '"'
                NewAction.OutputItems.append(DependFile)
                NewAction.DependencyListFile = DependFile

            NewAction.CurrentDirectory = Dir_Manager.Engine_Directory

            if self.ClangPath is not None and self.ClangPath != "":
                NewAction.CommandPath = self.ClangPath

            elif self.GCCPath is not None and self.GCCPath != "":
                NewAction.CommandPath = self.GCCPath
            else:
                Logger.Logger(5, "CLANGPATH AND GCCPATH IS EMPTY OR NONE!")

            AllArgs = Args + NewArgs + CompileEnv.AdditionalArgs

            # FIXME: REPLACE THIS WITH CUSTOM FUNCTION, LET'S JUST CREATE A NEW FILE VIA NORMAL METHOD FOR NOW!

            RespFileName = os.path.join(DirOutput, os.path.basename(Item) + ".rsp")

            Logger.Logger(2, "Creating dir: " + RespFileName)

            os.makedirs(os.path.dirname(RespFileName), exist_ok=True)

            RespFile = open(RespFileName, "w")

            RespFile.write(AllArgs)

            RespFile.close()

            CompileEnv.LinkEnvPrecondition.append(
                RespFileName
            )  # Put's Response name into LinkEnvPrecondition

            # NewAction.PreconditionItems.append(RespFileName)

            NewAction.Arguments = "@" + RespFileName

            NewAction.UsingGCCCompiler is True

            if CompileEnv.PCH_Act is True:
                if (
                    CompileEnv.PCH_Act == CompileEnvironment.PCHAction.Create
                    or CompileEnv.AllowRemotelyCompiledPCHs is True
                ):
                    NewAction.CanRunRemotely = True

            OutputActionList.append(NewAction)

        return CPPOut

    def _LinkArgs(self, LinkEnv):
        Ret = ""

        if self.UsingLld(LinkEnv.Arch) is True and LinkEnv.IsBuildingDynamic is False:
            Ret += " -Wl,-fuse-ld=lld"

        Ret += " -rdynamic"

        if LinkEnv.IsBuildingDynamic is True:
            Ret += " -shared"
        else:
            Ret += " -Wl,--unresolved-symbols=ignore-in-shared-libs"

        if self.Option.UseAddressSanitizer is True:
            Ret += " -g -fsanitize=address"

        elif self.Option.UseThreadSanitizer is True:
            Ret += " -g -fsanitize=thread"

        elif self.Option.UseUnknownSanitizer is True:
            Ret += " -g -fsanitize=undefined"

        Ret += ' -Wl,-rpath="${ORIGIN}" -Wl,-rpath-link="${ORIGIN}"'

        Ret += (
            " -Wl,-rpath='${ORIGIN}/../../bin/Linux' -Wl,-rpath='${ORIGIN}/ThirdParty'"
        )

        Ret += " -Wl,--as-needed -Wl,--hash-style=gnu -Wl,--build-id"

        if self.NotUsingPIE is True and LinkEnv.IsBuildingDynamic is False:
            Ret += " -Wl,-nopie"

        if LinkEnv.PGOOptimize is True:
            Ret += (
                ' -Wno-backend-plugin -fprofile-instr-use="'
                + os.path.join(LinkEnv.PGODirectory, LinkEnv.PGOFilePrefix)
                + '"'
            )

        elif LinkEnv.PGOProfile is True:
            Ret += " -fprofile-generate"

        if LinkEnv.AllowLTCG is True:
            Ret += " -flto"

        if self.IsCrossCompiling is True:

            if self.IsUsingClang is True:

                Ret += " -target " + LinkEnv.Arch

                # Ret += ' "--sysroot=' + BasePath + '"' # FIXME: This breaks my current code, since we are using system shit for now, once I replace those code, re-add this

                Ret += "-B" + self.BasePath + "/usr/lib/"

                Ret += "-B" + self.BasePath + "/usr/lib64/"

                Ret += "-L" + self.BasePath + "/usr/lib/"

                Ret += "-L" + self.BasePath + "/usr/lib64/"

        return Ret

    def _LinkGroups(self, LinkEnv, OutputResp, OutputAction):

        OutputResp.append(" --start-group")

        ExternalLibs = ""

        for Item in LinkEnv.AdditionalLibs:
            Extension = os.path.splitext(Item)[1]  # Get extension

            if os.path.dirname(Item) is None or os.path.dirname(Item) == "":
                ExternalLibs += " -l" + Item

            elif Extension == ".a":

                Abs = os.path.abspath(Item)

                # Add quotes if there's a space, so that there wouldn't be any errors
                if " " in Abs:
                    Abs = '"' + Abs + '"'

                if LinkEnv.IsBuildingDynamic is True and (
                    "libcrypto" in Abs or "libssl" in Abs
                ):
                    OutputResp.append(" --whole-archive" + Item + " --no-whole-archive")

                else:
                    OutputResp.append(" " + Item)

                AllFiles = File_Manager.GetAllFilesFromDir(Item)
                # OutputAction.PreconditionItems.append(AllFiles)

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

    # TODO: Add windows support!
    def _STEP1LinkShellFiles(self, LinkEnv, Output, Com, Action):
        LinkName = "link-" + os.path.basename(Output) + ".sh"

        LinkFile = os.path.join(LinkEnv.LocalShadowDir, LinkName)

        Logger.Logger(2, "Creating ShadowDir: " + LinkEnv.LocalShadowDir)

        os.makedirs(LinkEnv.LocalShadowDir, exist_ok=True)

        Logger.Logger(2, "Creating file: " + LinkFile)

        with open(LinkFile, "w") as f:
            Logger.Logger(2, "writing: " + LinkFile)
            f.write("#!/bin/sh\n")
            f.write("set -o errexit\n")
            f.write(Com + "\n")
            # f.write(self.GetEncodeCommand(LinkEnv, Output)) # FIXME: Readd this once we add Breakpad!

        Action.CommandPath = "/bin/sh"
        Action.Arguments = LinkFile

        LinkScriptFile = os.path.join(LinkEnv.LocalShadowDir, "remove-sym.ldscript")

        if os.path.exists(LinkScriptFile):
            Logger.Logger(2, "Removing file: " + LinkScriptFile)
            # os.remove(LinkScriptFile)

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
            f.write(Com + "\n")
            f.write("TIMESTAMP='stat --format %y \"" + os.path.abspath(Output) + '"\n')
            f.write("cp " + RelinkFile + " " + os.path.abspath(Output) + "\n")
            f.write(
                "mv "
                + os.path.abspath(Output)
                + ".temp "
                + os.path.abspath(Output)
                + "\n"
            )
            f.write(self.GetEncodeCommand(LinkEnv, Output) + "\n")
            f.write('touch -d "$TIMESTAMP"' + os.path.abspath(Output))

        Action.CommandPath = "/bin/sh"
        Action.Arguments = '"' + RelinkFile + '"'
        Action.InputFiles.append(RelinkFile)

    def LinkFiles(self, LinkEnv, ImportLibraryOnly, OutputActionList):

        if (
            LinkEnv.AllowLTCG is True
            or LinkEnv.PGOProfile is True
            or LinkEnv.PGOOptimize
        ) and self.CanAdvanceFeatures(LinkEnv.Arch) is False:
            Logger.Logger(
                5,
                "FATAL: AllowLTCG, PGOProfile, and/or PGOOptimize is true, but we cannot use advance features!",
            )

        if LinkEnv.IsBuildingLibrary is True or ImportLibraryOnly is True:
            return self.ArchiveAndIndex(LinkEnv, OutputActionList)

        RPath = []

        NewAction = Action.Action()

        NewAction.InputFiles.extend(LinkEnv.InputFiles)

        NewAction.PreconditionItems.extend(LinkEnv.LinkEnvPrecondition)

        NewAction.CurrentDirectory = Dir_Manager.Engine_Directory

        Com = ""

        if self.ClangPath is not None and self.ClangPath != "":
            Com += '"' + self.ClangPath + '"'

        else:
            Com += '"' + self.GCCPath + '"'

        Com += self._LinkArgs(LinkEnv)

        NewAction.CreateImportLib = LinkEnv.IsBuildingDynamic

        Output = LinkEnv.OutputPaths[0]

        NewAction.OutputItems.append(Output)

        # TODO: Add description debugging support

        Com += " -o " + os.path.abspath(Output)

        Resp = []

        for Item in LinkEnv.InputFiles:

            # print(LinkEnv.InputFiles)

            Resp.append(os.path.abspath(Item) + " ")
            # FIXME: THIS IS THE ISSUE THAT CAUSE ENDLESS LOOP IN ACTIONLISTMANAGER! \/
            # NewAction.PreconditionItems.append(Item)

        if LinkEnv.IsBuildingDynamic is True:
            Resp.append(" -soname=" + Output)

        AllLib = LinkEnv.LibraryPaths  # All libs combined

        for Item in LinkEnv.AdditionalLibs:

            ItemPath = os.path.dirname(Item)

            # If Item contains Plugin or ThirdParty, and is not the absolute file
            if ("Plugin" in Item or "bin/ThirdParty" in Item) and os.path.dirname(
                Item
            ) != os.path.abspath(Output):

                Relative = os.path.relpath(Item, os.path.dirname(Output))

                if (
                    self.IsCrossCompiling is True
                    and Dir_Manager.Engine_Directory in Relative
                ):
                    Temp = Relative.replace(Dir_Manager.Engine_Directory, "")

                    # If we are on Linux Root Directory, we just need to move back the directory, otherwise we will include Temp
                    Relative = "../../../"
                    if not Temp.startswith("/"):
                        Relative += Temp

                if Relative not in RPath:
                    RPath.append(Relative)
                    Resp.append(' -rpath=$"{{ORIGIN}}' + Relative + '"')

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

        # NewAction.PreconditionItems.append(RespFile)

        Com += " -Wl,--start-group" + ExternalLibs + " -Wl,--end-group -lrt -lm"

        # FIXME: Add libCXX support

        if self.SDK.VerboseLinker is True:
            Com += " -Wl,--verbose -Wl,--trace -v"

        Com += LinkEnv.AdditionalArgs

        # Fix bugs if we accidently use windows shit
        # Com = Com.replace("{", "'{")
        # Com = Com.replace("}", "}'")
        # Com = Com.replace("$'{", "'${")

        self._STEP1LinkShellFiles(LinkEnv, Output, Com, NewAction)

        OutputActionList.append(NewAction)

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
                Logger.Logger(
                    2,
                    "Copying "
                    + str(ItemNoDir)
                    + "To name "
                    + str(ItemNoDir + ".0")
                    + "Under output directory "
                    + str(os.path.basename(DynamicOutputDir)),
                )
                os.system(
                    "cp "
                    + Item
                    + " "
                    + os.path.join(DynamicOutputDir, ItemNoDir + ".0")
                )

        return Output

    # Return's the actions to do after building
    def PostBuilt(self, File, LinkEnv, ActionList):
        Output = super().PostBuilt(File, LinkEnv, ActionList)

        if LinkEnv.IsBuildingDynamic is True and LinkEnv.CrossedReference is True:
            RelinkMap = os.path.join(
                LinkEnv.LocalShadowDir, Output + ".Relink_Action_Ran"
            )
            Output.append(RelinkMap)

        return Output

    @staticmethod
    def Print(CompileEnv):
        return ""
