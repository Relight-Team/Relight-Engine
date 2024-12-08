// Log

// Handles Relight's Log System

#pragma once

#include "LogCategory.h"
#include "LogWarning.h"

#include <iostream>

using namespace std;

void LOG(CORE_API::LogCategory Category, ENGINE_INTERNAL::LogWarning Warning, string Text)
{
    string White = "\e[0m";
    cout << Warning.ConvertColor(Warning.GetColor());
    cout << Category.GetName() << ": ";
    Warning.Print();
    cout << ": " << Text << endl;
    cout << White;
}



