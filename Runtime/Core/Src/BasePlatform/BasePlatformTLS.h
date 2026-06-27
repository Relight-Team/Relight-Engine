#pragma onces

// Thread-local storage. A system in which each thread get's their own copy of a variable
class BasePlatformTLS
{
    public:
        static uint32 AllocateTLSSlot();

        static void FreeTLSSlot(uint32 Index);
};
