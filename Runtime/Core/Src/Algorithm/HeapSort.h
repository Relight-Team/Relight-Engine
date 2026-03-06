#pragma once
#include "Algorithm/Heapify.h"
#include "PlatformCore.h"
// Sort's an array using heap


template <typename ArrayType>
void HeapSort(ArrayType& Arr)
{
    int32 Length = Arr.Indices();

    for(int32 I = Length / 2 - 1; I >= 0; I--)
    {
        Heapify(Arr, Length, I);
    }

    for(int32 I = Length; I > 0; I--)
    {
        Arr.Swap(0, I);
        Heapify(Arr, I, 0);
    }
}
