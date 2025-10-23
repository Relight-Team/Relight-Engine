#pragma once

#include "Containers/Array.h"
#include "Etc/CharUtil.h"

// String system

// Handles Relight's strings

class String
{
    public:

    String(UTF16* InChars)
    {
        UTF16* PntTxt = InChars // The start of the chars
        while(PntTxt != '\0') // \0 means that we hit the end
        {
            CharArr.Add(PntTxt);
            ++PntTxt;
        }
    }

    private:

    Array<UTF16> CharArr;
};
