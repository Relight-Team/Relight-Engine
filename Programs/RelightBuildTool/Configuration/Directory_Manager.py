import os
import sys
from pathlib import Path

_Internal_Script_Dir = Path(__file__).resolve().parent

# Engine Directory (/USER/Relight_Engine/)
Engine_Directory = os.path.join(_Internal_Script_Dir, "..", "..", "..")

# Program Directory (/USER/Relight_Engine/Programs)
Program_Directory = os.path.join(Engine_Directory, "Programs")

# RBT Directory (/USER/Relight_Engine/Programs/RelightBuildTool)
RBT_Directory = os.path.join(Program_Directory, "RelightBuildTool")
