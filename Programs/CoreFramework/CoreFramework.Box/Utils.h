// Owned by Relight Engine 2024

#include <iostream>

using namespace std;

public static class Utils
{
public:
    static bool Avail = false;

    public static bool IsAvail()
    {
        return Avail;
    }


    // I'm not writting an alternative to <Lazy>, just use this method for setting the value for now
    public static void SetAvail(bool SetAv)
    {
        Avail = SetAv
    }

}
