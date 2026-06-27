#pragma once
#include "BasePlatform/BasePlatformAtomics.h"
#include "PlatformCore.h"

class UnixPlatformAtomics
{
public:

    static inline int32 InterlockedCompareExchange(volatile int32* Destination, int32 Exchange, int32 Comparand)
    {
        __atomic_compare_exchange_n(Destination, &Comparand, Exchange, false, __ATOMIC_SEQ_CST, __ATOMIC_SEQ_CST);
        return Comparand;
    }

    static inline void* InterlockedCompareExchangePtr(void*volatile* Destination, void* Exchange, void* Comparand)
    {
        __atomic_compare_exchange_n(Destination, &Comparand, Exchange, false, __ATOMIC_SEQ_CST, __ATOMIC_SEQ_CST);
        return Comparand;
    }

    static inline int32 InterlockedOr(volatile int8* ValueA, const int8 ValueB)
    {
        return __atomic_fetch_or(ValueA, ValueB, __ATOMIC_SEQ_CST);
    }

    static inline int32 AtomicReadRelaxed(volatile const int32* Value)
	{
		return __atomic_load_n(Value, __ATOMIC_RELAXED);
	}
};
