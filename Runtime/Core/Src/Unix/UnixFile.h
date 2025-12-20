#pragma once
#include "BasePlatform/BasePlatformFile.h"
#include "Unix/UnixIncludes.h"
#include "Containers/String.h"
#include "Containers/Array.h"

class UnixPlatformFile : public BasePlatformFile
{
public:
     static bool FileExists(String File);

     static bool ReadFile(String File, char** Output, size_t* OutputSize);

     static bool CreateFile(String File);

     static bool WriteFile(String File, Array<int> Contents);

     static bool CopyFile(String FileA, String FileB);

     static bool DeleteFile(String File);

     static bool MoveFile(String File, String MoveDirectory);

     static bool DirectoryExists(String Directory);

     static bool CreateDirectory(String Directory);

     static bool ListFiles(String Directory, Array<String>& Output, Array<String>& Directories, String Ext = "NULL");
};
