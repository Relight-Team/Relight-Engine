#pragma once
#include <new>
#include <type_traits>

// Alligns to certain part of memory, useful for optimization, since it ensures that all the data is in a single chunk the cpu reads instead of 2 seperate chunks
// (example: setting the input of 4 will start at memory [0, 4, 8, 12, 16, etc].)
// pretty much acts as padding
template<int32 Size, uint32 Alignment>
struct AlignedBytes
{
    alignas(Alignment) uint8 Padding[Size];
};
