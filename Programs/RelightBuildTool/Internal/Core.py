import os

from . import FileSystem as FS

from . import Logger

# Get variable from file
# <URL> the file to read
# <VarName> The name of the value
# <Alt> The alternative value if we couldn't find VarName
# <Return> variable of VarName, alt if not found
def GetVar(URL, VarName, Alt=None):
    with open(URL, "r") as file:
        try:
            return FS.InternalGetVar(URL, VarName, Alt)
        except Exception:
            return Alt

# Get variable from file TODO: Do we need this?
# <URL> the file to read
# <VarName> The name of the value
# <Alt> The alternative value if we couldn't find VarName
# <Return> variable of VarName, alt if not found
def GetVarOptional(URL, VarName, Alt):
    with open(URL, "r") as file:
        try:
            return FS.InternalGetVar(URL, VarName, Alt)
        except Exception:
            return Alt

# Check if folder exists, if it doesn't, log it and create it
# <URL> the directory to check, if failed, create it
def CheckFolder(URL):
    if not os.path.exists(URL):
        Logger.Logger(2, "Creating Dir: " + URL)
        os.makedirs(URL)

# Check if file exists
# <URL> the file to check
# <Return> true if file exists
def CheckFile(URL):
    if os.path.isfile(URL):
        return True
    else:
        return False


# Change the variables that the file will read
# <StartingTarget> The starting target
# <Reader> the reader file
def ChangeVar(StartingTarget, Reader):
    FS.ChangeVarInternal(StartingTarget, Reader)

# Print only if we are allowed to
# <Text> what to print
# <Show> true if we will print out debug stuff
def PrintDebug(Text, Show):
    if Show is True:
        print(Text)
