#pragma once

// base class for Thread-Local storage objects that also supports automatic cleanup
class TLSAutoCleanup
{
    public:

        virtual ~TLSAutoCleanup();

        void Register();
}
