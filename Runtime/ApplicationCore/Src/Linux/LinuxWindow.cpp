#include "Core.h"

#include "LinuxWindow.h"

#include "LinuxAppMisc.h"

#include "SDL3/SDL.h"

#include <iostream>

int Window::CreateWindow(const char* Title)
{
    if(!SDL_Init(SDL_INIT_VIDEO))
        {
            LOG(SDL3Log, Fatal, "Failed to initialize SDL library!!");
            LOG(SDL3Log, Fatal, SDL_GetError());
            return -1;
        }

        window = SDL_CreateWindow(Title, 680, 480, 0);


        LOG(SDL3Log, Log, "Window created!");
        return 0;
}
