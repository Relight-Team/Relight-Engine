// Log

// Handles Relight's Log System

#pragma once
#include "Log/LogSystem.h"
#include "Log/LogCategory.h"
#include "Containers/String.h"
#include "CoreLogType.h"

template <typename... InputTypes>
inline void LOG(CORE_API::LogCategory Category, LogType LogWarning, String Text, InputTypes... Input)
{
    if(EngineLogger.CanPrintToTerm())
    {
        EngineLogger.PrintLogToTerminal(Category, LogWarning, Text, Input...);
    }

    // FIXME: Temp solution
    Assert(LogWarning == LogType::Fatal, "Engine encountered runtime error!", "");
}

template <typename... InputTypes>
inline void LOG(String Text, InputTypes... Input)
{
    LOG(LogCore, LogType::Log, Text, Input...);
}
