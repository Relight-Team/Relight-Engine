import os
import subprocess
import Configuration as Cfg


## This file acts as an abstraction for compiler and SDK ##

class CompileError(Exception):
        def __init__(self, message):
            super().__init__(message)
            self.message = message




def Internal_Check_File_Exist(Array):
    try:
        # Run 'clang --version' to check if Clang is available
        subprocess.run(Array, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        # Clang is not installed or there's an error
        return False

# Set wrapper for Compiler/SDK

## EDIT HERE IF NEEDED FOR YOUR OWN COMPILER! ##

# Default
if Cfg.Compiler == "Default":
    if os.name == "posix":
        if Internal_Check_File_Exist(['clang', '--version']):
            import Compiler.CLANG.common as T
        elif Internal_Check_File_Exist('g++' '--version'):
            print("WARNING: clang is not installed or is setup improperly, clang is the recommended SDK for unix/posix OS, using g++ as a backup")
            import Compiler.GPP.common as T
        else:
            raise CompileError("Exiting: both clang and g++ are either not installed or is setup improperly, we recommend installing clang on this system")
    else:
        print("TODO: Add support for other OS like windows and mac")
# ==== #



elif Cfg.Compiler == "g++":
    import Compiler.GPP.common as T
elif Cfg.Compiler == "Clang":
    import Compiler.CLANG.common as T
else:
    raise CompileError("Error, Compiler in config is incorrect, we got " + Cfg.Compiler)


# Wrapper Functions
def Start(Platform='Unix'):
    return T.Start(Platform)

def Name():
    return T.Name()

def PublicLink(dire):
    return T.PublicLink(dire)

def CompileTag():
    return T.CompileTag()

def LinkTag(dire):
    return T.LinkTag(dire)

def LinkTagFinal(dire):
    return T.LinkTagFinal(dire)

def LinkTagMini(dire):
    return T.LinkTagMini(dire)

def LinkTagMiniFinal(dire):
    if T.Name() == "Clang":
        return T.LinkTagMiniFinal(dire)
    else:
        return T.LinkTagMini(dire)

def LinkCashe(Cashe1, Dep, Static_Lib):
    return T.LinkCashe(Cashe1, Dep, Static_Lib)

def Output(dire):
    return T.Output(dire)

def ComToStatic(dire):
    return T.ComToStatic(dire)

def Define(DefText):
    return T.Define(DefText)

def LoopCpp(Source):
    return T.LoopCpp(Source)
