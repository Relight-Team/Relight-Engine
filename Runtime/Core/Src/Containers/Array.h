// RELIGHT ENGINE'S ARRAY SYSTEM!

// This will be replacing both arrays and std::vector
// the goal of this class is to be a more optimized and easier to use version of arrays
// with game development in mind.

// This array class can be treated as either a static array or dynamic array

#pragma once
#include "PlatformCore.h"
#include <initializer_list>

template <typename T>
class Array
{
    public:

        Array() : Arr(nullptr), CurrentSize(0) {}

        // Deep copy constructor
        // prevents double pointer deletion bugs
        Array(const Array& Other) : Arr(nullptr), CurrentSize(0)
        {
            if(Other.CurrentSize > 0)
            {
                // Overwrite Arr
                Arr = new T[Other.CurrentSize];
                for(uint32 I = 0; I < Other.CurrentSize; I++)
                {
                    Arr[I] = Other.Arr[I];
                }
                CurrentSize = Other.CurrentSize;
            }
        }

//         template <typename... Args>
//         Array(Args... InArgs) : Arr(nullptr), CurrentSize(0)
//         {
//             const int32 Size = sizeof...(InArgs);
//             InternalChangeSize(Size);
//             T Temp[] = {InArgs...};
//             for (int32 i = 0; i < Size; i++)
//             {
//                 Arr[i] = (Temp[i]);
//             }
//         }


Array(std::initializer_list<T> Init) : Arr(nullptr), CurrentSize(0)
{
    InternalChangeSize(static_cast<int32>(Init.size()));

    int32 i = 0;
    for (const T& Elem : Init)
    {
        Arr[i++] = Elem;
    }
}

        Array(Array&& Other) noexcept : Arr (Other.Arr), CurrentSize(Other.CurrentSize)
        {
            Other.Arr = nullptr;
            Other.CurrentSize = 0;
        }

        // Initialize

        void Init(T Repeat, int32 Size)
        {
            InternalChangeSize(Size);

            for(int32 i = 0; i < Size; i++)
            {
                Arr[i] = Repeat;
            }
        }

        void Init(T Input[], int32 Size)
        {
            for (int32 i = 0; i < Size; i++)
            {
                this->Add(Input[i]);
            }
        }

        // == Operators ==

        const T& operator[](int32 i) const
        {
            Assert(i < 0, "index is lower than 0 when using [] operator. Index must be 0 or higher", i);
            Assert(i >= CurrentSize, "index is higher than the actual array size", i);
            return Arr[i];
        }

        T& operator[](int32 i)
        {
            Assert(i < 0, "index is lower than 0 when using [] operator. Index must be 0 or higher", i);
            Assert(i >= CurrentSize, "index is higher than the actual array size", i);
            return Arr[i];
        }

        Array<T>& operator=(const Array<T>& B)
        {
            if(this != &B)
            {
                this->Empty();
                for(int32 i = 0; i < B.Length(); i++)
                {
                    this->Add(B[i]);
                }
            }
            return *this;
        }

        Array<T>& operator+=(Array<T>& B)
        {
            this->Append(B, B.Length());
            return *this;
        }

        Array<T>& operator=(Array<T>&& Other) noexcept
        {
            if (this != &Other)
            {
                delete[] Arr;

                Arr = Other.Arr;
                CurrentSize = Other.CurrentSize;

                Other.Arr = nullptr;
                Other.CurrentSize = 0;
            }
            return *this;
        }

        // == Queries ==

        // Returns the number of elements
        int32 Length() const
        {
            return CurrentSize;
        }

        // Like Length(), but assumes the first element index is 0 instead of 1
        int32 Indices() const
        {
            return CurrentSize - 1;
        }


        bool Contains(T Input)
        {
            for(int32 i = 0; i < CurrentSize; i++)
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

            for(int32 i = 0; i < CurrentSize; i++)
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

            for(int32 i = CurrentSize - 1; i >= 0; i--)
            {
                if(Arr[i] == Input)
                {
                    Value = i;
                    return true;
                }
            }
            return false;
        }

        int32 GetTypeSize()
        {
            return sizeof(T);
        }

        bool IsValidIndex(int32 Index)
        {
            if(Index >= 0 && Index <= CurrentSize)
            {
                return true;
            }
            return false;
        }

        Array<T> Reverse()
        {
            Array<T> Ret;

            for(int32 I = Indices(); I >= 0 ; I--)
            {
                Ret.Add(Arr[I]);
            }
            return Ret;
        }

        T Last()
        {
            return Arr[CurrentSize - 1];
        }

