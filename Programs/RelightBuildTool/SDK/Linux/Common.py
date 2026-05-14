import os
import subprocess

from Internal import Logger

# Find system location of software
# <Name> The name of the software
# <Return> The directory of the system software, None if not found
def Which(Name):

    args = ["/bin/sh", "-c", f"which {Name}"]

    RunningProgram = subprocess.Popen(args, stdout=subprocess.PIPE)

    stdout, stderr = RunningProgram.communicate()

    if RunningProgram.returncode == 0:
        return stdout.decode().strip()
    return None

# <Return> Full directory of Clang++, None if not found
def WhichClang():
    return Which("clang++")

# <Return> Full directory of g++, None if not found
def WhichGCC():
    return Which("g++")

# <Return> Full directory of AR, None if not found
def WhichAR():
    return Which("ar")

# <Return> Full directory of LLVM, None if not found
def WhichLLVM():
    return Which("llvm-ar")

# <Return> Full directory of RanLib, None if not found
def WhichRanLib():
    return Which("ranLib")

# <Return> Full directory of Strip, None if not found
def WhichStrip():
    return Which("strip")

# <Return> Full directory of ObjCopy, None if not found
def WhichObjCopy():
    return Which("objcopy")
