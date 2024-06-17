// Owned by Relight Engine 2024

#include <iostream>

// set windows
#if defined(_WIN32) || defined(_WIN64)
  bool IsWindows() { return true; }
#else
  bool IsWindows() { return false; }
#endif

// set linux
#if defined(__linux__)
  bool IsLinux() { return true; }
#else
  bool IsLinux() { return false; }
#endif

// set mac
#if defined(__APPLE__) || defined(__MACH__)
  bool IsApple() { return true; }
#else
  bool IsApple() { return false; }
#endif


std::string GetCurrent()
{
 if(IsWindows() == true)
 {
   return "Windows";
 }
 else if(IsLinux() == true)
 {
   return "Linux";
 }
  else
 {
   return "Apple";
 }
}


std::string ExeExt()
{
  if(IsWindows() == true)
  {
    return ".exe";
  }
  else
  {
    return "";
  }
}
