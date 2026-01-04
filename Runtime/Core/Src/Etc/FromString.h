#pragma once
#include "Containers/String.h"

// Convert String contents to values

struct FromString
{
    static int Int(String& Input)
    {
        int IntRet = 0;
        int StartingIndex = 0;

        int Times = 1;

        // If negative number, skip the negative symbol
        if(Input[0] == '-')
        {
            StartingIndex = 1;
            Times = -1;
        }

        for(int I = StartingIndex; I < Input.Length(); I++)
        {
            int Digit = GetActualNumber(Input[I]);
            IntRet = IntRet * 10 + Digit;
        }

        return IntRet * Times;
    }

    static double Double(String& Input)
    {
        double DoubleRet = 0;
        int StartingIndex = 0;

        int Times = 1;

        // If negative number, skip the negative symbol

        if(Input[0] == '-')
        {
            StartingIndex = 1;
            Times = -1;
        }

        bool IsDecimal = false;
        double DecimalPlace = 0.1;

        for(int I = StartingIndex; I < Input.Length(); I++)
        {
            if(Input[I] == '.')
            {
                IsDecimal = true;
                continue;
            }
            int Digit = GetActualNumber(Input[I]);

            if(!IsDecimal)
            {
                DoubleRet = DoubleRet * 10 + Digit;
            }
            else
            {
                DoubleRet += Digit * DecimalPlace;
                DecimalPlace *= 0.1;
            }
        }

        return DoubleRet * Times;
    }

    static float Float(String& Input)
    {
        float DoubleRet = 0;
        int StartingIndex = 0;

        int Times = 1;

        // If negative number, skip the negative symbol

        if(Input[0] == '-')
        {
            StartingIndex = 1;
            Times = -1;
        }

        bool IsDecimal = false;
        float DecimalPlace = 0.1f;

        for(int I = StartingIndex; I < Input.Length(); I++)
        {
            if(Input[I] == '.')
            {
                IsDecimal = true;
                continue;
            }
            int Digit = GetActualNumber(Input[I]);

            if(!IsDecimal)
            {
                DoubleRet = DoubleRet * 10 + Digit;
            }
            else
            {
                DoubleRet += Digit * DecimalPlace;
                DecimalPlace *= 0.1f;
            }
        }

        return DoubleRet * Times;
    }

    static bool Bool(String& Input)
    {
        if(Input.ToLower() == "true")
        {
            return true;
        }
        else
        {
            return false;
        }
    }

    private:

        static int GetActualNumber(UTF16 Str)
        {
            return Str - u'0';
        }
};
