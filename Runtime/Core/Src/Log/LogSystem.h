// LogSystem holds all the logging details during the rutnime lifespan
#pragma once
#include "Platform.h"
#include "PlatformCore.h"
#include "Containers/String.h"
#include "Containers/Array.h"
#include "Log/LogCategory.h"
#include "PlatformCore.h"

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

        // Print the log entry to terminal
        void PrintLogToTerminal(CORE_API::LogCategory Cat, LogType Warn, String Msg);

        // Flush contents to .log file
        void Flush();

        bool CanPrintToFile()
        {
            return PrintToFile;
        }

        bool CanPrintToTerm()
        {
            return PrintToTerm;
        }

    private:

        // If we should print to log
        bool PrintToFile = false;

        // If we should print to OS terminal
        bool PrintToTerm = true;


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

        void GetColorPOSIX(enum LogType Type, String& ColorOutput);
        void GetWhitePOSIX(String& ColorOutput);
};

// The Engine Logger, used internally by engine, should be used for game runtime as well
inline LogSystem EngineLogger;
