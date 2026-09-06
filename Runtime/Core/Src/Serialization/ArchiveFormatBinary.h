#pragma once
#include "Serialization/Archive.h"
#include "Serialization/ArchiveFormat.h"

class RString;
class RName;
class RObject;

class RObjectPtr;
class RObjectWeakPtr;
class RAssetPtr;
class RAssetPath;

// Archive formatted as a binary
class ArchiveFormatBinary
{
    public:

        ArchiveFormatBinary(RArchive& Input)
        : Ar(Input)
        {
        }

        virtual void Serialize(int8& Data) override
        {
            Ar << Data
        }

        virtual void Serialize(uint8& Data) override
        {
            Ar << Data
        }

        virtual void Serialize(int16& Data) override
        {
            Ar << Data
        }

        virtual void Serialize(uint16& Data) override
        {
            Ar << Data
        }

        virtual void Serialize(int32& Data) override
        {
            Ar << Data
        }

        virtual void Serialize(uint32& Data) override
        {
            Ar << Data
        }

        virtual void Serialize(int64& Data) override
        {
            Ar << Data
        }

        virtual void Serialize(uint64& Data) override
        {
            Ar << Data
        }

        virtual void Serialize(float& Data) override
        {
            Ar << Data
        }

        virtual void Serialize(double& Data) override
        {
            Ar << Data
        }

        virtual void Serialize(bool& Data) override
        {
            Ar << Data
        }

        virtual void Serialize(RString& Data) override
        {
            Ar << Data
        }

        virtual void Serialize(RName& Data) override
        {
            Ar << Data
        }

        virtual void Serialize(RObject*& Data) override
        {
            Ar << Data
        }

        virtual void Serialize(RObjectPtr& Data) override
        {
            Ar << Data
        }

        virtual void Serialize(RObjectWeakPtr& Data) override
        {
            Ar << Data
        }

        virtual void Serialize(RAssetPtr& Data) override
        {
            Ar << Data
        }

        virtual void Serialize(RAssetPath& Data) override
        {
            Ar << Data
        }

        virtual void Serialize(Array<uint8>& Data) override
        {
            Ar << Data
        }

        virtual void Serialize(void* Data, uint64 Size) override
        {
            Ar.Serialize(Data, Size);
        }

    private:
        RArchive& Ar;
};
