# Owned by Relight Engine 2024

import argparse
import os
import RBT_Target as Targ

cfgver = "RBT_Ver = [0, 0, 4]\n"

Compiler = "Compiler = 'g++'\n"


def main(Target, Platform):

    print("WARNING: DEPRECIATED! WILL BE GONE SOON! PLEASE USE RELIGHTBUILDTOOL!")
    # Arguments

    #TODO: Add support for both platform and BuildCfg

    parser = argparse.ArgumentParser(description="Software Arguments")

    parser.add_argument('Target', type=str, help="The Target file")

    parser.add_argument('Platform', type=str, help="The platform for the desire output")

    #parser.add_argument('BuildCfg', type=str, help="The state of the output")

    for filename in os.listdir("Tmp"):
        file_path = os.path.join("Tmp", filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    print("Cleaning Temp File")

# Create/Reset Config file
    def CreateConfig():
        fil = open("GlobalCfg.py", "w")
        fil.write(cfgver + 'Engine_Directory = ""\n' + Compiler)
        fil.close

    class ConfigError(Exception):
        def __init__(self, message):
            super().__init__(message)
            self.message = message

    # Check for Config system


    if not os.path.exists("GlobalCfg.py"):
        CreateConfig()


    import GlobalCfg as cfg

    # RBT's auto-generate engine directory system

    if cfg.Engine_Directory == "":
        print("Warning: the config file for the engine directory is blank, do you want RBT to auto-generate the directory?")
        print("1 = yes")
        print("2 = no")
        choice1 = input("> ")

        if choice1 == "1":
            print("generating...")
            current_dir = os.getcwd()
            parent_dir01 = os.path.dirname(current_dir)
            parent_dir02 = os.path.dirname(parent_dir01)
            print("")
            print("Generation complete, is this the correct engine directory?")
            print("1 = yes")
            print("2 = no")
            print("")
            print(parent_dir02)
            choice2 = input("> ")
            if choice2 == "1":
                fil = open("GlobalCfg.py", "w")
                fil.write(cfgver + 'Engine_Directory = "' + parent_dir02 + '"\n' + Compiler)
                fil.close
                # Simple hack to fix the insta-crash
                raise ConfigError("Completed! Please re-run the program")
            elif choice2 == "2":
                raise ConfigError("ERROR: Failed to auto-set config, please manually set the engine directory yourself")
            else:
                raise ValueError("ERROR: Unknown option selected " + choice2)
        elif choice1 == "2":
            raise ConfigError("ERROR: Engine Directory Config is blank, please manually set the engine directory")
        else:
            raise ValueError("ERROR: Unknown option selected " + choice1)

    args = parser.parse_args()

    TF = args.Target

    PT = args.Platform

    Targ.Compile(TF, cfg.Engine_Directory, PT)


# So, if it's main() i doesn't store the arg, but if it's main(""), it does? Python, make it make sense

main("", "")



