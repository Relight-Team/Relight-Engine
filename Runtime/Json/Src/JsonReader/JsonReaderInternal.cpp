#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <cctype>

#include "Log/Log.h"

//TODO: FINISH THIS FILE!

// this whole entire thing is just a shitty fucking hack

// (at this point, this whole engine is a shitty fucking hack)


CORE_API::LogCategory* JSON_PARSE_ERR = new CORE_API::LogCategory("JSON PARSING");

// Relight's own json parsing function //

// each value will be stored like this
// "ValueString=hi | ValueInt=5 | ValueDoubleFloat=1.1 | ValueBool=true | ValueArray=[1, 2, 3, 4]

// if it's a structure, it will look like this
// ParentStructure.ChildStructure.Value=3




// ---------- //


std::string RemoveSpaceOutOfQuote(std::string A)
{
    // How this works...
    // Let's say the value is
    //         "ParentVar": "Parent Value",
    //


    std::vector<std::string> Vect;

}



bool ContainsAnywhereInternal(std::string Line, std::string Context)
{
      return Line.find(Context) != std::string::npos;
}




std::string RemoveLast(std::string Text)
{
    int LastDot = 0;

    // for each character, find the last .

    for(int i = 0; i < Text.size(); i++)
    {
        if(Text[i] == '.' && i > LastDot && i != Text.size() - 1)
        {
            LastDot = i;
        }

        i++;
    }

    std::string Ret;

    // store all text behind the dot

    for(int i = 0; i < LastDot; i++)
    {
        Ret += Text[i];
    }

    return Ret;
}



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


std::vector<std::string> Parse(std::string JsonFile)
{

    // loads file and stores it

    std::ifstream MyReadFile(JsonFile);

    std::string Text;

    std::vector<std::string> Ret;

    std::string ParentString = "";

// For each line
    while(std::getline(MyReadFile, Text))
    {
        // if Text has a {, store everything before {
        if(ContainsInternal(Text, "{"))
        {
            std::string EndDot; // simply adds a . at the end

            //
            if(ParentString != "")
            {
                ParentString += '.'; // add . to the start, seperating the previous item for the current
            }
            EndDot = ".";
        }
    }
}
