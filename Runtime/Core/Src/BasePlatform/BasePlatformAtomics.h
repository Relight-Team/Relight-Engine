#pragma once
#include "PlatformCore.h"

class BasePlatformAtomics
{
public:

    static inline void* InterlockedCompareExchangePtr(void*volatile* Destination, void* Exchange, void* Comparand);
};
