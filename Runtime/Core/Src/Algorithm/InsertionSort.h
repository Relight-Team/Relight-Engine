// Relight Engine Insertion Sort

template <typename ArrayType>
void InsertionSort(ArrayType& Arr, int Depth)
{
    for(int I = 1; I <= Depth; I++)
    {
        auto ArrObject = Arr[I];
        int J = I - 1;

        while(J >= 0 && Arr[J] > ArrObject)
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
    int Length = Arr.Length();
    InsertionSort(Arr, Length);
}
