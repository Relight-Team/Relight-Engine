#pragma once
#include "Platform.h"

struct RMath : public PlatformMath
{
    template <typename T>

    // Return the greater of 2 values
    inline T Max(const T A, const T B)
    {
        if (A > B)
        {
            return A;
        }
        return B;
    }

};
