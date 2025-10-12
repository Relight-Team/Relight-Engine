import os

from Internal import Logger
from Readers import TargetReader
from Configuration import Directory_Manager

SkipDialog = False

DeleteAllFiles = False

GlobalArgs = None

VerifySus = False

# Things to keep track of
DeleteAllPlatforms = False

DeleteAllArch = False

DeleteAllBuildType = False

SourceDir = None

Arch = None
Platform = None
BuildType = None


# TODO - Add project support, assuming we are just typing in target
def Main(Args):

    global GlobalArgs, SkipDialog, DeleteAllFiles, VerifySus, DeleteAllPlatforms, DeleteAllBuildType, SourceDir, Arch, Platform, BuildType, DeleteAllArch

    GlobalArgs = Args

    Project = Args.GetAndParse("Project")
    Target = Args.GetAndParse("Target")
    Platform = Args.GetAndParse("Platform")
    Arch = Args.GetAndParse("Arch")
    TargetDir = Args.GetAndParse("TargetDir")
    BuildType = Args.GetAndParse("BuildType")
    ShouldIgnoreConfirm = Args.GetAndParse("Ignore_All_Confirmation")

    DeleteAllFiles = Args.GetAndParse("Clean_Everything")
    InVerifySus = Args.GetAndParse("Verify_Sus_Directories")

    # If project and target not set, we cannot run
    if Project == None and Target == None:
        Logger.Logger(
            5,
            "Project and Target not set, please set Project, if not, at least set Target",
        )

    # Skip dialog if set
    if ShouldIgnoreConfirm is True:
        Logger.Logger(
            4,
            "You are running No Confirmation Mode, this is dangerous as we will not ask to verify directories to delete, type 'Continue' if you wish to continue with this risk",
        )
        Continue = input("")
        if Continue.lower() == "continue":
            SkipDialog = True

    # Verify Sus directories if set
    if InVerifySus is True:
        Logger.Logger(
            4,
            "You are running Verify Suspicious directory mode, instead of quitting upon issue, we will ask you if we should continue, are you sure you want to continue, if so, type 'Continue'",
        )
        Continue = input("")
        if Continue.lower() == "continue":
            VerifySus = True

    if Platform == None:
        ConfirmMessage(
            "Platform not set, do you wish to delete all platform data?", True
        )
        DeleteAllPlatforms = True

    if Arch == None:
        ConfirmMessage("Arch not set, do you wish to delete all Arch data?", True)
        DeleteAllArch = True

    if BuildType == None:
        ConfirmMessage(
            "BuildType not set, do you wish to delete all BuildType data?", True
        )
        DeleteAllBuildType = True

    if Project is None:
        if TargetDir is not None:
            SourceDir = Directory_Manager.Engine_Directory

        FullTargetPath = os.path.join(TargetDir, Target + ".Target")

        ST = TargetReader.StartingTarget("")

        TR = TargetReader.Target(FullTargetPath, ST, None)

        CleanTarget(SourceDir, TR.Name)


# Collects and returns an array of subdirectory names from directory
def GetNamesFromDir(SubDir):

    Ret = []

    if not os.path.isdir(SubDir):
        return Ret

    Dirs = os.listdir(SubDir)

    for Dir in Dirs:

        FullDir = os.path.join(SubDir, Dir)

        if os.path.isdir(FullDir):
            Ret.append(Dir)
    return Ret


# Clean everything, ignore if we skip it in command line
def CleanTarget(TargetDir, Target):
    Platforms = []
    Arches = []
    BuildTypes = []

    SkipBin = False
    SkipInter = False

    # If the bin exist, we will use it, otherwise we will use Intermediate
    if os.path.isdir(os.path.join(TargetDir, "bin", Target)):
        A = os.path.join(TargetDir, "bin", Target)
        GetLists(A, "", Arches, Platforms, BuildTypes)

    else:
        Logger.Logger(4, "Target in bin is already deleted, skipping...")
        SkipBin = True

    if GlobalArgs.GetAndParse("Ignore-Bin") is not True and SkipBin == False:
        CleanBin(TargetDir, Target, Arches, Platforms, BuildTypes)

    if os.path.isdir(os.path.join(TargetDir, "Intermediate", "Build")):
        Platforms = []
        Arches = []
        BuildTypes = []

        A = os.path.join(TargetDir, "Intermediate", "Build")
        B = Target
        GetLists(A, B, Arches, Platforms, BuildTypes)
    else:
        Logger.Logger(4, "Intermediate is already deleted, skipping...")
        SkipInter = True

    if GlobalArgs.GetAndParse("Ignore-Intermediate") is not True and SkipInter == False:
        CleanIntermediate(Target, TargetDir, Arches, Platforms, BuildTypes)

    if GlobalArgs.GetAndParse("Ignore-Cooked") is not True and SkipBin == False:
        CleanCook(Target, TargetDir, Arches, Platforms, BuildTypes)


