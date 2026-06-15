#pragma once
#include "Templates/FunctionStorage.h"
#include "Templates/FunctionRunner.h"
#include "Templates/Template.h"

// FunctionRef is a system that holds a reference to a callable object (function, lambda, etc)
// Note, this does not hold a function, only reference it, meaning that you must ensure that the object exists during this class lifetime
// Mostly used for function parameter

// Example Use:

// void FunctionStuff(int a, bool b) {};
// FunctionRef<void(int, bool)>

template <typename Signature>
class FunctionRef;

template <typename ReturnType, typename... ArgTypes>
class FunctionRef<ReturnType(ArgTypes...)>
{
    public:

        template <typename CallableObject>
        FunctionRef(CallableObject&& Obj)
        {
            // Bind Function to storage, uses Forward to keep lvalues/rvalues, stores the object without references
            auto* Bind = Func.Bind(Forward<CallableObject>(Obj));

            // Get the absolute type, removes the pointer and get's the type from Bind
            using Type = typename RemovePointer<decltype(Bind)>::Type;


            // Store the Run function, will be executed later
            Run = CORE_API::Internal::FunctionRunner::FunctionRunner<Type, ReturnType, ArgTypes...>::Run;
        }

        // Run function
        ReturnType operator()(ArgTypes... Args) const
        {
            return Run(Func.GetPointer(), Args...);
        }

        void Reset()
        {
            Func.Unbind();
            Run = nullptr;
        }

    private:

        // Contains the reference to the callable object itself
        CORE_API::Internal::FunctionReference::FunctionReferenceStorage Func;

        // Allows us to call operator() function
        // It works by storing the output result
        // Then, we set "Run as the name of the pointer
        // we use void* allows us to run on any callable object
        ReturnType (*Run)(void*, ArgTypes...) = nullptr;
};
