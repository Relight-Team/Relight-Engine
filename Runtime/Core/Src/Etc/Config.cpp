#include "Log/Log.h"

#include <iostream>
#include <string>
#include <algorithm>
#include <fstream>
#include <sstream>
#include <vector>

#include "Config.h"

static void Config::GetString(std::string PClass, std::string Value, std::string& Store, std::string File)
{

    std::vector<std::string> a = ReturnClassText(PClass, File);

    std::string b = ReturnValueText(a, Value);


    std::string c = ReturnVar(b);


    // Already String, no need to convert it!

    Store = c;
}

static void Config::GetInt(std::string PClass, std::string Value, int& Store, std::string File)
{

    std::vector<std::string> a = ReturnClassText(PClass, File);

    std::string b = ReturnValueText(a, Value);


    std::string c = ReturnVar(b);


    // Convert string to int

    int tmp = std::stoi(c);

    Store = tmp;

}

static void Config::GetDouble(std::string PClass, std::string Value, double& Store, std::string File)
{

    std::vector<std::string> a = ReturnClassText(PClass, File);

    std::string b = ReturnValueText(a, Value);


    std::string c = ReturnVar(b);


    // Convert string to double

    double tmp = std::stod(c);

    Store = tmp;

}


static void Config::GetBool(std::string PClass, std::string Value, bool& Store, std::string File)
{

    std::vector<std::string> a = ReturnClassText(PClass, File);

    std::string b = ReturnValueText(a, Value);


    std::string c = ReturnVar(b);


    // Convert string to boolean

    bool tmp = ENGINE_INTERNAL::StringToBool(c);

    Store = tmp;

}


 //== Internal Functions ==//

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

bool StringToBool(std::string Text)
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


// Shitty fucking hacks coming up!!!

// This should return all the text from a class via file

// TODO: Any better optimized way?

static std::vector<std::string> ReturnClassText(std::string PClass, const std::string File)
{

    std::vector<std::string> Tmp = ReadInternal(File);

    // Find index of PClass

    int i = FindTextIndex(File, AddBrackets(PClass));


    // Fix bug to not detect itself
    i += 1;

    std::vector<std::string> Ret;

    // Loop each vector and store it in Ret, until brackets are found

    while(i < Tmp.size() && !(ContainsInternal(Tmp[i], "[")))
    {
        Ret.push_back(Tmp[i]);
        i++;
    }


    return Ret;
}

static std::string ReturnValueText(std::vector<std::string> Vet, std::string Value)
{
    for(int i = 0; i < Vet.size(); i++)
    {
        if(ContainsInternal(Vet[i], Value))
        {
            return Vet[i];
        }
    }

    return "";
}


static std::string ReturnVar(std::string Value)
{
    int i = 0;

    // iterate until i is at '='

    while(Value[i] != '=')
    {
        i++;
    }

    // If nothing is after i, return nothing

    if(i == Value.size())
    {
        return "";
    }

    // store var and return it

    std::string Ret;

    for(int a = i + 1; a < Value.size(); a++)
    {
        Ret += Value[a];
    }

    return Ret;
}
