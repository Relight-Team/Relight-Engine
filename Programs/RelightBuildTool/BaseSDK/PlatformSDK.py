import os
import platform
import sys
import subprocess

from . import Platform as Plat
from Internal import Logger


class PlatformSDK:

    InstalledSDKString = "Installed.txt"

    LastScriptVersion = "InstalledVersion.txt"

    EnvironmentVar = "EnvVars.txt"

    RootEnvironment = "RELIGHT_SDKS_ROOT"

    SetupEnviornment = "AutoSDKSetup"

    AllowAutoSDKSwitching = True

    _CheckedAutoSDKRoot = False

    _AutoSDKSystem = False

    _SDKStatusTrack = -1

    _LocalSetupAutoSDK = False

    _HostOS = platform.system()

    # Return's if the SDK support AutoSDK (AutoSDK is when the SDK can handle switching between different SDK during compilation runtime)
    def SupportAutoSDK(self):
        return False

    # Set and Return's if AutoSDK is supported
    def AutoSDKEnabled(self):
        EnvRoot = os.environ.get(self.RootEnvironment)

        if EnvRoot is not None:
            self._AutoSDKSystem = True

        return self._AutoSDKSystem

    # Whether or not the SDK is safe, as some SDK will break manual install
    def AutoSDKSafe(self):
        if not self.IsAutoSDKDestructive() and not self.HasAnyManualInstall():
            return True
        else:
            return False

    # Return's the SDK that is required by the platform
    def GetRequiredSDKString(self):
        return ""

    # The version of the script
    def GetRequiredScriptVersion():
        return "1.0"

    # Returns the target platform name
    def GetTargetPlatformName(self):
        return ""

    # Return's the path to the SDK for the platform
    def PathToPlatformAutoSDK(self):
        Path = ""
        EnvRoot = os.environ.get(self.RootEnvironment)

        if EnvRoot is not None and EnvRoot != "":
            Path = EnvRoot + "/host" + self._HostOS + "/" + self.GetTargetPlatformName()
        return Path

    # Return's the path to the SDK for the host platform
    def HostPlatformAutoSDKDir(self):
        EnvRoot = os.environ.get(self.RootEnvironment)

        if EnvRoot is None or EnvRoot == "":
            return None
        else:
            return EnvRoot + "/Host" + self._HostOS

    # Returns the SDK platform name + Setup Environment
    def PlatAutoSDKSetupEnvVar(self):
        return self.GetTargetPlatformName() + self.SetupEnviornment

    # Return the installed SDK Version if the Type is AutoSDK
    def GetCurrentlyInstalledSDK(self, PlatformSDKRoot):
        if os.path.isdir(PlatformSDKRoot):
            Path = os.path.join(PlatformSDKRoot, self.InstalledSDKString)

            Logger.Logger(2, "Writing file: " + Path)

            if os.path.exists(Path):
                with open(Path, "r") as file:
                    Version = file.readline().strip()
                    Type = file.readline().strip()

                if Type is not None and Type == "AutoSDK" and Version is not None:
                    return Version

        return ""

    # Return the latest run script version
    def GetLastRunScriptVersion(self, PlatformSDKRoot):
        if os.path.isdir(PlatformSDKRoot):
            Path = PlatformSDKRoot + "/" + self.LastScriptVersion

            if os.path.exists(Path):
                Logger.Logger(2, "Writing file: " + Path)
                with open(Path, "r") as file:
                    Version = file.readline().strip()

                if Version is not None:
                    return Version

        return ""

    # Writes the installed file, return's true if successful
    def SetCurrentlyInstalledSDK(self, InstallSDK):
        Path = self.PathToPlatformAutoSDK()

        if os.path.isdir(Path):
            GetSDK = self.PlatformSDKRoot + self.InstalledSDKString

            if os.path.exists(GetSDK):
                Logger.Logger(2, "Removing file: " + GetSDK)
                # os.remove(GetSDK)

            Logger.Logger(2, "Writing file: " + GetSDK)
            with open(GetSDK, "w") as file:
                file.write(InstallSDK + "\n")
                file.write("AutoSDK")
                file.close()
                return True
        return False

    # Set's up manual SDK
    def SetupManualSDK(self):
        if self.SupportAutoSDK() and self.AutoSDKEnabled():
            GetSDK = self.GetRequiredSDKString()
            GetPath = self.PathToPlatformAutoSDK()

            if not os.path.exists(GetPath):
                Logger.Logger(2, "Creating dir: " + GetPath)
                os.makedirs(GetPath)

            VersionFile = GetSDK + "/" + self.InstalledSDKString
            if os.path.exists(VersionFile):
                Logger.Logger(2, "Removing file: " + VersionFile)
                # os.remove(VersionFile)

            EnvtVar = GetSDK + "/" + self.EnvironmentVar
            if os.path.exists(EnvtVar):
                Logger.Logger(2, "Creating dir: " + EnvtVar)
                os.makedirs(EnvtVar)

            Logger.Logger(2, "Writing file: " + VersionFile)
            with open(VersionFile, "w") as file:
                file.write(GetSDK + "\n")
                file.write("ManualSDK")

    # Write's and replaces Version File, return's true if successful
    def SetLastRunScriptVersion(self, InLastScriptVersion):
        GetPath = self.PathToPlatformAutoSDK()

        if os.path.exists(GetPath):

            VersionFile = GetPath + "/" + self.LastScriptVersion
            if os.path.exists(VersionFile):
                Logger.Logger(2, "Removing file: " + VersionFile)
                # os.remove(VersionFile)

            Logger.Logger(2, "Writing file: " + VersionFile)
            with open(VersionFile, "w") as file:
                file.write(InLastScriptVersion)
                return True
        return False

    # Return's command file name based on Hook Type
    def GetHookExeName(self, HookType):
        if self._HostOS == "Windows":
            if HookType == "Uninstaller":
                return "Undo_Setup.bat"
            else:
                return "Setup.bat"
        else:
            if HookType == "Uninstaller":
                return "Undo_Setup.sh"
            else:
                return "Setup.sh"

    # Run the AutoSDK Hooks
    def RunAutoSDKHooks(self, SDKRoot, VersionString, HookType, CanBeNonExistent=True):
        if self.AutoSDKSafe() is False:
            return False

        if VersionString == "":
            return CanBeNonExistent

        SDKDir = SDKRoot + "/" + VersionString
        HookExe = SDKDir + self.GetHookExeName(HookType)

        Result = subprocess.run(HookExe, cwd=SDKDir)

        ExitCode = Result.returncode

        if ExitCode != 0:
            return False

        return True

    # Setup the AutoSDK Environment, return's Valid or Invalid
    def SetupEnvAutoSDK(self):
        PlatSDKRoot = self.PathToPlatformAutoSDK()

        if not self.SetupEnvAutoSDKFull(PlatSDKRoot):
            self.InvalidateInstalledAutoSDK()
            return "Invalid"

        return "Valid"

    # Setup AutoSDK Environment, return's true if succeeded
    def SetupEnvAutoSDKFull(self, SDKRoot):
        EnvVarFile = SDKRoot + "/" + self.EnvironmentVar

        if os.path.exists(EnvVarFile):
            Logger.Logger(2, "Writing file: " + EnvVarFile)
            with open(EnvVarFile, "r") as file:

                AddPath = []
                RemovePath = []
                EnvVarNames = []
                EnvVarValues = []

                NeedToWriteAutoEnvVar = True

                PlatSetupEnvVar = self.PlatAutoSDKSetupEnvVar()

                for Line in file:

                    if Line is None:
                        break

                    Parts = Line.split("=")

                    if len(list) < 2:
                        return False

                    if Parts[0].lower() == "addpath":
                        AddPath.append(Parts[1])

                    elif Parts[0].lower() == "strippath":
                        RemovePath.append(Parts[1])

                    else:
                        if Parts[0] == PlatSetupEnvVar:
                            NeedToWriteAutoEnvVar = False

                        EnvVarNames.append(Parts[0].strip())
                        EnvVarValues.append(Parts[1].strip())

                i = 0

                while i < len(EnvVarNames):

                    EnvVarN = EnvVarNames[i]

                    EnvVarV = EnvVarValues[i]

                    os.environ[EnvVarN] = EnvVarV

                    i += 1

                OriginalPathVar = os.getenv("PATH")

                PathDelimiter = Plat.GetPathDelimiter()

                PathVars = []

                if OriginalPathVar is not None and OriginalPathVar != "":
                    PathVars = OriginalPathVar.split(PathDelimiter)

                NewPathVars = PathVars

                for Remove in RemovePath:
                    for Var in PathVars:
                        if Remove.upper() in Var.upper():
                            NewPathVars.remove(Var)

                for Add in AddPath:
                    for Var in PathVars:
                        if Add.lower() == Var.lower():
                            NewPathVars.remove(Var)

                for Add in AddPath:
                    if Add not in NewPathVars:
                        NewPathVars.append(Add)

                NewPath = PathDelimiter.join(NewPathVars)

                os.environ["PATH"] = NewPath

                if NeedToWriteAutoEnvVar is True:
                    Logger.Logger(2, "Writing file: " + EnvVarFile)
                    with open(EnvVarFile, "a") as file2:
                        file2.write(PlatSetupEnvVar + "=1\n")

                    os.enviorn[self.PlatformSetupEnvVar] = "1"

                self._LocalSetupAutoSDK = True

                return True

            return False

    # Removes all Installed files from AutoSDK
    def InvalidateInstalledAutoSDK(self):
        PlatformSDKRoot = self.PathToPlatformAutoSDK()

        if os.path.isdir(PlatformSDKRoot):

            EnvVarFile = PlatformSDKRoot + "/" + self.EnvironmentVar
            if os.path.exists(EnvVarFile):
                Logger.Logger(2, "Removing file: " + EnvVarFile)
                # os.remove(EnvVarFile)

            VersionFile = PlatformSDKRoot + "/" + self.LastScriptVersion
            if os.path.exists(VersionFile):
                Logger.Logger(2, "Removing file: " + VersionFile)
                # os.remove(VersionFile)

            SDKFilename = PlatformSDKRoot + "/" + self.InstalledSDKString
            if os.path.exists(SDKFilename):
                Logger.Logger(2, "Removing file: " + SDKFilename)
                # os.remove(SDKFilename)

    # Returns "Valid" if we have the Required SDK Installed, "Invalid" otherwise
    def HasRequiredAutoSDKInstalled(self):
        if self.SupportAutoSDK() and self.AutoSDKEnabled():
            AutoSDKRoot = self.PathToPlatformAutoSDK()

            if AutoSDKRoot != "":
                ScriptVersionMatches = False
                CurrentScriptVersion = self.GetLastRunScriptVersion(AutoSDKRoot)

                if (
                    CurrentScriptVersion != ""
                    and CurrentScriptVersion == self.GetRequiredScriptVersion()
                ):
                    ScriptVersionMatches = True

                EnvVarFile = AutoSDKRoot + "/" + self.EnvironmentVar

                EnvVarFileExists = os.path.exists(EnvVarFile)

                CurrentSDKString = self.GetCurrentlyInstalledSDK(AutoSDKRoot)

                if (
                    EnvVarFileExists is True
                    and CurrentSDKString != ""
                    and CurrentSDKString == self.GetRequiredSDKString()
                    and ScriptVersionMatches is True
                ):
                    return "Valid"
                return "Invalid"

        return "Invalid"

    # Returns true if AutoSDK had been setup
    def HasSetupAutoSDK(self):
        if self._LocalSetupAutoSDK is True or self.HasParentProcessAutoSDK() is True:
            return True
        return False

    # Return's true if we have the parent process SDK
    def HasParentProcessAutoSDK(self):
        SetupVarName = self.PlatAutoSDKSetupEnvVar()
        AutoSDKSetup = os.getenv(SetupVarName)

        if AutoSDKSetup is not None and AutoSDKSetup != "":
            return True
        return False

    # Return's true if we have the required manual SDK
    def HasRequiredManualSDK(self):

        if self.HasSetupAutoSDK() is True:
            return "Invalid"

        return self.InternalHasRequiredManualSDK()

    # Return's true if we have any manual install
    def HasAnyManualInstall(self):
        return False

    # Used in HasRequiredManualSDK()
    def InternalHasRequiredManualSDK(self):
        pass  # Will be overwritten with child class

    # Return's true if we are allowed to have invalid manual installs
    def AllowInvalidManualInstall(self):
        return True

    # If true, we will use AutoSDK over ManualSDK, otherwise, we will use ManualSDK over AutoSDK
    def PreferAutoSDK(self):
        return True

    # If true, then parallel installs will overwrite existing files
    def IsAutoSDKDestructive(self):
        return False

    # Setup the autoSDK
    def SetupAutoSDK(self):
        if (
            self.AutoSDKSafe() is True
            and self.SupportAutoSDK() is True
            and self.AutoSDKEnabled() is True
        ):
            if self.HasRequiredAutoSDKInstalled == "Invalid":
                self._SDKStatusTrack = -1
                AutoSDKRoot = self.PathToPlatformAutoSDK()
                CurrentSDKString = self.GetCurrentlyInstalledSDK(AutoSDKRoot)

                if not self.RunAutoSDKHooks(
                    AutoSDKRoot, CurrentSDKString, "Uninstaller"
                ):
                    self.InvalidateInstalledAutoSDK()
                    return None

                self.InvalidateInstalledAutoSDK()

                if not self.RunAutoSDKHooks(
                    AutoSDKRoot, CurrentSDKString, "Installer", False
                ):
                    self.RunAutoSDKHooks(
                        AutoSDKRoot, CurrentSDKString, "Uninstaller", False
                    )
                    return None

                EnvVarF = AutoSDKRoot + "/" + self.EnvironmentVar

                if not os.path.exists(EnvVarF):
                    self.RunAutoSDKHooks(
                        AutoSDKRoot, CurrentSDKString, "Uninstaller", False
                    )
                    return None

                self.SetCurrentlyInstalledSDK(self.GetRequiredSDKString())

                self.GetLastRunScriptVersion(self.GetRequiredScriptVersion())

            self.SetupEnvAutoSDK()

    # Return's "Valid" if we have the required SDK Installed
    def HasRequiredSDKsInstalled(self):
        if self._SDKStatusTrack == -1:
            HasManualSDK = False
            HasAutoSDK = False

            if self.HasRequiredManualSDK():
                HasManualSDK = True

            if self.HasRequiredAutoSDKInstalled():
                HasAutoSDK = True

            if self.HasManualSDK is True or HasAutoSDK is True:
                self._SDKStatusTrack == 1

        if self._SDKStatusTrack == 1:
            return "Valid"

        else:
            return "Invalid"

    # Manages and validates the SDK
    def ManageAndValidate(self):
        if self.AllowAutoSDKSwitching is True and not self.HasParentProcessAutoSDK():

            SetSDK = False
            aHasRequiredManualSDK = False

            if self.HasRequiredManualSDK() == "Valid":
                aHasRequiredManualSDK = True

            if self.AutoSDKSafe() and (
                self.PreferAutoSDK() or not aHasRequiredManualSDK
            ):
                self.SetupAutoSDK()
                SetSDK = True

            if aHasRequiredManualSDK is True and (
                self.HasRequiredAutoSDKInstalled() != "Valid"
            ):
                self.SetupManualSDK()
                SetSDK = True

            if SetSDK is False:
                self.InvalidateInstalledAutoSDK()

        self.Print()

    # Prints information about the SDK
    def Print(self):
        pass
