// Log

// Handles Relight's Log System

#pragma once

#include "LogCategory.h"
#include "LogWarning.h"

#include <iostream>

using namespace std;

void LOG(CORE_API::LogCategory Category, ENGINE_INTERNAL::LogWarning LogWarning, string Text)
{
    string White = "\e[0m";
    cout << LogWarning.ConvertColor(LogWarning.GetColor());
    cout << Category.GetName() << ": ";
    LogWarning.Print();
    cout << ": " << Text << endl;
    cout << White;
}



