#pragma once
#include "Containers/String.h"
#include "LinuxPlatform.h"
#include "Etc/CharUtil.h"
#include "Etc/ToString.h"
#include <iostream>

inline void Print(const String& Input)
{
    for(int I = 0; I <= Input.Length(); I++)
    {
        std::cout << CharUtil::IntToChar(Input[I]);
    }
}

inline void Print(const Array<UTF16>& Input)
{
    for(int I = 0; I <= Input.Length(); I++)
    {
        std::cout << CharUtil::IntToChar(Input[I]);
    }
}

inline void Print(const UTF16& Input)
{
    std::cout << CharUtil::IntToChar(Input);
}

inline void Print(const char& Input)
{
    std::cout << CharUtil::IntToChar(Input);
}

inline void Print(const UTF16* Input)
{
    String InputStr = Input;
    Print(InputStr);
}

inline void Print(const char* Input)
{
    String InputStr = Input;
    Print(InputStr);
}

template <typename NonStringType>
inline void Print(const NonStringType& Input)
{
    String Temp = ToString(Input);

    Print(Temp);
}

template <typename StringType>
void Println(const StringType& Input)
{
    String Temp = "\n";
    String TempInput = ToString(Input);
    Print(TempInput + Temp);
}
