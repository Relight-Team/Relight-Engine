// Log

// Handles Relight's Log System

#include "LogCategory.h"
#include "LogWarning.h"

#include <iostream>

using namespace std;

void LOG(CORE_API::LogCategory Category, CORE_INTERNAL::LogWarning Warning, string Text)
{
    cout << Warning.ConvertColor(Warning.GetColor());
    cout << Category.GetName() << ": ";
    Warning.Print();
    cout << ": " << Text << endl;
}



