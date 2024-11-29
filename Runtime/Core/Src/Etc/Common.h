// Common Misc functions

#pragma once
#include <iostream>
#include <variant>
#include <stdexcept>

// Invert's a bool (if bool is true, change it to false, and vice-versa)
void InvertBool(bool& Input)
{
    if(Input == true)
    {
        Input = false;
    }
    else if(Input == false)
    {
        Input = true;
    }
}


// Varient Converters

// template used so any varient
template <typename P>
bool VarientToInt(P Varient, int& Output)
{
    try
    {
        Output = std::get<int>(Varient);
        return true;
    }
    catch(const std::bad_variant_access& e)
    {
        return false;
    }
}
