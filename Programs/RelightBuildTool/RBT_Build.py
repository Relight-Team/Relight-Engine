# Owned by Relight Engine 2024

# build the build files, and store each one in .Output

#Output = side-Modules to combine into a single module for Cashe1

#Cashe1 = Modules combine into a single executable/library

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

PublicEntry = ""

Cashe1 = ""

def PrintDebug(Text, Show):
    if Show == True:
        print(Text)

def Build(f, URL, ED, Plat, Always, Output, Debug):

    Bin_Loc_Engine = ED + "/Bin/Engine/" + Plat + "/"
    Cashe1 = ED + "/Programs/RelightBuildTool/.Cashe1"

    Depend = Core.GetVar(f, "Dependencies")
    ThirdDepend = Core.GetVar(f, "ThirdPartyDependencies")
    ThirdLink = Core.GetVar(f, "ThirdPartyLink")

    Name = Core.GetVar(f, "Name")
    PublicEntry = Core.GetVar(f, "EntryFile")

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

    Comp_Com += "-I" + URL + "Src "

    # Public Link
    if PublicLink is not None:
        for Path in PublicLink:
            Comp_Com += Compiler.PublicLink(Path)

    # Define Based on compiled platform

    if Plat == "Win64":

        Comp_Com += Compiler.Define() + "WINDOWS=1 "
        Comp_Com += Compiler.Define() + "UNIX=0 "

    elif Plat == "Unix":

        Comp_Com += Compiler.Define() + "WINDOWS=0 "
        Comp_Com += Compiler.Define() + "UNIX=1 "
        Core.ChangeVar("UNIX", "1")


    # Link for depend

    tmp = TotalLink(f, EngineDir)

    if tmp is not None:
        for t in tmp:
            #Comp_Com += "-I" + EngineDir + "/Runtime/" + t + "/Public "
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
                    Comp_Com += Compiler.LinkTag() + b
                    Comp_Com += Compiler.LinkTagMini() + item + " "


    #Dependencies
    if Depend is not None:
        for Dep in Depend:
            # If depend is already compiled, link it,
            # Otherwise, build it, then link it

            #a = EngineDir + "/Runtime/" + Dep + "/Private "
            
            #Comp_Com += Compiler.PublicLink(a)

            if Core.CheckFile(Bin_Loc_Engine + Dep + Static_Lib):
                b = Cashe1 + "/" + Dep + Static_Lib + " "
                Comp_Com += Compiler.LinkTag() + b

            elif Core.CheckFile(Cashe1 + "/" + Dep + Static_Lib):
                b = Cashe1 + "/" + Dep + Static_Lib + " "
                Comp_Com += Compiler.LinkTag() + b
            else:

                Build(EngineDir + "/Runtime/" + Dep + "/" + Dep + ".Build",
                      EngineDir + "/Runtime/" + Dep + "/", EngineDir, Plat,
                      Always, Cashe1, Debug)

                b = Cashe1 + "/" + Dep + Static_Lib + " "
                Comp_Com += Compiler.LinkTag() + b


    # 3rd party Dependencies


    if ThirdDepend is not None:

        for Dep in ThirdDepend:
                Comp_Com += Compiler.LinkTag() + EngineDir + "/ThirdParty/" + Dep + "/Implement/" + Dep + ".a "


    if ThirdLink is not None:
        for Lnk in ThirdLink:
            Comp_Com += Compiler.PublicLink(EngineDir + "/ThirdParty/"+ Dep + "/Include ")



    Comp_Com += URL + "Src/" + PublicEntry

    Comp_Com += Compiler.Output() + Cashe1 + "/" + Name + Static_Lib
    PrintDebug("\n" + Comp_Com + "\n", Debug)

    os.system(Comp_Com)

    # Convert to static .a stuff

    Comp_Com = Compiler.ComToStatic()

    Comp_Com += Cashe1 + "/" + Name + ".a " + Cashe1 + "/" + Name + Static_Lib

    PrintDebug("\n" + Comp_Com + "\n", Debug)

    os.system(Comp_Com)



#def FThirdLink(f, EngineDir):
#    # Initialize an empty set to store unique dependencies
#    all_dependencies = set()
#
#    # Recursive function to gather dependencies
#    def gather_dependencies(dep_file):
#        Third = Core.GetVar(file, "ThirdPartyDependencies") or []
#        for T in Third:
#            # Add the dependency to the set
#            all_dependencies.add(T)
#           # Check if the dependency has its own dependencies and gather them recursively
#           dep_file = os.path.join(EngineDir, "Runtime", T, T + ".Build")
#            if os.path.isfile(dep_file):
#                gather_dependencies(dep_file)



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
                    Y = Compiler.LinkTag() + b
                    Z = Compiler.LinkTagMini() + item + " "

                    return Y + " " + Z

    return ""
