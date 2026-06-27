#pragma once

// Checks if Object can be constructed using the given arg type
template <typename Object, typename... ArgTypes>
struct IsConstructible
{
    static constexpr bool Value = __is_constructible(Object, ArgTypes...);
};
