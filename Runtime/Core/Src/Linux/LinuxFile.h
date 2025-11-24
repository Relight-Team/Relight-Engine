#pragma once
#include "Linux/LinuxIncludes.h"
#include "Containers/String.h"
#include "Containers/Array.h"

bool FileExists(String File);

bool ReadFile(String File, String& Output);

// Like ReadFile() but store each line in array
bool ReadFileLines(String File, Array<String>& Output);

bool CreateFile(String File);

bool WriteFile(String File, String Contents);

bool CopyFile(String FileA, String FileB);

bool DeleteFile(String File);

bool MoveFile(String File, String MoveDirectory);

bool DirectoryExist(String Directory);

bool CreateDirectory(String Directory);

const char* ToConstChar(String Input);
