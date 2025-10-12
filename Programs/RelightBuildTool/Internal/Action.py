from enum import Enum


# The type of action (for debugging)
class ActionType(Enum):
    Build = 0
    Compile = 1
    Link = 2
    CreateBundle = 3
    WriteMetadata = 4
    PostBuild = 5


# Implementation of Action

# Action in RBT is way to store different build steps, these will be stored in a list, and after the list is done, we will execute each one
# Each action could link files, compile files, etc


class Action:

    Type = ActionType  # The type of action, for debugging reasons

    CommandDescription = (
        ""  # Optional: The command we are going to execute, for debugging
    )

    StatusDescription = (
        ""  # Optional: The file we are going to do the action on, for debugging
    )

    PreconditionItems = (
        []
    )  # All dependencies our action needs before executing, will not execute if file is missing or outdated

    PreconditionActions = []  # All actions that our action needs before executing

    DeleteItems = []  # All files we will delete before executing the action

    OutputItems = []  # All files this action creates

    DependencyListFile = []  # A dependency list file to check each header

    CurrentDirectory = None  # The directory we will produce our OutputItems

    PrintDebugInfo = False  # Should we print info when we create files?

    CommandPath = None  # the command file to run when we are creating our output files

    Arguments = ""  # Parameters to run in the console when running the program

    DebugGroupNames = (
        []
    )  # For multiple compilers, this will add a group name everytime we change the target, mainly used for debugging

    CanRunRemotely = False  # If this is true, then we can run this file through a remote computer (I.E. Incredibuild)

    CanRunRemotelySNDBS = False  # If this and CanRunRemotely is true, means that this action supports SN-DBS (all #imports must be compiled locally)

    UsingGCCCompiler = False  # If true, we will use GCC instead, even if our compiler is set to use Clang

    UsingPCH = False  # If true, then we are using Precompiled header

    PrintStatusDescription = False  # If true, then we will print out StatusDescription when this action runs, for debugging

    CreateImportLib = (
        False  # If true, then any libraries created will be considered "import library"
    )

    DependCount = 0  # How much depend relies on this Action

    InputFiles = (
        []
    )  # Files that this action is using, this will be used to determined if compiled data is outdated compared to new data

    # Adds to the depend amount
    def AddDependCount(self, UsedActions):

        if self not in UsedActions:
            UsedActions.append(self)
            self.DependCount += 1

            for Item in self.PreconditionActions:
                Item.AddDependCount(UsedActions)

    @staticmethod
    def _Sign(Item):
        return (Item > 0) - (Item < 0)

    # Compares Depend Count or length of Precondition Items
    @staticmethod
    def ComparePrecondition(A, B):

        if B.PreconditionActions != B.PreconditionItems:

            return Action._Sign(B.DependCount - A.DependCount)

        else:

            return Action._Sign(len(B.PreconditionItems) - len(A.PreconditionItems))

    # These fix bugs
    def __eq__(self, Other):
        if isinstance(Other, Action):
            if (
                self.CommandPath == Other.CommandPath
                and self.Arguments == Other.Arguments
                and self.CurrentDirectory == Other.CurrentDirectory
            ):
                return True
        return False

    def __hash__(self):
        return hash((self.CommandPath, self.Arguments, self.CurrentDirectory))
