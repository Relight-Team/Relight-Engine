import os


def Start(Platform='Unix'):
    if Platform == 'Win64':
        return "x86_64-w64-mingw32-g++ -static -static-libgcc -static-libstdc++ "
    else:
        return "g++ "


#def PrivateLink(dire, item):
#    return "-I" + dire + "/Runtime/" + item + "/Private "



def PublicLink(dire):
    return "-I" + dire

def CompileTag():
    return "-c "

def LinkTag():
    return "-L"

def LinkTagMini():
    return "-l"

def LinkCashe(Cashe1, Dep, Static_Lib):
    return "-L" + Cashe1 + "/" + Dep + Static_Lib + " "

def Output():
    return " -o "

def ComToStatic():
    return " ar rcs "

def Define():
    return "-D"
