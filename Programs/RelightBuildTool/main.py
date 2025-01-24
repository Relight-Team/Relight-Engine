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






    class ConfigError(Exception):
        def __init__(self, message):
            super().__init__(message)
            self.message = message

    # Check for Config system

    if not os.path.exists(RBT + "Configuration.py"):
        CCfg.CreateConfig()

    # RBT's auto-generate engine directory system

    CCfg.BuildConfig()

    args = parser.parse_args()


    import Configuration as cfg

    print("---------------------------------------------------------------")
    print("|                    Relight Build Tool                       |")
    print("---------------------------------------------------------------")
    print("RBT Version: " + str(cfg.RBT_Ver[0]) + "." + str(cfg.RBT_Ver[1]) + "." + str(cfg.RBT_Ver[2]))
    print("Engine Directory: " + cfg.Engine_Directory)
    print("Host OS: " + os.name)
    print("Target OS: " + args.Platform)
    print("Compiler: " + cfg.Compiler)
    print("Targeting: " + args.Target)
    print("==========")

    print()
    print("Cleaning cashe folder")
    print()

    RBT_TMP_Path_02 = cfg.Engine_Directory + "/Programs/RelightBuildTool/.Cashe"


    for filename in os.listdir(RBT_TMP_Path_02):
        file_path = os.path.join(RBT_TMP_Path_02, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)


    TF = args.Target

    PT = args.Platform

    Targ.Compile(TF, cfg.Engine_Directory, PT, cfg.ShowDebug)


main("", "")
