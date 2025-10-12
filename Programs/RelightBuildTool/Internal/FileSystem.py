import os
from Configuration import Directory_Manager


# Read values and execute code from a txt fileY
def load_config_and_execute(filename):

    InConfig = {
        "TARGET_NAME": None,
        "TARGET_DIRECTORY": None,
        "PROJECT": None,
        "PLATFORM": None,
        "PLATFORM_GROUP": None,
        "FILEPATH": None,
    }  # Default defines

    Config = InConfig.copy()  # Final Config we are using

    # Set each Config to StartingTarget if it exist
    for ConfigItem in InConfig:
        if ConfigItem in globals():
            Config[ConfigItem] = globals()[ConfigItem]

    # Set some other config that isn't present in ConfigTarget

    Config["ENGINE_DIRECTORY"] = Directory_Manager.Engine_Directory

    Config["ENGINE_BIN_DIRECTORY"] = os.path.join(
        Directory_Manager.Engine_Directory, "bin"
    )

    Config["ENGINE_BIN_THIRDPARTY_DIRECTORY"] = os.path.join(
        Directory_Manager.Engine_Directory, "bin", "ThirdParty"
    )

    with open(filename, "r") as file:
        exec(
            file.read(), Config
        )  # Execute the contents of the file in a controlled scope

    return Config


# Get value from key, get's from file
def InternalGetVar(filename, value, Alt=None):
    config_values = load_config_and_execute(filename)

    Ret = config_values.get(value)

    if Ret is not None:
        return config_values.get(value)
    else:
        return Alt


# Change global var to match settings
def ChangeVarInternal(StartingTarget, Reader):

    global TARGET_NAME
    global TARGET_DIRECTORY
    global PROJECT
    global PLATFORM
    global PLATFORM_GROUP

    globals()["TARGET_NAME"] = StartingTarget.Name
    globals()["TARGET_DIRECTORY"] = StartingTarget.TargetDir
    globals()["PROJECT"] = StartingTarget.Project
    globals()["PLATFORM"] = StartingTarget.Platform.upper()
    globals()["FILEPATH"] = Reader.FilePath

    # Get platform group
    UnixGroupCheck = ["Linux"]

    GroupToUse = ""

    # Check Unix group
    if StartingTarget.Platform in UnixGroupCheck:
        GroupToUse = "UNIX"

    globals()["PLATFORM_GROUP"] = GroupToUse.upper()
