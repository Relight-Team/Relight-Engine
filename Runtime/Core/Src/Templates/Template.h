#pragma once
#include <type_traits>

// like std::forward
// Will preserve the lvalue and rvalue when being called from another function
// Mostly used in templates, where both types can be used, and the code needs to know
// which function type to call
template <typename T>
constexpr T&& Forward(std::remove_reference_t<T>& Obj) noexcept
{
	return (T&&)Obj;
};

template <typename T>
constexpr T&& Forward(std::remove_reference_t<T>&& Obj) noexcept
{
	return (T&&)Obj;
};

// Remove's 1 level of pointer
template <typename T>
struct RemovePointer
{
	using Type = T;
};

template <typename T>
struct RemovePointer<T*>
{
	using Type = T;
};

// like std::enable_if
// Compiles a function based on if the conditions are true. needs to be declared as typename EnableIf<> underneath the template
// Example: you can have 2 functions with same name and params, one checks if it's a float and another checks if it's a pointer
// based on your template input, a certain function will run
// Return is void by default
template <bool Condition, typename Return = void>
struct EnableIf;

template <typename Return>
struct EnableIf<true, Return>
{
	using Type = Return;
};

// Type doesn't exist, so it will ignore the function
template <typename Return>
struct EnableIf<false, Return>
{
};

// AND statement, checks if 2 statements are true
// NOTE: Do NOT include ::Value inside LValue and RValue

template <typename... Types>
struct And;

template <bool LValue, typename... RValues>
struct AndInternal
{
	// Recursively run the And struct to ensure everything is true
	static constexpr bool Value = And<RValues...>::Value;
};

template <typename... RValues>
struct AndInternal<false, RValues...>
{
	// If something is false, then Value will be false
	static constexpr bool Value = false;
};

// Run's AndInternal, which will run recursively for each and value
template <typename LValue, typename... RValues>
struct And<LValue, RValues...> : AndInternal<LValue::Value, RValues...>
{
};

// If we have 0 arguments, then it's always true
template <>
struct And<>
{
	static constexpr bool Value = true;
};

// OR statement, checks if any statements are true
// NOTE: Do NOT include ::Value inside LValue and RValue

template <typename... Types>
struct Or;

template <bool LValue, typename... RValues>
struct OrInternal
{
	// Recursively run the Or struct to ensure everything is true
	static constexpr bool Value = Or<RValues...>::Value;
};

template <typename... RValues>
struct OrInternal<true, RValues...>
{
	// If something is true, then Value will be true
	static constexpr bool Value = true;
};

// Run's OrInternal, which will run recursively for each and value
template <typename LValue, typename... RValues>
struct Or<LValue, RValues...> : OrInternal<LValue::Value, RValues...>
{
};

// If we have 0 arguments, then it's always false
template <>
struct Or<>
{
	static constexpr bool Value = false;
};

// Return's the opposite of a type
// NOTE: Do NOT include ::Value inside AnyTemplate

template <typename AnyTemplate>
struct Not
{
	static constexpr bool Value = !AnyTemplate::Value;
};

// Checks if the type is a pointer

template <typename T>
struct IsPointer
{
	static constexpr bool Value = false;
};

template <typename T>
struct IsPointer<T*>
{
	static constexpr bool Value = true;
};

// Checks if the type is a const

template <typename T>
struct IsConst
{
	static constexpr bool Value = false;
};

template <typename T>
struct IsConst<const T>
{
	static constexpr bool Value = true;
};

template <typename T>
struct IsReference
{
	static constexpr bool Value = false;
};

template <typename T>
struct IsReference<T&>
{
	static constexpr bool Value = true;
};
