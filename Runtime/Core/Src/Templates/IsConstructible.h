#pragma once

// Checks if Object can be constructed using the given args
template <typename Object, typename... Args>
struct IsConstructible
{
    static constexpr bool Value = __is_constructible(Object, Args...);
};
