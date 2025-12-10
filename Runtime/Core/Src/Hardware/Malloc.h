#pragma once

// FIXME: Everything

class Malloc
{
public:
    virtual void* Malloc(size_t Count, int Alignment=0);

    virtual void* Realloc(void* Ptr, size_t Count, int Alignment=0);

    virtual void Free(void* Ptr, int Count, int Alignment=0);

    virtual size_t QuantCount(void* Ptr, size_t Count, int Alignment)
    {
        return Count;
    }

    virtual void Trim(bool ShouldTrimThreadCashes);
};
