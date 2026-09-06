#pragma once
#include "Serialization/StructuredArchive.h"

// Uses tree system
// example:

// Root (Element: 1)
//  |
//  - Name (Depth: 1, Element: 2)
//  - Inv (Depth: 1, Element: 3)
//      - Index 0 (Depth: 2, Element: 4)
//      - Index 1 (Depth: 2, Element: 5)


namespace RE::Internal::StructureArchive
{

    // The element of the tree, always increases by one no matter the depth
    // use to keep of the ordering of data
    struct Element
    {
        Element() = default;

        Element(uint32 InID)
        {
            ID = InID;
        }

        void Reset()
        {
            ID = 0;
        }

        bool IsValid() const
        {
            return ID != 0;
        }

        bool operator==(const Element& Other) const
        {
            return ID == Other.ID;
        }

        bool operator!=(const Element& Other) const
        {
            return ID != Other.ID;
        }

        private:

            uint32 ID = 0;
    };

    // Keeps track of a specific data, includes Element and Depth
    // Depth keeps track of how nested the data is
    class SlotNode
    {
        friend class StructureArchive;

        public:

        int32 Depth;
        Element ID;

        explicit SlotNode(int32 InDepth, Element InElement)
        : Depth(InDepth),
          Element(InElement)
        {
        }

    };

    // TODO - Add option for text-based structure archive using SlotNode
    class StructureArchiveSlotBase
    {
        friend class StructureArchive;

        public:

        protected:
            StructureArchive& StAr;

        private:
            // System where only friends of this class can create this class
            explicit StructureArchiveSlot(StructureArchive& InAr)
            : StAr(InAr);
            {
            }
    };
}

// Slot system, represents a value in the archive
class StructureArchiveSlot : public RE::Internal::StructureArchive::StructureArchiveSlotBase
{
    friend class StructureArchive;

    public:

        template <typename T>
        void operator<<(T& Value)
        {
            StAr << Temp;
        }


};
