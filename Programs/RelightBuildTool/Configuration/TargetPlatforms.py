from enum import Enum


class TargetPlatform(Enum):
    Unknown = 0
    Linux = 1
    Win32 = 2
    Win64 = 3


class TargetGroupPlatform(Enum):
    Unix = [
        TargetPlatform.Linux.name
    ]  # Platforms using UNIX/POSIX based system (Linux, Solaris, Unix, etc)
    NT = [
        TargetPlatform.Win32.name,
        TargetPlatform.Win64.name,
    ]  # Platforms using Microsoft's NT Kernel (Win32, Win64, Xbox, etc)


def Valid(T):
    for i in TargetPlatform:
        if i.name.lower() == T.lower() and i.name.lower() != "Unknown":
            return True

    return False


def GetPlatformGroup(Platform):
    for Group in TargetGroupPlatform:

        Val = Group.value

        for i in Val:
            if i.lower() == Platform.lower():
                return Group.name

    return None


def ReturnTargetGroupVar(Group):
    for Grou in TargetGroupPlatform:

        if Group.lower == Grou.lower:
            return Grou.value


def StringToPlatform(Str):
    for Index in TargetPlatform:
        if Index.name.lower == Str.lower:
            return Index.name

    return ""
