#include "Platform.h"
#include "Hardware/Malloc.h"

//FIXME:
// This is a VERY wip code that handles Malloc operations, however the codebase has become too much for me, so I am pausing development on Malloc until I can come back with fresh mind

class MALLOCBINNEDv1 : public Malloc
{
    struct BundleNode
    {
      BundleNode* NextNode;

      union
      {
        BundleNode* NextBundle;
        int Count;
      };
    };

    struct Bundle
    {
        BundleNode* Head;
        int Count;

        Bundle()
        {
            Reset();
        }

        void Reset()
        {
            Head = nullptr;
            Count = 0;
        }

        BundleNode* PopHead()
        {
            BundleNode* Ret = Head;
            Count--;
            Head = Head->NextNode;
            return Ret;
        }

        void PushHead(BundleNode* Node)
        {
            Node->NextNode = Head;
            Node->NextBundle = nullptr;
            Head = Node;
            Count++;
        }
    };

    struct ListFreeBlocks
    {

        bool CanPushToFront(int BlockSize)
        {
            if(Full.Head && (Partial.Count >= 64 || Partial.Count * BlockSize >= 64))
            {
             return false;
            }
            return true;
        }

        bool PushToFront(void* Ptr, int BlockSize)
        {
            if(CanPushToFront(BlockSize) == false)
            {
                return false;
            }

            if(Partial.Count >= 64 || Partial.Count * BlockSize >= 64)
            {
                Full = Partial;
                Partial.Reset();
            }

            Partial.PushHead((BundleNode*)Ptr);
            return true;
        }

        void* PopFromFront()
        {
            if(!Partial.Head and Full.Head)
            {
                Partial.Head = Full.Head;
                Full.Reset();
            }

            if(Partial.Head)
            {
                return Partial.PopHead();
            }
            else
            {
                return nullptr;
            }
        }

    private:
        Bundle Partial;
        Bundle Full;
    };

public:

    void* Malloc(size_t Count, int Alignment=0);
    {
        return FreeBlocksList[Count].PopFromFront();
    }

    bool Free(void* Ptr, int Count, int Alignment=0)
    {
        return FreeBlocksList[Count].PushToFront(Ptr, );
    }

    bool CanFree(int Count, int Size)
    {
        return FreeBlocksList[Count].CanPushToFront(Size);
    }

private:

    ListFreeBlocks FreeBlocksList[45];

};
