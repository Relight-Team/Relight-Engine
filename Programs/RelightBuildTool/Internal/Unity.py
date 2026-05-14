import os
from Internal import Logger


# System that combines .cpp files together
class Unity:

    # Checks if there's any condition that requires another object file, returns true if we need to create new .o file
    # For example, conflicts, PCH usage, headerTool, etc
    # <CppCode> The cpp code
    # <Return> true if there's conflicts in code and needs a new cpp file
    @staticmethod
    def DoesCodeHaveConficts(CppCode):
        return False

    # Cleans up the code for optimization, returns optimized code
    # <CppCode> The Cpp code
    # <Return> the optimized cpp content
    @staticmethod
    def OptimizeCodePost(CppCode):
        CCode = CppCode

        RetLines = CCode.split("\n")

        Ret = ""

        AllIncludes = []
        for Line in RetLines:

            StrippedLine = Line.strip()

            # Only include 1 time, useful for compile times
            if StrippedLine.startswith("#include "):

                # If this is the first time we have this include, leave it alone
                if StrippedLine not in AllIncludes:
                    AllIncludes.append(StrippedLine)

                # Otherwise we will remove that line
                else:
                    Ret += "\n"
                    continue

            Ret += StrippedLine + "\n"

        return Ret

    # Main function, compiles Unity object files, returns list of output object files
    # <FilesList> List of files to unified
    # <CompileEnv> The Compile Environment
    # <InToolchain> The toolchain to compile unified cpp file with
    # <Intermed> The intemediate directory
    # <OutputActionList> The list actions to output, will be appended
    # <ModName> The name of module
    # <Return> List of object files to link
    @staticmethod
    def UniteCPPFiles(FilesList, CompileEnv, InToolchain, Intermed, OutputActionList, ModName):

        Logger.Logger(3, "Uniting module: " + ModName)

        # The Object file count we are currently on (will be used for naming files)
        ObjFileCount = 0

        OutputObjectFiles = []

        # Clean Unity Files if they exist
        CleanIntermed = os.path.join(Intermed, "Unity")

        for Root, _, Files in os.walk(CleanIntermed):
            for File in Files:
                FullPath = os.path.join(Root, File)

                # If there's a custom cpp file in unity directory, then delete it
                if os.path.exists(FullPath) and FullPath.endswith(".cpp"):
                    os.remove(FullPath)

        # For each file in list
        for File in FilesList:

            # Read file
            ReadCppCodeInternal = open(os.path.join(File), "r")

            ReadCppCode = ReadCppCodeInternal.read()

            # If we have a conflict, then we will switch to a new file to continue unifying
            if Unity.DoesCodeHaveConficts(ReadCppCode) is True:
                ObjFileCount += 1

            # Get full directory of unity cpp file
            IntermedCppFile = os.path.join(Intermed, "Unity", ModName + "." + str(ObjFileCount) + ".cpp")

            os.makedirs(os.path.dirname(IntermedCppFile), exist_ok=True)

            # Write to file
            WriteCppCode = open(IntermedCppFile, "a")

            WriteCppCode.write(ReadCppCode)

            WriteCppCode.close()

            # Add to output objects files if not already in it
            if IntermedCppFile not in OutputObjectFiles:
                OutputObjectFiles.append(IntermedCppFile)

        LinkArray = []

        # Optimize code
        for PostFiles in OutputObjectFiles:
            ReadCpp = open(PostFiles, "r")
            ReadCppCode = ReadCpp.read()

            # Get optimized code
            UpdatedCppCode = Unity.OptimizeCodePost(ReadCppCode)

            ReadCpp.close()

            # Write opimized code

            WriteCpp = open(PostFiles, "w")

            WriteCpp.write(UpdatedCppCode)

            WriteCpp.close()

        # Compile the unity files
        LinkArray.extend(InToolchain.CompileMultiArchCPPs(CompileEnv, OutputObjectFiles, Intermed, OutputActionList))

        return LinkArray
