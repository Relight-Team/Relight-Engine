// Common Misc functions

#pragma once
#include <iostream>
#include <variant>
#include <stdexcept>
#include <sstream>
#include <string>
#include "PlatformCore.h"

// Invert's a bool (if bool is true, change it to false, and vice-versa)
inline void InvertBool(bool& Input)
{
    if(Input == true)
    {
        Input = false;
    }
    else if(Input == false)
    {
        Input = true;
    }
}


// Varient Converters

// template used so any varient
template <typename P>
int32 VarientToInt(P Varient)
{
    return std::get<int>(Varient);
}


inline bool StringContainsChar(std::string Str, char Ch)
{
    for(int32 i = 0; i < Str.size(); i++)
    {
        if(Str[i] == Ch)
        {
            return true;
        }
    }
    return false;
}


// String to any value

template <typename T>

T StringToVar(std::string& Str)
{
    T Value;
    std::istringstream(Str) >> Value;
    return Value;
}
