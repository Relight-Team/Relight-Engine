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
