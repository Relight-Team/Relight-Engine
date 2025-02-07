import os
import sys

sys.path.append("../../")

import RBT_Core as Core
import Platform.RBT_Platform as LC
import ProjectFiles.ProjectGenerator as P

class MakeFileGenerator(P.ProjectGenerator):
    def __init__(self):
        self.ProjectFileName = "Makefile"

    def Find(self, Fil, Ext):
        return "$(shell find " + Fil + " -name '" + Ext + "')"

    # Recursively Stores each module command into an array
    def Store(self, f, Name, Engine_Directory, Target_Directory, OS):
        A = Core.GetVar(Core.FindDepend(Name, Engine_Directory, Target_Directory) + "/" + Name + ".Build", "Dependencies")
        B = Core.GetVar(Core.FindDepend(Name, Engine_Directory, Target_Directory) + "/" + Name + ".Build", "ThirdPartyDependencies")
        Ret = "$(OBJ_DIR)/" + Name + LC.StaticFile() + ": "
        Ret += self.Find(f + "/Src/", "*.cpp") + " "

        # Each Dep in A
        if A is not None:
            for De in A:
                Ret += "$(OBJ_DIR)/" + De + ".o "

        # Commands
        Ret += LC.NewLine() + LC.NewTab()
        Ret += "$(CXX) $(LDFLAGS) -c "

        # Defines

        DefineArray = []

        super().DefineGen(DefineArray, OS, Engine_Directory)

        # Add each define to file
        for Defi in DefineArray:
            Ret += Defi + " "

        # Link Self

        Ret += "-I" + f + "/Src/ "

        # Link each Dep:
        if A is not None:
            for De in A:
                Ret += "-I" + Core.FindDepend(De, Engine_Directory, Target_Directory) + "/Src/ "



        # Add link to thirdparty if it exist
        if A is not None:
            for De in A:
                array = Core.GetVar(Core.FindDepend(De, Engine_Directory, Target_Directory) + "/" + De + ".Build", "ThirdPartyLink")

                if array is not None:
                    for i in array:
                        Ret += "-I" + Engine_Directory + "/ThirdParty/" + i + "/Include/ "


        Ret += "$< -o $@" + LC.NewLine()

        # Add Ret to Array

        self.Side_Command.append(Ret)

        if B is not None:
            self.ThirdParties.extend(B)


        # Recrusive part

        if A is not None:
            for De in A:
                self.Store(Core.FindDepend(De, Engine_Directory, Target_Directory), De, Engine_Directory, Target_Directory, OS)


    def IsCompilerSupported(self, Compiler):
        if Compiler != "g++" and Compiler != "clang++":
            LC.PrintWarning("Compiler isn't g++ or clang++, we will continue, but there could be errors!")

        if Compiler == "g++":
            LC.PrintWarning("The compiler is g++, we will continue, but we recommend using clang++ instead")


    def Make(self, Target, Engine_Directory, Compiler, OS):

        TargetDirectory = os.path.dirname(Target)

        ProjectFile = TargetDirectory + "/" + self.ProjectFileName

        OBJ_DIR = Engine_Directory + "/Programs/RelightBuildTool/.Cashe/"

        super().CreateFolder(OBJ_DIR)

        THIRDPARTY = Engine_Directory + "/ThirdParty/"

        Target_Exe_Name = Core.GetVar(Target, "Name")

        Target_Exe = TargetDirectory + "/bin/" + OS + "/" + Target_Exe_Name + LC.Extension()


        # Target Values

        TargetDependencies = Core.GetVar(Target, "ExtraDependencies")



        # If project file doesn't exist, create it
        if not (os.path.isfile(ProjectFile)):
            LC.CreateFile(ProjectFile)

        # Clear project file

        tmp = open(ProjectFile, "w")
        tmp.write("")
        tmp.close()

        # Initialize file
        super().PreMake(ProjectFile)

        # Adds all values for the file
        super().Append(ProjectFile, "CC = " + Compiler + LC.NewLine() + "CXX = " + Compiler + LC.NewLine()) # CC and CXX

        super().Append(ProjectFile, "OBJ_DIR = " + OBJ_DIR + LC.NewLine() + "THIRDPARTY = " + THIRDPARTY + LC.NewLine()) # OBJ_DIR and THIRDPARTY

        super().Append(ProjectFile, "OBJ_FILES = " + self.Find(OBJ_DIR, "*" + LC.StaticFile()) + LC.NewLine()) # OBJ_FILES

        super().Append(ProjectFile, "EXEC = " + Target_Exe + LC.NewLine())



        # For each dependencies, store them in array for later

        for Dep in TargetDependencies:
            self.Store(Core.FindDepend(Dep, Engine_Directory, TargetDirectory), Dep, Engine_Directory, TargetDirectory, OS)



        # Start final executable file

        super().Append(ProjectFile, "$(EXEC): $(OBJ_FILES) ")

        # For each ExtraDependencies, super().Append it to file

        for Dep in TargetDependencies:
            super().Append(ProjectFile, "$(OBJ_DIR)/" + Dep + LC.StaticFile() + " ")

        # Get ready for command portion
        super().Append(ProjectFile, LC.NewLine() + LC.NewTab())

        super().Append(ProjectFile, "$(CXX) $(OBJ_FILES) ")

        # Defines

        DefineArray = []

        super().DefineGen(DefineArray, OS, Engine_Directory)

        # Add each define to file
        for Defi in DefineArray:
            super().Append(ProjectFile, Defi + " ")

        # For each Third party, add it

        if self.ThirdParties is not None:
            for Party in self.ThirdParties:
                super().Append(ProjectFile, "$(THIRDPARTY)" + str(Party) + "/Implement/lib" + str(Party) + ".a ")

        super().Append(ProjectFile, " -o $(EXEC)" + LC.NewLine())
        super().Append(ProjectFile, LC.NewLine() + LC.NewLine())

        # Add each Side_Command

        New_Command = super().ReturnNoDuplicateArrays(self.Side_Command)

        for i in New_Command:
            super().Append(ProjectFile, i)
            super().Append(ProjectFile, LC.NewLine() + LC.NewLine())


    def RunBuildFile(self, FilePath, Rebuild, CompilerDebug):
        Ret = "make -f "
        Ret += FilePath

        if CompilerDebug == False:
            Ret += " -s "

        if Rebuild == True:
            Ret += " -B "
        return Ret
