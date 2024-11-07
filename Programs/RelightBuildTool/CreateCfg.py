import os


# Default shit

cfgver = "RBT_Ver = [0, 1, 0]\n"

Compiler = "Compiler = 'g++'\n"

ShowDebug = "ShowDebug = False\n"

RBT = os.path.dirname(os.path.abspath(__file__)) + "/"



class ConfigError(Exception):
        def __init__(self, message):
            super().__init__(message)
            self.message = message


# Create/Reset Config file

def CreateConfig():
    fil = open(RBT + "GlobalCfg.py", "w")
    fil.write(cfgver + 'Engine_Directory = ""\n' + Compiler + ShowDebug)
    fil.close

def BuildConfig():
    # RBT's auto-generate engine directory system

    import GlobalCfg as cfg

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
                fil = open(RBT + "GlobalCfg.py", "w")
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

