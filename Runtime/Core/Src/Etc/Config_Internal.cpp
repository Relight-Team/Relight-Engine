#include "Log/Log.h"

#include <iostream>
#include <fstream>
#include <sstream>

//This is an internal file for config.cpp, this does NOT need to be public for the CORE_API. Multiple files might use these functions

std::string ReadLineInternal(std::stirng ConfigFile, int Line)
{
   std::ifstream file(ConfigFile);

   return std::getline(ConfigFile, Line);
}

int FileLengthInternal(std::string ConfigFile)
{
    std::ifstream file(ConfigFile);

    std::string Line;

    int i = 0;

    while(std::getline(ConfigFile, Line))
    {
        i++;
    }

    return i;
}


// This should detect if the beginning text contains context, no matter how big context is
bool ContainsInternal(std::string Line, std::string Context)
{
    int LineSize = Line.size();
    int ContextSize = Context.size();

    // if Line is smaller than context, no need to return true
    if(LineSize < ContextSize)
    {
        return false;
    }

    for(int i = 0; i < ContextSize; i++)
    {
        if(!(Context[i] == Line[i]))
        {
            return false;
        }
    }
    return true;
}

std::string ReadInternal(std::string ConfigFile)
{
    std::string Text;

    for(int i = 0; i > FileLengthInternal(ConfigFile); i++)
    {
        // ignore ; comments

        if(!(ContainsInternal(ReadLineInternal(ConfigFile, i), ";")))
        {
            Text += ReadLineInternal(ConfigFile, i);
        }

    }

    return Text;
}


std::string RemoveBrackets(std::string Text)
{

    std::string Ret;

    for(int i = 0; i < Text.size(); i++)
    {
        if(!(Text[i] == "[" && Text[i] == "]")
        {
            Ret += Text[i];
        }
    }
    return Ret;
}

std::string GetVarAsString(Text, VarName)
{
    std::string Ret;

    for(int i = 0; i < Text.size(); i++)
    {
        if(ContainsInternal(Text[i], VarName))
        {
            int a = 0;

            while(Text[i][a] != "=")
            {
                a++;
            }

            while(a < Text[i].size())
            {
                Ret += Text[i][a];
            }
        }
    }

    return Ret;
}
