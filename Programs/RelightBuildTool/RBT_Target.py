# Owned by Relight Engine 2024

import os

import RBT_Core as Core

import RBT_Build as Build

import RBT_Platform as Compiler

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

def ReturnNoDuplicateArrays(Array):
    Ret = []
    i = 0
    while i < len(Array):
        Repeat = False
        j = 0
        while j < len(Ret):
            if Array[i] == Ret[j]:
                Repeat = True
            j += 1
        if Repeat == False:
            Ret.append(Array[i])
        i += 1
    return Ret

def process_files(f, Array, EngineDire):
    if os.path.exists(f):
        TmpDependencies = Core.GetVar(f, 'Dependencies')
        TmpThirdParty = Core.GetVar(f, 'ThirdPartyDependencies')

        if Core.GetVar(f, 'ExtraDependencies') is not None:
            TmpDependencies += Core.GetVar(f, 'ExtraDependencies')

        if TmpThirdParty is not None:
            Array.extend(TmpThirdParty)

        if TmpDependencies is not None:
            for i in TmpDependencies:
                process_files(EngineDire + "/Runtime/" + i + "/" + i + ".Build", Array, EngineDire)


def Compile(f, ED, Plat, Debug):

    ClangThirdDepend = []

    # set values

    EngineDir = ED

    Cashe1 = EngineDir + "/Programs/RelightBuildTool/.Cashe"

    Plat_Dir = os.path.dirname(f)

    Name = Core.GetVar(f, "Name")

    Target = Core.GetVar(f, "Target")

    ExtraDepend = Core.GetVar(f, "ExtraDependencies")

    AlwaysUpdate = Core.GetVarOptional(f, "AlwaysUpdateDynamic", False)


    # Store All thirdPartyDepend names (For Clang)

    #Build each module and store it to ".Cashe"
    if ExtraDepend is not None:
        for i in range(len(ExtraDepend)):
            dire = os.path.dirname(f)
            VarOld = ExtraDepend[i].replace("\n", "")
            Var = "/" + VarOld + "/" + VarOld + ".Build"

            URL = dire + Var

            URL_Without_Build = dire + "/" + VarOld + "/"

            Build.Build(URL, URL_Without_Build, EngineDir, Plat, AlwaysUpdate, EngineDir + "/Programs/RelightBuildTool/.Cashe", Debug)


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
        TargCom = EngineDir + "/bin/" + Target + "/" + Plat + "/"
        Core.CheckFolder(TargCom)

    else:
        raise ValueError("ERROR: invalid Target, must be 'Game, Full, Client, Server, Editor, or Software'. Instead we got " + Target)



    if Plat == "Unix":
        Exec = ".bin"
    elif Plat == "Win64":
        Exec = ".exe"


    Comp_Com += Compiler.Output(TargCom + Name + Exec + " ")

     # Add .a files to command



    # main .o file

    for Depend in ExtraDepend:
        Comp_Com += Cashe1 + "/" + Depend + ".o "


    Comp_Com += Compiler.LinkTagFinal(EngineDir + "/bin/" + Plat + " ")


    # Move .a from cashe to /Bin
    for fil in os.listdir(Cashe1):
        full_path = os.path.join(Cashe1, fil)

        NoExte = os.path.splitext(fil)[0]


        if os.path.isfile(full_path):
            if ".a" in full_path and not Core.ArraySearch(NoExte, ExtraDepend):
                os.system("mv " + Cashe1 + "/" + fil + " " + EngineDir + "/bin/" + Plat + "/" + fil)

                Comp_Com += Compiler.LinkTagMiniFinal(":" +  fil + " ")



    for id in files:
        Comp_Com += id + " "

    if Compiler.Name() == "g++" or Compiler.Name() == "Clang":
        if ExtraDepend is not None:
            for i in range(len(ExtraDepend)):
                dire = os.path.dirname(f)
                VarOld = ExtraDepend[i].replace("\n", "")
                Var = "/" + VarOld + "/" + VarOld + ".Build"
                Comp_Com += Build.ExternalThirdParty(dire + Var, EngineDir, Debug)


    # For Clang, loop each dependencies, store in array, remove duplicates, and add the -l
    if Compiler.Name() == "Clang" and ExtraDepend is not None:
        ArrayVar = []
        for i in range(len(ExtraDepend)):
            dire = os.path.dirname(f)
            VarOld = ExtraDepend[i].replace("\n", "")
            Var = dire + "/" + VarOld + "/" + VarOld + ".Build"
            process_files(Var, ArrayVar, EngineDir)


        ArrayVar2 = ReturnNoDuplicateArrays(ArrayVar)

        for i in ArrayVar2:
            Comp_Com += "-l" + i + " "

        Comp_Com += " -lstdc++"


    PrintDebug(Comp_Com, Debug)
    print()

    os.system(Comp_Com + "\n")

    print(Name + " has finished compiling")
