// Relight Engine Archive System

// Archive is an abstract base class allowing abstractions for data reading and writing
// Examples of child class: Memory reader/writer, file reader/writer, etc

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
}

class Archive : private ArchiveState
{
    public:
    void Serialize(void* Input, int Length)
    {
        memset(Input, 0, Length);
    }
}
