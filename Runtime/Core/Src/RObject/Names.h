#pragma once
#include "Core.h"
#include "PlatformCore.h"

// List of common ID's the engine will use
enum class RNameIDList
{
    NONE = 0
};

struct RNameID
{
    public:

        constexpr RNameID()
            : Var(0)
        {
        }

        RNameID(uint32 Input)
        {
            Var = Input;
        }

        RNameID(RNameIDList Input)
        {
            Var = Input;
        }

        uint32 Get()
        {
            return Var;
        }

        bool operator==(RNameID Second)
        {
            return Get() == Second.Get();
        }

    private:

        uint32 Var;
};

class RNamePool
{
    public:

        uint32 Length()
        {
            return IDToName.Indices() + 1;
        }

        uint32 Indices()
        {
            return IDToName.Indices();
        }

        // get existing ID if it exists, otherwise return a new ID
        RNameID FindOrAdd(String Input, bool IsDupList)
        {
            // search for each string
            for(int32 I = 0; I < Length(); I++)
            {
                String Sec = IDToName.Second(I);

                // Return ID if it already exists
                if(Sec == Input)
                {
                    if(IsDupList)
                    {
                        DupList[I]++;
                    }
                    return IDToName.First(I);
                }
            }

            // if it doesn't exist, create a new one

            RNameID Ret(Length());

            String Name(Input);

            IDToName.SetAdd(Ret, Name);

            DupList.Add(0);

            return Ret;
        }

        RNameID FindOrAdd(char* Input, bool IsDupList)
        {
            return FindOrAdd(String(Input), IsDupList);
        }

        uint32 GetDup(uint32 Index)
        {
            return DupList[Index];
        }

        String GetNameFromID(uint32 Index)
        {
            return IDToName.Second(Index);
        }

    private:

        // TODO: Replace this with RNameIDList
        Map<RNameID, String> IDToName;
        Array<uint32> DupList;
};

extern RNamePool GlobalRNamePool;

class RName
{
    public:

        RName(String Input, bool Unique = false)
        {
            IDIndex = GlobalRNamePool.FindOrAdd(Input, Unique);
            if(Unique)
            {
                DupIndex = GlobalRNamePool.GetDup(IDIndex.Get());
            }
            else
            {
                DupIndex = 0;
            }
        }

        RName(UTF16* Input, bool Unique = false)
        {
            RName(String(Input), Unique);
        }

        inline uint32 GetIndex()
        {
            return IDIndex.Get();
        }

        inline String ToString()
        {
            return GlobalRNamePool.GetNameFromID(IDIndex.Get());
        }

        inline uint32 GetDupIndex()
        {
            return DupIndex;
        }

        // TODO: In the future do a hash lookup to speed things up

        inline bool operator==(RName& Other)
        {
            return (IDIndex.Get() == Other.IDIndex.Get()) && (DupIndex == Other.GetDupIndex());
        }

    private:

        RNameID IDIndex;
        uint32 DupIndex;
};
