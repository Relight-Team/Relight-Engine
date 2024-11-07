#include "Log/Log.h"

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

//This is an internal file for config.cpp, this does NOT need to be public for the CORE_API. Multiple files might use these functions



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



std::vector<std::string> ReadInternal(const std::string ConfigFile)
{
    std::string Text;

    std::vector<std::string> Ret;

    std::ifstream MyReadFile(ConfigFile);

    while(std::getline(MyReadFile, Text))
    {
        if(!(ContainsInternal(Text, ";")))
        {
            Ret.push_back(Text);
        }
    }

    return Ret;
}



int FindTextIndex(std::string ConfigFile, std::string Context)
{

    std::vector<std::string> tmp = ReadInternal(ConfigFile);



    if(tmp.empty())
    {
        return -1;
    }

    for(int i = 0; i < tmp.size(); i++)
    {
        if(tmp[i].find(Context) != std::string::npos)
        {
            return i;
        }
    }
    return -1; // if -1, then it wasn't found
}





// This is a lazy way to clean up the code
std::string AddBrackets(std::string Text)
{
    return "[" + Text + "]";
}
