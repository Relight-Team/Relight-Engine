#include "LinuxWindow.h"

#include "Core.h"

#include "LinuxMisc.h"

#include "SDL.h"

#include <iostream>

int Window::CreateWindow(const char* Title);
{
    if(SDL_Init(SDL_INIT_VIDEO) < 0)
        {
            LOG(*SDL2, Fatal, "Failed to initialize SDL library!!");
            LOG(*SDL2, Fatal, SDL_GetError());
            return -1;
        }

        window = SDL_CreateWindow(Title, SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,680, 480, 0);


        LOG(*SDL2, Log, "Window created!");
        return 0;
}
