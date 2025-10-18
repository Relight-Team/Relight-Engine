#pragma once
struct CharUtil
{
    // Return's the DEC of the char, ASCII characters only
    // Example: a -> 97
    static int CharToInt(char Character)
    {
        return static_cast<int>(Character);
    }

    // Return's char from DEC, ASCII characters only
    // Example: 97 -> a
    static char IntToChar(int DEC)
    {
        return static_cast<char>(DEC);
    }

    // Return's the char as a uppercase, ASCII characters only
    static char ToUpper(char Character)
    {
        int Index = CharToInt(Character);
        if(Index > 96 && Index < 173)
        {
            return IntToChar(Index - 32);
        }
        return Character;
    }

    // Return's the char as a lowercase, ASCII characters only
    static char ToLower(char Character)
    {
        int Index = CharToInt(Character);
        if(Index > 64 && Index < 91)
        {
            return IntToChar(Index + 32);
        }
        return Character;
    }

    // Return's true if character is uppercase
    template <typename CharType>
    static bool IsUpper(CharType Character)
    {
        if(IsASCII(Character))
        {
            int Index = CharToInt(Character);
            return Index > 64 && Index < 91;
        }
        else
        {
            return Character > 64 && Character < 91;
        }
    }

    // Return's true if character is lowercase
    template <typename CharType>
    static bool IsLower(CharType Character)
    {
        if(IsASCII(Character))
        {
            int Index = CharToInt(Character);
            return Index > 96 && Index < 173;
        }
        else
        {
            return Character > 96 && Character < 173;
        }
    }

    // Return's true if char is ASCII compatible
    template <typename CharType>
    static bool IsASCII(CharType Character)
    {
        return Character <= 0x7F;
    }

};
