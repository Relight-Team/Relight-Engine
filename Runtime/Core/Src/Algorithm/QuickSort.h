// Relight Engine QuickSort and Partition
#pragma once
#include "PlatformCore.h"

template <typename ArrayType>
int32 Partition(ArrayType& Arr, int32 Min, int32 Max)
{
    int32 Piv = Arr[Max];
    int32 I = Min - 1;

    for(int32 J = Min; J <= Max - 1; J++)
    {
        if(Arr[J] <= Piv)
        {
            I++;
            Arr.Swap(I, J);
        }
    }

    Arr.Swap(I + 1, Max);
    return I + 1;
}

template <typename ArrayType>
void QuickSort(ArrayType& Arr, int32 Min, int32 Max)
{
    if (Min >= Max)
    {
        return;
    }

    int32 Part = Partition(Arr, Min, Max);

    QuickSort(Arr, Min, Part - 1);
    QuickSort(Arr, Part + 1, Max);
}

template <typename ArrayType>
void QuickSort(ArrayType& Arr)
{
    int32 Length = Arr.Indices();
    QuickSort(Arr, 0, Length);
}
