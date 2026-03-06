#pragma once
#include "Platform.h"
#include "PlatformCore.h"
#include "Serialization/ArchiveProxy.h"
#include "Serialization/Archive.h"
#include "Containers/String.h"
#include "Etc/CharUtil.h"

// FIXME: This is a placeholder until custom file reader is implemented
class FileReader : public Archive
{
public:
    // Store File data in class
    void Serialize(void* Input, uint32 Length) override
    {
        InnerFile = static_cast<const char*>(Input);

        Size = static_cast<size_t>(Length);
    }

    void Flush() override
    {
    }

    void Seek(int32 Offset) override
    {
    }

    size_t GetSize()
    {
        return Size;
    }

    const char operator[](int32 I) const
    {
        return InnerFile[I];
    }

    String ToString()
    {
        String Ret;

        for(int32 I = 0; I < GetSize(); I++)
        {
            Ret.Append(CharUtil::IntToChar(InnerFile[I]));
        }

        return Ret;
    }

private:

    const char* InnerFile;

    size_t Size;
};
