#pragma once
#include "Containers/String.h"
#include "Platform.h"
#include "Serialization/FileReader.h"
//#include "Serialization/FileWriter.h"

class FileManager
{
public:

    static bool FileExists(String File)
    {
        return PlatformFile::FileExists(File);
    }

    static bool ReadFile(String File, FileReader& Output)
    {

        //Filename = File;

        // Get platform's read data

        char* OutChar;

        size_t OutTemp;

        bool Success = PlatformFile::ReadFile(File, &OutChar, &OutTemp);

        if(!Success)
        {
            return false;
        }

        Output.Serialize(OutChar, static_cast<int>(OutTemp));

        return true;
    }

    private:

       // static String Filename;

};
