// Relight Engine QuickSort and Partition
#pragma once


template <typename ArrayType>
int Partition(ArrayType& Arr, int Min, int Max)
{
    int Piv = Arr[Max];
    int I = Min - 1;

    for(int J = Min; J <= Max - 1; J++)
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
void QuickSort(ArrayType& Arr, int Min, int Max)
{
    if (Min >= Max)
    {
        return;
    }

    int Part = Partition(Arr, Min, Max);

    QuickSort(Arr, Min, Part - 1);
    QuickSort(Arr, Part + 1, Max);
}

template <typename ArrayType>
void QuickSort(ArrayType& Arr)
{
    int Length = Arr.Length();
    QuickSort(Arr, 0, Length);
}
