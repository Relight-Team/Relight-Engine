import subprocess
import threading
import os
import time
from pathlib import Path
import sys

from Internal import Logger


# This handles the different types of execution of the list of actions
class RBTThread:

    def __init__(self, InAction):
        self.ExitCode = 0
        self.Action = InAction
        self.Finished = False

    # These 2 functions will allow the program to print the output that should be printed from the command line
    def _ReadOutput(self, pipe):
        for line in iter(pipe.readline, ""):
            print(line.strip())
        pipe.close()

    def _ReadError(self, pipe):
        for line in iter(pipe.readline, ""):
            print(line.strip())
        pipe.close()

    # The function that will be run by the thread, this will execute the process based on the action
    def FunctionToRun(self):

        if self.Action.Arguments == "" and self.Action.CommandPath == "":
            raise ValueError("ACTION ARGUMENTS AND COMMAND PATH IS EMPTY")

        # Start program
        try:
            try:

                args = [self.Action.CommandPath, self.Action.Arguments]  # Combines file path and arguments

                # Run the action
                RunningProgram = subprocess.Popen(args, cwd=self.Action.CurrentDirectory, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                # Run ReadOutput and ReadError
                stdout, stderr = RunningProgram.communicate()

                if stdout:
                    print(stdout)

                if stderr:
                    print(stderr)
            except Exception:
                pass

            RunningProgram.wait()  # Wait until program stops running

            # Get exit code, and quit if the action's program returns an error
            self.ExitCode = RunningProgram.returncode

            if self.ExitCode != 0:
                Logger.Logger(5, "Error while running program, Error Code: " + str(self.ExitCode) + ", Program name: " + self.Action.CommandPath + ", Program Arguments: " + self.Action.Arguments)

        except Exception:
            print("ERROR")

        self.Finished = True

    # Starts the threading
    def Start(self):
        athread = threading.Thread(target=self.FunctionToRun)
        athread.start()


# Base class for executer type
class ExecuteBase:

    # Get the name
    # <Return> name of executer type
    def Name(self):
        return "Base"

    # Execute the list of actions
    # <ActionList> The list of actions to execute
    # <Return> true if there are no errors while executing actions
    def ExecuteActionList(self, ActionList):
        pass  # Overritten by child class


# Executes actions one at a time
class LinearExecuter(ExecuteBase):

    # Get the name
    # <Return> name of executer type
    def Name(self):
        return "Linear"

    # Execute each action from the action list
    # <ActionList> the list of actions to execute
    # <Return> true if there are no errors while executing actions
    def ExecuteActionList(self, ActionList):

        ActionThreadDict = {}  # A dictionary of {Action | Thread}
        Logger.Logger(3, "Compiling C++ Code...")

        Progress = 0 # Progress of the execution

        Loop = True # If we should loop

        TotalActions = len(ActionList) # The number of total actions in list

        ActionsExecuted = 0 # The amount of actions we have executed

        # Loop until we are done
        while Loop:

            ExeAction = 0  # All actions that we are currently executing
            NonExeAction = 0  # All actions that isn't executed

            # Update the progress
            for Action, Thread in ActionThreadDict.items():
                if Thread is None or not Thread.Finished:
                    NonExeAction += 1


            # Calculate the progress
            Progress = len(ActionList) - NonExeAction

            # Print out the progress
            sys.stdout.write(f"\rAction Progress: {Progress}/{len(ActionList)}\r")
            sys.stdout.flush()
            time.sleep(0.5)

            # Break the loop if we executed more than what's in the action list
            if ActionsExecuted >= TotalActions:
                break

            # we will update ExeAction and NonExeAction every loop instance
            for Action in ActionList:
                InpThread = None

                # if the action key is not in the dictionary, add 1 to NonExeAction
                if ActionThreadDict.get(Action) == False:
                    NonExeAction += 1

                # else, if the thread (value of key) is not None but the thread is not finished, add 1 to both ExeAction and NonExeAction
                else:
                    InpThread = ActionThreadDict.get(Action)
                    if InpThread is not None and InpThread.Finished is False:
                        #ExeAction += 1 # FIXME: THIS IS PROBLEMATIC!
                        NonExeAction += 1

            # Loop for every action in list
            for ActionItem in ActionList:

                ActionThr = None # The thread of the action

                ActionThrFound = False # If the action is found in dictionary

                # if Action is in Dictionary, set both ActionThrFound and ActionThr
                if ActionItem in ActionThreadDict:
                    ActionThrFound = True
                    ActionThr = ActionThreadDict[ActionItem]

                # If we haven't found the action thread, then create one
                if ActionThrFound is False:
                    # only Execute Actions if we have less than the cpu count
                    if ExeAction < max(1, os.cpu_count()):
                        ContainOutdatedPre = False  # If any action's Precondition is outdated
                        ContainFailedPre = False  # If any action's Precondition has failed

                        # Detect if any Precondition Actions is either outdated or has failed
                        for PreconditionActionItem in ActionItem.PreconditionActions:

                            # If the precondition action is in the action thread dict
                            if PreconditionActionItem in ActionThreadDict:

                                # Create thread
                                PreThread = ActionThreadDict[PreconditionActionItem]

                                # Check if we successfully created PreThread
                                if PreThread is None:
                                    ContainFailedPre = True

                                # Action will be outdated if the Precondition is not finished
                                elif PreThread.Finished is False:
                                    ContainOutdatedPre = True

                                # Action will fail if the precondition action software failed
                                elif PreThread.ExitCode != 0:
                                    ContainFailedPre = True

                            # If precondition action is not in action thread dict, then it's outdated
                            else:
                                ContainOutdatedPre = True

                        # If we failed, we can add the action to dictionary, but we should leave the thread blank, since we are not ready to execute yet
                        if ContainFailedPre is True:
                            ActionThreadDict[ActionItem] = None

                        # If it hasn't failed and isn't outdated, add action and the thread to the dictionary
                        elif ContainFailedPre is False:

                            TD = RBTThread(ActionItem)  # Store action to execute
                            try:
                                TD.Start()  # Execute action

                                # Force to run once at a time

                                while not TD.Finished:
                                   time.sleep(0.1)

                            except Exception:
                                print("FAILED")

                            ActionThreadDict[ActionItem] = TD  # Store Action with the value of the thread into the dictionary)

                            ExeAction += 1  # add 1 to Executing Actions
                            ActionsExecuted += 1



        # The value to return
        Ret = True

        # If there's any errors in the dictionary, return false
        for Action, ThreadItem in ActionThreadDict.items():

            # If the thread part in dictionary is empty, or if the exit code is not 0, then we have errors
            if ThreadItem is None or ThreadItem.ExitCode != 0:
                Ret = False

        # Add space between logs
        print()

        # Return's the Ret value, this will let us know if there was any errors (true if no errors, false if there was errors)
        return Ret


# TODO: Add support for ParallelExecuter
# Executes multiple actions at a time, mainly for AutomationTool
# class ParallelExecuter(ExecuteBase)
