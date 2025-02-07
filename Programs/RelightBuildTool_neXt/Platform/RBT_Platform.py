import platform

HostOS = platform.system()

if HostOS == "Linux":
    import Platform.Linux.LinuxCommon as Common


def CheckFileExist(Array):
    return Common.CheckFileExist(Array)

def Exec(fil):
    Common.Exec(fil)

def NewLine():
    return Common.NewLine()

def NewTab():
    return Common.NewTab()

def PrintWarning(Text):
    Common.PrintWarning(Text)

def DefaultSDK():
    Common.DefaultSDK()

def CreateFile(Fil):
    Common.CreateFile(Fil)

def Extension():
    return Common.Extension()

def StaticFile():
    return Common.StaticFile()

def Define(Def):
    return Common.Define(Def)

def DoesFileExist(Array):
    return Common.DoesFileExist(Array)
