#pragma once
#include "Containers/Map.h"
#include "Containers/Array.h"
#include "Containers/String.h"
#include "Etc/ConfigSection.h"

// Represents a file in Config
class ConfigFile
{
    public:

        void Serialize(String FileContents)
        {
            String Name;
            String Section;


            int Index = 0;

            // For every character in file
            while(Index < FileContents.Length())
            {
                Name = "";
                Section = "";
                // For each line
                    // If we encountered a comment, instantly return to new line
                    if(FileContents[Index] == ';')
                    {
                        while(Index < FileContents.Length() && FileContents[Index] != '\n')
                        {
                            Index++;
                        }
                        continue;
                    }

                    // If character starts with [, then start getting the name of the section
                    if(FileContents[Index] == '[')
                    {
                        Index++;

                        // Get the name
                        while(Index < FileContents.Length() && FileContents[Index] != ']')
                        {
                            Name.Append(FileContents[Index]);
                            Index++;
                        }
                        Index++; // Skip ']'

                        while(Index < FileContents.Length() && FileContents[Index] != '[')
                        {
                            if(FileContents[Index] == ';')
                            {
                                while(Index < FileContents.Length() && FileContents[Index] != '\n')
                                {
                                    Index++;
                                }
                                continue;
                            }
                            Section.Append(FileContents[Index]);
                            Index++;
                        }

                        ConfigSection SectionClass;
                        SectionClass.Serialize(Section);
                        Sections.SetAdd(Name, SectionClass);

                        continue;
                    }
            Index++;

            }
        }

        bool Get(String SectionName, ConfigSection& Output)
        {
            int I = Sections.Find(SectionName);
            if(I == -1)
            {
                LOG(LogCore, LogType::Warning, "Config Section '" + SectionName + "' is missing");
                return false;
            }
            else
            {
                Output = Sections.Second(I);
                return true;
            }
        }

    private:

        // Section Name | Config Section Data
        Map<String, ConfigSection> Sections;
};
