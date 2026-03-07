#pragma once
#include "BasePlatform/BasePlatformAtomics.h"
#include "PlatformCore.h"

class UnixPlatformAtomics
{
public:

    static inline void* InterlockedCompareExchangePtr(void*volatile* Destination, void* Exchange, void* Comparand)
    {
        __atomic_compare_exchange_n(Destination, &Comparand, Exchange, false, __ATOMIC_SEQ_CST, __ATOMIC_SEQ_CST);
        return Comparand;
    }
};
