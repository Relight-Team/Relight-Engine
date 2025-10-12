# ExamplePlatformSDK will handle platform-specific SDK functions, and use in most of the other classes

# Examples of some of the use this class has: Ensure SDK files are installed, whether to use system version of SDK or the path to SDK file

from BaseSDK import PlatformSDK

class LinuxPlatformSDK(PlatformSDK.PlatformSDK):

    # Return's if the SDK support AutoSDK (AutoSDK is when the SDK can handle switching between different SDK during compilation runtime)
    # <Returns> True if this SDK supports AutoSDK
    def SupportAutoSDK(self):
        return False

    # Return's the SDK that is required by the platform
    # <Returns> The SDK that is required by this platform as a string
    def GetRequiredSDKString(self):
        return ""

    # Returns the target platform name
    # <Returns> The target platform name
    def GetTargetPlatformName(self):
        return ""

    # Return's true if we have any manual install
    # <Returns> true if any manual install exists
    def HasAnyManualInstall(self):
        return False

    # Used in HasRequiredManualSDK()
    # <Returns> true if we have any required Manual SDK
    def InternalHasRequiredManualSDK(self):
        pass  # Will be overwritten with child class

    # Return's true if we are allowed to have invalid manual installs
    # <Returns> True if we can continue with invalid manual installs
    def AllowInvalidManualInstall(self):
        return False

    # If true, we will use AutoSDK over ManualSDK, otherwise, we will use ManualSDK over AutoSDK
    # <Returns> True if we will use AutoSDK over ManualSDK
    def PreferAutoSDK(self):
        return False

    # If true, then parallel installs will overwrite existing files
    # <Returns> True if SDK is destructive (AKA parallel installs overwriting existing files)
    def IsAutoSDKDestructive(self):
        return False

    # Prints information about the SDK
    def Print(self):
        pass
