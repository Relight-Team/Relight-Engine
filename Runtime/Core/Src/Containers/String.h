#pragma once
#include "Containers/Array.h"
#include "Etc/CharUtil.h"
#include "Platform.h"

// String system

// Handles Relight's strings

class String
{
    public:

    String(const UTF16* InChars);

    String(const char* InChars);

    String(const Array<UTF16> InChars);

    UTF16 operator[](int I)
    {
        return CharArr[I];
    }

    bool operator==(String B)
    {
        return Compare(B, true);
    }

    bool Compare(String B, bool CaseSensitive = true);

    // Converts a UTF16 character into a ASCII character in string. Mostly used for displaying characters in terminal
    char ToChar(int I)
    {
        return CharUtil::IntToChar(CharArr[I]);
    }

    // Length of array starting at 0
    int Length()
    {
        return CharArr.Length();
    }

    // Get's the size of array starting at 1
    int Size()
    {
        return CharArr.Length();
    }

    String ToUpper();

    String ToLower();

    private:

    Array<UTF16> CharArr;
};
