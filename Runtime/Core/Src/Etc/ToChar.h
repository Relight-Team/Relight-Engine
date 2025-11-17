#include "Containers/String.h"
#include "Containers/Array.h"
#include "Platform.h"
#include <iostream>
String ToString(int Input)
{
    String Ret = "";

    int Progress = 0;

    int CheckLoop = -1;

    while(CheckLoop < abs(Input))
    {

        int PowValue;

        if(Progress == 0)
        {
            PowValue = 1;
        }
        else
        {
            PowValue = pow(10, Progress);
        }

        int Num = abs((Input / PowValue) % 10);

        UTF16 CharTemp = 48 + Num;

        Ret.Append(CharTemp);

        Progress++;

        CheckLoop = pow(10, Progress);
    }

    // Add negative
    if(Input < 0)
    {
        Ret.Append("-");
    }

    return Ret.Reverse();
}

String ToString(float Input)
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

String ToString(double Input)
{
    return ToString(float(Input));
}
