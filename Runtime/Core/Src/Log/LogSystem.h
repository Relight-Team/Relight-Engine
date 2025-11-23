// LogSystem holds all the logging details during the rutnime lifespan
#pragma once
#include "Platform.h"
#include "PlatformCore.h"
#include "Containers/String.h"
#include "Containers/Array.h"
#include "Log/LogCategory.h"

enum LogType
{
    Log,
    Warning,
    Error,
    Fatal
};

class LogSystem
{
    public:

        void Add(CORE_API::LogCategory Cat, LogType Warn, String Msg);

        // Print the latest entry to terminal
        void PrintLatestToTerminal();

    private:
        Array<CORE_API::LogCategory> CategoryList;
        Array<LogType> WarningList;
        Array<String> MessageList;

        String GetLogTypeName(const LogType& Input)
        {
            switch (Input)
            {
                case (LogType::Log): return "Log";
                case (LogType::Warning): return "Warning";
                case (LogType::Error): return "Error";
                case (LogType::Fatal): return "Fatal";
            }

        }

        void GetColorPOSIX(String& ColorOutput);
        void GetWhitePOSIX(String& ColorOutput);
};

// The Engine Logger, used internally by engine, should be used for game runtime as well
inline LogSystem EngineLogger;
