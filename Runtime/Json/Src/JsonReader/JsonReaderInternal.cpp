#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <cctype>

#include "Log/Log.h"

//TODO: FINISH THIS FILE@

// this whole entire thing is just a shitty fucking hack

// (at this point, this whole engine is a shitty fucking hack)


CORE_API::LogCategory* JSON_PARSE_ERR = new CORE_API::LogCategory("JSON PARSING");

// Relight's own json parsing function //

// each value will be stored like this
// "ValueString=hi | ValueInt=5 | ValueDoubleFloat=1.1 | ValueBool=true | ValueArray=[1, 2, 3, 4]

// if it's a structure, it will look like this
// ParentStructure.ChildStructure.Value=3

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

// A shitty fucking hack where we split the string to 2
std::vector<std::string> ShittyHack(std::string Text)
{
    //TODO: FIX THIS FUCKING SHIT
}


std::vector<std::string> Parse(std::string JsonFile)
{

    // loads file and stores it

    std::ifstream MyReadFile(JsonFile);

    std::string Text;

    std::vector<std::string> Ret;

    // this value that handles the main structure before value name (Minor TODO: describe this value better? I don't think this comment clearly explain what ParentString does)

    std::string ParentString = "";


    while(std::getline(MyReadFile, Text))
    {

        if(ContainsAnywhereInternal(Text, "{"))
        {
            std::string EndDot = "";
            // if there's already a value in ParentString, add a '.'

            if(ParentString != "")
            {
                ParentString += '.';
                EndDot = ".";
            }

            // start from index 0 of line, loop, and store it until the current index is '{'

            std::string tmp;

            for(int i = 0; Text[i] != '{'; i++)
            {
                tmp += Text[i];
            }

            // remove whitespace TODO: Removes whitespace from actual value as well, avoid this somehow...
            //tmp.erase(std::remove_if(tmp.begin(), tmp.end(), ::isspace), tmp.end());
            // remove :
            tmp.erase(std::remove(tmp.begin(), tmp.end(), ':'), tmp.end());
            // remove "
            tmp.erase(std::remove(tmp.begin(), tmp.end(), '"'), tmp.end());

            // store it to ParentString
            ParentString += tmp + EndDot;
        }

        // if } detected, remove the section from ParentString

        if(ContainsAnywhereInternal(Text, "}") && ParentString != "")
        {
            RemoveLast(Text);
        }


        // Add to Vector that will be returned
        if(!(ContainsAnywhereInternal(Text, "}") || ContainsAnywhereInternal(Text, "{") || Text == ""))
        {
            Ret.push_back(ParentString + Text);
        }
    }

    return Ret;
}





