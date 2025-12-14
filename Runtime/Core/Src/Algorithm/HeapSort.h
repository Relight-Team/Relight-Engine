#pragma once
#include "Algorithm/Heapify.h"
// Sort's an array using heap


template <typename ArrayType>
void HeapSort(ArrayType& Arr)
{
    int Length = Arr.Indices();

    for(int I = Length / 2 - 1; I >= 0; I--)
    {
        Heapify(Arr, Length, I);
    }

    for(int I = Length; I > 0; I--)
    {
        Arr.Swap(0, I);
        Heapify(Arr, I, 0);
    }
}
