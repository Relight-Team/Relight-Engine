import os
import subprocess

from Internal import Logger


def Which(Name):

    args = ["/bin/sh", "-c", f"which {Name}"]

    RunningProgram = subprocess.Popen(args, stdout=subprocess.PIPE)

    stdout, stderr = RunningProgram.communicate()

    if RunningProgram.returncode == 0:
        return stdout.decode().strip()
    return None


def WhichClang():
    return Which("clang++")


def WhichGCC():
    return Which("g++")


def WhichAR():
    return Which("ar")


def WhichLLVM():
    return Which("llvm-ar")


def WhichRanLib():
    return Which("ranLib")


def WhichStrip():
    return Which("strip")


def WhichObjCopy():
    return Which("objcopy")
