import argparse
from Configuration import Arguments
from Configuration import RelightBuildTool_Info as RBT_INFO

from Internal import Logger


def main():
    Args = GetArgs()

    Logger.Logger(3, "Setting Up Logger...", Args.GetAndParse("NoMessages"), Args.GetAndParse("NoLog"))

    if Args.GetAndParse("NoLog") is not True:
        F = open("log.txt", "w")
        F.write("")
        F.close()

    # Set mode to default

    if Args.GetAndParse("Mode") is None:
        ModeToUse = "Build"
    else:
        ModeToUse = Args.GetAndParse("Mode")

    if ModeToUse.lower() == "build":
        from Modes import BuildMode as Mode
    elif ModeToUse.lower() == "clean":
        from Modes import CleanMode as Mode
    elif ModeToUse.lower() == "projectfiles":
        Logger.Logger(5, "Project Files are not yet implemented due to lack of .RProject reader. Add this in future!")
    else:
        Logger.Logger(5, "The mode is " + str(ModeToUse) + " which we cannot detect!")

    PrintIntro(ModeToUse)

    Mode.Main(Args)


def GetArgs():
    Parser = argparse.ArgumentParser(
        description="Builder tool for Relight Engine"
    )  # Description for RBT

    # Global
    Parser.add_argument(
        "-Mode",
        type=str,
        metavar="(Global) [STRING]",
        help="The mode we are using (Default: Build)",
    )  # Options: Build, Clean, ProjectFiles, Test
    Parser.add_argument(
        "-Project",
        type=str,
        metavar="(Global) [PATH STRING]",
        help="The .RProject directories + file(s) we are using",
    )

    Parser.add_argument(
        "-Target",
        type=str,
        metavar="(Global) [PATH STRING]",
        help="The .Target file(s) we are using (Will be used if -Project is not defined",
    )

    Parser.add_argument(
        "-Platform",
        type=str,
        metavar="(Global) [STRING]",
        help="The platform(s) we are using (Default: Building Platform)",
    )

    Parser.add_argument(
        "-Arch",
        type=str,
        metavar="(Global) [STRING]",
        help="The Arch(es) we are using",
    )

    Parser.add_argument(
        "-TargetDir",
        type=str,
        metavar="(Global) [PATH STRING]",
        help="The custom directory to search for target file (use if we have no project file and its not an engine target)",
    )

    Parser.add_argument(
        "-BuildType",
        type=str,
        metavar="(Global) [STRING]",
        help="The Build Type we are using (Debug, Development, or Final)",
    )

    Parser.add_argument(
        "-NoMessages",
        type=str,
        metavar="[BOOL]",
        help="If true, then we will not print log messages",
    )

    Parser.add_argument(
        "-NoLog",
        type=str,
        metavar="[BOOL]",
        help="If true, then we will not log messages in log.txt",
    )

    # Build Mode
    Parser.add_argument(
        "-Module",
        type=str,
        metavar="(Build) [STRING]",
        help="Compile any module(s), even if its not defined in the target file",
    )

    Parser.add_argument(
        "-Precompile",
        type=bool,
        metavar="(Build) [BOOL]",
        help="If true, we will use existing binaries for engine modules (Default: False)",
    )

    Parser.add_argument(
        "-Cook",
        type=bool,
        metavar="(Build) [BOOL]",
        help="If true, we will run RelightCookerTool on the project",
    )


    # Clean Mode
    Parser.add_argument(
        "-Ignore-Bin",
        type=bool,
        metavar="(Clean) [BOOL]",
        help="Ignore's the bin directory",
    )

    Parser.add_argument(
        "-Ignore-Intermediate",
        type=bool,
        metavar="(Clean) [BOOL]",
        help="Ignore's the Intermediate directory",
    )

    Parser.add_argument(
        "-Ignore-Cooked",
        type=bool,
        metavar="(Clean) [BOOL]",
        help="Ignore's the Cooked directories (Configs, shaders, Paks, and Content)",
    )

    Parser.add_argument(
        "--Ignore-All-Confirmation",
        type=bool,
        metavar="(Clean) [BOOL]",
        help="(NOT RECOMMENDED) if true, we will skip confirmation section",
    )

    Parser.add_argument(
        "--Verify-Sus-Directories",
        type=bool,
        metavar="(Clean) [BOOL]",
        help="If true, then instead of closing the cleaner if the directory is suspicious, it will ask to verify",
    )

    Parser.add_argument(
        "--Clean-Everything",
        type=bool,
        metavar="(Clean) [BOOL]",
        help="If true, then instead of checking each extension, we will just delete every file (warning, ensure everything is backed up before doing this!)",
    )

    # Parse all args into custom class so we can use it!
    ArgsTemp = Parser.parse_args()

    Args = Arguments.Args(ArgsTemp)

    return Args


def PrintIntro(Mode):
    print("====================")
    print(RBT_INFO.Name)
    print(RBT_INFO.Copyright)
    print("License: " + RBT_INFO.License)
    print("Version: " + RBT_INFO.Version)
    print("Mode: " + Mode)
    print("====================")


if __name__ == "__main__":
    main()
