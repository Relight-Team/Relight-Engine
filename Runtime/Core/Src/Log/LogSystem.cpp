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

void LogSystem::GetColor(enum LogType Type, String& ColorOutput)
{
    GetColorPOSIX(Type, ColorOutput);
}

void LogSystem::GetWhite(String& ColorOutput)
{
    GetWhitePOSIX(ColorOutput);
}


void LogSystem::PrintLogToTerminal(CORE_API::LogCategory Cat, LogType Warn, String Msg)
{

    StartLogInfo(Cat, Warn);

    PlatformOutput::Print(Msg);

    EndLogInfo();
}

void LogSystem::StartLogInfo(CORE_API::LogCategory Cat, LogType Warn)
{
    String Color;
    GetColor(Warn, Color);

    String CategoryName = Cat.GetName();

    PlatformOutput::Print(Color);
    PlatformOutput::Print("[" + CategoryName + "] ");
    PlatformOutput::Print(GetLogTypeName(Warn) + ": ");
}

void LogSystem::EndLogInfo()
{
    String Color;
    GetWhite(Color);
    PlatformOutput::Println(Color);
}
