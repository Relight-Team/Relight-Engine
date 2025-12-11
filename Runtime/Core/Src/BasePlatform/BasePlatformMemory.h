#pragma once
class BasePlatformMemory
{
public:
    bool IsOutOfMemory;

    size_t PageSize = 0;

    size_t BinnedPageSize = 0;

    static void Start();

    static void ExecWhenOOM(int Size, int Ali);

    static void BinnedAlloc(size_t Size);
};
