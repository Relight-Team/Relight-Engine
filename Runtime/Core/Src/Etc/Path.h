#pragma once
#include "Containers/String.h"
#include "Platform.h"

class Path
{
public:

// Get Main exe dir (Game/)
    static bool ExeDir(String& Output)
    {
        return PlatformMisc::ExeDir(Output);
    }

    // Get config dir (Game/Config)
    static bool ConfigDir(String& Output)
    {
        return PlatformMisc::ConfigDir(Output);
    }

    // Get Content dir (Game/Content)
    static bool ContentDir(String& Output)
    {
        return PlatformMisc::ContentDir(Output);
    }

    // Get Shader dir (Game/Shader)
    static bool ShaderDir(String& Output)
    {
        return PlatformMisc::ShaderDir(Output);
    }

    // Get Saved dir (Game/Saved)
    static bool SavedDir(String& Output)
    {
        return PlatformMisc::SavedDir(Output);
    }

    // Get Saved Config dir (Game/Saved/Config)
    static bool SavedConfigDir(String& Output)
    {
        return PlatformMisc::SavedConfigDir(Output);
    }

    // Get Engine dir (Game/Engine)
    static bool EngineDir(String& Output)
    {
        return PlatformMisc::EngineDir(Output);
    }
};
