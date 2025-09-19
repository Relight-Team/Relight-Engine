RCT_Name = "RelightCookerTool (Config Sync Prototype)"
RCT_Ver = "1.0.0"

import os
import argparse
import importlib
import subprocess
import inspect
import sys
from pathlib import Path

from BaseSDK import Cook

_Internal_Script_Dir = Path(__file__).resolve().parent

EngineDir = os.path.join("..", "..")

ExtraSDKDir = os.path.join("Extras", "CustomSDK")

sys.path.append(ExtraSDKDir)



def main():
    print("=====")
    print(RCT_Name)
    print(RCT_Ver)
    print()
    print("Asset, config, and shaders cooker")
    print("=====")

    Parser = argparse.ArgumentParser(
        description="Cooker tool for Relight Engine"
    )  # Description for RCT

    Parser.add_argument(
        "-Project",
        type=str,
        metavar="[PATH STRING]",
        help="The .RProject file and directory we are baking",
    )

    Parser.add_argument(
        "-Target",
        type=str,
        metavar="[PATH STRING]",
        help="The .RProject file and directory we are baking, alt if we cannot find Project file",
    )

    Parser.add_argument(
        "-SourceDir",
        type=str,
        metavar="[PATH STRING]",
        help="The Directory of the project/target file",
    )

    Parser.add_argument(
        "-Platform",
        type=str,
        metavar="[STRING]",
        help="The platform we are baking (Default: Building Platform)",
    )

    Parser.add_argument(
        "-OutputDir",
        type=str,
        metavar="[STRING]",
        help="The binary directory to put all the content in",
    )

    Args = Parser.parse_args()

    # Import Baker/Cooker
    if os.path.isfile(os.path.join(_Internal_Script_Dir, "Platform", Args.Platform, "Cook.py")):
        print("Platform found in base program!")
        SDKFile = importlib.import_module("Platform." + Args.Platform + ".Cook")

    elif os.path.isfile(os.path.join(ExtraSDKDir, Args.Platform, "Cook.py")):
        print("Platform found in base program!")
        SDKFile = importlib.import_module(Args.Platform + ".Cook")
    else:
        raise ValueError("Error: Cannot find Cook.py in either base program or CustomSDK, Trying to look for [" + Args.Platform + "] Failed")

    Types = []

    if Args.SourceDir is not None and Args.SourceDir != "":
        OutputSourceDir = Args.SourceDir

    else:
        if Args.Project is not None and Args.Project != "":
            OutputSourceDir = os.path.dirname(Args.Project)
        else:
            OutputSourceDir = os.path.dirname(Args.Target)

    # Get class from file
    for Name, Object in inspect.getmembers(SDKFile):

        if inspect.isclass(Object):
            Types.append(Object)

        for T in Types:
            if issubclass(T, Cook.BaseCooker):
                SDKClass = T(OutputSourceDir, EngineDir, Args.OutputDir)

                SDKClass.CookAll()





if __name__ == "__main__":
    main()
