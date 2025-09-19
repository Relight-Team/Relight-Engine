import os

class BaseCooker:

    SourceDir = None # Game/
    EngineDir = None # RelightEngine/
    BinDir = None # Game/bin/subdirs/

    ContentSourcePath = None
    ContentBinPath = None
    ContentEnginePath = None

    ConfigSourcePath = None
    ConfigBinPath = None
    ConfigEnginePath = None


    def Name(self):
        return "Base"


    def __init__(self, SourceDir, EngineDir, BinDir):
        print("Using " + self.Name() + " Baker")

        self.SourceDir = SourceDir
        self.EngineDir = EngineDir
        self.BinDir = BinDir

        self.ContentSourcePath = os.path.join(self.SourceDir, "Content")
        self.ContentBinPath = os.path.join(self.BinDir, "Content")
        self.ContentEnginePath = os.path.join(self.EngineDir, "Content")

        self.ConfigSourcePath = os.path.join(self.SourceDir, "Config")
        self.ConfigBinPath = os.path.join(self.BinDir, "Config")
        self.ConfigEnginePath = os.path.join(self.EngineDir, "Config")


    # Compiles the config
    def BakeConfigs(self):
        print("Baking Configs")

        # Configs that are not needed by Game, Engine, or Editor
        ForbiddenConfigs = ["BaseBuilder.cfg", "BaseBuilder.Template.cfg"]

        # Create Config directory in bin if it doesn't exist
        os.makedirs(self.ConfigBinPath, exist_ok=True)

        # For each Engine Config, duplicate it to bin
        for Root, SubDirList, FileList in os.walk(self.ConfigEnginePath):
            for File in FileList:
                if File not in ForbiddenConfigs:

                    # Set areas to read and write content
                    FullEngineConfig = os.path.join(Root, File)
                    RelativeFilePath = os.path.relpath(os.path.join(Root, File), self.ConfigEnginePath)
                    FullBinConfig = os.path.join(self.ConfigBinPath, RelativeFilePath)

                    #Run Code
                    os.makedirs(os.path.dirname(FullBinConfig), exist_ok=True)
                    CommandToRun = "cp " + FullEngineConfig + " " + FullBinConfig
                    os.system(CommandToRun)


        # Now, for each Source Configs, sync them
        for SourceRoot, SourceSubDirList, SourceFileList in os.walk(self.ConfigSourcePath):
            for SourceFile in SourceFileList:

                SourceFullFilePath = os.path.join(SourceRoot, SourceFile)
                RelativeFilePath = os.path.relpath(os.path.join(SourceRoot, SourceFile), self.ConfigSourcePath)
                FullSourceConfig = os.path.join(self.ConfigBinPath, RelativeFilePath)

                os.makedirs(os.path.dirname(FullSourceConfig), exist_ok=True)

                # If source file doesn't exist, we can just copy it over
                if not os.path.isfile(os.path.join(self.ConfigBinPath, FullSourceConfig)):
                    CommandToRun = "cp " + SourceFullFilePath + " " + os.path.join(self.ConfigBinPath, FullSourceConfig)
                    os.system(CommandToRun)

                else:
                    # Override engine configs
                    with open(SourceFullFilePath, "r+") as FullSourceConfig:

                        for BinRoot, BinSubDirList, BinFileList in os.walk(self.ConfigBinPath):

                            # For each binary config file
                            for BinFile in BinFileList:

                                BinFullFilePath = os.path.join(BinRoot, BinFile)

                                # Read bin file
                                with open(BinFullFilePath, "r") as BinFile:

                                    # Tracks the group, this is to ensure we don't accidently overwrite same value name in another group
                                    SourceGroupName = ""

                                    for SourceLine in FullSourceConfig:

                                        StripSourceLine = SourceLine.strip()

                                        # If line starts with '[', then it's a group, track it!
                                        if StripSourceLine.startswith("["):
                                            SourceGroupName = StripSourceLine
                                            continue

                                        SourceName = FullSourceConfig.name
                                        BaseSourceName = os.path.basename(SourceName)

                                        self.OverwriteConfigs(os.path.join(self.ConfigBinPath, BaseSourceName), SourceGroupName, SourceLine)


    # Find line in bin file and replace it, seperate function to make code easier to read
    def OverwriteConfigs(self, InFile, Group, InLine):

        Lines = []
        NewLines = []

        with open(InFile, "r") as File:
            Lines = File.readlines()

        BinGroup = ""

        for Line in Lines:

            if Line is None:
                continue

            LineStrip = Line.strip()

            if LineStrip.startswith("["):
                BinGroup = LineStrip

            else:

                InKey = InLine.split('=')[0]
                BinKey = LineStrip.split('=')[0]

                if InKey == BinKey and Group == BinGroup and BinKey != "" and BinKey != " ":

                    NewLines.append(InLine)
                    continue


            NewLines.append(LineStrip)

        with open(InFile, "w") as File:
            for Line in NewLines:
                File.write(Line + "\n")


    # Cooks everything, will ignore certain steps based on settings
    def CookAll(self):
        # For now, always do configs
        self.BakeConfigs()



