#include "Containers/String.h"
#include <iostream>

String::String(const UTF16* InChars)
    {
        const UTF16* PntTxt = InChars; // The start of the chars
        while(*PntTxt != '\0') // \0 means that we hit the end
        {
            CharArr.Add(*PntTxt);
            ++PntTxt;
        }
    }

String::String(const UTF16& InChars)
    {
        CharArr.Add(InChars);
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

String String::ToLower()
{
    Array<UTF16> Temp;
    for(int I = 0; I <= Length(); I++)
    {
        Temp.Add(CharUtil::ToLower(CharArr[I]));
    }
    String Ret = Temp;
    return Ret;
}

void String::Append(const UTF16& B)
{
    String StrB = B;
    CharArr.Append(StrB.CharArr, StrB.CharArr.Count());
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
                if((ArrIndex + CheckIndex > CharArr.Length()) || (CharArr[ArrIndex + CheckIndex] != StrCheck[CheckIndex]))
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

int String::Find(const String& StrCheck, bool CaseSensitive)
{
    for(int Index = 0; Index < CharArr.Length(); Index++)
    {

        bool IsCharMatch = false;

        // Check if first chars matches
        if(CaseSensitive == false)
        {
            IsCharMatch = ((CharUtil::ToLower(StrCheck[0]) == CharArr[Index]) || (CharUtil::ToUpper(StrCheck[0] == CharArr[Index])));
        }
        else
        {
            IsCharMatch = (StrCheck[0] == CharArr[Index]);
        }

        // If it does not match, continue to next index
        if(IsCharMatch == false)
        {
            continue;
        }

        // If the index for the word we found in the StrCheck cannot fit into Stirng, then return -1
        if(Index + StrCheck.Length() > CharArr.Length())
        {
            return -1;
        }

        // check if word exist on current index
        int StrCheckIndex = 0;
        for(int Ind2 = Index + 1; Ind2 < StrCheck.Length(); Ind2++)
        {
            if(CaseSensitive == false)
            {
                IsCharMatch = ((CharUtil::ToLower(StrCheck[StrCheckIndex]) == CharArr[Ind2]) || (CharUtil::ToUpper(StrCheck[StrCheckIndex]) == CharArr[Ind2]));
            }
            else
            {
                IsCharMatch = (StrCheck[StrCheckIndex] == CharArr[Ind2]);
            }

            if(IsCharMatch == false)
            {
                break;
            }

            StrCheckIndex++;
        }

        if(IsCharMatch == true)
        {
            return Index;
        }
    }

    return -1;
}

bool String::Split(String& Str, String& Left, String& Right, bool CaseSensitive)
{
   if(Contains(Str) == false)
   {
        return false;
   }

   int Index = Find(Str);

   Array<UTF16> RetLeft;
   Array<UTF16> RightTemp;

   bool FailCheck = CharArr.SplitIndex(Index, RetLeft, RightTemp);

   if(FailCheck == false)
   {
        return false;
   }

   Array<UTF16> TempLeft;
   Array<UTF16> RetRight;

   FailCheck = RightTemp.SplitIndex(Index + Str.Length(), TempLeft, RetRight);

   if(FailCheck == false)
   {
        return false;
   }

   String RetLeftStr(RetLeft);
   String RetRightStr(RetRight);

   Left = RetLeftStr;
   Right = RetRightStr;

   return true;
}
