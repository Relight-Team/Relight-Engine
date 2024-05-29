// Owned by Relight Engine 2024

#include <iostream>
#include <unistd.h>
#include <limits.h>

using namespace std;


// Returns the currently running exe path
static string GetOriginalLoc()
{
  char buffer[PATH_MAX];
  ssize_t count = readlink("/proc/self/exe", buffer, PATH_MAX);
  if (count != -1) {
      buffer[count] = '\0';
      return buffer;
  }
  else
  {
    return "ERR";
  }
}



// TODO:
// This other method doesn't work correctly, appears to just print the ERR. Please FIX

// Returns the input exe path
  static string GetOriginalLoc(const char* TheAssembly)
  {
    char buffer[PATH_MAX];
    ssize_t count = readlink(TheAssembly, buffer, PATH_MAX);
    if (count != -1) {
        buffer[count] = '\0';
        return buffer;
    }
    else
    {
      return "ERR";
    }
  }



//TODO:

// Don't forget to finish the rest of the methods in this file