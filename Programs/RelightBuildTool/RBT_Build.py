# Owned by Relight Engine 2024

import os

import RBT_Core as Core

import Compiler.GPP.common as Compiler

# values

Name = ""

EngineDir = ""

Path = ""

PublicDepend = []

PrivateDepend = []

PrecompileU = ""

Dyn_Lib = ""





def Build(f, ED, Plat):

    EngineDir = ED

    RBT_TMP_Path = EngineDir + "/Programs/RelightBuildTool/Tmp"

    if Plat == "Unix":
        Dyn_Lib = ".so"
    elif Plat == "Win64":
        Dyn_Lib = ".dll"


    # Set values

    EntryFile = Core.GetVar(f, "EntryFile")
    PublicDepend = Core.GetVar(f, "PublicDependencies")
    PrivateDepend = Core.GetVar(f, "PrivateDependencies")
    ThirdPartyDepend = Core.GetVar(f, "ThirdPartyDependencies")
    PrecompileU = Core.GetVar(f, "PrecompileUnix")

    Name = Core.GetVar(f, "Name")

    BuildCom = Compiler.Start()

    if Plat == "Win64":
        BuildCom = Compiler.Start("Win64")

    print("Building Module " + Name)

    # Start compiling/Applying settings

    index = 0


    if PrivateDepend is not None:
        while index < len(PrivateDepend):

            # private Depend

            BuildCom += Compiler.PrivateLink(EngineDir, PrivateDepend[index])

            index += 1

    if PublicDepend is not None:
        while index < len(PublicDepend):

            # Public Depend

           BuildCom += Compiler.PublicLink(EngineDir, PublicDepend[index])

           index += 1


     #Build each third party module and store it into tmp as well
    if ThirdPartyDepend is not None:
        for i in range(len(ThirdPartyDepend)):
            dire = os.path.dirname(f)
            VarOld = ThirdPartyDepend[i].replace("\n", "")
            Var = "/" + VarOld + "/" + ThirdPartyDepend[i] + ".Build"


            URL = EngineDir + "/ThirdParty/" + Var

            Build(URL, EngineDir, Plat)


    if PrecompileU is not None:
        os.system("cp " + os.path.dirname(f) + "/" + PrecompileU + " Tmp/")

    # Final step, only if PrecompileU isn't settings

    if PrecompileU is None:
        #BuildCom = Compiler.Return()

        BuildCom += Compiler.Finish(os.path.dirname(f), Name, EntryFile, Dyn_Lib, RBT_TMP_Path)


        os.system(BuildCom)
