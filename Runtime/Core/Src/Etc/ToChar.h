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
