#pragma once
#include "Containers/Array.h"
#include "Etc/CharUtil.h"
#include "PlatformCore.h"

// String system

// Handles Relight's strings

class String
{
    public:

    String() {}

    String(const UTF8* InChars);

    String(const UTF8& InChars);

    String(const char* InChars);

    String(const Array<UTF8> InChars);

    UTF8 operator[](const int32 I) const
    {
        return CharArr[I];
    }

    bool operator==(String B)
    {
        return Compare(B, true);
    }

    bool operator!=(String B)
    {
        return !Compare(B, true);
    }

    String operator+(const String& Other) const
    {
        String Ret = CharArr;

        // Remove \0
        Ret.CharArr.RemoveAt(CharArr.Indices());

        for(int32 I = 0; I <= Other.Indices(); I++)
        {
            Ret.Add(Other.CharArr[I]);
        }

        return Ret;
    }

    bool Compare(String B, bool CaseSensitive = true);

    // Converts a UTF8 character into a ASCII character in string. Mostly used for displaying characters in terminal
    char ToChar(int32 I)
    {
        return CharUtil::IntToChar(CharArr[I]);
    }

    // Length of array starting at 0
    // Example, "Hello" -> 4
    int32 Indices() const
    {
        return RealStringLength - 1;
    }

    // Get's the size of array starting at 1
    // Example, "Hello" -> 5
    int32 Length() const
    {
        return RealStringLength;
    }

    String ToUpper();

    String ToLower();

    void Append(const UTF8& B);

    void Append(const String& B);

    void Append(const UTF8* B);

    void Append(const char* B);

    void Add(const UTF8& B)
    {
        Append(B);
    }

    bool StartsWith(const String& B, bool CaseSensitive = true);

    bool EndsWith(const String& B, bool CaseSensitive = true);

    String Reverse();

    bool Contains(const UTF8& StrCheck);

    bool Contains(const String& StrCheck);

    int32 Find(const String& StrCheck, bool CaseSensitive = true);

    bool Split(String& Str, String& Left, String& Right, bool CaseSensitive = true);

    // TODO - Simple hack to fix issue with const, please merge this later
    bool Split(const String& Str, String& Left, String& Right, bool CaseSensitive = true)
    {
        return Split(const_cast<String&>(Str), Left, Right, CaseSensitive);
    }

    void Empty()
    {
        CharArr.Empty();
        RealStringLength = 0;
    }

    void TrimStart();

    void TrimEnd();

    void Trim()
    {
        TrimStart();
        TrimEnd();
    }

    void TrimStartChar(UTF8 Input)
    {
        if(CharArr[0] == Input)
        {
            CharArr.RemoveAt(0);
            RealStringLength--;
        }
    }

    void TrimEndChar(UTF8 Input)
    {
        if(CharArr[CharArr.Indices() - 1] == Input)
        {
            CharArr.RemoveAt(CharArr.Indices() - 1);
            RealStringLength--;
        }
    }

    void TrimChar(UTF8 Input)
    {
        TrimStartChar(Input);
        TrimEndChar(Input);
    }

    void TrimStartChar(String Input);

    void TrimEndChar(String Input);

    void TrimChar(String Input)
    {
        TrimStartChar(Input);
        TrimEndChar(Input);
    }

    void TrimQuotes()
    {
        TrimChar("\"");
    }

    Array<UTF8> ToArr()
    {
        Array<UTF8> Temp = CharArr;
        Temp.RemoveAt(CharArr.Indices());
        return Temp;
    }

    void Swap(int32 A, int32 B)
    {
        CharArr.Swap(A, B);
    }

    void Replace(UTF8 Input, int32 Index)
    {
        CharArr.Replace(Input, Index);
    }

    Array<char> ToArrayChar()
    {
        Array<char> Ret;
        for(int32 i = 0; i <= Indices(); i++)
        {
            Ret.Add(ToChar(i));
        }
        return Ret;
    }

    UTF8* ReturnPointer()
    {
        return CharArr.ReturnPointer();
    }

    uint32 TrueLength()
    {
        return CharArr.Length();
    }

    private:

    Array<UTF8> CharArr;

    uint32 RealStringLength = 0;

    bool WithInternal(const UTF8 B, int32 Index, bool Case = true);
    bool WithInternal(const char B, int32 Index, bool Case = true);

    void AddInternal(UTF8 Input)
    {
        // If the string is empty, then add both
        if(CharArr.Length() == 0)
        {
            CharArr.Add(Input);
            CharArr.Add('\0');
            RealStringLength++;

        }
        // Else, we will override old termination and add new one
        else
        {
            uint32 OldCount = CharArr.Indices();
            CharArr[OldCount] = Input;
            CharArr.Add('\0');
            RealStringLength++;
        }
    }

};

inline String operator+(String& A, const char* B)
{
    return A + String(B);
}

inline String operator+(const char* A, String& B)
{
    return String(A) + B;
}

inline String operator+(String& A, const UTF8* B)
{
    return A + String(B);
}

inline String operator+(const UTF8* A, String& B)
{
    return String(A) + B;
}

inline String operator+(const char* A, const String& B)
{
    return String(A) + B;
}
