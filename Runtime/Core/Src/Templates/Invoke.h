#pragma once
#include "Template.h"

// Allows you to call a function object or pointer
template <typename FuncT, typename... ArgsT>
auto Invoke(FuncT&& Func, ArgsT&&... Args) ->
    decltype(Forward<FuncT>(Func)(Forward<ArgsT>(Args)...))
    {
        return Forward<FuncT>(Func)(Forward<ArgsT>(Args)...);
    }
