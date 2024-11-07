#include "Log/Log.h"
#include "Config_Internal.cpp"
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

        static void GetString(std::string PClass, std::string Value, std::string& Store, std::string File)
        {

             std::vector<std::string> a = ReturnClassText(PClass, File);

             std::string b = ReturnValueText(a, Value);


             std::string c = ReturnVar(b);


             // Already String, no need to convert it!

             Store = c;

        }



        static void GetInt(std::string PClass, std::string Value, int& Store, std::string File)
        {

             std::vector<std::string> a = ReturnClassText(PClass, File);

             std::string b = ReturnValueText(a, Value);


             std::string c = ReturnVar(b);


             // Convert string to int

             int tmp = std::stoi(c);

             Store = tmp;

        }


    private:

        // Shitty fucking hacks coming up!!!

        // This should return all the text from a class via file

        // TODO: Any better optimized way?

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
