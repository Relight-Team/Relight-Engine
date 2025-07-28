import argparse
from Configuration import Arguments
from Configuration import RelightBuildTool_Info as RBT_INFO

from Internal import Logger


def main():
    Args = GetArgs()

    # Set mode to default

    if Args.GetAndParse("Mode") is None:
        ModeToUse = "Build"
    else:
        ModeToUse = Args.GetAndParse("Mode")

    if ModeToUse.lower() == "build":
        from Modes import BuildMode as Mode
    elif ModeToUse.lower() == "clean":
        from Modes import CleanMode as Mode
    else:
        Logger.Logger(5, "The mode is " + str(ModeToUse + " which we cannot detect!"))

    PrintIntro()

    Mode.Main(Args)


def GetArgs():
    Parser = argparse.ArgumentParser(
        description="Builder tool for Relight Engine"
    )  # Description for RBT

    # Global
    Parser.add_argument(
        "-Mode",
        type=str,
        metavar="[STRING]",
        help="The mode we are using (Default: Build)",
    )  # Options: Build, Clean, ProjectFiles, Test

    # Build Mode
    Parser.add_argument(
        "-Project",
        type=str,
        metavar="[PATH STRING]/[PATH ARRAY]",
        help="The .RProject file(s) we are compiling",
    )

    Parser.add_argument(
        "-Target",
        type=str,
        metavar="[PATH STRING]/[PATH ARRAY]",
        help="The .Target file(s) we are compiling (Will be used if -Project is not defined",
    )

    Parser.add_argument(
        "-Platform",
        type=str,
        metavar="[STRING]/[ARRAY]",
        help="The platform(s) we are compiling (Default: Building Platform)",
    )

    Parser.add_argument(
        "-Module",
        type=str,
        metavar="[STRING]/[ARRAY]",
        help="Compile any module(s), even if its not defined in the target file",
    )

    Parser.add_argument(
        "-Precompile",
        type=bool,
        metavar="[BOOL]",
        help="If true, we will use existing binaries for engine modules (Default: False)",
    )

    Parser.add_argument(
        "-TargetDir",
        type=str,
        metavar="[PATH STRING]",
        help="The custom directory to search for target file (use if we have no project file and its not an engine target)",
    )

    # Parse all args into custom class so we can use it!
    ArgsTemp = Parser.parse_args()

    Args = Arguments.Args(ArgsTemp)

    return Args


def PrintIntro():
    print("====================")
    print(RBT_INFO.Name)
    print(RBT_INFO.Copyright)
    print("License: " + RBT_INFO.License)
    print("Version: " + RBT_INFO.Version)
    print("====================")


if __name__ == "__main__":
    main()
