#include "Containers/String.h"

String::String(const UTF16* InChars)
    {
        const UTF16* PntTxt = InChars; // The start of the chars
        while(*PntTxt != '\0') // \0 means that we hit the end
        {
            CharArr.Add(*PntTxt);
            ++PntTxt;
        }
    }

String::String(const char* InChars)
    {
        const char* PntTxt = InChars; // The start of the chars
        while(*PntTxt != '\0') // \0 means that we hit the end
        {
            UTF16 ToUtf = static_cast<UTF16>(*PntTxt);
            CharArr.Add(ToUtf);
            ++PntTxt;
        }
    }

String::String(const Array<UTF16> InChars)
    {
        CharArr = InChars;
    }

bool String::Compare(String B, bool CaseSensitive)
    {
        bool IsEqual = true;

        // If size of both strings do not match, the return false
        if(CharArr.Length() != B.Length())
        {
            return false;
        }

        for(int I = 0; I < B.Length(); I++)
        {
            if(CaseSensitive == false && CharUtil::IsASCII(CharArr[I]))
            {
                if((CharArr[I] != CharUtil::ToUpper(B[I])) and (CharArr[I] != CharUtil::ToLower(B[I])))
                {
                    IsEqual = false;
                }
            }
            else
            {
                IsEqual = CharArr[I] == B[I];
            }

            // if IsEqual is false, then we can return it without checking every other character
            if(IsEqual == false)
            {
                return false;
            }
        }

        return IsEqual;
    }

String String::ToUpper()
{
    Array<UTF16> Temp;
    for(int I = 0; I <= Length(); I++)
    {
        Temp.Add(CharUtil::ToUpper(CharArr[I]));
    }
    String Ret = Temp;
    return Ret;
}
