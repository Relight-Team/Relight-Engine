# Owned by Relight Engine 2024

import os

import RBT_Core as Core


# values

Name = ""

EngineDir = ""

Path = ""

PublicDepend = []

PrivateDepend = []

BuildCom = "g++ "

def Build(f, ED):

    EngineDir = ED


    # Set values

    PublicDepend = Core.GetVar(f, "PublicDependencies")
    PrivateDepend = Core.GetVar(f, "PrivateDependencies")

    Name = Core.GetVar(f, "Name")




    # Start compiling/Applying settings

    index = 0

    while index < len(PublicDepend):

        # Public Depend

        BuildCom += "-I" + EngineDir + "/" + PublicDepend[index] + "/Public "

        # TODO: Add Private Depend

        BuildCom += EngineDir + "/" + Name + "/Public/" + Name + ".h -o Tmp/" + Name + ".o"

        os.system(BuildCom)
