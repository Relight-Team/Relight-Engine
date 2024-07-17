// Owned by Relight Engine 2024

#include <unistd.h> 
#include <sys/types.h>
#include <iostream>
#include <sys/wait.h>

class LinuxCommon
{

public:
    static std::string GetExecutablePath(std::string TheName)
      {
        pid_t Process = fork();

        execlp("/bin/sh", "sh", "-c", ("which " + TheName).c_str(), nullptr);

        int status;

        waitpid(Process, &status, 0);

        // I used replit's ai help with this, ai is always shit with code so this may or may not work. Maybe I should ban AI from the project, but I like using it for documentation and reference, idk

        //does the readline
        if (WIFEXITED(status))
        {
          char path[1024]; // Adjust size as necessary
          ssize_t count = read(STDIN_FILENO, path, sizeof(path));

          if (count > 0) {
              path[count - 1] = '\0'; // Remove newline
              return std::string(path);
          }
        }
      }
};