#pragma once
#include "RemoveReference.h"
#include <type_traits>

namespace RE::Internal::DecayInternal
{
    // removes const and volatile
    template <typename T>
	struct DecayInternal
	{
		using Type = std::remove_cv_t<T>;
	};

    // convert Value[] to Value*
    template <typename T>
	struct DecayInternal<T[]>
	{
		using Type = T*;
	};

    // same as above but for fixed size
    template <typename T, uint32 Value>
	struct DecayInternal<T[Value]>
	{
		using Type = T*;
	};

    // Converts function into a raw pointer
    template <typename ReturnType, typename... Arguments>
	struct DecayInternal<ReturnType(Arguments...)>
	{
		using Type = ReturnType(*)(Arguments...);
	};
}

template <typename T>
struct Decay
{
    // Strip away any '&' and '&&' first, then either convert an array to pointer, fixed sized array to pointer, or convert function to raw pointer
	// First, we will remove the reference, had to be typename since we do not know what value the removed reference will be.
	// Then, we will get the decay
    using Type = typename RE::Internal::DecayInternal::DecayInternal<typename RemoveReference<T>::Type>::Type;
};
