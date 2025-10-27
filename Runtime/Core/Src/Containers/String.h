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

    String operator+(const String& Other) const
    {
        String Ret;
        Ret.CharArr = CharArr;
        for(int I = 0; I <= Other.Length(); I++)
        {
            Ret.CharArr.Add(Other.CharArr[I]);
        }

        return Ret;
    }

    bool Compare(String B, bool CaseSensitive = true);

    // Converts a UTF16 character into a ASCII character in string. Mostly used for displaying characters in terminal
    char ToChar(int I)
    {
        return CharUtil::IntToChar(CharArr[I]);
    }

    // Length of array starting at 0
    int Length() const
    {
        return CharArr.Length();
    }

    // Get's the size of array starting at 1
    int Size() const
    {
        return CharArr.Length();
    }

    String ToUpper();

    String ToLower();

    void Append(const String& B);

    void Append(const UTF16* B);

    void Append(const char* B);

    bool StartsWith(const String& B, bool CaseSensitive = true);

    private:

    String() {}

    Array<UTF16> CharArr;

    bool WithInternal(const UTF16 B, int Index, bool Case = true);
    bool WithInternal(const char B, int Index, bool Case = true);
};

inline String operator+(String& A, const char* B)
{
    return A + String(B);
}

inline String operator+(const char* A, String& B)
{
    return String(A) + B;
}

inline String operator+(String& A, const UTF16* B)
{
    return A + String(B);
}

inline String operator+(const UTF16* A, String& B)
{
    return String(A) + B;
}
