# Owned by Relight Engine 2024

import os

import RBT_Core as Core


# values

Name = ""

EngineDir = ""

Path = ""

PublicDepend = []

PrivateDepend = []



def Build(f, ED):

    EngineDir = ED


    # Set values

    PublicDepend = Core.GetVar(f, "PublicDependencies")
    PrivateDepend = Core.GetVar(f, "PrivateDependencies")

    Name = Core.GetVar(f, "Name")

    BuildCom = "g++ "

    print("Building Module " + Name)

    # Start compiling/Applying settings

    index = 0



    while index < len(PublicDepend):

        # Public Depend

        BuildCom += "-I" + EngineDir + "/Runtime/" + PublicDepend[index] + "/Public "

        index += 1

    # TODO: Add Private Depend

    BuildCom += "-c " + os.path.dirname(f) + "/Public/" + Name + ".cpp -o Tmp/" + Name + ".so"


    os.system(BuildCom)
