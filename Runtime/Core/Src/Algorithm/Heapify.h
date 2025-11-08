// Relight Engine's heapify function

template <typename ArrayType>
void Heapify(ArrayType& Arr, int HeapSize, int Root)
{


    int Largest = Root;
    int Left = 2 * Root + 1;
    int Right = 2 * Root + 2;

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
