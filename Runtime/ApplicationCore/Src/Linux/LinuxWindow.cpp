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

    // Get default size
    int X;
    int Y;

    bool XSuccess = Config::GetInt("/Relight/EngineSettings.Window", "DefaultResX", X, "BaseEngine.cfg");

    if(!(XSuccess))
    {
        LOG(SDL3Log, Fatal, "Failed to get default X Size from config");
        return -1;
    }

    bool YSuccess = Config::GetInt("/Relight/EngineSettings.Window", "DefaultResY", Y, "BaseEngine.cfg");

    if(!(YSuccess))
    {
        LOG(SDL3Log, Fatal, "Failed to get default Y Size from config");
        return -1;
    }

    window = SDL_CreateWindow(Title, X, Y, 0);


    LOG(SDL3Log, Log, "Window created!");
    return 0;
}
