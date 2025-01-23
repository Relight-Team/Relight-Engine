# Owned by Relight Engine 2024

import argparse
import os
import RBT_Target as Targ

import CreateCfg as CCfg



RBT = os.path.dirname(os.path.abspath(__file__)) + "/"



def main(Target, Platform):
    # Arguments

    #TODO: Add support for both platform and BuildCfg

    parser = argparse.ArgumentParser(description="Software Arguments")

    parser.add_argument('Target', type=str, help="The Target file")

    parser.add_argument('Platform', type=str, help="The platform for the desire output")

    #parser.add_argument('BuildCfg', type=str, help="The state of the output")

    print()
    print("Cleaning cashe folder")
    print()


    class ConfigError(Exception):
        def __init__(self, message):
            super().__init__(message)
            self.message = message

    # Check for Config system

    if not os.path.exists(RBT + "Configuration.py"):
        CCfg.CreateConfig()

    # RBT's auto-generate engine directory system

    CCfg.BuildConfig()


    import Configuration as cfg


    RBT_TMP_Path_02 = cfg.Engine_Directory + "/Programs/RelightBuildTool/.Cashe"


    for filename in os.listdir(RBT_TMP_Path_02):
        file_path = os.path.join(RBT_TMP_Path_02, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    args = parser.parse_args()

    TF = args.Target

    PT = args.Platform

    Targ.Compile(TF, cfg.Engine_Directory, PT, cfg.ShowDebug)


main("", "")
