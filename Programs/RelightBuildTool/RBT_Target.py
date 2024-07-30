# Owned by Relight Engine 2024

import os

import RBT_Core as Core

import RBT_Build as Build


# Values

Name = ""

Target = "" # Game, Full, Client, Server, Editor, Software

EngineDir = ""

ExtraDepend = []

platform = ""

Plat_Dir = ""


def Compile(f, ED):

    # set values

    EngineDir = ED

    Plat_Dir = os.path.dirname(f)

    Name = Core.GetVar(f, "Name")

    Target = Core.GetVar(f, "Target")

    ExtraDepend = Core.GetVar(f, "ExtraDependencies")

    #Build each module and store it to "tmp"

    for i in len(ExtraDepend):
        Var = ExtraDepend[i] + "/" + ExtraDepend[i] + ".Build"

        URL = EngineDir + Var

        Build.Build(URL, EngineDir)

    # Get each file name in the tmp directory

    files = []

    for fil in os.listdir("tmp"):
        full_path = os.path.join("tmp", fil)

        if os.path.isfile(full_path):
            files.append(fil)


    # Compile each .o file into a single executable

    comm = "g++ "

    for ind in files:
        comm += files[ind] + " "


    targCom = ""
    # Compile Directory based on target and platform

    # Game is the only unique one, building within the directory of it's own instead of the engine's bin directory
    if Target == "Game":
        targCom = Plat_Dir + "/bin/"


    elif Target == "Full" or Target == "Client" or Target == "Server" or Target == "Editor" Target == "Software":
        targCom = EngineDir + "/Bin/" + Target + "/" + Name + "/"

    else:
        raise ValueError("ERROR: invalid Target, must be 'Game, Full, Client, Server, Editor, or Software'. Instead we got " + Target)


    comm += "-o " + targCom + Name
