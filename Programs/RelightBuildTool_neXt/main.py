import os
import platform
import argparse


def Main():

    BuildVersion = "0.5.0"

    RBT_Directory = os.getcwd()

    Engine_Directory = os.path.dirname(os.path.dirname(RBT_Directory)) ## Equivalent to /../..

    HostOS = platform.system() # Linux, Windows, or Darwin


    import Platform.RBT_Platform as LC

    # Required Arguments
    parser = argparse.ArgumentParser(description="Software Arguments")

    parser.add_argument('Target', type=str, help="The Target file")

    parser.add_argument('Platform', type=str, help="The platform for the desire output")

    #parser.add_argument('BuildCfg', type=str, help="The state of the output")

    # Optional Arguments

    parser.add_argument('--ProjectDebug', action='store_true', help="Prints each command of the project file while executing")

    parser.add_argument('--Rebuild', action='store_true', help="Build's all modules, even if they are already compiled")

    parser.add_argument('--Compiler', type=str, help="The compiler")

    parser.add_argument('--ProjectFile', type=str, help="The Project File")

    ## Set values

    args = parser.parse_args()


    TargetFile = args.Target

    TargetOS = args.Platform

    ProjectDebug = args.ProjectDebug

    Rebuild = args.Rebuild

    Compiler = args.Compiler

    ProjectType = args.ProjectFile

    if Compiler == None:
        # TODO: Add advance default system, for now we are just using clang++ as default
        Compiler = "clang++"

    # Set Default Project File
    if ProjectType == "" or ProjectType == "Default" or ProjectType is None:
        if platform.system() == "Linux":
            # If Make exist
            if LC.DoesFileExist(['make', '--version']):
                ProjectType = "Makefile"

    # === #

    ## Print title
    print("---------------------------------------------------------------")
    print("|                    Relight Build Tool                       |")
    print("---------------------------------------------------------------")
    print("RBT Version: " + BuildVersion)
    print("Engine Directory: " + Engine_Directory)
    print("Host OS: " + HostOS)
    print("Target OS: " + TargetOS)
    print("Compiler: " + Compiler)
    print("Project Type: " + ProjectType)
    print("Targeting: " + TargetFile)
    print("==========")
    print()


    if ProjectType == "Makefile":
        import ProjectFiles.Make.MakeFileGenerator as MFG
        ProjectFileClass = MFG.MakeFileGenerator()

    # Start Building the project file

    ProjectFileClass.IsCompilerSupported(Compiler)


    print("Generating " + ProjectType + " at: " + os.path.dirname(TargetFile))
    ProjectFileClass.Make(TargetFile, Engine_Directory, Compiler, TargetOS)

    print("Executing " + ProjectType + "...")
    # Execute Build File
    Comm = ProjectFileClass.RunBuildFile(os.path.dirname(TargetFile) + "/" + ProjectFileClass.ReturnProjectFileName(), Rebuild, ProjectDebug)

    LC.Exec(Comm)

    print()
    print("==== Finished ====")


Main()
