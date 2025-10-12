import configparser
import os


# Read the config file, get's the value
def ReadConfig(File, Class, Value):
    Config = configparser.ConfigParser()

    if not os.path.exists(File):
        raise ValueError("Error, Config file not found: " + str(File))

    try:
        Config.read(File)
    except Exception:
        raise ValueError("Error, unable to read and parse config file: " + str(File))

    try:
        Ret = Config.get(Class, Value)
    except Exception:
        raise ValueError(
            "Error, unable to read value (CLASS: "
            + str(Class)
            + ", VALUE: "
            + str(Value)
        )
    return Ret
