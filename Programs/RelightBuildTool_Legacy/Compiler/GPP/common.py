import os


def Start(Platform='Unix'):
    if Platform == 'Win64':
        return "x86_64-w64-mingw32-g++ -static -static-libgcc -static-libstdc++ "
    else:
        return "g++ "

def PrivateLink(dire, item):
    return "-I" + dire + "/Runtime/" + item + "/Private "


def PublicLink(dire, item):
    return "-I " + dire + "/Runtime/" + item + "/Public "


def Finish(dire, name, dyn):
    return "-c " + dire + "/Public/" + name + ".cpp -o Tmp/" + name + dyn


def Return():
    return command

def FinalCompile(targCom, Name):
    return "-o " + targCom + Name
