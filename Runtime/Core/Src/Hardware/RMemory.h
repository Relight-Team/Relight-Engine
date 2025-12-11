#pragma once

// FIXME: THIS IS A TEMP SOLUTION!!!
// Turns out writing your own Malloc is hard, so for now, we will be using iostream's malloc/free
// Please replace this later with custom version!
#include <iostream>
#include <cstdlib>
#include <string.h>

struct RMemory
{

    static void* Malloc(size_t Size, int Alignment = 0)
    {
        return malloc(Size);
    }

    static void* Realloc(void* Ptr, size_t Size, int Alignment = 0)
    {
        return realloc(Ptr, Size);
    }

    static void Free(void* Ptr)
    {
        free(Ptr);
    }

    static void* Memmove(void* Dest, void* Src, size_t Size)
    {
        return memmove(Dest, Src, Size);
    }

    static int Memcmp(void* A, void* B, size_t Size)
    {
        return memcmp(A, B, Size);
    }

    static void* Memset(void* A, int C, size_t Size)
    {
        return memset(A, C, Size);
    }

    static void* Memcpy(void* Dest, void* Src, size_t Size)
    {
        return memcpy(Dest, Src, Size);
    }

};
