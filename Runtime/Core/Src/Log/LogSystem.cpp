#include "Log/LogSystem.h"
#include "Platform.h"
#include "PlatformCore.h"
#include "Containers/String.h"
#include "Containers/Array.h"
#include "Log/LogCategory.h"
#include "PlatformCore.h"

void LogSystem::GetColorPOSIX(enum LogType Type, String& ColorOutput)
{
    switch(Type)
    {
        case (LogType::Warning):
            ColorOutput = "\e[93m";
            break;
        case (LogType::Error):
            ColorOutput = "\e[31m";
            break;
        case (LogType::Fatal):
            ColorOutput = "\e[91m";
            break;
        default:
            ColorOutput = "";
            break;
    }
}

void LogSystem::GetWhitePOSIX(String& ColorOutput)
{
    ColorOutput = "\e[0m";
}

void LogSystem::PrintLogToTerminal(CORE_API::LogCategory Cat, LogType Warn, String Msg)
{

    String Color;
    GetColorPOSIX(Warn, Color);

    String CategoryName = Cat.GetName();

    PlatformOutput::Print(Color);
    PlatformOutput::Print("[" + CategoryName + "] ");
    PlatformOutput::Print(GetLogTypeName(Warn) + ": ");
    PlatformOutput::Print(Msg);
    GetWhitePOSIX(Color);
    PlatformOutput::Println(Color);
}
