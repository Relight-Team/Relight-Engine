import os
from . import Logger


# Get every file from dirctory
# <Path> The path to get every file from
# <Return> the list of files, or if the path is a file, return itself. It will return empty if no files in directory
def GetAllFilesFromDir(Path):

    if os.path.isdir(Path):
        return os.listdir(Path)
    elif os.path.isfile(Path):
        return Path  # Return the file name only
    else:
        return []


# Create an intermediate file and add content into that file, will create backup if file already exists
# <Path> The full path and file name
# <Content> The contents of the file
def CreateIntermedFile(Path, Content):

    Logger.Logger(2, "Creating Intermediate file at " + Path)

    # Directory of the file
    Dir_Name = os.path.dirname(Path)

    # Create directory if it doesn't exist
    os.makedirs(Dir_Name, exist_ok=True)

    # File doesn't exist, nothing to back up, just write to file
    if not os.path.exists(Path):
        Fil = open(Path, "w")
        NewWrite = str("".join(Content))
        Fil.write(NewWrite)
        Fil.close()

    # Backup old data
    else:

        BackupFile = Path + ".backup"

        Logger.Logger(2, "Creating backup of " + Path + " called " + BackupFile + ". Writing to initial path now")

        # TODO: Add windows support
        os.system("mv " + Path + " " + BackupFile)

        # Write file
        Fil = open(Path, "w")
        NewWrite = str("".join(Content))
        Fil.write(NewWrite)
        Fil.close()
