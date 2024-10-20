#pragma once
#include "Core.h"
#include "SDL.h"


CORE_API::LogCategory* SDL2Misc = new CORE_API::LogCategory("SDL2 Misc");



int WindowStyle = SDL_WINDOW_OPENGL;

void SetVulkan()
{
    LOG(*SDL2Misc, Log, "Using 3D API: Vulkan");
    WindowStyle = SDL_WINDOW_VULKAN;
}

void SetOpenGL()
{
    LOG(*SDL2Misc, Log, "Using 3D API: OpenGL");
    WindowStyle = SDL_WINDOW_OPENGL;
}
