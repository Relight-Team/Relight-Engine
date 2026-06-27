#pragma once
#include "BasePlatform/BasePlatformTLS.h"
#include "PlatformCore.h"

class UnixPlatformTLS : public BasePlatformTLS
{
    public:
        static uint32 AllocateTLSSlot()
        {

            pthread_key_t Key;

            // Create thread key, return -1 if failed
            if(pthread_key_create(&Key, nullptr) != 0)
            {
                return -1;
            }

            return Key;
        }

        static void FreeTLSSlot(uint32 Index)
        {
            pthread_key_delete((pthread_key_t)Index);
        }
};