# Cleans binary directory
def CleanBin(TargetDir, Target, ArchList, PlatList, BuildTypeList):

    print("deleting binary files")

    ValidExtensions = [".exe", ".so", ".dll"]

    if not os.path.isdir(os.path.join(TargetDir, "bin", Target)):
        Logger.Logger(3, "Directory " + DirToClear + " is already cleaned, skipping...")
        return

    for Platform in PlatList:
        for Arch in ArchList:
            for BuildType in BuildTypeList:
                DirToClear = os.path.join(
                    TargetDir, "bin", Target, Platform, Arch, BuildType
                )
                CheckForSusPaths(DirToClear, Target)

                # If directory doesn't exist, we can skip it
                if not os.path.isdir(DirToClear):
                    Logger.Logger(
                        3,
                        "Directory " + DirToClear + " is already cleaned, skipping...",
                    )
                    continue

                ConfirmMessage("Do you wish to delete [" + str(DirToClear) + "]")

                for Root, SubDirList, Files in os.walk(DirToClear):
                    for File in Files:

                        if DeleteAllFiles is None:
                            Rootn, Ext = os.path.splitext(
                                File
                            )  # This is to check special condition on linux where the binary doesn't have extension

                            if (
                                any(File.endswith(Item) for Item in ValidExtensions)
                                or Ext == ""
                            ):
                                os.remove(os.path.join(Root, File))

                        # If DeleteAllFiles is true, then we will always delete every file in this directory
                        else:
                            if os.path.exists(os.path.join(Root, File)):
                                os.remove(os.path.join(Root, File))

        DeleteEmptyDirs(os.path.join(TargetDir, "bin", Target, Platform))


# Cleans intermediate directory
def CleanIntermediate(Target, TargetDir, ArchList, PlatList, BuildTypeList):

    print("deleting Intermediate files")

    ValidExtensions = [".o", ".obj", ".rsp", ".rsp.backup", ".d", ".cpp", ".sh"]

    for Platform in PlatList:
        for Arch in ArchList:
            for BuildType in BuildTypeList:
                DirToClear = os.path.join(
                    TargetDir,
                    "Intermediate",
                    "Build",
                    Platform,
                    Arch,
                    Target,
                    BuildType,
                )
                CheckForSusPaths(DirToClear, Target)

                # If directory doesn't exist, we can skip it
                if not os.path.isdir(DirToClear):
                    Logger.Logger(
                        3,
                        "Directory " + DirToClear + " is already cleaned, skipping...",
                    )
                    continue

                ConfirmMessage("Do you wish to delete [" + str(DirToClear) + "]")

                for Root, SubDirList, Files in os.walk(DirToClear):
                    for File in Files:

                        if DeleteAllFiles is None:
                            if any(File.endswith(Item) for Item in ValidExtensions):
                                os.remove(os.path.join(Root, File))

                        # If DeleteAllFiles is true, then we will always delete every file in this directory
                        else:
                            if os.path.exists(os.path.join(Root, File)):
                                os.remove(os.path.join(Root, File))

            DeleteEmptyDirs(
                os.path.join(TargetDir, "Intermediate", "Build", Platform, Arch, Target)
            )


