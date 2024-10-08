#include "Core.h"

#include "SDL.h"


CORE_API::LogCategory* SDL2 = new CORE_API::LogCategory("SDL2");

int CreateWindow()
{
    if(SDL_Init(SDL_INIT_VIDEO) < 0)
    {
        LOG(*SDL2, Fatal, "Failed to initialized SDL library!!");
        return -1;
    }

    SDL_Window *window = SDL_CreateWindow("SDL2 Window", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,680, 480, 0);


    LOG(*SDL2, Log, "Window created!");
    return 0;
}
