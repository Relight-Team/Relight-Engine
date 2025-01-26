import os


def Start(Platform='Unix'):
    if Platform == 'Win64':
        return "x86_64-w64-mingw32-clang++ -static -static-libgcc -static-libstdc++ "
    else:
        return "clang "


def Name():
    return "Clang"


def PublicLink(dire):
    return "-I" + dire

def CompileTag():
    return "-c "

def LinkTag(dire):
    return ""

def LinkTagFinal(dire):
    return "-L" + dire

def LinkTagMini(dire):
    return ""

def LinkTagMiniFinal(dire):
    return "-l" + dire

def LinkCashe(Cashe1, Dep, Static_Lib):
    return "-L" + Cashe1 + "/" + Dep + Static_Lib + " "

def Output(dire):
    return " -o " + dire

def ComToStatic(dire):
    return " ar rcs " + dire

def Define(DefText):
    return "-D" + DefText + " "

def LoopCpp(Source):
    return '$(find ' + Source + ' -type f -name "*.cpp" | head -n 1) '
