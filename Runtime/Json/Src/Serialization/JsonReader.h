#pragma once

#include "Core.h"
//#include "Serialization/Types.h"
#include "DOM/JsonClass.h"
#include "DOM/JsonVar.h"
#include "GlobalJson.h"

#include <iostream>

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





    bool Deserialize(std::string Input, JSON_API::JsonObject& Output)
    {
        if(Input == "")
        {
            return false;
        }

        std::string Name;
        std::string ValueStr;

        bool IsQuote = false; // This is so we can store the contents in the quote, while keeping name and value seperated
        bool IsValue = false; // If we are currently in a variable (both name and value)
        bool IsName = true; // If true, then the quotes will be stored in the name. If false, then the quotes wil be stored as the value

        for(int i = 1; i < Input.size() - 1; i++)
        {

            if(IsQuote == true)
            {
                if(IsName == true)
                {
                    Name += Input[i];
                }
                else
                {
                    ValueStr += Input[i];
                }
            }

            if(Input[i] == ',' && IsQuote == false)
            {

                auto tmp = JSON_API::JsonValue<std::string>(StringToVar<std::string>(ValueStr));

                Output.AddValue(Name, tmp);

                // Reset everything!

                Name == "";
                ValueStr == "";

                IsQuote = false;
                IsValue = false;
                IsName = false;
            }

            if(Input[i] == ':' && IsQuote == false)
            {
                InvertBool(IsName);
            }

            if(Input[i] == '"')
            {
                InvertBool(IsQuote);
            }
        }

        return true;

    }
}
