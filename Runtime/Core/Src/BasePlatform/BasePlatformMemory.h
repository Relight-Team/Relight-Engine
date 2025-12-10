class BasePlatformMemory
{
public:
    static bool IsOutOfMemory;

    static void Start();

    static void ExecWhenOOM(int Size, int Ali);


};
