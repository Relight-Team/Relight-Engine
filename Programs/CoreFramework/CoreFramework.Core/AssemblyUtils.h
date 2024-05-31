// Owned by Relight Engine 2024

#include <iostream>
#include <unistd.h>
#include <limits.h>
#include <filesystem>


using namespace std;



// Returns the currently running exe path
static string GetOriginalLoc()
{
  char buffer[PATH_MAX];
  ssize_t count = readlink("/proc/self/exe", buffer, PATH_MAX);
  if (count != -1)
  {
      buffer[count] = '\0';
      return buffer;
  }
  else
  {
    perror("readlink");
    return "ERR -1";
  }
}




// This code is very shitty, but hey, it now works I guess
// Returns the input exe path
std::string GetOriginalLoc(const std::string& filepath)
{
  
  char resolved_path[PATH_MAX];
  if (realpath(filepath.c_str(), resolved_path) != NULL)
  {
      return std::string(resolved_path);
  }
  else
  {
      // Handle error if realpath() fails
      return "ERR -1";
  }
}




// TODO: Finish this after getting all third party stuff
