// Relight Engine Archive System

// Archive is an abstract base class allowing abstractions for data reading and writing
// Examples of child class: Memory reader/writer, file reader/writer, etc
#pragma once
#include "Hardware/RMemory.h"

struct ArchiveState
{
    public:
    bool ContainCode = false; // Does Archive contain code
    bool ContainRMap = false; // Does Archive contain RLevel or RWorld?
    bool IsSaveLoadGame = false; // Is Archive for saving/loading a game?
    bool IsCountingMem = false; // Does Archive count memory?

    protected:
    bool IsLoading = false; // Is Archive for loading data?
    bool IsSaving = false; // Is Archive for saving data?
    bool IsTracking = false; // Is Archive tracking something? (like redo/undo)
    bool IsLoadingPak = false; // Is loading from pak file?



    private:
    bool IsError = false; // Does Archive contain errors?
    bool IsFatal = false; // Does Archive have fatal errors?

    friend class Archive;
};

class Archive: private ArchiveState
{
    public:

    virtual ~Archive() = default;

    // Convert data into a readable format
    virtual void Serialize(void* Input, int Length)
    {
        RMemory::Memset(Input, 0, Length);
    }

    // Fource to finish writing buffered data to hard disk
    virtual void Flush() = 0;

    // Set the current offset of data storage
    virtual void Seek(int Offset) = 0;

    bool DoesReturnCode()
    {
        return ContainCode;
    }

    bool DoesContainRMap()
    {
        return ContainRMap;
    }

    bool DoesIsSaveLoadGame()
    {
        return IsSaveLoadGame;
    }

    bool DoesIsCountingMem()
    {
        return IsCountingMem;
    }

    bool DoesIsLoading()
    {
        return IsLoading;
    }

    bool DoesIsSaving()
    {
        return IsSaving;
    }

    bool DoesIsTracking()
    {
        return IsTracking;
    }

    bool DoesIsLoadingPak()
    {
        return IsLoadingPak;
    }

    bool DoesIsError()
    {
        return IsError;
    }

    bool DoesIsFatal()
    {
        return IsFatal;
    }
};
