#pragma once
#include "Core.h"
#include "SDL3/SDL.h"
#include "Linux/SDL_LOG.h"



extern int WindowStyle;

inline void SetVulkan()
{
    LOG(SDL3Log, Log, "Using 3D API: Vulkan");
    WindowStyle = SDL_WINDOW_VULKAN;
}

inline void SetOpenGL()
{
    LOG(SDL3Log, Log, "Using 3D API: OpenGL");
    WindowStyle = SDL_WINDOW_OPENGL;
}
