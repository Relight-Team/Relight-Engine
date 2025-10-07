#include <iostream>
#include <string>
#include <algorithm>
#include <fstream>
#include <sstream>
#include <vector>

#include "Etc/Config.h"

void Config::GetString(std::string PClass, std::string Value, std::string& Store, std::string File)
{

    std::vector<std::string> a = ReturnClassText(PClass, File);

    std::string b = ReturnValueText(a, Value);


    std::string c = ReturnVar(b);


    // Already String, no need to convert it!

    Store = c;
}

void Config::GetInt(std::string PClass, std::string Value, int& Store, std::string File)
{

    std::vector<std::string> a = ReturnClassText(PClass, File);

    std::string b = ReturnValueText(a, Value);


    std::string c = ReturnVar(b);


    // Convert string to int

    int tmp = std::stoi(c);

    Store = tmp;

}

void Config::GetDouble(std::string PClass, std::string Value, double& Store, std::string File)
{

    std::vector<std::string> a = ReturnClassText(PClass, File);

    std::string b = ReturnValueText(a, Value);


    std::string c = ReturnVar(b);


    // Convert string to double

    double tmp = std::stod(c);

    Store = tmp;

}


void Config::GetBool(std::string PClass, std::string Value, bool& Store, std::string File)
{

    std::vector<std::string> a = ReturnClassText(PClass, File);

    std::string b = ReturnValueText(a, Value);


    std::string c = ReturnVar(b);


    // Convert string to boolean

    bool tmp = StringToBool(c);

    Store = tmp;

}


 //== Internal Functions ==//

// This should detect if the beginning text contains context, no matter how big context is
bool Config::ContainsInternal(std::string Line, std::string Context)
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



std::vector<std::string> Config::ReadInternal(const std::string ConfigFile)
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



int Config::FindTextIndex(std::string ConfigFile, std::string Context)
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
std::string Config::AddBrackets(std::string Text)
{
    return "[" + Text + "]";
}

bool Config::StringToBool(std::string Text)
{
    std::string tmp = Text;

    std::transform(tmp.begin(), tmp.end(), tmp.begin(), ::tolower); // not case sensitive

    if(tmp == "true")
    {
        return true;
    }
    else if(tmp == "false")
    {
        return false;
    }
    else
    {
        // If it fails, just return false
        return false;
    }
}


