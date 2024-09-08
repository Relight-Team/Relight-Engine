# Owned by Relight Engine 2024

import os

import RBT_Core as Core

import RBT_Build as Build

import Compiler.GPP.common as Compilers


# Values

Name = ""

Target = "" # Game, Full, Client, Server, Editor, Software

EngineDir = ""

ExtraDepend = []

ThirdPartyDepend = []

Plat_Dir = ""

Exec = ""


def Compile(f, ED, Plat):

    # set values

    EngineDir = ED

    Plat_Dir = os.path.dirname(f)

    Name = Core.GetVar(f, "Name")

    Target = Core.GetVar(f, "Target")

    ExtraDepend = Core.GetVar(f, "ExtraDependencies")



    #Build each module and store it to "tmp"
    if ExtraDepend is not None:
        for i in range(len(ExtraDepend)):
            dire = os.path.dirname(f)
            VarOld = ExtraDepend[i].replace("\n", "")
            Var = "/" + VarOld + "/" + VarOld + ".Build"

            URL = dire + Var

            Build.Build(URL, EngineDir, Plat)


     #Build each third party module and store it into tmp as well
    if ThirdPartyDepend is not None:
        for i in range(len(ThirdPartyDepend)):
            dire = os.path.dirname(f)
            VarOld = ThirdPartyDepend[i].replace("\n", "")
            Var = "/" + VarOld + "/" + ThirdPartyDepend[i] + ".Build"


            URL = EngineDir + "/ThirdParty/" + Var

            Build.Build(URL, EngineDir, Plat)

    # Get each file name in the tmp directory

    files = []

    RBT_TMP_Path = EngineDir + "/Programs/RelightBuildTool/Tmp"

    for fil in os.listdir(RBT_TMP_Path):
        full_path = os.path.join(RBT_TMP_Path, fil)

        if os.path.isfile(full_path):
            files.append(fil)


    # Compile each .o file into a single executable

    comm = Compilers.Start()

    if Plat == "Win64":
        comm = Compilesr.Start("Win64")

    for ind in files:
        comm += RBT_TMP_Path + "/" + ind + " "


    targCom = ""
    # Compile Directory based on target and platform

    # Game is the only unique one, building within the directory of it's own instead of the engine's bin directory
    if Target == "Game":
        targCom = Plat_Dir + "/bin/" + Plat + "/"
        Core.CheckFolder(targCom)


    elif Target == "Full" or Target == "Client" or Target == "Server" or Target == "Editor" or Target == "Software":
        targCom = EngineDir + "/Bin/" + Target + "/" + Plat + "/" + Name + "/"
        Core.CheckFolder(targCom)

    else:
        raise ValueError("ERROR: invalid Target, must be 'Game, Full, Client, Server, Editor, or Software'. Instead we got " + Target)


    if Plat == "Unix":
        Exec = ""
    elif Plat == "Win64":
        Exec = ".exe"


    comm += Compilers.FinalCompile(targCom, Name + Exec)

    print(comm)

    os.system(comm)

    print(Name + " with " + Target + " Target is Completed")
