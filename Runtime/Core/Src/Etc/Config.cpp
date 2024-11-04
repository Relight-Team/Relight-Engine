#include "Log.h"
#include "Config_Internal.cpp"
#include <iostream>


// Note, params for getting values in configs
// ------------------------------------------------
// PClass: the config class the value is stored in
// Value: the value name from the class to get
// Store: The value to store the config
// File: The file location that stores the configs

class Config
{

    public:

        // Get values

        static void GetString(std::string PClass, std::string Value, std::string& Store, std::string File)
        {
            // TODO: Test this code!

            SetText(File);

            std::string tmp = ReturnClassText(PClass);

            std::string Ret;

            Ret = GetVarAsString(Tmp, Value);

            // Already string, no need to convert it!

            Store = Ret;
        }


    private:

    std::string Text;

    void SetText(std::string ConfigFile)
    {
        Text = ReadInternal(ConfigFile);
    }


    // Shitty fucking hack coming up!!!

    // This should return all the text from a class via file

    // TODO: Any better optimized way?

    std::string ReturnClassText(std::string PClass)
    {

        std::string Ret;

        for(int i = 0; i < Text.size(); i++)
        {
            if(RemoveBrackets(Text[i]) == PClass)
            {
                i++;

                while(!(ContainsInternal(Text[i], "[")) && i < Text.size())
                {
                    Ret += Text[i];
                }
            }
        }

        return Ret;
    }

};
