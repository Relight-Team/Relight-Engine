# Owned by Relight Engine 2024

import os

import RBT_Core as Core


# values

Name = ""

EngineDir = ""

Path = ""

PublicDepend = []

PrivateDepend = []

PrecompileUnix = ""

Dyn_Lib = ""





def Build(f, ED, Plat):

    EngineDir = ED

    if Plat == "Unix":
        Dyn_Lib = ".so"
    elif Plat == "Win64":
        Dyn_Lib = ".dll"


    # Set values

    PublicDepend = Core.GetVar(f, "PublicDependencies")
    PrivateDepend = Core.GetVar(f, "PrivateDependencies")
    PrecompileUnix = Core.GetVar(f, "PrecompileUnix")

    Name = Core.GetVar(f, "Name")

    BuildCom = "g++ "

    if Plat == "Win64":
        BuildCom = "x86_64-w64-mingw32-g++ -static -static-libgcc -static-libstdc++ "

    print("Building Module " + Name)

    # Start compiling/Applying settings

    index = 0


    if PrivateDepend is not None:
        while index < len(PrivateDepend):

            # Public Depend

            BuildCom += "-I" + EngineDir + "/Runtime/" + PrivateDepend[index] + "/Private "

            index += 1

    if PublicDepend is not None:
        while index < len(PublicDepend):

            # Public Depend

            BuildCom += "-I" + EngineDir + "/Runtime/" + PublicDepend[index] + "/Public "

            index += 1


    if PrecompileUnix is not None:
        os.system("cp " + os.path.dirname(f) + "/" + PrecompileUnix + " Tmp/")

    # Final step
    BuildCom += "-c " + os.path.dirname(f) + "/Public/" + Name + ".cpp -o Tmp/" + Name + Dyn_Lib


    os.system(BuildCom)
