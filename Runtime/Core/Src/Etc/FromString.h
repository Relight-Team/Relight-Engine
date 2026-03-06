#pragma once
#include "Containers/String.h"
#include "PlatformCore.h"

// Convert String contents to values

struct FromString
{
    static int32 Int(String& Input)
    {
        int32 IntRet = 0;
        int32 StartingIndex = 0;

        int32 Times = 1;

        // If negative number, skip the negative symbol
        if(Input[0] == '-')
        {
            StartingIndex = 1;
            Times = -1;
        }

        for(int32 I = StartingIndex; I < Input.Length(); I++)
        {
            int32 Digit = GetActualNumber(Input[I]);
            IntRet = IntRet * 10 + Digit;
        }

        return IntRet * Times;
    }

    static double Double(String& Input)
    {
        double DoubleRet = 0;
        int32 StartingIndex = 0;

        int32 Times = 1;

        // If negative number, skip the negative symbol

        if(Input[0] == '-')
        {
            StartingIndex = 1;
            Times = -1;
        }

        bool IsDecimal = false;
        double DecimalPlace = 0.1;

        for(int32 I = StartingIndex; I < Input.Length(); I++)
        {
            if(Input[I] == '.')
            {
                IsDecimal = true;
                continue;
            }
            int32 Digit = GetActualNumber(Input[I]);

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
        int32 StartingIndex = 0;

        int32 Times = 1;

        // If negative number, skip the negative symbol

        if(Input[0] == '-')
        {
            StartingIndex = 1;
            Times = -1;
        }

        bool IsDecimal = false;
        float DecimalPlace = 0.1f;

        for(int32 I = StartingIndex; I < Input.Length(); I++)
        {
            if(Input[I] == '.')
            {
                IsDecimal = true;
                continue;
            }
            int32 Digit = GetActualNumber(Input[I]);

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

        static int32 GetActualNumber(UTF16 Str)
        {
            return Str - u'0';
        }
};
