#pragma once
#include "Containers/String.h"
#include "Platform.h"
#include "Serialization/FileReader.h"
#include "Containers/Array.h"
#include "Etc/CharUtil.h"

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

    static bool CreateFile(String File)
    {
        return PlatformFile::CreateFile(File);
    }

    static bool WriteFile(String File, Array<int> Contents)
    {
        return PlatformFile::WriteFile(File, Contents);
    }

    static bool WriteFile(String File, int* Contents)
    {
        Array<int> Ret = *Contents;
        return PlatformFile::WriteFile(File, Ret);
    }

    static bool WriteFile(String File, String Contents)
    {
        Array<char> RetA = Contents.ToArrayChar();
        Array<int> RetB;

        for(int I = 0; I < RetA.Length(); I++)
        {
            RetB.Add(CharUtil::CharToInt(RetA[I]));
        }

        return PlatformFile::WriteFile(File, RetB);
    }

    static bool CopyFile(String A, String B)
    {
        return PlatformFile::CopyFile(A, B);
    }

    static bool DeleteFile(String File)
    {
        return PlatformFile::DeleteFile(File);
    }

    static bool MoveFile(String File, String Directory)
    {
        return PlatformFile::MoveFile(File, Directory);
    }

    static bool DirectoryExists(String Directory)
    {
        return PlatformFile::DirectoryExists(Directory);
    }

    static bool CreateDirectory(String Directory)
    {
        return PlatformFile::CreateDirectory(Directory);
    }

    private:

       // static String Filename;

};
