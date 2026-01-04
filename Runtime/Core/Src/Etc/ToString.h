#pragma once
#include "Containers/String.h"
#include "Containers/Array.h"
#include "Platform.h"
inline String ToString(int Input)
{
    if(Input == 0)
    {
        return "0";
    }

    String Ret;
    int Value = abs(Input);

    while (Value > 0)
    {
        int Digit = Value % 10;
        Ret.Append(static_cast<char16_t>('0' + Digit));
        Value /= 10;
    }

    if (Input < 0)
    {
        Ret.Append('-');
    }

    return Ret.Reverse();
}

// FIXME: print's incorrectly with negative values, please find a fix and fix it!
inline String ToString(float Input)
{
    String Ret = "";
    int Whole = int((floor((Input))));
    float Dec = abs(Input - Whole);

    Ret.Append(ToString(Whole));

    if(Dec > 0)
    {
        Ret.Append(".");

        for(int I = 0; I < 5 && Dec != 0.0f; I++)
        {

            Dec *= 10;
            int Digit = int(Dec);
            UTF16 CharTemp = 48 + Digit;
            Ret.Append(CharTemp);
            Dec -= Digit;
        }
    }

    return Ret;
}

inline String ToString(double Input)
{
    return ToString(float(Input));
}

inline String ToString(bool Input)
{
    String Ret = "False";
    if(Input == true)
    {
        Ret = "True";
    }
    return Ret;
}

// Just here so String Arrays can be displayed
inline String ToString(String Input)
{
    return Input;
}

inline String ToString(const UTF16* Input)
{
    String Ret = Input;
    return Ret;
}

template <size_t N>
inline String ToString(const char (&Input)[N])
{
    return String(Input);
}

template <typename ArrayInput>
inline String ToString(Array<ArrayInput> Input)
{
    // Fallback if array is empty
    if(Input.Length() == 0)
    {
        return "[]";
    }

    String Ret = "[";
    for(int I = 0; I < Input.Indices(); I++)
    {
        Ret.Append(ToString(Input[I]));
        Ret.Append(", ");
    }
    Ret.Append(ToString(Input[Input.Indices()]));
    Ret.Append("]");

    return Ret;
}
