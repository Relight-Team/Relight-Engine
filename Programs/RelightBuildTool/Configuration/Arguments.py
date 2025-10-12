class Args:

    ParseArgs = None  # The Arg class that we will use

    def __init__(self, Args):
        self.ParseArgs = Args

    # Get's the value of arguments, this is seperate to support the '+' array system
    def GetAndParse(self, ArgPass):

        Value = getattr(self.ParseArgs, ArgPass, None)

        if Value is None or Value == "":
            return None

        if isinstance(Value, str) and "+" not in Value:
            return Value

        else:
            Ret = Value
            if isinstance(Value, str):
                Ret = Value.split("+")
            return Ret
