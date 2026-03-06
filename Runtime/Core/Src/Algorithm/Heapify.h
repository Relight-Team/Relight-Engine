#pragma once
#include "PlatformCore.h"
// Relight Engine's heapify function

template <typename ArrayType>
void Heapify(ArrayType& Arr, int32 HeapSize, int32 Root)
{


    int32 Largest = Root;
    int32 Left = 2 * Root + 1;
    int32 Right = 2 * Root + 2;

    // If left is larger than root
    if(Left < HeapSize && Arr[Left] > Arr[Largest])
    {
        Largest = Left;
    }

    // If right is larger than root
    if(Right < HeapSize && Arr[Right] > Arr[Largest])
    {
        Largest = Right;
    }

    if(Largest != Root)
    {
        Arr.Swap(Root, Largest);
        Heapify(Arr, HeapSize, Largest);
    }
}
template <typename ArrayType>
void Heapify(ArrayType& Arr)
{
    int32 Size = Arr.Indices();
    int32 StartIndex = (Size / 2) - 1;

    for(int32 I = StartIndex; I >= 0; I--)
    {
        Heapify(Arr, Size, I);
    }
}
