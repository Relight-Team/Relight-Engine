#pragma once
#include "Containers/String.h"

class BasePlatformMisc
{
    public:

        // Get Main exe dir (Game/)
        static bool ExeDir(String& Output);

        // Get config dir (Game/Config)
        static bool ConfigDir(String& Output);

        // Get Content dir (Game/Content)
        static bool ContentDir(String& Output);

        // Get Shader dir (Game/Shader)
        static bool ShaderDir(String& Output);

        // Get Saved dir (Game/Saved)
        static bool SavedDir(String& Output);

        // Get Saved Config dir (Game/Saved/Config)
        static bool SavedConfigDir(String& Output);

        // Get Engine dir (Game/Engine)
        static bool EngineDir(String& Output);
};
