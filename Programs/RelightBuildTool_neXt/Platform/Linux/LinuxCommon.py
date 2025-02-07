import os
import subprocess

def CheckFileExist(Array):
    try:
        # Run 'clang --version' to check if Clang is available
        subprocess.run(Array, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        # Clang is not installed or there's an error
        return False

def Exec(fil):
    os.system(fil)

def NewLine():
    return "\n"

def NewTab():
    return "\t"

def PrintWarning(Text):
    print('\033[93m' + "Warning: " + Text + '\033[0m')

def DefaultSDK():
    if CheckFileExist(['clang++', '--version']):
        return "Clang++"
    elif CheckFileExist(['g++', '--version']):
        PrintWarning("Clang is recommended for compiling on linux platform, using g++ as backup")
        return "g++"


def CreateFile(Fil):
    os.system("touch " + Fil)

def Extension():
    return ""

def StaticFile():
    return ".o"

def Define(Def):
    return "-D" + Def

def DoesFileExist(Array):
    try:
        subprocess.run(Array, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False
