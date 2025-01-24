# Owned by Relight Engine 2024

# build the build files, and store each one in .Cashe

import os

import RBT_Core as Core

import Compiler.GPP.common as Compiler

# values

Name = ""

EngineDir = ""

Path = ""

Depend = []

PublicLink = []

PrivateLink = []

Dyn_Lib = ""

Static_Lib = ""

Cashe = ""

def PrintDebug(Text, Show):
    if Show == True:
        print(Text)

def Build(f, URL, ED, Plat, Always, Output, Debug):

    Bin_Loc_Engine = ED + "/Bin/Engine/" + Plat + "/"
    Cashe = ED + "/Programs/RelightBuildTool/.Cashe"

    Depend = Core.GetVar(f, "Dependencies")
    ThirdDepend = Core.GetVar(f, "ThirdPartyDependencies")
    ThirdLink = Core.GetVar(f, "ThirdPartyLink")

    Name = Core.GetVar(f, "Name")

    EngineDir = ED

    Dyn_Lib = ""

    print("Building " + Name + "...")


    BuildCom = Compiler.Start()

    if Plat == "Win64":
        BuildCom = Compiler.Start("Win64")

    if Plat == "Unix":
        Dyn_Lib = ".so"
        Static_Lib = ".o"

    elif Plat == "Win64":
        Dyn_Lib = ".dll"

    # Add beginning command
    Comp_Com = Compiler.Start(Plat)

    # Add shared stuff

    Comp_Com += Compiler.CompileTag()

    # Link to public

    Comp_Com += Compiler.PublicLink(URL + "Src ")

    # Public Link
    if PublicLink is not None:
        for Path in PublicLink:
            Comp_Com += Compiler.PublicLink(Path)

    # Define Based on compiled platform

    if Plat == "Win64":

        Comp_Com += Compiler.Define("WINDOWS=1")
        Comp_Com += Compiler.Define("UNIX=0")

    elif Plat == "Unix":

        Comp_Com += Compiler.Define("WINDOWS=0")
        Comp_Com += Compiler.Define("UNIX=1")
        Core.ChangeVar("UNIX", "1")



    # Set engine directory

    Comp_Com += Compiler.Define('ENGINEDIR=\\"' + EngineDir + '\\"')


    # Link for depend

    tmp = TotalLink(f, EngineDir)

    if tmp is not None:
        for t in tmp:
            a = EngineDir + "/Runtime/" + t + "/Src "
            Comp_Com += Compiler.PublicLink(a)


    # Link for Third

    tmp2 = TotalLink(f, EngineDir)
    PrintDebug(tmp2, Debug)

    if tmp2 is not None:
        for t in tmp2:
            fil = EngineDir + "/Runtime/" + t + "/" + t + ".Build"
            ta = Core.GetVar(fil, "ThirdPartyDependencies")
            if ta is not None:
                for item in ta:
                    a = EngineDir + "/ThirdParty/" + item + "/Include "
                    b = EngineDir + "/ThirdParty/" + item + "/Implement "
                    Comp_Com += Compiler.PublicLink(a)
                    Comp_Com += Compiler.LinkTag(b)
                    Comp_Com += Compiler.LinkTagMini(item + " ")


    #Dependencies
    if Depend is not None:
        for Dep in Depend:
            # If depend is already compiled, link it,
            # Otherwise, build it, then link it

            if Core.CheckFile(Bin_Loc_Engine + Dep + Static_Lib):
                b = Cashe + "/" + Dep + Static_Lib + " "
                Comp_Com += Compiler.LinkTag(b)

            elif Core.CheckFile(Cashe + "/" + Dep + Static_Lib):
                b = Cashe + "/" + Dep + Static_Lib + " "
                Comp_Com += Compiler.LinkTag(b)
            else:

                Build(EngineDir + "/Runtime/" + Dep + "/" + Dep + ".Build",
                      EngineDir + "/Runtime/" + Dep + "/", EngineDir, Plat,
                      Always, Cashe, Debug)

                b = Cashe + "/" + Dep + Static_Lib + " "
                Comp_Com += Compiler.LinkTag(b)


    # 3rd party Dependencies


    if ThirdDepend is not None:

        for Dep in ThirdDepend:
                Comp_Com += Compiler.LinkTag(EngineDir + "/ThirdParty/" + Dep + "/Implement/" + Dep + ".a ")


    if ThirdLink is not None:
        for Lnk in ThirdLink:
            Comp_Com += Compiler.PublicLink(EngineDir + "/ThirdParty/"+ Lnk + "/Include ")



    Comp_Com += Compiler.LoopCpp(URL + "Src/")

    Comp_Com += Compiler.Output(Cashe + "/" + Name + Static_Lib)
    PrintDebug("\n" + Comp_Com + "\n", Debug)

    os.system(Comp_Com)

    # Convert to static .a stuff

    Comp_Com = Compiler.ComToStatic(Cashe + "/" + Name + ".a " + Cashe + "/" + Name + Static_Lib)

    PrintDebug("\n" + Comp_Com + "\n", Debug)

    os.system(Comp_Com)



def TotalLink(f, EngineDir):
    # Initialize an empty set to store unique dependencies
    all_dependencies = set()

    # Recursive function to gather dependencies
    def gather_dependencies(file):
        dependencies = Core.GetVar(file, "Dependencies") or []
        for dep in dependencies:
            # Add the dependency to the set
            all_dependencies.add(dep)
            # Check if the dependency has its own dependencies and gather them recursively
            dep_file = os.path.join(EngineDir, "Runtime", dep, dep + ".Build")
            if os.path.isfile(dep_file):
                gather_dependencies(dep_file)




    # Start gathering from the initial build file
    gather_dependencies(f)

    # Return the combined list of dependencies
    return list(all_dependencies)


def ExternalThirdParty(f, EngineDir, Debug):
    # Link for Third

    tmp2 = TotalLink(f, EngineDir)
    PrintDebug(tmp2, Debug)

    if tmp2 is not None:
        for t in tmp2:
            fil = EngineDir + "/Runtime/" + t + "/" + t + ".Build"
            ta = Core.GetVar(fil, "ThirdPartyDependencies")
            if ta is not None:
                for item in ta:
                    b = EngineDir + "/ThirdParty/" + item + "/Implement "
                    Y = Compiler.LinkTag(b)
                    Z = Compiler.LinkTagMini(item + " ")

                    return Y + " " + Z

    return ""
