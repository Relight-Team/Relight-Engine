// RELIGHT ENGINE'S ARRAY SYSTEM!

// This will be replacing both arrays and std::vector
// the goal of this class is to be a more optimized and easier to use version of arrays
// with game development in mind.

// This array class can be treated as either a static array or dynamic array

#include "Log/Log.h"
#include "Containers/Array.h"


template <typename T>
void Array<T>::Init(T Repeat, int Size)
{
    InternalChangeSize(Size);

    for(int i = 0; i < Size; i++)
    {
        Arr[i] = Repeat;
    }
}

template <typename T>
void Array<T>::Init(int Size)
{
    InternalChangeSize(Size);
}

template <typename T>
void Array<T>::Add(T Input)
{
    int OldSize = CurrentSize;

    InternalChangeSize(OldSize + 1);

    Arr[OldSize] = Input;
}

template <typename T>
void Array<T>::SetNum(int NewSize)
{
    InternalChangeSize(NewSize);
}

template <typename T>
void Array<T>::Insert(T Input, int Index)
{
    InternalChangeSize(CurrentSize + 1);

    for(int i = CurrentSize; i > Index + 1; i--)
    {
        Arr[i] = Arr[i - 1];
    }
    Arr[Index] = Input;
}

template <typename T>
void Array<T>::Empty()
    {
        InternalChangeSize(0);
    }
