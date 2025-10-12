import os
from Internal import Logger


# System that combines .cpp files together
class Unity:

    # Checks if there's any condition that requires a second object file, returns true if we need to create new .o file
    # For example, conflicts, PCH usage, headerTool, etc
    @staticmethod
    def DoesCodeHaveConficts(CppCode):
        return False

    # Cleans up the code for optimization, returns optimized code
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
    @staticmethod
    def UniteCPPFiles(
        FilesList, CompileEnv, InToolchain, Intermed, OutputActionList, ModName
    ):

        Logger.Logger(3, "Uniting module: " + ModName)

        # The Object file count we are currently on (will be used for naming files)
        ObjFileCount = 0

        OutputObjectFiles = []

        # Clean Unity Files if they exist
        CleanIntermed = os.path.join(Intermed, "Unity")

        for Root, _, Files in os.walk(CleanIntermed):
            for File in Files:
                FullPath = os.path.join(Root, File)
                if os.path.exists(FullPath) and FullPath.endswith(".cpp"):
                    os.remove(FullPath)

        for File in FilesList:

            ReadCppCodeInternal = open(os.path.join(File), "r")

            ReadCppCode = ReadCppCodeInternal.read()

            if Unity.DoesCodeHaveConficts(ReadCppCode) is True:
                ObjFileCount += 1

            IntermedCppFile = os.path.join(
                Intermed, "Unity", ModName + "." + str(ObjFileCount) + ".cpp"
            )

            os.makedirs(os.path.dirname(IntermedCppFile), exist_ok=True)

            WriteCppCode = open(IntermedCppFile, "a")

            WriteCppCode.write(ReadCppCode)

            WriteCppCode.close()

            if IntermedCppFile not in OutputObjectFiles:
                OutputObjectFiles.append(IntermedCppFile)

        LinkArray = []

        # Optimize code
        for PostFiles in OutputObjectFiles:
            ReadCpp = open(PostFiles, "r")
            ReadCppCode = ReadCpp.read()

            UpdatedCppCode = Unity.OptimizeCodePost(ReadCppCode)

            ReadCpp.close()

            WriteCpp = open(PostFiles, "w")

            WriteCpp.write(UpdatedCppCode)

            WriteCpp.close()

        LinkArray.extend(
            InToolchain.CompileMultiArchCPPs(
                CompileEnv, OutputObjectFiles, Intermed, OutputActionList
            )
        )

        return LinkArray
