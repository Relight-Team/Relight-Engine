// Relight Engine's IntroSort

// Default algorithm for general engine arrays

#pragma once
#include "Platform.h"
#include "Algorithm/HeapSort.h"
#include "Algorithm/InsertionSort.h"
#include "Algorithm/QuickSort.h"
#include <iostream>

template <typename ArrayType>
void IntroSort(ArrayType& Arr, int Min, int Max, int Depth)
{
    int Length = Max - Min + 1;

    // If the Length of array is 16 or less, then use insertionSort
    if(Length <= 16)
    {
        InsertionSort(Arr, Min, Max);
        return;
    }

    // If the Depth of array is 0, then use HeapSort
    if(Depth == 0)
    {
        HeapSort(Arr);
        return;
    }
    // If Length of array is more than 16 and the depth isn't 0, use Partition and rerun Introsort
    if(Min < Max)
    {
        int Part = Partition(Arr, Min, Max);
        IntroSort(Arr, Min, Part - 1, Depth - 1);
        IntroSort(Arr, Part + 1, Max, Depth - 1);
    }
}

template <typename ArrayType>
void IntroSort(ArrayType& Arr)
{
    int Max = Arr.Indices();

    int Depth = 2 * floor(log(Arr.Indices()));

    IntroSort(Arr, 0, Max, Depth);
}
