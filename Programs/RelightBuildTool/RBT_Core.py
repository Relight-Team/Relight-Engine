import os
import json


# The code will now be using a json




def GetVar(URL, VarName):
    #print(URL)
    #print(VarName)
    with open(URL, 'r') as file:
        try:
            data = json.load(file)
            return data[VarName]
        except:
            return None




def GetVarOptional(URL, VarName, Alt):
    with open(URL, 'r') as file:
        try:
            data = json.load(URL)
            return data.get
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