# ExamplePlatformFactory handles the universial functions for running the building and having an interface for RBT to interact with

# Examples include The main run function and the platform name function

from BaseSDK import PlatformFactory

class LinuxFactory(PlatformFactory.FactorySDK):

    # Return's the target platform for this factory
    # <Returns> The name of the platform
    def TargetPlatform(self):
        return "Example"

    # Register the Build Platform w/ Platform Class
    # Usually this will create SDK and Platform class and register them
    def RegBuildPlatform(self):
        pass
