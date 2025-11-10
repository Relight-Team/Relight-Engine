#pragma once

#include "Algorithm/IntroSort.h"
#include "Algorithm/HeapSort.h"
#include "Algorithm/InsertionSort.h"
#include "Algorithm/QuickSort.h"

// Relight Engine Sorting System
// A system where a list can be sorted

enum class ArrayAlgo
{
    IntroSort,
    HeapSort,
    InsertionSort,
    QuickSort
};

namespace Algo
{
    template <typename ArrayType>

    // Sort an array using IntroSort
    void Sort(ArrayType& Input, ArrayAlgo Type = ArrayAlgo::IntroSort)
    {
        switch(Type)
        {
            case ArrayAlgo::IntroSort:
                IntroSort(Input);
                break;

            case ArrayAlgo::HeapSort:
                HeapSort(Input);
                break;

            case ArrayAlgo::InsertionSort:
                InsertionSort(Input);
                break;

            case ArrayAlgo::QuickSort:
                QuickSort(Input);
                break;
        }
    }
}
