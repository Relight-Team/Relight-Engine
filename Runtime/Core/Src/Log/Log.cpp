#include "Log/Log.h"

#include "Log/LogCategory.h"
#include "Log/LogWarning.h"

#include <iostream>

void LOG(CORE_API::LogCategory Category, ENGINE_INTERNAL::LogWarning LogWarning, string Text)
{
    string White = "\e[0m";
    cout << LogWarning.ConvertColor(LogWarning.GetColor());
    cout << Category.GetName() << ": ";
    LogWarning.Print();
    cout << ": " << Text << endl;
    cout << White;
}
