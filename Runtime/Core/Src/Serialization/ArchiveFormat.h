#pragma once
#include "Container/Array.h"
#include "Serialization/Archive.h"

class RString;
class RName;
class RObject;

class RObjectPtr;
class RObjectWeakPtr;
class RAssetPtr;
class RAssetPath;

// Tells how to format an archive
class RArchiveFormatter
{
    public:

        virtual void Serialize(void* Data, uint64 Size) = 0;

        virtual void Serialize(int8& Data) = 0;

        virtual void Serialize(uint8& Data) = 0;

        virtual void Serialize(int16& Data) = 0;

        virtual void Serialize(uint16& Data) = 0;

        virtual void Serialize(int32& Data) = 0;

        virtual void Serialize(uint32& Data) = 0;

        virtual void Serialize(int64& Data) = 0;

        virtual void Serialize(uint64& Data) = 0;

        virtual void Serialize(float& Data) = 0;

        virtual void Serialize(double& Data) = 0;

        virtual void Serialize(bool& Data) = 0;

        virtual void Serialize(RString& Data) = 0;

        virtual void Serialize(RName& Data) = 0;

        virtual void Serialize(RObject*& Data) = 0;

        virtual void Serialize(RObjectPtr& Data) = 0;

        virtual void Serialize(RObjectWeakPtr& Data) = 0;

        virtual void Serialize(RAssetPtr& Data) = 0;

        virtual void Serialize(RAssetPath& Data) = 0;

        virtual void Serialize(Array<uint8> Data) = 0;
};
