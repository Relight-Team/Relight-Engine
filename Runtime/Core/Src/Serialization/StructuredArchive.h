#pragma once
#include "Serialization/ArchiveFormatBinary.h"

// TODO - Add support for structured archive formatter if defined using -D
using StructureArchiveFormatType = ArchiveFormatBinary

// System to read and write data in hierarchical.
class StructureArchive
{
    friend class StructureArchiveSlot

    public:

        using ArSlot = StructuredArchiveSlot;

        template <typename T>
        void operator<<(T& Data)
        {
            Format << Data;
        }

    private:

        StructureArchiveFormatType Format;

        friend class StructuredArchiveSlot;
};
