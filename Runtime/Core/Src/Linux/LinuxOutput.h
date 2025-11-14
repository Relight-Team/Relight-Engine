#pragma once
#include "Containers/String.h"
#include "LinuxPlatform.h"
#include "Etc/CharUtil.h"
#include <iostream>

void Print(const String& Input)
{
    for(int I = 0; I <= Input.Length(); I++)
    {
        std::cout << CharUtil::IntToChar(Input[I]);
    }
}

void Print(const Array<UTF16>& Input)
{
    for(int I = 0; I <= Input.Length(); I++)
    {
        std::cout << CharUtil::IntToChar(Input[I]);
    }
}

void Print(const UTF16& Input)
{
    std::cout << CharUtil::IntToChar(Input);
}

template <typename StringType>
void Println(const StringType& Input)
{
    String Temp = "\n";
    Print(Input + Temp);
}
