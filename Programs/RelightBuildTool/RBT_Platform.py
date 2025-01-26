import os
import Configuration as Cfg


## This file acts as an abstraction for compiler and SDK ##

class CompileError(Exception):
        def __init__(self, message):
            super().__init__(message)
            self.message = message


# Set wrapper for Compiler/SDK

## EDIT HERE IF NEEDED FOR YOUR OWN COMPILER! ##
if Cfg.Compiler == "g++":
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
