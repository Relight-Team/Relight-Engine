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

    CommandDescription = ""  # Optional: The command we are going to execute, for debugging

    StatusDescription = ""  # Optional: The file we are going to do the action on, for debugging

    PreconditionItems = [] # All dependencies our action needs before executing, will not execute if file is missing or outdated

    PreconditionActions = []  # All actions that our action needs before executing

    DeleteItems = []  # All files we will delete before executing the action

    OutputItems = []  # All files this action creates

    DependencyListFile = []  # A dependency list file to check each header

    CurrentDirectory = None  # The directory we will produce our OutputItems

    PrintDebugInfo = False  # Should we print info when we create files?

    CommandPath = None  # the command file to run when we are creating our output files

    Arguments = ""  # Parameters to run in the console when running the program

    DebugGroupNames = [] # For multiple compilers, this will add a group name everytime we change the target, mainly used for debugging

    CanRunRemotely = False  # If this is true, then we can run this file through a remote computer (I.E. Incredibuild)

    CanRunRemotelySNDBS = False  # If this and CanRunRemotely is true, means that this action supports SN-DBS (all #imports must be compiled locally)

    UsingGCCCompiler = False  # If true, we will use GCC instead, even if our compiler is set to use Clang

    UsingPCH = False  # If true, then we are using Precompiled header

    PrintStatusDescription = False  # If true, then we will print out StatusDescription when this action runs, for debugging

    CreateImportLib = False  # If true, then any libraries created will be considered "import library"

    DependCount = 0  # How much dependencies relies on this Action

    InputFiles = [] # Files that this action is using, this will be used to determined if compiled data is outdated compared to new data

    # Recursively adds to the dependencies amount
    # <UsedActions> Lists of actions we already counted, runs recursively
    def AddDependCount(self, UsedActions):

        # Only execute if we haven't counted the action
        if self not in UsedActions:

            # Since we haven't count it yet, we can append it to used actions and increase the count
            UsedActions.append(self)
            self.DependCount += 1

            # Count the dependences for each precondition actions
            for Item in self.PreconditionActions:
                Item.AddDependCount(UsedActions)

    # Returns the sign of item
    # <Item> the item to compare
    # <Return> 1 if positive, 0 if it's actually zero, and -1 if negative
    @staticmethod
    def _Sign(Item):
        return (Item > 0) - (Item < 0)

    # Compares Dependency Count or length of Precondition Items
    # <A> First action to compare
    # <B> Second action to compare
    # <Return> 1 if B has higher precondition items, 0 if both are same, or -1 if A has higher precondition items
    @staticmethod
    def ComparePrecondition(A, B):

        # If Precondition actions and Precondition items are not the same, return the sign
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
