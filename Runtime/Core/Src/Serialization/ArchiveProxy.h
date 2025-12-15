#include "Serialization/Archive.h"


class Archive: private ArchiveState
{
    public:
    virtual void Serialize(void* Input, int Length)
    {
        BaseArchive.Serialize(Input, Length);
    }

    virtual void Flush()
    {
        BaseArchive.Flush();
    }

    virtual void Seek(int Offset)
    {
        BaseArchive.Seek(Offset);
    }

    protected:
        Archive& BaseArchive;
};
