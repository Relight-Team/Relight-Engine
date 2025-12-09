#include "Linux/LinuxFile.h"
#include "Linux/LinuxPlatform.h"
#include "Linux/LinuxIncludes.h"
#include "Containers/String.h"
#include "Containers/Array.h"


bool FileExists(String File)
{
    Array<char> Temp1 = File.ToArrayChar();
    const char* Temp2 = Temp1.ReturnPointer();
    return (access(Temp2, F_OK) == 0);
}