# Cleans all cook content
# TODO - Doesn't clean all cook content yet
def CleanCook(Target, TargetDir, ArchList, PlatList, BuildTypeList):

    print("deleting Cooked files")

    ValidExtensions = [".cfg"]

    for Platform in PlatList:
        for Arch in ArchList:
            for BuildType in BuildTypeList:
                DirToClearConfig = os.path.join(
                    TargetDir, "bin", Target, Platform, Arch, BuildType, "Config"
                )
                DirToClearContent = os.path.join(
                    TargetDir, "bin", Target, Platform, Arch, BuildType, "Content"
                )
                DirToClearShaders = os.path.join(
                    TargetDir, "bin", Target, Platform, Arch, BuildType, "Shaders"
                )
                CheckForSusPaths(DirToClearConfig, Target)
                CheckForSusPaths(DirToClearContent, Target)
                CheckForSusPaths(DirToClearShaders, Target)

                # If directory doesn't exist, we can skip it
                if not os.path.isdir(DirToClearConfig):
                    Logger.Logger(
                        3,
                        "Directory "
                        + DirToClearConfig
                        + " is already cleaned, skipping...",
                    )
                if not os.path.isdir(DirToClearContent):
                    Logger.Logger(
                        3,
                        "Directory "
                        + DirToClearContent
                        + " is already cleaned, skipping...",
                    )
                if not os.path.isdir(DirToClearShaders):
                    Logger.Logger(
                        3,
                        "Directory "
                        + DirToClearShaders
                        + " is already cleaned, skipping...",
                    )

                ConfirmMessage("Do you wish to delete [" + str(DirToClearConfig) + "]")
                ConfirmMessage("Do you wish to delete [" + str(DirToClearContent) + "]")
                ConfirmMessage("Do you wish to delete [" + str(DirToClearShaders) + "]")

                # Each config file
                for Root, SubDirList, Files in os.walk(DirToClearConfig):
                    for File in Files:

                        if DeleteAllFiles is None:
                            Rootn, Ext = os.path.splitext(
                                File
                            )  # This is to check special condition on linux where the binary doesn't have extension

                            if (
                                any(File.endswith(Item) for Item in ValidExtensions)
                                or Ext == ""
                            ):
                                os.remove(os.path.join(Root, File))

                        # If DeleteAllFiles is true, then we will always delete every file in this directory
                        else:
                            if os.path.exists(os.path.join(Root, File)):
                                os.remove(os.path.join(Root, File))

                # Each Content file
                for Root, SubDirList, Files in os.walk(DirToClearContent):
                    for File in Files:

                        if DeleteAllFiles is None:
                            Rootn, Ext = os.path.splitext(
                                File
                            )  # This is to check special condition on linux where the binary doesn't have extension

                            if (
                                any(File.endswith(Item) for Item in ValidExtensions)
                                or Ext == ""
                            ):
                                os.remove(os.path.join(Root, File))

                        # If DeleteAllFiles is true, then we will always delete every file in this directory
                        else:
                            if os.path.exists(os.path.join(Root, File)):
                                os.remove(os.path.join(Root, File))

                # Each Shader file
                for Root, SubDirList, Files in os.walk(DirToClearShaders):
                    for File in Files:

                        if DeleteAllFiles is None:
                            Rootn, Ext = os.path.splitext(
                                File
                            )  # This is to check special condition on linux where the binary doesn't have extension

                            if (
                                any(File.endswith(Item) for Item in ValidExtensions)
                                or Ext == ""
                            ):
                                os.remove(os.path.join(Root, File))

                        # If DeleteAllFiles is true, then we will always delete every file in this directory
                        else:
                            if os.path.exists(os.path.join(Root, File)):
                                os.remove(os.path.join(Root, File))

    DeleteEmptyDirs(os.path.join(TargetDir, "bin", Target))


# If a check fails, we will print it
def FailOrAskToContinue(Text, Dir):
    if VerifySus == False:
        Logger.Logger(
            5,
            "Suspicious Directory detected: "
            + Text
            + " ["
            + str(Dir)
            + "], Exiting...",
        )
    else:
        Logger.Logger(
            4,
            "Suspicious Directory detected: "
            + Text
            + " ["
            + str(Dir)
            + "], Type 'Continue' if you wish to continue anyways",
        )
        Continue = input("")
        if not Continue.lower() == "continue":
            Logger.Logger(
                5,
                "Suspicious Directory Detected and user failed to give permission to continue",
            )


# Checks for issues about the path we are deleting
# TODO - Add more checks
def CheckForSusPaths(Path, TargetName):

    if not TargetName in Path:
        FailOrAskToContinue(
            "Target Name " + str(TargetName) + " instance not found in path", Path
        )

    if Path is None:
        FailOrAskToContinue("Path is None", Path)

    if Path == "":
        FailOrAskToContinue("Path is empty", Path)


# Ask if we should continue
def ConfirmMessage(Message, IsWarning=False):

    # If we are skipping dialog, do nothing
    if SkipDialog is True:
        return

    if IsWarning is True:
        Logger.Logger(4, Message)
    else:
        print(Message)

    print("Type 'Continue' to continue with operation, otherwise cleaner will quit")
    ShouldContinue = input("")

    if not ShouldContinue.lower() == "continue":
        Logger.Logger(5, "User denied continuation of cleaner")


def DeleteEmptyDirs(RootDir):

    for Root, SubDirList, Files in os.walk(RootDir, topdown=False):
        for Dirs in SubDirList:
            Full = os.path.join(Root, Dirs)
            if os.path.isdir(Full) and not os.listdir(Full):
                os.rmdir(Full)

        if os.path.isdir(Root) and not os.listdir(Root):
            os.rmdir(Root)


def GetLists(OSPathA, OSPathB, ArchList, PlatformList, BuildTypeList):
    if DeleteAllPlatforms is False:
        PlatformList.append(Platform)
    else:
        PlatformList.extend(GetNamesFromDir(os.path.join(OSPathA)))

    for Pl in PlatformList:

        if DeleteAllArch is False:
            ArchList.append(Arch)
        else:
            ArchList.extend(GetNamesFromDir(os.path.join(OSPathA, Pl)))

        for Ar in ArchList:

            if DeleteAllBuildType is False:
                BuildTypeList.append(BuildType)
            else:
                BuildTypeList.extend(
                    GetNamesFromDir(os.path.join(OSPathA, Pl, Ar, OSPathB))
                )
