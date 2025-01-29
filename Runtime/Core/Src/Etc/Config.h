#pragma once
#include <iostream>
#include <vector>


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

        static void GetString(std::string PClass, std::string Value, std::string& Store, std::string File);


        static void GetInt(std::string PClass, std::string Value, int& Store, std::string File);


        static void GetDouble(std::string PClass, std::string Value, double& Store, std::string File);


        static void GetBool(std::string PClass, std::string Value, bool& Store, std::string File);

    private:

        static bool ContainsInternal(std::string Line, std::string Context);

        static std::vector<std::string> ReadInternal(const std::string ConfigFile);

        static int FindTextIndex(std::string ConfigFile, std::string Context);

        static std::string AddBrackets(std::string Text);

        static bool StringToBool(std::string Text);

        static std::vector<std::string> ReturnClassText(std::string PClass, const std::string File)
        {

            std::vector<std::string> Tmp = ReadInternal(File);

            // Find index of PClass

            int i = FindTextIndex(File, AddBrackets(PClass));


            // Fix bug to not detect itself
            i += 1;

            std::vector<std::string> Ret;

            // Loop each vector and store it in Ret, until brackets are found

            while(i < Tmp.size() && !(ContainsInternal(Tmp[i], "[")))
            {
                Ret.push_back(Tmp[i]);
                i++;
            }


            return Ret;
        }

        static std::string ReturnValueText(std::vector<std::string> Vet, std::string Value)
        {
            for(int i = 0; i < Vet.size(); i++)
            {
                if(ContainsInternal(Vet[i], Value))
                {
                    return Vet[i];
                }
            }

            return "";
        }


        static std::string ReturnVar(std::string Value)
        {
        int i = 0;

        // iterate until i is at '='

        while(Value[i] != '=')
        {
            i++;
        }

        // If nothing is after i, return nothing

        if(i == Value.size())
        {
            return "";
        }

        // store var and return it

        std::string Ret;

        for(int a = i + 1; a < Value.size(); a++)
        {
            Ret += Value[a];
        }

        return Ret;
        }

};
