#pragma once

#include "Core.h"
//#include "Serialization/Types.h"
#include "DOM/JsonClass.h"
#include "DOM/JsonVar.h"
#include "GlobalJson.h"
#include <cctype>  // For isdigit

#include <iostream>
#include <string>

namespace JSON_API
{

    // This should remove every whitespace, unless it's in a string, then keep whitespace
    std::string Json_Remove_Whitespace(std::string JsonString)
    {
        bool IsQuote = false;

        std::string Ret;

        for(char i : JsonString)
        {
            if(i == '"')
            {
                InvertBool(IsQuote);
            }

            if(IsQuote == true)
            {
                Ret += i;
            }

            if(IsQuote == false && i != ' ' && i != '\n' && i != '\t')
            {
                Ret += i;
            }
        }

        return Ret;
    }

  //  template <typename T>
    std::variant<int, std::string, double, bool> ConvertStringToVar(std::string Input, int Type)
    {
        if(Type == 0)
        {
            std::cout << "Returning String!" << std::endl;
            return Input;
        }
        if(Type == 1)
        {
            std::cout << "Returning Int!" << std::endl;
            return std::stoi(Input);
        }
        if(Type == 2)
        {
            std::cout << "Returning Double!" << std::endl;
            return std::stod(Input);
        }
        if(Type == 3)
        {
            std::cout << "Returning Bool!" << std::endl;
            if(Input[0] == 't')
            {
                return true;
            }
            else
            {
                return false;
            }
        }

        return -1;
    }



    bool Deserialize(std::string InputRaw, JSON_API::JsonObject& Output)
    {
        if(InputRaw == "")
        {
            JSON_INTERNAL::PrintJsonError(Error, "Error, json input doesn't have any data!");
            return false;
        }

        std::string Input = Json_Remove_Whitespace(InputRaw);

        std::string Name;
        std::string ValueStr;

        bool IsQuote = false; // This is so we can store the contents in the quote, while keeping name and value seperated
        bool IsValue = false; // If we are currently in a variable (both name and value)
        bool IsName = true; // If true, then the quotes will be stored in the name. If false, then the quotes wil be stored as the value
        bool IsArray = false; // true if it's an array, false otherwise

        int Type = 0; // 0 = string. 1 = int, 2 = double. 3 = bool. 4 = array. 5 = object

        for(int i = 1; i < Input.size() - 1; i++)
        {

            //if(IsQuote == true)
            //{
                if(IsName == true && Input[i] != '"' && Input[i] != ':')
                {
                    Name += Input[i];
                }
            //}

            // add ValueStr if isn't name.
            if(IsName == false && Input[i] != ',')
            {
                ValueStr += Input[i];
            }



            if(Input[i] == ',' && IsQuote == false)
            {
                std::variant<int, std::string, double, bool>  i = ConvertStringToVar(ValueStr, Type);

                auto tmp = JSON_API::JsonValue<std::variant<int, std::string, double, bool>>(i);

                Output.AddValue(Name, tmp);

                // DEBUG ONLY!!!

                std::cout << "Name: " << Name << std::endl;
                std::cout << "Value: " << ValueStr << std::endl;
                std::cout << std::endl;

                // Reset everything!

                Name = "";
                ValueStr = "";

                IsQuote = false;
                IsValue = false;
                IsName = true;
            }

            if(Input[i] == ':' && IsQuote == false)
            {
                InvertBool(IsName);
            }

            // shitty Value detector 2000, this shitty hack will detect the value and set it for us! Wowie, can't wait for me to write all this only to find out there's an easier fucking way to do it!

            if(Input[i] == ':' && Input[i + 1] == '"' && IsQuote == false)
            {
               Type = 0;
            }
            if(Input[i] == ':' && isdigit(Input[i + 1]) && IsQuote == false)
            {
                // Detects if it's an int or double
                for(int j = i; Input[j] != ','; j++)
                {
                    if(Input[j] == '.')
                    {
                        Type = 2;
                    }

                if(Type != 2)
                {
                    Type = 1;
                }
            }
            if(Input[i] == ':' && (Input[i + 1] == 't' || Input[i + 1] == 'f') && IsQuote == false)
            {
                Type = 3;
            }

            // == //

            if(Input[i] == '"')
            {
                InvertBool(IsQuote);
            }
        }
    }
    return true;
    }
}
