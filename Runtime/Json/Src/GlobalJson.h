#pragma once
#include "Core.h"
#include <iostream>




namespace JSON_INTERNAL
{
    CORE_API::LogCategory* JSON_ERROR = new CORE_API::LogCategory("JSON");

    void PrintJsonError(ENGINE_INTERNAL::LogWarning a, std::string b)
    {
        LOG(*JSON_ERROR, a, b);
    }
}
