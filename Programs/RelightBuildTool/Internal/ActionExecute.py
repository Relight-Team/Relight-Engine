import subprocess
import threading
import os
import time
from pathlib import Path

from Internal import Logger


# This handles the different types of execution of the list of actions
class RBTThread:

    ExitCode = 0

    Action = None

    Finished = False

    def __init__(self, InAction):
        self.Action = InAction

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

        # Start program
        try:
            try:
                args = [
                    self.Action.CommandPath,
                    self.Action.Arguments,
                ]  # Combines file path and arguments
                RunningProgram = subprocess.Popen(
                    args,
                    cwd=self.Action.CurrentDirectory,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )

                # Run ReadOutput and ReadError
                self._ReadOutput(RunningProgram.stdout)
                self._ReadError(RunningProgram.stderr)
            except Exception:
                pass

            RunningProgram.wait()  # Wait until program stops running

            self.ExitCode = RunningProgram.returncode

            if self.ExitCode != 0:
                Logger.Logger(
                    5,
                    "Error while running program, Error Code: "
                    + str(self.ExitCode)
                    + ", Program name: "
                    + self.Action.CommandPath
                    + ", Program Arguments: "
                    + self.Action.Arguments,
                )

        except Exception:
            print("ERROR")

        self.Finished = True

    # Starts the threading
    def Start(self):
        athread = threading.Thread(target=self.FunctionToRun)
        athread.start()


class ExecuteBase:

    def Name(self):
        return "Base"

    def ExecuteActionList(self, ActionList):
        pass  # Overritten by child class


# Executes actions one at a time
class LinearExecuter(ExecuteBase):

    def Name(self):
        return "Linear"

    # Execute each action from the action list
    def ExecuteActionList(self, ActionList):

        ActionThreadDict = {}  # A dictionary of Action : Thread
        Logger.Logger(3, "Compiling C++ Code...")

        Progress = 0

        Loop = True

        # Loop until we are done
        while Loop:

            ExeAction = 0  # All actions that we are currently executing
            NonExeAction = 0  # All actions that isn't executed

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
                        ExeAction += 1
                        NonExeAction += 1

            # Update the progress
            Progress = len(ActionList) + 1 - NonExeAction
            Logger.Logger(3, "Progress: " + str(Progress))

            # If we have no more actions that isn't executed, then we can stop
            if NonExeAction == 0:
                Loop = False

            for i in ActionList:

                ActionThr = None

                ActionThrFound = False

                # if true, set both ActionThrFound and ActionThr
                if i in ActionThreadDict:
                    ActionThrFound = True
                    ActionThr = ActionThreadDict[i]

                if ActionThrFound is False:

                    # if Execute Actions is less than the cpu count
                    if ExeAction < max(1, os.cpu_count()):
                        ContainOutdatedPre = (
                            False  # If any action's Precondition is outdated
                        )
                        ContainFailedPre = (
                            False  # If any action's Precondition has failed
                        )

                        # Detect if any Precondition Actions is either outdated or has failed
                        for j in i.PreconditionActions:

                            # Detect if any Precondition Actions is either outdated or has failed
                            if j in ActionThreadDict:
                                PreThread = ActionThreadDict[j]

                                if PreThread is None:
                                    ContainFailedPre = True

                                elif PreThread.Finished is False:
                                    ContainOutdatedPre = True

                                elif PreThread.ExitCode != 0:
                                    ContainFailedPre = True
                            else:
                                ContainOutdatedPre = True

                        # If we failed, we can add the action to dictionary, but we should leave the thread blank, since we are not ready to execute yet
                        if ContainFailedPre is True:
                            ActionThreadDict[i] = None

                        # If it hasn't failed and isn't outdated, add action and the thread to the dictionary
                        elif ContainFailedPre is False:

                            TD = RBTThread(i)  # Store action to execute
                            try:
                                TD.Start()  # Execute action

                                # Force to run once at a time

                                while not TD.Finished:
                                    time.sleep(0.1)

                            except Exception:
                                pass

                            ActionThreadDict[i] = (
                                TD  # Store Action with the value of the thread into the dictoonary
                            )

                            ExeAction += 1  # add 1 to Executing Actions

        Ret = True

        # If there's any errors in the dictionary, return false
        for Action, ThreadItem in ActionThreadDict.items():

            if ThreadItem is None or ThreadItem.ExitCode != 0:
                Ret = False

        print()

        # Return's the Ret value, this will let us know if there was any errors (true if no errors, false if there was errors)
        return Ret


# TODO: Add support for ParallelExecuter
# Executes multiple actions at a time, mainly for AutomationTool
# class ParallelExecuter(ExecuteBase)
