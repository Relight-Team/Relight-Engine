#include "Unix/UnixFile.h"
#include "Unix/UnixPlatform.h"
#include "Unix/UnixIncludes.h"
#include "Containers/String.h"
#include "Containers/Array.h"
#include "Hardware/RMemory.h"


bool UnixPlatformFile::FileExists(String File)
{
    Array<char> Temp1 = File.ToArrayChar();
    Temp1.Add('\0');
    const char* Temp2 = Temp1.ReturnPointer();
    return (access(Temp2, F_OK) == 0);
}

bool UnixPlatformFile::ReadFile(String File, char** Output, size_t* OutputSize)
{
    // Open binary file
    Array<char> Temp1 = File.ToArrayChar();
    Temp1.Add('\0');
    const char* Temp2 = Temp1.ReturnPointer();
    FILE* Fiptr = fopen(Temp2, "rb");

    if(!Fiptr)
    {
        return false;
    }

    // Get size
    fseek(Fiptr, 0, SEEK_END);
    long Size = ftell(Fiptr);
    rewind(Fiptr);

    if(Size <= 0)
    {
        fclose(Fiptr);
        return false;
    }

    // Load into buffer and read it
    unsigned char* Buffer = (unsigned char*) RMemory::Malloc(Size);
    size_t Read = fread(Buffer, 1, Size, Fiptr);

    if(Read != (size_t)Size)
    {
        RMemory::Free(Buffer);
        return false;
    }

    fclose(Fiptr);

    *OutputSize = (size_t)Size;
    *Output = reinterpret_cast<char*>(Buffer);
    return true;
}

bool UnixPlatformFile::CreateFile(String File)
{
    Array<char> Temp1 = File.ToArrayChar();
    Temp1.Add('\0');
    const char* Temp2 = Temp1.ReturnPointer();
    FILE* FilePointer = fopen(Temp2, "w");

    if(FilePointer == nullptr)
    {
        return false;
    }

    fclose(FilePointer);
    return true;
}

bool UnixPlatformFile::WriteFile(String File, Array<int> Contents)
{
    Array<char> Temp1 = File.ToArrayChar();
    Temp1.Add('\0');
    const char* Temp2 = Temp1.ReturnPointer();
    FILE* FilePointer = fopen(Temp2, "wb");

    if(FilePointer == nullptr)
    {
        return false;
    }

    size_t Size = Contents.Length();

    fwrite(Contents.ReturnPointer(), sizeof(int), Size, FilePointer);

    fclose(FilePointer);
    return true;

}

bool WriteFile(String File, char* Contents, size_t Size)
{
    Array<char> Temp1 = File.ToArrayChar();
    Temp1.Add('\0');
    const char* Temp2 = Temp1.ReturnPointer();
    FILE* FilePointer = fopen(Temp2, "wb");

    if(FilePointer == nullptr)
    {
        return false;
    }

    fwrite(Contents, 1, Size, FilePointer);

    fclose(FilePointer);
    return true;

}

bool UnixPlatformFile::CopyFile(String FileA, String FileB)
{
    char* FileAData;
    size_t FileASize;

    bool Check = UnixPlatformFile::ReadFile(FileA, &FileAData, &FileASize);

    if(Check == false)
    {
        return false;
    }

    Check = ::WriteFile(FileB, FileAData, FileASize);

    if(Check == false)
    {
        return false;
    }

    return true;
}

bool UnixPlatformFile::DeleteFile(String File)
{
    Array<char> Temp1 = File.ToArrayChar();
    Temp1.Add('\0');
    const char* Temp2 = Temp1.ReturnPointer();

    int Check = remove(Temp2);

    if(Check != 0)
    {
        return false;
    }
    return true;
}

bool UnixPlatformFile::MoveFile(String File, String MoveDirectory)
{
    Array<char> Temp = File.ToArrayChar();
    Array<char> FileNameArr;
    Array<char> Bad; // TODO: Fix this so it can take nullptr
    Temp.Split('/', Bad, FileNameArr, true);
    String FileName;

    for(int I = 0; I < FileNameArr.Length(); I++)
    {
        FileName.Append(FileNameArr[I]);
    }

    bool Check = UnixPlatformFile::CopyFile(File, MoveDirectory + FileName);

    if(Check == false)
    {
        return false;
    }

    Check = UnixPlatformFile::DeleteFile(File);

    if(Check == false)
    {
        return false;
    }

    return true;
}

bool UnixPlatformFile::DirectoryExists(String Directory)
{
    Array<char> Temp1 = Directory.ToArrayChar();
    Temp1.Add('\0');
    const char* Temp2 = Temp1.ReturnPointer();

    struct stat info;

    if(stat(Temp2, &info) != 0)
    {
        return false;
    }

    return (info.st_mode & S_IFDIR) != 0;
}

bool UnixPlatformFile::CreateDirectory(String Directory)
{
    Array<char> Temp1 = Directory.ToArrayChar();
    Temp1.Add('\0');
    const char* Temp2 = Temp1.ReturnPointer();


    if(mkdir(Temp2, 0755) == 0)
    {
        return true;
    }
    else if(errno == EEXIST)
    {
        return true;
    }
    else
    {
        return false;
    }
}

bool UnixPlatformFile::ListFiles(String Directory, Array<String>& Files, Array<String>& Directories, String Ext)
{
    Array<char> Temp1 = Directory.ToArrayChar();
    Temp1.Add('\0');
    const char* Temp2 = Temp1.ReturnPointer();

    DIR *Dir = opendir(Temp2);

    if(!Dir)
    {
        return false;
    }

    struct dirent *entry;
    while ((entry = readdir(Dir)) != NULL)
    {
        // Skip . and ..
        if (entry->d_name[0] == '.' && (entry->d_name[1] == '\0' || (entry->d_name[1] == '.' && entry->d_name[2] == '\0')))
        {
            continue;
        }

        // If Ext is defined, then skip files that doesn't have the extension
        if(Ext != "NULL")
        {
            String EndWithCheck = entry->d_name;
            if(!EndWithCheck.EndsWith("." + Ext) && !UnixPlatformFile::DirectoryExists(Directory + entry->d_name))
            {
                continue;
            }
        }

        if(UnixPlatformFile::DirectoryExists(Directory + entry->d_name))
        {
            Directories.Add(Directory + entry->d_name);
        }
        else
        {
            Files.Add(Directory + entry->d_name);
        }
    }

    closedir(Dir);
    return true;
}
