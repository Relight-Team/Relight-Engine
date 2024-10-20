#include "Core.h"

#include "LinuxMisc.h"

#include "SDL.h"

#include <iostream>

CORE_API::LogCategory* SDL2 = new CORE_API::LogCategory("SDL2");


class Window
{
public:
    int CreateWindow(const char* Title)
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

    int DestroyWindow()
    {
        //Destroy window
        SDL_DestroyWindow(window);

        //Quit SDL subsystems
        SDL_Quit();

        LOG(*SDL2, Log, "SDL quit");

        return 0;
    }


    void SetTitle(const char* name)
    {
        SDL_SetWindowTitle(window, name);
    }

    void Minimize()
    {
        SDL_MinimizeWindow(window);
    }

    void Maximize()
    {
        SDL_MaximizeWindow(window);
    }

    void Show()
    {
        SDL_ShowWindow(window);
    }

    void Hide()
    {
        SDL_HideWindow(window);
    }

    void Restore()
    {
        SDL_RestoreWindow(window);
    }

    void ToTop()
    {
        SDL_RaiseWindow(window);
    }

    void SetLocation(int x, int y)
    {
        SDL_SetWindowPosition(window, x, y);
    }

    void Opacity(float op)
    {
        SDL_SetWindowOpacity(window, op);
    }


    // Returns

    bool IsMaximized()
    {
        return SDL_GetWindowFlags(window) & SDL_WINDOW_MAXIMIZED;
    }

    bool IsMinimized()
    {
        return SDL_GetWindowFlags(window) & SDL_WINDOW_MINIMIZED;
    }

private:

    SDL_Window* window = NULL;
};
