#pragma once
#include "BasePlatform/BasePlatformFile.h"
#include "Linux/LinuxIncludes.h"
#include "Containers/String.h"
#include "Containers/Array.h"

class LinuxPlatformFile : public BasePlatformFile
{
public:
     static bool FileExists(String File);

     static bool ReadFile(String File, String& Output);

    // Like ReadFile() but store each line in array
     static bool ReadFileLines(String File, Array<String>& Output);

     static bool CreateFile(String File);

     static bool WriteFile(String File, String Contents);

     static bool CopyFile(String FileA, String FileB);

     static bool DeleteFile(String File);

     static bool MoveFile(String File, String MoveDirectory);

     static bool DirectoryExist(String Directory);

     static bool CreateDirectory(String Directory);

     static const char* ToConstChar(String Input);
};
