#pragma once
#include "Serialization/Archive.h"

// Proxy's are used as a wrapper around a normal archive to inject and override custom functions at runtime.
class ArchiveProxy : public Archive
{
    public:
    ArchiveProxy(Archive& InArchive) : BaseArchive(InArchive)
    {
    }

    virtual void Serialize(void* Input, uint32 Length)
    {
        BaseArchive.Serialize(Input, Length);
    }

    virtual void Flush()
    {
        BaseArchive.Flush();
    }

    virtual void Seek(int32 Offset)
    {
        BaseArchive.Seek(Offset);
    }

    protected:
        Archive& BaseArchive;
};
