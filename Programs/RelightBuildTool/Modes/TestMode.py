import sys
import os

from Internal import TargetBuilder
from Internal import Logger

from BaseSDK import Platform

from Readers import TargetReader


def Error(Str):
    Logger.Logger(5, "Testing failed, " + Str)


def Main(Args):

    StartingTarget = TargetReader.StartingTarget(Args.GetAndParse("Platform"))

    StartingTarget.Name = os.path.basename(Args.GetAndParse("Target"))

    StartingTarget.Project = Args.GetAndParse("Project")

    StartingTarget.TargetDir = Args.GetAndParse("TargetDir")

    StartingTarget.Arch = Args.GetAndParse("Arch")

    StartingTarget.BuildType = Args.GetAndParse("BuildType")

    Logger.Logger(3, "Checking if arguments are valid")

    if StartingTarget.Project is None:
        if StartingTarget.Name is None:
            Error("Project File and Target File not set")

    if StartingTarget.TargetDir is None:
        Logger.Logger(4, "TargetDir is not set")

    if StartingTarget.Arch is None:
        Logger.Logger(4, "Arch is not set")

    if StartingTarget.BuildType is not None:
        if (
            StartingTarget.BuildType != "Final"
            and StartingTarget.BuildType != "Development"
            and StartingTarget.BuildType != "Debug"
        ):
            Error(
                "BuildType is incorrect and is set, we got "
                + str(StartingTarget.BuildType)
            )

    TB = TargetBuilder.TargetBuilder.CreateTargetReaderFromTargetName(
        StartingTarget.Name, StartingTarget
    )

    if TB is None:
        Error(
            "Somehow TargetBuilder.CreateTargetReaderFromTargetName pass initially, but we still got None"
        )
