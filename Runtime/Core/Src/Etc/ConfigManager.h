#pragma once
#include "Containers/Map.h"
#include "Containers/Array.h"
#include "Containers/String.h"
#include "Etc/ConfigFile.h"

// Represents all config files we will use
class ConfigManager
{
    public:

    void Serialize(String FileName, String Contents)
    {
        ConfigFile CF;
        CF.Serialize(Contents);
        Files.SetAdd(FileName, CF);
    }

    void Remove(String FileName)
    {
        Files.Remove(FileName);
    }

    bool Get(String File, ConfigFile& Output)
        {
            int I = Files.Find(File);
            if(I == -1)
            {
                LOG(LogCore, LogType::Warning, "Config File '" + File + "' is missing");
                return false;
            }
            else
            {
                Output = Files.Second(I);
                return true;
            }
        }

    private:
        // File Name | File Data
        Map<String, ConfigFile> Files;
};
