# Read values and execute code from a txt file

UNIX = False

def load_config_and_execute(filename):
    global UNIX
    config = {'UNIX': UNIX} # Default defines
    with open(filename, 'r') as file:
        exec(file.read(), {}, config)  # Execute the contents of the file in a controlled scope
    return config


def InternalGetVar(filename, value):
    config_values = load_config_and_execute(filename)
    return config_values.get(value)

def ChangeVarInternal(Var, New):
    global UNIX
    if Var == "UNIX":
        UNIX = New
