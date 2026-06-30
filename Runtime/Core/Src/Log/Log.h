// Log

// Handles Relight's Log System

#pragma once
#include "Log/LogSystem.h"
#include "Log/LogCategory.h"
#include "Containers/String.h"
#include "CoreLogType.h"

inline void LOG(CORE_API::LogCategory Category, LogType LogWarning, String Text)
{
    if(EngineLogger.CanPrintToTerm())
    {
        EngineLogger.PrintLogToTerminal(Category, LogWarning, Text);
    }

    // FIXME: Temp solution
    Assert(LogWarning == LogType::Fatal, "Engine encountered runtime error!", "");
}

inline void LOG(String Text)
{
    LOG(LogCore, LogType::Log, Text);
}

