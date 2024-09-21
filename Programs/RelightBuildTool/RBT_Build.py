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

PrecompileU = ""

Dyn_Lib = ""

Static_Lib = ""

PublicEntry = ""

Cashe1 = ""


def Build(f, URL, ED, Plat, Always, Output):

    Bin_Loc_Engine = ED + "/Bin/Engine/" + Plat + "/"
    Cashe1 = ED + "/Programs/RelightBuildTool/.Cashe1"

    Depend = Core.GetVar(f, "Dependencies")
    ThirdPartyDepend = Core.GetVar(f, "ThirdPartyDependencies")
    PrecompileU = Core.GetVar(f, "PrecompileUnix")
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

    # Public Link
    if PublicLink is not None:
        for Path in PublicLink:
            Comp_Com += Compiler.PublicLink(Path)

    # Private Link
    if PrivateLink is not None:
        for Path in PrivateLink:
            Comp_Com += Compiler.PrivateLink(Path)

    # Link for depend

    tmp = TotalLink(f, EngineDir)

    if tmp is not None:
        for t in tmp:
            #Comp_Com += "-I" + EngineDir + "/Runtime/" + t + "/Public "
            a = EngineDir + "/Runtime/" + t + "/Public "
            Comp_Com += Compiler.PublicLink(a)

    #Dependencies
    if Depend is not None:
        for Dep in Depend:
            # If depend is already compiled, link it,
            # Otherwise, build it, then linCok it

            a = EngineDir + "/Runtime/" + Dep + "/Public "
            
            Comp_Com += Compiler.PublicLink(a)

            if Core.CheckFile(Bin_Loc_Engine + Dep + Static_Lib):
                b = Cashe1 + "/" + Dep + Static_Lib + " "
                Comp_Com += Compiler.LinkTag() + b

            elif Core.CheckFile(Cashe1 + "/" + Dep + Static_Lib):
                b = Cashe1 + "/" + Dep + Static_Lib + " "
                Comp_Com += Compiler.LinkTag() + b
            else:
                Build(EngineDir + "/Runtime/" + Dep + "/" + Dep + ".Build",
                      EngineDir + "/Runtime/" + Dep + "/", EngineDir, Plat,
                      Always, Cashe1)

                b = Cashe1 + "/" + Dep + Static_Lib + " "
                Comp_Com += Compiler.LinkTag() + b

    Comp_Com += URL + "Public/" + PublicEntry

    Comp_Com += Compiler.Output() + Cashe1 + "/" + Name + Static_Lib
    #print("\n" + Comp_Com + "\n")

    os.system(Comp_Com)

    # Convert to static .a stuff

    Comp_Com = Compiler.ComToStatic()

    Comp_Com += Cashe1 + "/" + Name + ".a " + Cashe1 + "/" + Name + Static_Lib

    #print(Comp_Com)

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