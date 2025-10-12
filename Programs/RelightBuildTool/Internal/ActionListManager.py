import os

from . import Action
from . import ActionExecute
from . import Logger

from functools import cmp_to_key


# Sort the list (this is to help executer)
def Sort(ActionList):

    # Reset all DependCount
    for Item in ActionList:
        Item.DependCount = 0

    # Set all DependCount

    for Item in ActionList:
        Lis = []
        Item.AddDependCount(Lis)

    # We can now sort ActionList

    Ret = ActionList.sort(key=cmp_to_key(Action.Action.ComparePrecondition))

    ActionList = Ret


# Checks if there's a circular dependency (when modules rely on each other)
def CycleDetection(ActionList, ItemActionDictionary):
    pass


# Add's the PreconditionListOutput of all actions and it's Precondition
def GetPrecondition(ActionList, PreconditionListOutput):

    # For each action, run the GetPreconditionSingle

    for Item in ActionList:
        GetPreconditionSingle(Item, PreconditionListOutput)


# Add's the PreconditionListOutput of an action and all it's Precondition
def GetPreconditionSingle(InAction, PreconditionListOutput):

    # Ensure's that there are no duplicates
    if InAction not in PreconditionListOutput:
        PreconditionListOutput.append(InAction)  # Add self to list

        # Adds all Precondition Items to list, via recursive
        for Item in InAction.PreconditionActions:
            GetPreconditionSingle(Item, PreconditionListOutput)


# Checks if there's any issues with the action list
def CheckConflicts(ActionList):
    pass


# Get's all Actions that are oudated
def GetAllOutdatedActions(ActionList, OutdatedActionList, IgnoreOutdatedLib):
    for Item in ActionList:
        AddActionOutdated(Item, OutdatedActionList, IgnoreOutdatedLib)


# Set's a specified action to check if it's outdated
def AddActionOutdated(Action, OutdatedActionList, IgnoreOutdatedLib):

    Outdated = False

    # If Action already exist in OutdatedActionList, we will just return the same thing
    if OutdatedActionList.get(Action) is True:
        return OutdatedActionList[Action]

    # if the imput file doesn't exist, and it ends with .obj or .o, then we gotta update it

    for Input in Action.InputFiles:
        if not os.path.exists(Input):
            Outdated = True
            if Action not in OutdatedActionList:
                OutdatedActionList[Action] = Outdated

                return Outdated

    # If the file doesn't exist, and it isn't an object file, then we gotta compile it!
    for Output in Action.OutputItems:

        if not os.path.exists(Output):
            Outdated = True

    # If any input has been updated compared to all the output, then the entire action is outdated
    for Input in Action.InputFiles:

        SourceFileTime = os.path.getmtime(Input)

        for Output in Action.OutputItems:

            if os.path.exists(Output):

                OutputFileTime = os.path.getmtime(Output)

                if SourceFileTime > OutputFileTime:
                    Outdated = True

    # If the file does exist, but has no bytes and it isn't an object file, then we also gotta compile it!
    # Used incase of corruption
    for Output in Action.OutputItems:
        if not Output.endswith(".obj") and not Output.endswith(".o"):

            if os.path.exists(Output) and os.path.getsize(Output) == 0:
                Outdated = True

    if IgnoreOutdatedLib is False:
        # Check if action is outdated for all precondition actions
        for Item in Action.PreconditionActions:
            if AddActionOutdated(Item, OutdatedActionList, IgnoreOutdatedLib) == True:
                Outdated = True

        # If any Precondition item has been updated compared to all the output, then the entire action is outdated
        for Input in Action.PreconditionItems:

            if os.path.exists(Input):
                SourceFileTime = os.path.getmtime(Input)

                for Output in Action.OutputItems:

                    if os.path.exists(Output):
                        OutputFileTime = os.path.getmtime(Output)

                        if SourceFileTime > OutputFileTime:
                            Outdated = True

    # TODO: Add Dependency file support

    if Action not in OutdatedActionList:
        OutdatedActionList[Action] = Outdated

    return Outdated


# Deletes all files that are outdated
def DeleteOutdatedFiles(OutdatedActionList):
    pass


# Link the actions together
def Link(ActionList):

    # This dictionary will attach each output file to an action, there can be multiple actions per file, but only one file name
    # Example:
    # File1.o | Action1
    # File2.a | Action1
    # Output.exe | Action2
    ItemAction = {}

    for Item in ActionList:

        for Fil in Item.OutputItems:
            ItemAction[Fil] = Item

    # Checks for any cycles
    CycleDetection(ActionList, ItemAction)

    # Set the PreconditionAction for each action
    for Item in ActionList:
        # Clear PreconditionAction in the action
        Item.PreconditionActions = []

        # For each PreconditionItems, add it the action's PreconditionActions if it's not in ItemAction list
        for PreItem in Item.PreconditionItems:

            if PreItem in ItemAction:
                New = ItemAction[PreItem]
                Item.PreconditionActions.append(New)

    # Sorts the action list
    Sort(ActionList)


# Returns all Actions to Execute
def GetActionToExecute(ActionList, PreconditionActionList, CppCache, IgnoreOutdatedLib):

    ActionOutdatedMap = {}  # Action | Bool

    # By default, set everything to true
    for Item in PreconditionActionList:
        ActionOutdatedMap[Action] = True

    ActionOutdatedDict = {}  # Action | Bool

    GetAllOutdatedActions(ActionList, ActionOutdatedDict, IgnoreOutdatedLib)

    Ret = []

    # Set Ret to all actions to execute, so long as it's invalid or outdated
    for Item in ActionList:
        if Item.CommandPath is not None and ActionOutdatedMap.get(Item, True):
            if ActionOutdatedDict.get(Item) is True:
                Ret.append(Item)

    return Ret


# Execute the list of actions
def Execute(BuildConfig, ActionToExecuteList):

    # If the list is empty, we can quit the execution
    if len(ActionToExecuteList) == 0:
        return

    Executer = (
        ActionExecute.LinearExecuter()
    )  # FIXME: As a temp solution, we are just using LinearExecuter, add support for switching to multiple executers!

    # Execute the action list, stores if successful
    Ex = Executer.ExecuteActionList(ActionToExecuteList)

    # If not successful, throw an error

    if Ex is False:
        Logger.Logger(5, "We have failed to run ActionToExecuteList") # TODO: Add detailed description

    # FIXME: Verify and read all file output info
