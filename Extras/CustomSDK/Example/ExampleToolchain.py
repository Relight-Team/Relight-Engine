# ExampleToolChain handles the actual compiling and linking using tools from SDK

# Examples include: Linking Files, Compiling Files, Flags

from BaseSDK import Toolchain

class ExampleToolchain(Toolchain.ToolchainSDK):

    # First function to run once we create toolchain
    # Usually used for setting up values passed from Platform class
    # Parameters depends per class
    def __init__(self):
        pass

    # Toolchain arguments that will be used in both Compiling and Linking
    # <CompileEnv> - The compile Environment, to check for conditions
    # <Returns> - A string that contains arguments to run the compiler with
    def GetGlobalArg(self, CompileEnv):
        return ""

    # The process of archiving a group of object files (Static Libs)
    # <LinkEnv> - The Link Environment, to check for conditions
    # <OutputActionList> - An array of actions we will append
    # <Returns> - Output File String
    def ArchiveAndIndex(self, LinkEnv, OutputActionList):
        return ""

    # The process of compiling each file into object files, stores each file command into ActionList
    # <CompileEnv> - The Compile Environment, to check for conditions
    # <InputFilesList> - An array of files to compile
    # <DirOutput> - The full output path
    # <OutputActionList> - An array of actions we will append for each file
    # <Returns> - List of all Object Files
    def CompileFiles(self, CompileEnv, InputFilesList, DirOutput, OutputActionList):
        return []

    # The process of linking object files together to form a binary file (executable or dynamic), stores each file command into ActionList
    # <LinkEnv> - The Link Environment, to check for conditions
    # <ImportLibraryOnly> - If true, then we wil always build like a static library, even if LinkEnv is false
    # <OutputActionList> - An array of actions we will append for each file
    # <Returns> - List of all binary files (Executable, Dynamic library, or Static library)
    def LinkFiles(self, LinkEnv, ImportLibraryOnly, OutputActionList):
        return []

    # Actions to run after we compile and link the build, this will run for each binary file created by Linker
    # <File> - The file we will apply the actions
    # <LinkEnv> - The Link Environment, to check for conditions
    # <ActionList> - The list of actions we will append
    # <Returns> - A list of output files
    def PostBuilt(self, File, LinkEnv, ActionList):
        return []
