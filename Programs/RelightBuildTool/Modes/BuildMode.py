import sys
import os

from Action import ActionListManager
from Builders import TargetBuilder
from Internal import Logger

from BaseSDK import Platform

from Readers import TargetReader

# The main function we are going to execute in this mode
# <Args> The argument object from main.py
def Main(Args):

    # Convert Args to StartingTarget
    StartingTarget = TargetReader.StartingTarget(Args.GetAndParse("Platform"))

    # TODO: Add Project Reader support to read targets listed in that, for now we will always use -Target= argument

    StartingTarget.Name = os.path.basename(Args.GetAndParse("Target"))

    StartingTarget.Project = Args.GetAndParse("Project")

    StartingTarget.Modules = Args.GetAndParse("Module")

    StartingTarget.TargetDir = Args.GetAndParse("TargetDir")

    StartingTarget.GonnaCook = Args.GetAndParse("Cook")

    StartingTarget.Arch = Args.GetAndParse("Arch")

    StartingTarget.BuildType = Args.GetAndParse("BuildType")

    print("Building " + str(StartingTarget.Name))

    StartingTargetList = []
    StartingTargetList.append(StartingTarget)

    SkipBuild = Args.GetAndParse("SkipBuild")
    NoMessages = Args.GetAndParse("NoMessages")
    PreCompile = Args.GetAndParse("PreCompile")

    Logger.Logger(3, "Registering platforms...")

    # Register the platform, let's RBT know it exist
    Platform.Platform.RegPlatform(Args, False)

    # Start build process
    BuildProcess(StartingTargetList, SkipBuild, NoMessages, PreCompile)

    Logger.Logger(3, "Build Completed!")


# Build's the list of target
# <StartingTargetList> The list of all starting target
# <SkipBuild> If we should skip the build process, used for testing
# <NoMessages> If true, do not print anything
# <PreCompile> If true, we will use precompiled binary for engine modules
def BuildProcess(StartingTargetList, SkipBuild, NoMessages, PreCompile):

    # If we are skipping build, don't build it
    if SkipBuild == None or SkipBuild == False:

        # Lists of actions we need to execute
        ExecuteActionsTarget = []

        # For each beginning target
        for Item in StartingTargetList:

            FileBuild = CreateAndRunTargetBuilder(PreCompile, Item)

            TargetAction = GetActionFromTarget(Item, FileBuild)

            ExecuteActionsTarget.append(TargetAction)

        # If there's only one target, add it to the action to execute, otherwise we will combine them into one list of actions
        if len(StartingTargetList) == 1:
            ExecuteActions = []
            ExecuteActions.extend(ExecuteActionsTarget[0])
        else:
            ExecuteActions = MergeActionList(StartingTargetList, ExecuteActionsTarget)

        # Link actions together
        Logger.Logger(1, "Linking all Execution Actions...")
        ActionListManager.Link(ExecuteActions)

        # Ensures that each item has the same config
        for Item in StartingTargetList:
            BuildPlatform = Platform.Platform.GetBuildPlatform(Item.Platform)

        # If we have no actions to execute and we are allowed to send messages, let user know
        if len(ExecuteActions) == 0 and (NoMessages != None or NoMessages == True):
            Logger.Logger(3, "All targets are up to date")

        else:
            # Execute Actions
            ActionListManager.Execute(ExecuteActions)


# Create's a TargetBuilder and build's it
# <Precompile> true if we are using precompiled binary
# <StartingTarget> The starting target to Compile
# <Return> The Filebuilder class
def CreateAndRunTargetBuilder(Precompile, StartingTarget):

    Logger.Logger(1, "Creating TargetBuilder...")

    Builder = TargetBuilder.TargetBuilder.Create(StartingTarget, Precompile)  # This will create TargetRules as well

    Logger.Logger(1, "Building TargetBuilder...")

    return Builder.Build()


# Create's a Relight Header file
def CreateRHFile():
    pass


# if there's multiple target's, we will merge them together into a single action list and return the new list
def MergeActionList(TargetList, ActionList):
    pass


# Get all actions to execute
# <StartingTarget> The starting target to use
# <FileBuild> The FileBuilder class
# <Return> List of actions to execute
def GetActionFromTarget(StartingTarget, FileBuild):

    Logger.Logger(1, "Getting Actions from target...")

    Logger.Logger(1, "Linking main action list from TargetBuilder...")
    ActionListManager.Link(FileBuild.ActionList)  # Link the main action list

    # TODO: Add Hot Reload support

    PreconditionActions = GetPreconditionActions(StartingTarget, FileBuild)

    ActionListManager.Link(PreconditionActions)  # Link the precondition action list

    # TODO: add CppDependencies support

    Logger.Logger(1, "Linking all Precondition actions...")
    ActionsToExecute = ActionListManager.GetActionToExecute(FileBuild.ActionList, PreconditionActions, False)  # TODO: This is a temp

    return ActionsToExecute


# This will get all precondition from actions
# <StartingTarget> The starting target to use (Used for SingleFileToCompile, so unused for now)
# <FileBuild> The FileBuilder Class
# <Return> List of all precondition actions
def GetPreconditionActions(StartingTarget, FileBuild):
    Ret = []

    # TODO: Add SingleFileToCompile support!

    # Get the precondition actions
    GetPreconditionActionsFromActions(FileBuild.ActionList, Ret)

    return Ret


# Get Precondition action from list of actions
# <ActionList> The list of actions to get precondition actions from
# <OutputList> List of all precondition actions, will be appended
def GetPreconditionActionsFromActions(ActionList, OutputList):

    # For each action, get precondition actions
    for Action in ActionList:
        GetPreconditionActionsFromSingleAction(Action, OutputList)


# Recursively Get Precondition actions from action
# <Action> The action to check
# <OutputList> List of Precondition actions, will be appended
def GetPreconditionActionsFromSingleAction(Action, OutputList):

    # Only run if actions isn't already in list
    if Action not in OutputList:

        # Append parent action
        OutputList.append(Action)

        # If Action.PreconditionActions exists, use it, otherwise use empty list
        for Precondition in getattr(Action, "PreconditionActions", []):

            # Run this function with the precondition
            GetPreconditionActionsFromSingleAction(Precondition, OutputList)
