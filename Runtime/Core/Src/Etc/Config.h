#pragma once
#include "Etc/ConfigManager.h"
#include "Containers/String.h"
#include "Serialization/FileReader.h"
#include "Etc/FileManager.h"
#include "Etc/Path.h"
#include "Etc/CharUtil.h"
#include "Etc/FromString.h"

ConfigManager GlobalConfig;


// FIXME: Rewrite ConfigSection to make it in order
struct Config
{
    // Add file to Global Config
    static void AddFile(String LocalFilePath, String ForceFullPath = "")
    {
        String Directory;

        if(ForceFullPath != "")
        {
            Directory = ForceFullPath;
        }
        // Get Saved config, else get main config
        else
        {
            String SaveConfigDir;
            String ConfigDir;

            Path::SavedConfigDir(SaveConfigDir);
            Path::ConfigDir(ConfigDir);

            if(FileManager::FileExists(SaveConfigDir + "/" + LocalFilePath))
            {
                Directory = SaveConfigDir;
            }
            else
            {
                Directory = ConfigDir;
            }
        }


        FileReader Container;

        FileManager::ReadFile(Directory + "/" + LocalFilePath, Container);

        String Contents = Container.ToString();

        GlobalConfig.Serialize(LocalFilePath, Contents);
    }

    static bool GetString(String Section, String Variable, String& Output, String File)
    {
        ConfigLine Ret;
        bool Check = InternalGetValue(Section, Variable, Ret, File);
        if(Check == false)
        {
            return false;
        }

        Output = Ret.Value;
        return true;
    }

    static bool GetInt(String Section, String Variable, int& Output, String File)
    {
        ConfigLine Ret;
        bool Check = InternalGetValue(Section, Variable, Ret, File);
        if(Check == false)
        {
            return false;
        }
        String StrOutput = Ret.Value;

        Output = FromString::Int(StrOutput);
        return true;
    }

    static bool GetDouble(String Section, String Variable, double& Output, String File)
    {
        ConfigLine Ret;
        bool Check = InternalGetValue(Section, Variable, Ret, File);
        if(Check == false)
        {
            return false;
        }

        String StrOutput = Ret.Value;

        Output = FromString::Double(StrOutput);
        return true;
    }

    static bool GetFloat(String Section, String Variable, float& Output, String File)
    {
        ConfigLine Ret;
        bool Check = InternalGetValue(Section, Variable, Ret, File);
        if(Check == false)
        {
            return false;
        }

        String StrOutput = Ret.Value;

        Output = FromString::Float(StrOutput);
        return true;
    }

    static bool GetBool(String Section, String Variable, bool& Output, String File)
    {

        ConfigLine Ret;

        bool Check = InternalGetValue(Section, Variable, Ret, File);

        if(Check == false)
        {
            return false;
        }

        String StrOutput = Ret.Value;

        Output = FromString::Bool(StrOutput);

        return true;
    }

    static bool GetArray(String Section, String Variable, Array<String>& Output, String File)
    {
        ConfigFile CFile;
        ConfigSection CSection;

        bool Check = GlobalConfig.Get(File, CFile);

        if(Check == false)
        {
            return false;
        }

        Check = CFile.Get(Section, CSection);

        if(Check == false)
        {
            return false;
        }

        Array<ConfigLine> Configs;

        CSection.ReturnArray(Configs);

        int I = 0;

        while(I < Configs.Length())
        {
            ConfigLine CLine = Configs[I];

            if(CLine.Key == "+" + Variable)
            {
                Output.AddUnique(CLine.Value);
            }

            else if(CLine.Key == "-" + Variable)
            {
                Output.Remove(CLine.Value);
            }

            else if(CLine.Key == "!" + Variable)
            {
                Array<String> Ret;
                Output = Ret;
            }

            else if(CLine.Key == "." + Variable)
            {
                Output.Add(CLine.Value);
            }

            else if(CLine.Key == Variable)
            {
                Array<String> Ret;
                Ret.Add(CLine.Value);
                Output = Ret;
            }

            I++;
        }

        return true;
    }

private:

    static bool InternalGetValue(String Section, String Variable, ConfigLine& Output, String File)
    {
        ConfigFile CFile;
        ConfigSection CSection;

        bool Check = GlobalConfig.Get(File, CFile);

        if(Check == false)
        {
            return false;
        }

        Check = CFile.Get(Section, CSection);

        if(Check == false)
        {
            return false;
        }
        Check = CSection.Get(Variable, Output);

        if(Check == false)
        {
            return false;
        }
        return true;
    }

    static int GetActualNumber(UTF16 Str)
    {
        return Str - u'0';
    }

};
