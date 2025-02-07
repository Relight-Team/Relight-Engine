import os
import FileSystem as FS





def GetVar(URL, VarName):
    #print(URL)
    #print(VarName)
       with open(URL, 'r') as file:
        try:
            return FS.InternalGetVar(URL, VarName)
        except:
            return None




def GetVarOptional(URL, VarName, Alt):
    with open(URL, 'r') as file:
        try:
            return FS.InternalGetVar(URL, VarName)
        except:
            return Alt




def CheckFolder(URL):
    if not os.path.exists(URL):
        os.makedirs(URL)


def CheckFile(URL):
    if os.path.isfile(URL):
        return True
    else:
        return False


def ArraySearch(Search, Array):
    for i in range(len(Array)):
        if Search == Array[i]:
            return True
    return False

def ChangeVar(Var, New):
    FS.ChangeVarInternal(Var, New)



def PrintDebug(Text, Show):
    if Show == True:
        print(Text)

def FindDepend(DepName, Engine_Directory, Target_Directory):
    if os.path.isdir(Target_Directory + "/Src/" + DepName):
        return Target_Directory + "/Src/" + DepName

    # If it is a Target File
    elif os.path.isdir(Target_Directory + "/" + DepName):
        return Target_Directory + "/" + DepName

    elif os.path.isdir(Engine_Directory + "/Runtime/" + DepName):
        return Engine_Directory + "/Runtime/" + DepName

    elif os.path.isdir(Engine_Directory + "/Editor/" + DepName):
        return Engine_Directory + "/Editor/" + DepName

    else:
        return ""
