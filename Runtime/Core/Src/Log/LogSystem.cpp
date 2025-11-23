#include "Log/LogSystem.h"
#include "Platform.h"
#include "PlatformCore.h"
#include "Containers/String.h"
#include "Containers/Array.h"
#include "Log/LogCategory.h"

void LogSystem::Add(CORE_API::LogCategory Cat, LogType Warn, String Msg)
{
    CategoryList.Add(Cat);
    WarningList.Add(Warn);
    MessageList.Add(Msg);

    PrintLatestToTerminal();

    // FIXME: Temp solution
    Assert(Warn == LogType::Fatal, "Engine encountered runtime error!", "");
}

void LogSystem::GetColorPOSIX(String& ColorOutput)
{
    switch(WarningList[WarningList.Length()])
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

void LogSystem::PrintLatestToTerminal()
{

    String Color;
    GetColorPOSIX(Color);
    CORE_API::LogCategory Category = CategoryList[CategoryList.Length()];
    String CategoryName = Category.GetName();

    Print(Color);
    Print("[" + CategoryName + "] ");
    Print(GetLogTypeName(WarningList[WarningList.Length()]) + ": ");
    Print(MessageList[MessageList.Length()]);
    GetWhitePOSIX(Color);
    Println(Color);
}
