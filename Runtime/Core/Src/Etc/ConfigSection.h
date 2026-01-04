#pragma once
#include "Containers/Map.h"
#include "Containers/Array.h"
#include "Containers/String.h"

// Represents a section in Config

struct ConfigLine
{
    String Key;
    String Value;
};

class ConfigSection
{
    public:

        void Serialize(String SectionContents)
        {

            Array<String> Ret = Parse(SectionContents);

            for(int I = 0; I < Ret.Length(); I++)
            {
                String Temp = Ret[I];

                String Key;
                String Var;

                Temp.Split("=", Key, Var);

                ConfigLine Line;

                Line.Key = Key;
                Line.Value = Var;
                Vars.Add(Line);
            }
        }

        bool Get(String Value, ConfigLine& Output)
        {
            int I = -1;
            for(int J = 0; J < Vars.Length(); J++)
            {
                if(Vars[J].Key == Value)
                {
                    I = J;
                }
            }

            if(I == -1)
            {
                LOG(LogCore, LogType::Warning, "Config Value '" + Value + "' is missing");
                return false;
            }
            else
            {
                Output = Vars[I];
                return true;
            }
        }

        void GetIndex(int I, ConfigLine& Output)
        {
            Output = Vars[I];
        }

        void ReturnArray(Array<ConfigLine>& Output)
        {
            Output = Vars;
        }


    private:

        // Returns an array of each line in contents, trimmed
        Array<String> Parse(String SectionContents)
        {
            int Index = 0;

            Array<String> Ret;

            // For the entire section
            while(Index < SectionContents.Length())
            {
                String Str = "";
                // For each line
                while(SectionContents[Index] != '\n')
                {
                    Str.Append(SectionContents[Index]);
                    Index++;
                }
                Str.Trim();

                // Do not append if the line is empty
                if(Str != "")
                {
                    Ret.Add(Str);
                }

                Index++;
            }

            return Ret;
        }


        // Value Name | All inputs
        Array<ConfigLine> Vars;
};
