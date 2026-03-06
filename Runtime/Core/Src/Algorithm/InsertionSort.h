// Relight Engine Insertion Sort
#pragma once
#include "PlatformCore.h"

template <typename ArrayType>
void InsertionSort(ArrayType& Arr, int32 Min, int32 Max)
{
    for(int32 I = Min + 1; I <= Max; I++)
    {
        auto ArrObject = Arr[I];
        int32 J = I - 1;

        while(J >= Min && Arr[J] > ArrObject)
        {
            Arr.Replace(Arr[J], J + 1);
            J -= 1;
        }
        Arr.Replace(ArrObject, J + 1);
    }
}

template <typename ArrayType>
void InsertionSort(ArrayType& Arr)
{
    int32 Length = Arr.Indices();
    InsertionSort(Arr, 0, Length);
}
