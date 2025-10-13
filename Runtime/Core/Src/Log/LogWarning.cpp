#include "Log/LogWarning.h"
#include <iostream>

using namespace ENGINE_INTERNAL;
using namespace std;

LogWarning::LogWarning(string Name)
{
    Title = Name;
}

LogWarning::LogWarning(string Name, string Crayon)
{
    Title = Name;

    Color = Crayon;
}

string LogWarning::PrivConvertColor(string InColor)
{
    if(InColor == "White")
    {
        return "";
    }
    else if(InColor == "Yellow")
    {
        return "\e[93m";
    }
    else if(InColor == "Red")
    {
        return "\e[31m";
    }
    else if(InColor == "Dark Red")
    {
        return "\e[91m";
    }
    else
    {
        return "";
    }
}
