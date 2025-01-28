// RELIGHT ENGINE'S ARRAY SYSTEM!

// This will be replacing both arrays and std::vector
// the goal of this class is to be a more optimized and easier to use version of arrays
// with game development in mind.

// This array class can be treated as either a static array or dynamic array

#pragma once

#include "Log/Log.h"

//#include <iostream> // TODO: Replace this with Relight's alt

CORE_API::LogCategory* Array_Error = new CORE_API::LogCategory("Array");

template <typename T>


class Array
{
    public:

        Array() : Arr(nullptr), CurrentSize(0) {}

        // Initialize

        void Init(T Repeat, int Size);

        void Init(int Size);

        void Init(T Input[], int Size)
        {
            for (int i = 0; i < Size; i++)
            {
                this->Add(Input[i]);
            }
        }

        // == Operators ==

        T& operator[](int i)
        {
            if(i < 0)
            {
                LOG(*Array_Error, Fatal, "index is lower than 0 when using [] operator. Index must be 0 or higher");
            }

            if(i >= CurrentSize)
            {
                LOG(*Array_Error, Fatal, "index is higher than the actual array size");
            }

            return Arr[i];
        }

        Array<T>& operator=(Array<T>& B)
        {
            this->Empty();
            for(int i = 0; i < B.Num(); i++)
            {
                this->Add(B[i]);
            }
            return *this;
        }

        Array<T>& operator+=(Array<T>& B)
        {
            this->Append(B, B.Num());
            return *this;
        }

        // == Queries ==

        // Returns the number of elements
        int Num()
        {
            return CurrentSize;
        }

        // Like Num(), but assumes the first element index is 0 instead of 1
        int Size()
        {
            return CurrentSize - 1;
        }

        // for debugging only
        void Print()
        {
            std::string tmp;
            for(int i = 0; i < CurrentSize; i++)
            {
                std::cout << Arr[i];
                std::cout << " | ";
            }
            std::cout << std::endl;
        }


        bool Contains(T Input)
        {
            for(int i = 0; i < CurrentSize; i++)
            {
                if(Arr[i] == Input)
                {
                    return true;
                }
            }
            return false;
        }

        bool Find(T Input, int& Value)
        {
            if(!(Contains(Input)))
            {
                return false;
            }

            for(int i = 0; i < CurrentSize; i++)
            {
                if(Arr[i] == Input)
                {
                    Value = i;
                    return true;
                }
            }
            return false;
        }

        bool FindLast(T Input, int& Value)
        {
            if(!(Contains(Input)))
            {
                return false;
            }

            for(int i = CurrentSize - 1; i >= 0; i++)
            {
                if(Arr[i] == Input)
                {
                    Value = i;
                    return true;
                }
            }
            return false;
        }

        int GetTypeSize()
        {
            return sizeof(T);
        }

        bool IsValidIndex(int Index)
        {
            if(Index >= 0 && Index <= CurrentSize)
            {
                return true;
            }
            return false;
        }

        T Last()
        {
            return Arr[CurrentSize - 1];
        }

        T Last(int a)
        {
            return Arr[CurrentSize - 1 - a];
        }

        T Top()
        {
            return Arr[0];
        }

        T Top(int a)
        {
            return Arr[0 + a];
        }

        // == Write ==

        void Add(T Input);

        void Append(Array& Input, int Size)
        {

            int OldSize = CurrentSize;

            for(int i = 0; i < Size; i++)
            {
                this->Add(Input[i]);
            }
        }

        void SetNum(int NewSize);

        // Only adds the value if it doesn't exist in an array
        void AddUnique(T Input)
        {

            bool AlreadyExist = false;

            for(int i = 0; i < CurrentSize; i++)
            {
                if(Arr[i] == Input)
                {
                    AlreadyExist = true;
                }
            }

            if(AlreadyExist == false)
            {
                this->Add(Input);
            }
        }

        void Insert(T Input, int Index);

        void RemoveAt(int Index)
        {

            int Cur = CurrentSize;
            for(int i = Index; i < this->Num(); i++)
            {
                Arr[i] = Arr[i + 1];
            }

            InternalChangeSize(CurrentSize - 1);
        }

        bool RemoveSingle(T Input)
        {

            int StoreIndex;

            for(int i = 0; i < CurrentSize; i++)
            {
                if(Arr[i] == Input)
                {
                    this->RemoveAt(i);
                    return true;
                }
            }
            return false;
        }

        void Remove(T Input)
        {

            int StoreIndex;

            for(int i = 0; i < CurrentSize; i++)
            {
                if(Arr[i] == Input)
                {
                    this->RemoveAt(i);
                }
            }
        }

        void Empty();

        // Destructor to free memory
    ~Array()
    {
        delete[] Arr;
        Arr = nullptr;
    }

    private:

    T* Arr;


    // Reminder, this assumes the first element is 1, this is very annoying, but some functions requires it
    int CurrentSize;

    void InternalChangeSize(int Size)
    {

        T* NewArr = new T[Size];


        int CopySize = (Size < CurrentSize) ? Size : CurrentSize;

            if (Arr != nullptr)
            {
                for(int i = 0; i < CopySize; i++)
                {
                    NewArr[i] = Arr[i];
                }
            }


        delete[] Arr;

        Arr = NewArr;

        CurrentSize = Size;
    }

};