        T Last(int32 a)
        {
            return Arr[CurrentSize - 1 - a];
        }

        T Top()
        {
            return Arr[0];
        }

        T Top(int32 a)
        {
            return Arr[0 + a];
        }

        // == Write ==

        void Add(T Input)
        {
            int32 OldSize = CurrentSize;

            InternalChangeSize(OldSize + 1);

            Arr[OldSize] = Input;
        }

        void Append(const Array& Input, int32 Size)
        {

            int32 OldSize = CurrentSize;

            for(int32 i = 0; i < Size; i++)
            {
                this->Add(Input[i]);
            }
        }

        // Only adds the value if it doesn't exist in an array
        void AddUnique(T Input)
        {

            bool AlreadyExist = false;

            for(int32 i = 0; i < CurrentSize; i++)
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

        void Insert(T Input, int32 Index)
        {
            InternalChangeSize(CurrentSize + 1);

            for(int32 i = CurrentSize; i > Index + 1; i--)
            {
                Arr[i] = Arr[i - 1];
            }
            Arr[Index] = Input;
        }

        void RemoveAt(int32 Index)
        {

            int32 Cur = CurrentSize;
            for(int32 i = Index; i < this->Indices(); i++)
            {
                Arr[i] = Arr[i + 1];
            }

            InternalChangeSize(CurrentSize - 1);
        }

        T Pop(int32 Index)
        {
            T Ret = Arr[Index];
            RemoveAt(Index);
            return Ret;
        }

        T Pop()
        {
            return Pop(Indices());
        }

        bool RemoveSingle(T Input)
        {

            int32 StoreIndex;

            for(int32 i = 0; i < CurrentSize; i++)
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

            int32 StoreIndex;

            for(int32 i = 0; i < CurrentSize; i++)
            {
                if(Arr[i] == Input)
                {
                    this->RemoveAt(i);
                }
            }
        }

        void Empty()
        {
            InternalChangeSize(0);
        }

        bool SplitIndex(int32 Index, Array<T>& Left, Array<T>& Right)
        {
            if(Index < 0 or Index > CurrentSize)
            {
                return false;
            }

            Left.Empty();
            Right.Empty();

            // Add left
            for(int32 I = 0; I < Index; I++)
            {
                Left.Add(Arr[I]);
            }

            for(int32 I = Index + 1; I < CurrentSize; I++)
            {
                Right.Add(Arr[I]);
            }

            return true;
        }

        // Like SplitIndex, but keeps the Index value, put's index value on Right
        bool SplitIndexInclusive(int32 Index, Array<T>& Left, Array<T>& Right)
        {
            if(Index < 0 or Index > CurrentSize)
            {
                return false;
            }

            Left.Empty();
            Right.Empty();

            // Add left
            for(int32 I = 0; I < Index; I++)
            {
                Left.Add(Arr[I]);
            }

            for(int32 I = Index; I < CurrentSize; I++)
            {
                Right.Add(Arr[I]);
            }

            return true;
        }

        bool Split(const T& ItemToSplit, Array<T>& Left, Array<T>& Right, bool Last = false, bool Inclusive = false)
        {
            int32 Index;
            bool NoErr;
            if(Last == false)
            {
                NoErr = Find(ItemToSplit, Index);
            }
            else
            {
                NoErr = FindLast(ItemToSplit, Index);
            }

            if(NoErr == false)
            {
                return false;
            }

            if(Inclusive == false)
            {
                return SplitIndex(Index, Left, Right);
            }
            else
            {
                return SplitIndexInclusive(Index, Left, Right);
            }
        }

        void Swap(int32 A, int32 B)
        {
            T ContentA = Arr[A];
            Arr[A] = Arr[B];
            Arr[B] = ContentA;
        }

        void Replace(T Input, int32 Index)
        {
            Arr[Index] = Input;
        }

        T* ReturnPointer()
        {
            return Arr;
        }

        // Destructor to free memory
    ~Array()
    {
        delete[] Arr;
        Arr = nullptr;
        CurrentSize = 0;
    }

    private:

    T* Arr;


    // Reminder, this assumes the first element is 1, this is very annoying, but some functions requires it
    int32 CurrentSize;

    void InternalChangeSize(int32 Size)
    {

        T* NewArr = new T[Size];


        int32 CopySize = (Size < CurrentSize) ? Size : CurrentSize;

            if (Arr != nullptr)
            {
                for(int32 i = 0; i < CopySize; i++)
                {
                    NewArr[i] = Arr[i];
                }
            }


        delete[] Arr;

        Arr = NewArr;

        CurrentSize = Size;
    }

};
