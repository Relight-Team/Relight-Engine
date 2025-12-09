#pragma once
#include "BasePlatform/BasePlatformOutput.h"
#include "Containers/String.h"
#include "LinuxPlatform.h"
#include "Etc/CharUtil.h"
#include "Etc/ToString.h"
#include <iostream>

class LinuxPlatformOutput : public BasePlatformOutput
{
public:
    static inline void Print(const String& Input)
    {
        for(int I = 0; I <= Input.Length(); I++)
        {
            std::cout << CharUtil::IntToChar(Input[I]);
        }
    }

    static inline void Print(const Array<UTF16>& Input)
    {
        for(int I = 0; I <= Input.Length(); I++)
        {
            std::cout << CharUtil::IntToChar(Input[I]);
        }
    }

    static inline void Print(const UTF16& Input)
    {
        std::cout << CharUtil::IntToChar(Input);
    }

    static inline void Print(const char& Input)
    {
        std::cout << CharUtil::IntToChar(Input);
    }

    static inline void Print(const UTF16* Input)
    {
        String InputStr = Input;
        Print(InputStr);
    }

    static inline void Print(const char* Input)
    {
        String InputStr = Input;
        Print(InputStr);
    }

    template <typename NonStringType>
    static inline void Print(const NonStringType& Input)
    {
        String Temp = ToString(Input);

        Print(Temp);
    }

    template <typename StringType>
    static void Println(const StringType& Input)
    {
        String Temp = "\n";
        String TempInput = ToString(Input);
        Print(TempInput + Temp);
    }
};
