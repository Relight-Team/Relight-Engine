from enum import Enum
import sys
import os

from Internal import ActionListManager
from Internal import TargetBuilder
from Internal import Logger

from BaseSDK import Platform

from Readers import TargetReader


class Options:

    SkipBuild = False  # If we should skip the build, used for testing

    NoMessages = False  # If true, do not print anything

    Precompile = False  # If true, we will use precompiled binary for engine modules

    def __init__(self):
        pass


# The main function we are going to execute in this mode
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

    Option = Options()

    Logger.Logger(3, "Registering platforms...")

    Platform.Platform.RegPlatform(Args, False)

    BuildProcess(StartingTargetList, None, Option)

    Logger.Logger(3, "Build Completed!")


# Build's the list of target
def BuildProcess(StartingTargetList, WorkingSet, InOptions):

    if InOptions.SkipBuild is False:

        ExecuteActionsTarget = []

        # Have a list to convert all targets into actions
        for Item in StartingTargetList:
            FileBuild = CreateAndRunTargetBuilder(InOptions, Item, WorkingSet)
            TargetAction = GetActionFromTarget(Item, InOptions, FileBuild)
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
            # TODO: Sync XGE, Distcc, and SNDBS from BuildPlatform to InOptions, should only be set true/false if all of them are that value

        if len(ExecuteActions) == 0 and InOptions.NoMessages is True:
            Logger.Logger(3, "All targets are up to date")

        else:
            # Execute Actions
            ActionListManager.Execute(InOptions, ExecuteActions)


# Create's a TargetBuilder and build's it
def CreateAndRunTargetBuilder(InOptions, StartingTarget, WorkingSet):

    Logger.Logger(1, "Creating TargetBuilder...")

    Builder = TargetBuilder.TargetBuilder.Create(
        StartingTarget, InOptions.Precompile
    )  # This will create TargetRules as well

    Logger.Logger(1, "Building TargetBuilder...")

    return Builder.Build(InOptions, WorkingSet, True)


# Create's a Relight Header file
def CreateRHFile():
    pass


# if there's multiple target's, we will merge them together into a single action list and return the new list
def MergeActionList(TargetList, ActionList):
    pass


# Get all actions to execute
def GetActionFromTarget(StartingTarget, BuildConfig, FileBuild):

    Logger.Logger(1, "Getting Actions from target...")

    Logger.Logger(1, "Linking main action list from TargetBuilder...")
    ActionListManager.Link(FileBuild.ActionList)  # Link the main action list

    # TODO: Add Hot Reload support

    PreconditionActions = GetPreconditionActions(StartingTarget, FileBuild)

    ActionListManager.Link(PreconditionActions)  # Link the precondition action list

    # TODO: add CppDependencies support

    Logger.Logger(1, "Linking all Precondition actions...")
    ActionsToExecute = ActionListManager.GetActionToExecute(
        FileBuild.ActionList, PreconditionActions, None, False
    )  # TODO: This is a temp

    return ActionsToExecute


# This will get all precondition from actions
def GetPreconditionActions(StartingTarget, FileBuild):
    Ret = []

    # TODO: Add SingleFileToCompile support!

    GetPreconditionActionsFromActions(FileBuild.ActionList, Ret)

    return Ret


# Function that helps GetPreconditionActions    print("asdfadfadf " + StartingTarget.Name)
def GetPreconditionActionsFromActions(ActionList, OutputList):
    Ret = []

    for Action in ActionList:
        GetPreconditionActionsFromSingleAction(Action, OutputList)


# Function that helps GetPreconditionActions
def GetPreconditionActionsFromSingleAction(Action, OutputList):
    if Action not in OutputList:
        OutputList.append(Action)

        for Precondition in getattr(Action, "PreconditionActions", []):
            GetPreconditionActionsFromSingleAction(Precondition, OutputList)
