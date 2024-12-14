// RELIGHT ENGINE'S ARRAY SYSTEM!

// This will be replacing both arrays and std::vector
// the goal of this class is to be a more optimized and easier to use version of arrays
// with game development in mind.

// This array class can be treated as either a static array or dynamic array

#include "Core.h" // TODO: replace this for minimal version

#include <iostream> // TODO: Replace this with Relight's alt

CORE_API::LogCategory* Array_Error = new CORE_API::LogCategory("Array");

template <typename T>

class Array
{
    public:

        Array() : Arr(nullptr), CurrentSize(0) {}

        // Initialize

        void Init(T Repeat, int Size)
        {
            InternalChangeSize(Size);

            for(int i = 0; i < Size; i++)
            {
                Arr[i] = Repeat;
            }
        }

        void Init(int Size)
        {
            InternalChangeSize(Size);
        }

        void Init(T Input[])
        {
            InternalChangeSize(sizeof(Input));

            for(int i = 0; i < sizeof(Input); i++)
            {
                Arr[i] = Input[i];
            }
        }

        // == Operators ==

        T& operator[](int i)
        {
            if(i < 0)
            {
                LOG(*Array_Error, Error, "index is lower than 0 when using [] operator. Index must be 0 or higher");
            }

            if(i >= CurrentSize)
            {
                LOG(*Array_Error, Error, "index is higher than the actual array size");
            }

            return Arr[i];
        }

        // == Queries ==

        // Returns the number of elements
        int Num()
        {
            return CurrentSize;
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

        // == Write ==

        void Add(T Input)
        {
            int OldSize = CurrentSize;

            InternalChangeSize(OldSize + 1);

            Arr[OldSize] = Input;
        }

        //void Append

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

        // Destructor to free memory
    ~Array()
    {
        delete[] Arr;
    }

    private:

    T* Arr;

    int CurrentSize;

    void InternalChangeSize(int Size)
    {

        T* NewArr = new T[Size];



        if (Arr != nullptr)
        {
            for(int i = 0; i <= CurrentSize; i++)
            {
                NewArr[i] = Arr[i];
            }
        }

        delete[] Arr;

        Arr = NewArr;

        CurrentSize = Size;
    }

};
