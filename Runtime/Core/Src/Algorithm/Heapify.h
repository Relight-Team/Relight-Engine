// Relight Engine's heapify function

#include <iostream>

template <typename ArrayType>
void Heapify(ArrayType& Arr, int HeapSize, int Root)
{


    int Largest = Root;
    int Left = 2 * Root + 1;
    int Right = 2 * Root + 2;

        std::cout << "Root=" << Root
          << " Left=" << Left
          << " Right=" << Right
          << " HeapSize=" << HeapSize
          << std::endl;

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
