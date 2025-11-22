// Error handling for LOW-LEVEL SYSTEMS (I.E Arrays)

// for fatal errors that cannot use LOG() for one reason or another
#pragma once
#include "Linux/LinuxIncludes.h"
#include <iostream>

template <typename Input>
inline void AssertInternal(bool Condition, const char* Message, Input InputVar, const char* ConStr, const char* File, int Line)
{
    if(Condition == true)
    {
        std::cerr << "\n";
        std::cerr << "[LOW-LEVEL FATAL ERROR VIA ASSERTION!] " << Message << "\n";
        std::cerr << "[FAILED CONDITION]: " << ConStr << "\n";
        std::cerr << "[INPUT]: " << InputVar << "\n";
        std::cerr << "[FILE]: " << File << "\n";
        std::cerr << "[LINE]: " << Line << "\n";
        std::abort();
    }
}

#define Assert(Condition, Message, InputVar) \
do { \
    AssertInternal(Condition, Message, InputVar, #Condition, __FILE__, __LINE__); \
} while(0)
