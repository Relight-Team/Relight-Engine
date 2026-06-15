#pragma once

template <typename A, typename B>
struct IsSameType
{
    static constexpr bool Value = false;
};

template <typename A>
struct IsSameType<A, A>
{
    static constexpr bool Value = true;
};
