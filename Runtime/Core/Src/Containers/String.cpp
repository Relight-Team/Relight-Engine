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

void String::Append(const String& B)
{
    CharArr.Append(B.CharArr, B.CharArr.Count());
}

void String::Append(const UTF16* B)
{
    String StrB = B;
    CharArr.Append(StrB.CharArr, StrB.CharArr.Count());
}

void String::Append(const char* B)
{
    String StrB = B;
    CharArr.Append(StrB.CharArr, StrB.CharArr.Count());
}

bool String::StartsWith(const String& B, bool CaseSensitive)
{
    bool DoesStart = false;

    // If B length is longer than String, then we know it's false
    if(B.CharArr.Length() > CharArr.Length())
    {
        return false;
    }

    for(int I = 0; I <= B.CharArr.Length(); I++)
    {
        DoesStart = WithInternal(B.CharArr[I], I, CaseSensitive);

        if(DoesStart == false)
        {
            return false;
        }
    }
    return DoesStart;
}

bool String::EndsWith(const String& B, bool CaseSensitive)
{
    bool DoesStart = false;

    // If B length is longer than String, then we know it's false
    if(B.CharArr.Length() > CharArr.Length())
    {
        return false;
    }

    int BaseI = CharArr.Length();

     for(int I = B.CharArr.Length(); I >= 0; I--)
    {
        DoesStart = WithInternal(B.CharArr[I], BaseI, CaseSensitive);

        if(DoesStart == false)
        {
            return false;
        }

        BaseI--;
    }
    return DoesStart;
}

bool String::WithInternal(const UTF16 B, int Index, bool Case)
{
    if(Case == true)
    {
        if(CharArr[Index] == B)
        {
            return true;
        }
        else
        {
            return false;
        }
    }
    else
    {
        if((CharUtil::ToUpper(CharArr[Index]) == B) or (CharUtil::ToLower(CharArr[Index]) == B))
        {
            return true;
        }
        else
        {
            return false;
        }
    }
}

bool String::WithInternal(const char B, int Index, bool Case)
{
    if(Case == true)
    {
        if(CharArr[Index] == B)
        {
            return true;
        }
        else
        {
            return false;
        }
    }
    else
    {
        if((CharUtil::ToUpper(CharArr[Index]) == B) or (CharUtil::ToLower(CharArr[Index]) == B))
        {
            return true;
        }
        else
        {
            return false;
        }
    }
}

String String::Reverse()
{
    String StrRet;

    StrRet.CharArr = CharArr.Reverse();

    return StrRet;
}

bool String::Contains(const UTF16& StrCheck)
{
    return CharArr.Contains(StrCheck);
}

bool String::Contains(const String& StrCheck)
{

    if(StrCheck.Length() > Length())
    {
        return false;
    }

    bool Ret = true;

    for(int ArrIndex = 0; ArrIndex < Length() ; ArrIndex++)
    {
        // if the first character is the same as the string we are checking, then check if it matches
        if(CharArr[ArrIndex] == StrCheck[0])
        {
            for(int CheckIndex = 0; CheckIndex <= StrCheck.Length(); CheckIndex++)
            {
                if(CharArr[ArrIndex + CheckIndex] != StrCheck[CheckIndex])
                {
                    Ret = false;
                    break;
                }
                else
                {
                    Ret = true;
                }
            }

            if(Ret == true)
            {
                return true;
            }
        }
    }

    return false;
}

//bool String::Split(const String& Str, String& Left, String& Right, CaseSensitive)
//{

//}
