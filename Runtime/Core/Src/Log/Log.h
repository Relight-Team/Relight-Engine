// Log

// Handles Relight's Log System

#pragma once
#include "Log/LogSystem.h"
#include "Log/LogCategory.h"
#include "Containers/String.h"
#include "CoreLogType.h"

void LOG(CORE_API::LogCategory Category, LogType LogWarning, String Text)
{
    EngineLogger.Add(Category, LogWarning, Text);
}

void LOG(String Text)
{
    LOG(LogCore, LogType::Log, Text);
}

