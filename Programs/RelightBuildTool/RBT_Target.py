# Owned by Relight Engine 2024

import os

import RBT_Core as Core

import RBT_Build as Build

import Compiler.GPP.common as Compiler

# Values

Name = ""

Target = ""  # Game, Engine, Software, Editor

EngineDir = ""

ExtraDepend = []

ThirdPartyDepend = []

Plat_Dir = ""

Exec = ""

def PrintDebug(Text, Show):
    if Show == True:
        print(Text)


def Compile(f, ED, Plat, Debug):

    # set values

    EngineDir = ED

    Cashe1 = EngineDir + "/Programs/RelightBuildTool/.Cashe1"

    Plat_Dir = os.path.dirname(f)

    Name = Core.GetVar(f, "Name")

    Target = Core.GetVar(f, "Target")

    ExtraDepend = Core.GetVar(f, "ExtraDependencies")

    AlwaysUpdate = Core.GetVarOptional(f, "AlwaysUpdateDynamic", False)

    #Build each module and store it to ".Cashe1"
    if ExtraDepend is not None:
        for i in range(len(ExtraDepend)):
            dire = os.path.dirname(f)
            VarOld = ExtraDepend[i].replace("\n", "")
            Var = "/" + VarOld + "/" + VarOld + ".Build"

            URL = dire + Var

            URL_Without_Build = dire + "/" + VarOld + "/"

            Build.Build(URL, URL_Without_Build, EngineDir, Plat, AlwaysUpdate, EngineDir + "/Programs/RelightBuildTool/.Cashe1", Debug)


    print()
    print("Building modules completed")
    print("Starting to build the exe")
    print()

    # Build the executable

    # Add beginning command
    Comp_Com = Compiler.Start(Plat)

    files = []

    # Exe name

    TargCom = ""

    if Target == "Game":
        TargCom = Plat_Dir + "/bin/" + Plat + "/"
        Core.CheckFolder(TargCom)



    elif Target == "Engine" or Target == "Editor" or Target == "Programs":
        TargCom = EngineDir + "/Bin/" + Target + "/" + Plat + "/"
        Core.CheckFolder(TargCom)

    else:
        raise ValueError("ERROR: invalid Target, must be 'Game, Full, Client, Server, Editor, or Software'. Instead we got " + Target)



    if Plat == "Unix":
        Exec = ".bin"
    elif Plat == "Win64":
        Exec = ".exe"

    
    Comp_Com += Compiler.Output() + TargCom + Name + Exec + " "

     # Add .a files to command



    # main .o file

    for Depend in ExtraDepend:
        Comp_Com += Cashe1 + "/" + Depend + ".o "


    Comp_Com += Compiler.LinkTag() + EngineDir + "/Bin/" + Plat + " "

    # Move .a from cashe to /Bin
    for fil in os.listdir(Cashe1):
        full_path = os.path.join(Cashe1, fil)

        NoExte = os.path.splitext(fil)[0]

        
        if os.path.isfile(full_path):
            if ".a" in full_path and not Core.ArraySearch(NoExte, ExtraDepend):
                os.system("mv " + Cashe1 + "/" + fil + " " + EngineDir + "/Bin/" + Plat + "/" + fil)

                Comp_Com += Compiler.LinkTagMini() + ":" +  fil + " "
    



    #for ind in ExtraDepend:
    #    Comp_Com += " -l:" + ind + ".a"
        

    for id in files:
        Comp_Com += id + " "



    # g++ requires me to re-add the same 3rd party libraries

    # Fuck g++ all my homies hate g++

    if ExtraDepend is not None:
        for i in range(len(ExtraDepend)):
            dire = os.path.dirname(f)
            VarOld = ExtraDepend[i].replace("\n", "")
            Var = "/" + VarOld + "/" + VarOld + ".Build"
            Comp_Com += Build.ExternalThirdParty(dire + Var, EngineDir, Debug)

    PrintDebug(("\n" + Comp_Com + "\n"), Debug)

    os.system(Comp_Com + "\n")

    print(Name + " has finished compiling")
