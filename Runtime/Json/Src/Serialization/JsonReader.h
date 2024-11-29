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


    }
}
